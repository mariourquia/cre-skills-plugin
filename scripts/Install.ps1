# ──────────────────────────────────────────────────────────────────────
# CRE Skills Plugin installer for Windows
#
# Called by the Inno Setup installer after file copy, or run standalone:
#   powershell -ExecutionPolicy Bypass -File Install.ps1 -InstallDir "C:\path\to\plugin"
#
# Detects Claude Code CLI and Claude Desktop, registers plugin with each.
# ──────────────────────────────────────────────────────────────────────

param(
    [string]$InstallDir = $PSScriptRoot
)

if ($InstallDir -eq $PSScriptRoot) {
    $InstallDir = Split-Path $PSScriptRoot -Parent
}

$ErrorActionPreference = 'Continue'

# Global error trap: ensure the window stays open on any crash
trap {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "  INSTALLATION ERROR" -ForegroundColor Red
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host ""
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""

    Send-InstallerTelemetry -StepFailed "unhandled_exception" -ErrorMsg $_.Exception.Message

    Write-Host "  An anonymous error report was sent to help improve the installer." -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  You can also submit a bug report:" -ForegroundColor Yellow
    Write-Host "  https://github.com/mariourquia/cre-skills-plugin/issues/new?labels=bug,installer" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Press Enter to close this window." -ForegroundColor White
    Read-Host
    exit 1
}

# ── Colors ──────────────────────────────────────────────────────────

function Write-Green  { param([string]$Text) Write-Host $Text -ForegroundColor Green }
function Write-Blue   { param([string]$Text) Write-Host $Text -ForegroundColor Blue }
function Write-Cyan   { param([string]$Text) Write-Host $Text -ForegroundColor Cyan }
function Write-Yellow { param([string]$Text) Write-Host $Text -ForegroundColor Yellow }
function Write-Red    { param([string]$Text) Write-Host $Text -ForegroundColor Red }
function Write-Bold   { param([string]$Text) Write-Host $Text -ForegroundColor White }
function Write-Dim    { param([string]$Text) Write-Host $Text -ForegroundColor DarkGray }

# ── Telemetry (PowerShell-native, no Python/Node dependency) ───────

$TelemetryUrl = "https://cre-skills-feedback-api.vercel.app/api/installer-telemetry"
$PluginNameConst = "cre-skills-plugin"
$InstallerVersionConst = "4.1.0"

function Send-InstallerTelemetry {
    param(
        [string]$StepFailed,
        [string]$ErrorMsg,
        [string]$PrereqsJson = "{}"
    )
    try {
        $idSource = "$env:COMPUTERNAME-$env:USERNAME"
        $sha = [System.Security.Cryptography.SHA256]::Create()
        $hashBytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($idSource))
        $installHash = [System.BitConverter]::ToString($hashBytes).Replace("-", "").ToLower()

        $eventSeed = "$StepFailed-$ErrorMsg-$(Get-Date -Format 'yyyyMMddHHmmssffff')"
        $eventBytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($eventSeed))
        $eventId = "it_" + [System.BitConverter]::ToString($eventBytes).Replace("-", "").ToLower().Substring(0, 16)

        $truncatedMsg = $ErrorMsg
        if ($ErrorMsg.Length -gt 2000) { $truncatedMsg = $ErrorMsg.Substring(0, 2000) }

        $body = @{
            id              = $eventId
            plugin_name     = $PluginNameConst
            plugin_version  = $InstallerVersionConst
            installer_type  = "ps1"
            os              = "windows"
            os_version      = [System.Environment]::OSVersion.Version.ToString()
            arch            = $env:PROCESSOR_ARCHITECTURE
            step_failed     = $StepFailed
            error_message   = $truncatedMsg
            prereqs         = $PrereqsJson | ConvertFrom-Json
            install_id_hash = $installHash
        } | ConvertTo-Json -Depth 5 -Compress

        Invoke-RestMethod -Uri $TelemetryUrl -Method POST -Body $body `
            -ContentType "application/json" -TimeoutSec 5 `
            -ErrorAction SilentlyContinue | Out-Null
    } catch {
        # Telemetry is best-effort -- never block installation
    }
}

# ── Node.js detection and auto-install ─────────────────────────────

