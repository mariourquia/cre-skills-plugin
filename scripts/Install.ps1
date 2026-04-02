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

Write-Blue  "  Plugin Installer v4.0.0"
Write-Dim   "  112 skills | 54 agents | 6 workflow chains"
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

# Install to Claude Desktop (register in ~/.claude/ plugin system)
if ($HasClaudeDesktop -and -not $HasClaudeCode) {
    Write-Blue "  Registering plugin for Claude Desktop..."

    # Plugin cache location: ~/.claude/plugins/cache/local/cre-skills-plugin/<version>
    $ClaudeHome = Join-Path $env:USERPROFILE ".claude"
    $PluginVersion = "4.0.0"
    $PluginCachePath = Join-Path $ClaudeHome "plugins\cache\local\cre-skills-plugin\$PluginVersion"
    $InstalledPluginsFile = Join-Path $ClaudeHome "plugins\installed_plugins.json"
    $SettingsFile = Join-Path $ClaudeHome "settings.json"

    try {
        # 1. Copy plugin files to the plugin cache
        if (-not (Test-Path $PluginCachePath)) {
            New-Item -ItemType Directory -Path $PluginCachePath -Force | Out-Null
        }

        $robocopyArgs = @(
            $InstallDir,
            $PluginCachePath,
            '/MIR',
            '/XD', '.git', '__pycache__', 'node_modules', 'dist', '.venv', '.local', '.claude',
            '/XF', '*.pyc', '.DS_Store',
            '/NFL', '/NDL', '/NJH', '/NJS', '/NP'
        )
        & robocopy @robocopyArgs | Out-Null

        if ($LASTEXITCODE -ge 8) {
            throw "Robocopy failed with exit code $LASTEXITCODE"
        }

        Write-Green "  Plugin files copied to cache"

        # 2. Register in installed_plugins.json
        $pluginKey = "cre-skills@local"
        $now = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")

        if (Test-Path $InstalledPluginsFile) {
            $ipData = Get-Content $InstalledPluginsFile -Raw | ConvertFrom-Json
        } else {
            New-Item -ItemType Directory -Path (Split-Path $InstalledPluginsFile) -Force | Out-Null
            $ipData = [PSCustomObject]@{ version = 2; plugins = [PSCustomObject]@{} }
        }

        $entry = @(
            [PSCustomObject]@{
                scope = "user"
                installPath = $PluginCachePath
                version = $PluginVersion
                installedAt = $now
                lastUpdated = $now
            }
        )

        if ($ipData.plugins.PSObject.Properties.Name -contains $pluginKey) {
            $ipData.plugins.$pluginKey = $entry
        } else {
            $ipData.plugins | Add-Member -NotePropertyName $pluginKey -NotePropertyValue $entry
        }

        $ipData | ConvertTo-Json -Depth 10 | Set-Content $InstalledPluginsFile -Encoding UTF8
        Write-Green "  Plugin registered in installed_plugins.json"

        # 3. Enable in settings.json
        if (Test-Path $SettingsFile) {
            $settings = Get-Content $SettingsFile -Raw | ConvertFrom-Json
        } else {
            $settings = [PSCustomObject]@{ enabledPlugins = [PSCustomObject]@{} }
        }

        if (-not $settings.PSObject.Properties.Name -contains "enabledPlugins") {
            $settings | Add-Member -NotePropertyName "enabledPlugins" -NotePropertyValue ([PSCustomObject]@{})
        }

        if ($settings.enabledPlugins.PSObject.Properties.Name -contains $pluginKey) {
            $settings.enabledPlugins.$pluginKey = $true
        } else {
            $settings.enabledPlugins | Add-Member -NotePropertyName $pluginKey -NotePropertyValue $true
        }

        $settings | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
        Write-Green "  Plugin enabled in settings.json"

        $InstalledSomewhere = $true

    } catch {
        Write-Yellow "  Could not register plugin automatically."
        Write-Host "  Error: $_"
        Write-Host ""
        Write-Host "  Manual install: run this in Claude Code CLI:"
        Write-Dim  "    claude plugin add `"$InstallDir`""
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
Write-Host "  " -NoNewline; Write-Green "112" -NoNewline:$false
Write-Host " skills across 18 categories"
Write-Host "  " -NoNewline; Write-Green "54" -NoNewline:$false
Write-Host " expert agents (Pension Fund, PE, REIT, Risk Mgr, ...)"
Write-Host "  " -NoNewline; Write-Green " 6" -NoNewline:$false
Write-Host " workflow chains (Acquisition, Capital Stack, Hold, ...)"
Write-Host ""
Write-Dim  "  Plugin location: $InstallDir"
Write-Host ""
Write-Host ""
Write-Bold "  Press Enter to close this window."
Read-Host
