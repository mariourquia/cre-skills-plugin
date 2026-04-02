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

# Check for Claude Code CLI
# Official install paths per Anthropic docs:
#   Windows native: $env:USERPROFILE\.local\bin\claude.exe
#   npm global:     $env:APPDATA\npm\claude.cmd
$ClaudePath = $null

# Method 1: PATH lookup
$found = Get-Command claude -ErrorAction SilentlyContinue
if ($found) {
    $ClaudePath = $found.Source
}

# Method 2: Official Windows native install location
if (-not $ClaudePath) {
    $nativePath = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
    if (Test-Path $nativePath) {
        $ClaudePath = $nativePath
    }
}

# Method 3: npm global install
if (-not $ClaudePath) {
    $npmPath = Join-Path $env:APPDATA "npm\claude.cmd"
    if (Test-Path $npmPath) {
        $ClaudePath = $npmPath
    }
}

# Method 4: Check ~/.claude config dir (proof Claude Code was used)
$ClaudeConfigDir = Join-Path $env:USERPROFILE ".claude"
$HasClaudeConfig = Test-Path $ClaudeConfigDir

if ($ClaudePath) {
    $HasClaudeCode = $true
    try {
        $ver = & $ClaudePath --version 2>$null
        Write-Green "  Claude Code CLI found: $ver"
    } catch {
        Write-Green "  Claude Code CLI found at: $ClaudePath"
    }
} elseif ($HasClaudeConfig) {
    $HasClaudeCode = $true
    Write-Green "  Claude Code detected (~/.claude exists)"
    Write-Yellow "  CLI binary not in PATH -- will show manual registration"
} else {
    Write-Yellow "  Claude Code CLI not found (optional)"
    Write-Dim  "  Install: irm https://claude.ai/install.ps1 | iex"
}

# Check for Claude Desktop -- official config location: %APPDATA%\Claude
$ClaudeDesktopDir = Join-Path $env:APPDATA "Claude"
if (Test-Path $ClaudeDesktopDir) {
    $HasClaudeDesktop = $true
    Write-Green "  Claude Desktop found"
} else {
    # Also check LocalAppData (some versions)
    $ClaudeLocalDir = Join-Path $env:LOCALAPPDATA "Claude"
    if (Test-Path $ClaudeLocalDir) {
        $HasClaudeDesktop = $true
        $ClaudeDesktopDir = $ClaudeLocalDir
        Write-Green "  Claude Desktop found (LocalAppData)"
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
    Write-Host "    Claude Code:    irm https://claude.ai/install.ps1 | iex"
    Write-Host "    Claude Desktop: https://claude.ai/download"
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

# Register plugin in ~/.claude/ plugin system (works for both Claude Code and Desktop)
if ($HasClaudeCode -or $HasClaudeDesktop) {
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

        # 4. Register MCP server in Claude Desktop config
        #    Per Anthropic docs: Claude Desktop reads ONLY from
        #    %APPDATA%\Claude\claude_desktop_config.json (not .mcp.json)
        #    Windows requires cmd /c wrapper for stdio MCP servers
        $DesktopConfigDir = Join-Path $env:APPDATA "Claude"
        $DesktopConfigFile = Join-Path $DesktopConfigDir "claude_desktop_config.json"

        try {
            # Ensure the Claude Desktop config directory exists
            if (-not (Test-Path $DesktopConfigDir)) {
                New-Item -ItemType Directory -Path $DesktopConfigDir -Force | Out-Null
            }

            if (Test-Path $DesktopConfigFile) {
                $desktopConfig = Get-Content $DesktopConfigFile -Raw | ConvertFrom-Json
            } else {
                $desktopConfig = [PSCustomObject]@{ mcpServers = [PSCustomObject]@{} }
            }

            if (-not $desktopConfig.PSObject.Properties.Name -contains "mcpServers") {
                $desktopConfig | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue ([PSCustomObject]@{})
            }

            # Windows stdio MCP servers need cmd /c wrapper per Anthropic docs
            $mcpEntry = [PSCustomObject]@{
                command = "cmd"
                args = @("/c", "node", "$PluginCachePath\mcp-server.mjs")
            }

            if ($desktopConfig.mcpServers.PSObject.Properties.Name -contains "cre-skills") {
                $desktopConfig.mcpServers.'cre-skills' = $mcpEntry
            } else {
                $desktopConfig.mcpServers | Add-Member -NotePropertyName "cre-skills" -NotePropertyValue $mcpEntry
            }

            $desktopConfig | ConvertTo-Json -Depth 10 | Set-Content $DesktopConfigFile -Encoding UTF8
            Write-Green "  MCP server registered for Claude Desktop"
            Write-Dim  "  Config: $DesktopConfigFile"
            Write-Dim  "  Restart Claude Desktop to activate"
        } catch {
            Write-Yellow "  Could not register MCP server: $_"
            Write-Host ""
            Write-Host "  Manual: add this to $DesktopConfigFile:"
            Write-Dim  '  {"mcpServers":{"cre-skills":{"command":"cmd","args":["/c","node","' + $PluginCachePath + '\mcp-server.mjs"]}}}'
        }

        $InstalledSomewhere = $true

    } catch {
        Write-Yellow "  Could not register plugin automatically."
        Write-Host "  Error: $_"
        Write-Host ""
        Write-Host "  Manual install: run this in Claude Code CLI:"
        Write-Dim  "    claude --plugin-dir `"$InstallDir`""
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