function Find-OrInstallNode {
    # 1. Check if node is already available and working
    $nodeCmd = Get-Command node -ErrorAction SilentlyContinue
    if ($nodeCmd) {
        try {
            $ver = & node --version 2>&1
            if ($ver -match "v\d+\.\d+") {
                Write-Green "  Node.js found: $ver"
                return $true
            }
        } catch {}
    }

    # 2. Check common install locations
    foreach ($path in @(
        "${env:ProgramFiles}\nodejs\node.exe",
        "${env:ProgramFiles(x86)}\nodejs\node.exe"
    )) {
        if (Test-Path $path) {
            $env:PATH = "$(Split-Path $path);$env:PATH"
            $ver = & $path --version 2>&1
            Write-Green "  Node.js found at: $path ($ver)"
            return $true
        }
    }

    Write-Yellow "  Node.js not found. Attempting to install..."

    # 3. Try winget (most common on modern Windows, no admin needed)
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Dim "  Installing via winget..."
        & winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements --silent 2>&1 | Out-Null
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

        $nodeCheck = Get-Command node -ErrorAction SilentlyContinue
        if ($nodeCheck) {
            $ver = & node --version 2>&1
            Write-Green "  Node.js installed via winget: $ver"
            return $true
        }
    }

    # 4. Try chocolatey
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    if ($choco) {
        Write-Dim "  Installing via chocolatey..."
        & choco install nodejs-lts -y --no-progress 2>&1 | Out-Null
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

        $nodeCheck = Get-Command node -ErrorAction SilentlyContinue
        if ($nodeCheck) {
            $ver = & node --version 2>&1
            Write-Green "  Node.js installed via chocolatey: $ver"
            return $true
        }
    }

    return $false
}

# ── ASCII art header ────────────────────────────────────────────────

Write-Host ""
Write-Host "   ____ ____  _____   ____  _    _ _ _     " -ForegroundColor Cyan
Write-Host "  / ___|  _ \| ____| / ___|| | _(_) | |___ " -ForegroundColor Cyan
Write-Host " | |   | |_) |  _|   \___ \| |/ / | | / __|" -ForegroundColor Cyan
Write-Host " | |___|  _ <| |___   ___) |   <| | | \__ \" -ForegroundColor Cyan
Write-Host "  \____|_| \_\_____| |____/|_|\_\_|_|_|___/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "  Commercial Real Estate Skills for Claude" -ForegroundColor Cyan

Write-Blue  "  Plugin Installer v4.0.0"
Write-Dim   "  112 skills | 54 agents | 6 workflow chains"
Write-Host  ""

# ── Verify plugin files exist ───────────────────────────────────────

# Check for plugin files (flat layout from Inno Setup, or src/ layout from repo)
$hasFlat = (Test-Path (Join-Path $InstallDir "skills")) -and (Test-Path (Join-Path $InstallDir "agents"))
$hasSrc = (Test-Path (Join-Path $InstallDir "src\skills")) -and (Test-Path (Join-Path $InstallDir "src\agents"))
if (-not $hasFlat -and -not $hasSrc) {
    Write-Red "  Could not find the CRE Skills Plugin files."
    Write-Host "  Expected at: $InstallDir"
    Write-Host "  Looked for: skills\ and agents\ (or src\skills\ and src\agents\)"
    Write-Host ""
    Write-Bold "  Press Enter to close this window."
    Read-Host
    exit 1
}
$LayoutIsFlat = $hasFlat

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

$HasClaudeHome = Test-Path (Join-Path $env:USERPROFILE ".claude")

