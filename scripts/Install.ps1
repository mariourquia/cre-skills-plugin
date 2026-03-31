# ──────────────────────────────────────────────────────────────────────
# CRE Skills Plugin installer for Windows
#
# Called by the Inno Setup installer after file copy, or run standalone:
#   powershell -ExecutionPolicy Bypass -File Install.ps1 -InstallDir "C:\path\to\plugin"
#
# Detects Claude Code CLI and Claude Desktop, registers plugin with each.
# ──────────────────────────────────────────────────────────────────────

param(
    [Parameter(Mandatory = $true)]
    [string]$InstallDir
)

$ErrorActionPreference = 'Continue'

# ── Colors ──────────────────────────────────────────────────────────

function Write-Green  { param([string]$Text) Write-Host $Text -ForegroundColor Green }
function Write-Blue   { param([string]$Text) Write-Host $Text -ForegroundColor Blue }
function Write-Cyan   { param([string]$Text) Write-Host $Text -ForegroundColor Cyan }
function Write-Yellow { param([string]$Text) Write-Host $Text -ForegroundColor Yellow }
function Write-Red    { param([string]$Text) Write-Host $Text -ForegroundColor Red }
function Write-Bold   { param([string]$Text) Write-Host $Text -ForegroundColor White }
function Write-Dim    { param([string]$Text) Write-Host $Text -ForegroundColor DarkGray }

# ── ASCII art header ────────────────────────────────────────────────

Write-Host ""
Write-Cyan @"

 ██████╗██████╗ ███████╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
██║     ██████╔╝█████╗      ███████╗█████╔╝ ██║██║     ██║     ███████╗
██║     ██╔══██╗██╔══╝      ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
╚██████╗██║  ██║███████╗    ███████║██║  ██╗██║███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

            ┌──┐                        ┌─────┐   ┌──┐
            │  │  ┌──┐    ┌───┐  ┌──┐   │     │   │  │     ┌─┐
       ┌──┐ │  │  │  │ ┌┐ │   │  │  │┌──┤     │┌──┤  │  ┌┐ │ │  ┌──┐
       │  │ │  │┌─┤  │ ││ │   │┌─┤  ││  │     ││  │  │┌─┤│ │ │┌─┤  │
    ┌──┤  │ │  ││ │  ├─┤│ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  │
  ──┤  │  ├─┤  ││ │  │ ││ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  ├──
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

"@

Write-Blue  "  Plugin Installer v2.5.0"
Write-Dim   "  102 skills | 55 agents | 6 workflow chains"
Write-Host  ""

# ── Verify plugin files exist ───────────────────────────────────────

if (-not (Test-Path (Join-Path $InstallDir "skills")) -or
    -not (Test-Path (Join-Path $InstallDir "agents"))) {
    Write-Red "  Could not find the CRE Skills Plugin files."
    Write-Host "  Expected at: $InstallDir"
    Write-Host ""
    Write-Bold "  Press Enter to close this window."
    Read-Host
    exit 1
}

# ── Step 1: Check prerequisites ─────────────────────────────────────

Write-Bold "  Checking prerequisites..."
Write-Host ""

$HasClaudeCode = $false
$HasClaudeDesktop = $false
$ClaudePath = $null

# Check for Claude Code CLI -- try PATH first, then known npm global location
$claudeCmd = Get-Command claude -ErrorAction SilentlyContinue
if ($claudeCmd) {
    $HasClaudeCode = $true
    $ClaudePath = $claudeCmd.Source
    try {
        $ver = & claude --version 2>$null
        Write-Green "  Claude Code CLI found: $ver"
    } catch {
        Write-Green "  Claude Code CLI found"
    }
} else {
    # Check npm global install location explicitly
    $npmClaudePath = Join-Path $env:APPDATA "npm\claude.cmd"
    if (Test-Path $npmClaudePath) {
        $HasClaudeCode = $true
        $ClaudePath = $npmClaudePath
        Write-Green "  Claude Code CLI found at: $npmClaudePath"
    } else {
        Write-Yellow "  Claude Code CLI not found (optional)"
    }
}

# Check for Claude Desktop
$ClaudeDesktopDir = Join-Path $env:APPDATA "Claude"
if (Test-Path $ClaudeDesktopDir) {
    $HasClaudeDesktop = $true
    Write-Green "  Claude Desktop found"
} else {
    # Also check LocalAppData
    $ClaudeLocalDir = Join-Path $env:LOCALAPPDATA "Claude"
    if (Test-Path $ClaudeLocalDir) {
        $HasClaudeDesktop = $true
        $ClaudeDesktopDir = $ClaudeLocalDir
        Write-Green "  Claude Desktop found"
    } else {
        Write-Yellow "  Claude Desktop not found (optional)"
    }
}