if ($ClaudePath) {
    $HasClaudeCode = $true
    try {
        $ver = & $ClaudePath --version 2>$null
        Write-Green "  Claude Code CLI found: $ver"
    } catch {
        Write-Green "  Claude Code CLI found at: $ClaudePath"
    }
} else {
    Write-Yellow "  Claude Code CLI not found"
    Write-Dim  "  Install: irm https://claude.ai/install.ps1 | iex"
    if ($HasClaudeHome) {
        Write-Dim  "  (~/.claude exists -- will register plugin there)"
    }
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

# Node.js is required for the MCP server
$HasNode = Find-OrInstallNode
if (-not $HasNode) {
    Write-Red "  Node.js is required but could not be installed."
    Write-Host ""
    Write-Host "  Install manually: https://nodejs.org/"
    Write-Host ""
    Send-InstallerTelemetry -StepFailed "node_install" `
        -ErrorMsg "Node.js not found and auto-install failed"
    Write-Bold "  Press Enter to close this window."
    Read-Host
    exit 1
}

# At least one must exist
if (-not $HasClaudeCode -and -not $HasClaudeDesktop -and -not $HasClaudeHome) {
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
    Send-InstallerTelemetry -StepFailed "no_claude" -ErrorMsg "Neither Claude Code nor Claude Desktop found"
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
if ($HasClaudeCode -or $HasClaudeDesktop -or $HasClaudeHome) {
    Write-Blue "  Registering plugin..."

    # Plugin cache location: ~/.claude/plugins/cache/local/cre-skills-plugin/<version>
    $ClaudeHome = Join-Path $env:USERPROFILE ".claude"

    # Find plugin.json (flat layout: plugin\plugin.json, src layout: src\plugin\plugin.json)
    $pjPath = $null
    foreach ($candidate in @(
        (Join-Path $InstallDir "plugin\plugin.json"),
        (Join-Path $InstallDir "src\plugin\plugin.json"),
        (Join-Path $InstallDir ".claude-plugin\plugin.json")
    )) {
        if (Test-Path $candidate) { $pjPath = $candidate; break }
    }
    if ($pjPath) {
        $PluginVersion = (Get-Content $pjPath | ConvertFrom-Json).version
    }
    if (-not $PluginVersion) { $PluginVersion = "4.0.0" }
    $PluginCachePath = Join-Path $ClaudeHome "plugins\cache\local\cre-skills-plugin\$PluginVersion"
    $InstalledPluginsFile = Join-Path $ClaudeHome "plugins\installed_plugins.json"
    $SettingsFile = Join-Path $ClaudeHome "settings.json"

    try {
        # 1. Copy plugin files to the plugin cache
        if (Test-Path $PluginCachePath) {
            Remove-Item -Path $PluginCachePath -Recurse -Force
        }
        New-Item -ItemType Directory -Path $PluginCachePath -Force | Out-Null

        if ($LayoutIsFlat) {
            # Flat layout (from Inno Setup extraction): files are directly at $InstallDir
            $robocopyArgs = @(
                $InstallDir,
                $PluginCachePath,
                '/E',
                '/XD', '.git', '__pycache__', 'node_modules', 'dist', '.venv', '.local', '.claude', 'scripts',
                '/XF', '*.pyc', '.DS_Store',
                '/NFL', '/NDL', '/NJH', '/NJS', '/NP'
            )
            & robocopy @robocopyArgs | Out-Null

            if ($LASTEXITCODE -ge 8) {
                throw "Robocopy failed with exit code $LASTEXITCODE"
            }
        } else {
            # Src layout (from repo checkout): content is under src/
            $srcDir = Join-Path $InstallDir "src"
            $robocopyArgs1 = @(
                $srcDir,
                $PluginCachePath,
                '/E',
                '/XD', '.git', '__pycache__', 'node_modules',
                '/XF', '*.pyc', '.DS_Store',
                '/NFL', '/NDL', '/NJH', '/NJS', '/NP'
            )
            & robocopy @robocopyArgs1 | Out-Null

            if ($LASTEXITCODE -ge 8) {
                throw "Robocopy step 1 (src/) failed with exit code $LASTEXITCODE"
            }

            # Copy non-src top-level items (README, LICENSE, registry, etc.)
            $robocopyArgs2 = @(
                $InstallDir,
                $PluginCachePath,
                '/E',
                '/XD', '.git', '__pycache__', 'node_modules', 'dist', '.venv', '.local', '.claude', 'src', 'builds', 'tools', 'config',
                '/XF', '*.pyc', '.DS_Store',
                '/NFL', '/NDL', '/NJH', '/NJS', '/NP'
            )
            & robocopy @robocopyArgs2 | Out-Null

            if ($LASTEXITCODE -ge 8) {
                throw "Robocopy step 2 (top-level) failed with exit code $LASTEXITCODE"
            }
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

        # Verify mcp-server.mjs ended up in the cache
        $mcpInCache = Join-Path $PluginCachePath "mcp-server.mjs"
        if (-not (Test-Path $mcpInCache)) {
            Write-Yellow "  WARNING: mcp-server.mjs not found in plugin cache at: $mcpInCache"
            # Try to find and copy it manually
            $mcpSources = @(
                (Join-Path $InstallDir "mcp-server.mjs"),
                (Join-Path $InstallDir "src\mcp-server.mjs")
            )
            foreach ($src in $mcpSources) {
                if (Test-Path $src) {
                    Copy-Item $src $mcpInCache
                    Write-Green "  Recovered mcp-server.mjs from: $src"
                    break
                }
            }
        }

        # 4. Register MCP server in Claude Desktop config
        #    Uses Node.js for JSON manipulation (PowerShell can't handle hyphenated keys)
        #    Windows stdio MCP servers need cmd /c wrapper per Anthropic docs
        $DesktopConfigDir = Join-Path $env:APPDATA "Claude"
        $DesktopConfigFile = Join-Path $DesktopConfigDir "claude_desktop_config.json"
        $mcpServerPath = $mcpInCache

        try {
            if (-not (Test-Path $DesktopConfigDir)) {
                New-Item -ItemType Directory -Path $DesktopConfigDir -Force | Out-Null
            }
            if (-not (Test-Path $DesktopConfigFile)) {
                '{"mcpServers":{}}' | Set-Content $DesktopConfigFile -Encoding UTF8
            }

            # Backup before modifying
            $backup = $DesktopConfigFile + ".backup-" + (Get-Date -Format "yyyyMMdd-HHmmss")
            Copy-Item $DesktopConfigFile $backup -ErrorAction SilentlyContinue

            Write-Dim "  Config: $DesktopConfigFile"
            Write-Dim "  MCP server: $mcpServerPath"

            # Use Node.js for JSON (no Python dependency)
            $tempJs = Join-Path $env:TEMP "cre_skills_mcp_config.js"
            @"
const fs = require('fs');
const cp = process.argv[1];
const sp = process.argv[2];
let d = {};
try { d = JSON.parse(fs.readFileSync(cp, 'utf8')); } catch {}
d.mcpServers = d.mcpServers || {};
d.mcpServers['cre-skills'] = { command: 'cmd', args: ['/c', 'node', sp] };
fs.writeFileSync(cp, JSON.stringify(d, null, 2));
console.log('OK');
"@ | Set-Content $tempJs -Encoding UTF8

            $result = & node $tempJs $DesktopConfigFile $mcpServerPath 2>&1
            Remove-Item $tempJs -ErrorAction SilentlyContinue

            if ("$result" -match "OK") {
                Write-Green "  MCP server registered for Claude Desktop"
                Write-Dim  "  Restart Claude Desktop to activate"

                # Verify the MCP server file exists at the registered path
                if (-not (Test-Path $mcpServerPath)) {
                    Write-Yellow "  WARNING: MCP server file not found at: $mcpServerPath"
                    Send-InstallerTelemetry -StepFailed "mcp_verify" -ErrorMsg "mcp-server.mjs not found at $mcpServerPath"
                } else {
                    Write-Green "  MCP config verified"
                }
            } else {
                Write-Yellow "  MCP config update returned: $result"
                Send-InstallerTelemetry -StepFailed "mcp_config_write" -ErrorMsg "Node returned: $result"
            }
        } catch {
            Write-Yellow "  Could not register MCP server: $_"
            Send-InstallerTelemetry -StepFailed "mcp_config_exception" -ErrorMsg "$_"
        }

        $InstalledSomewhere = $true

    } catch {
        Write-Yellow "  Could not register plugin automatically."
        Write-Host "  Error: $_"
        Send-InstallerTelemetry -StepFailed "plugin_registration" -ErrorMsg "$_"
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
Write-Host "  112 skills across 18 categories" -ForegroundColor Green
Write-Host "   54 expert agents (Pension Fund, PE, REIT, Risk Mgr, ...)" -ForegroundColor Green
Write-Host "    6 workflow chains (Acquisition, Capital Stack, Hold, ...)" -ForegroundColor Green
Write-Host ""
Write-Dim  "  Plugin location: $InstallDir"
Write-Host ""
Write-Host ""
Write-Bold "  Press Enter to close this window."
Read-Host