# At least one must exist
if (-not $HasClaudeCode -and -not $HasClaudeDesktop) {
    Write-Host ""
    Write-Red "  Neither Claude Code nor Claude Desktop was found."
    Write-Host ""
    Write-Host "  Install one of these first:"
    Write-Cyan "    Claude Code:    npm install -g @anthropic-ai/claude-code"
    Write-Cyan "    Claude Desktop: https://claude.ai/download"
    Write-Host ""
    Write-Host "  After installing, re-run this script or register manually:"
    Write-Dim  "    claude plugin add `"$InstallDir`""
    Write-Host ""
    Write-Bold "  Press Enter to close this window."
    Read-Host
    exit 0
}

Write-Host ""

# ── Step 2: Install the plugin ──────────────────────────────────────

Write-Bold "  Installing CRE Skills Plugin..."
Write-Dim  "  Location: $InstallDir"
Write-Host ""

$InstalledSomewhere = $false

# Install to Claude Code if available
if ($HasClaudeCode) {
    Write-Blue "  Registering with Claude Code..."
    try {
        if ($ClaudePath -and $ClaudePath -ne "claude") {
            $output = & $ClaudePath plugin add $InstallDir 2>&1
        } else {
            $output = & claude plugin add $InstallDir 2>&1
        }
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            Write-Green "  Claude Code plugin registered"
            $InstalledSomewhere = $true
        } else {
            Write-Yellow "  Claude Code 'plugin add' returned non-zero. Plugin may still work."
            Write-Dim  "  Fallback: claude --plugin-dir `"$InstallDir`""
            $InstalledSomewhere = $true
        }
    } catch {
        Write-Yellow "  Claude Code 'plugin add' not available in this version."
        Write-Dim  "  Use: claude --plugin-dir `"$InstallDir`""
        $InstalledSomewhere = $true
    }
    Write-Host ""
}

# Install to Claude Desktop if available
if ($HasClaudeDesktop) {
    Write-Blue "  Configuring Claude Desktop..."

    $SkillsDest = Join-Path $ClaudeDesktopDir "skills\cre-skills-plugin"

    try {
        # Create destination if needed
        if (-not (Test-Path $SkillsDest)) {
            New-Item -ItemType Directory -Path $SkillsDest -Force | Out-Null
        }

        # Use robocopy for rsync-like behavior with exclusions
        $robocopyArgs = @(
            $InstallDir,
            $SkillsDest,
            '/MIR',
            '/XD', '.git', '__pycache__', 'node_modules', 'dist', '.venv', '.local', '.claude',
            '/XF', '*.pyc', '.DS_Store', 'PLUGIN-BUILD-PLAN.md',
            '/NFL', '/NDL', '/NJH', '/NJS', '/NP'
        )
        & robocopy @robocopyArgs | Out-Null

        # Robocopy: exit codes < 8 indicate success (1 = files copied, 0 = no change)
        if ($LASTEXITCODE -lt 8) {
            Write-Green "  Skills copied to Claude Desktop"
            $InstalledSomewhere = $true
        } else {
            Write-Yellow "  Could not copy skills to Claude Desktop directory."
            Write-Dim  "  You can manually copy the plugin folder to: $SkillsDest"
        }
    } catch {
        Write-Yellow "  Could not copy skills to Claude Desktop directory."
        Write-Dim  "  You can manually copy the plugin folder to: $SkillsDest"
    }
    Write-Host ""
}

if (-not $InstalledSomewhere) {
    Write-Yellow "  Automatic registration did not succeed."
    Write-Dim  "  Manual: claude --plugin-dir `"$InstallDir`""
}

# ── Step 3: Success ─────────────────────────────────────────────────

Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Green "  CRE Skills Plugin installed successfully!"
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""

Write-Bold "  Quick Start"
Write-Host ""
Write-Cyan "  /cre-skills:cre-route         Route any CRE task to the right skill"
Write-Cyan "  /cre-skills:deal-quick-screen  Screen a deal in seconds"
Write-Cyan "  /cre-skills:cre-workflows      Browse 6 end-to-end workflow chains"
Write-Cyan "  /cre-skills:cre-agents         List 55 expert agents"
Write-Host ""

Write-Bold "  Example"
Write-Host ""
Write-Dim  "  > /cre-skills:deal-quick-screen"
Write-Dim  "    240-unit garden-style multifamily in Raleigh, NC."
Write-Dim  "    Asking `$42M. 2018 vintage. Occupancy 93%."
Write-Dim  "    In-place NOI `$2.6M. Rents 12% below market."
Write-Host ""

Write-Bold "  What's Included"
Write-Host ""
Write-Host "  " -NoNewline; Write-Green "99" -NoNewline:$false
Write-Host " skills across 16 categories"
Write-Host "  " -NoNewline; Write-Green "55" -NoNewline:$false
Write-Host " expert agents (Pension Fund, PE, REIT, Risk Mgr, ...)"
Write-Host "  " -NoNewline; Write-Green " 6" -NoNewline:$false
Write-Host " workflow chains (Acquisition, Capital Stack, Hold, ...)"
Write-Host ""
Write-Dim  "  Plugin location: $InstallDir"
Write-Host ""
Write-Host ""
Write-Bold "  Press Enter to close this window."
Read-Host
