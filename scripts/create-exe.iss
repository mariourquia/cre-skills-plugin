; ──────────────────────────────────────────────────────────────────────
; CRE Skills Plugin -- Inno Setup installer script
;
; Builds a Windows .exe installer that:
;   1. Copies plugin files to %APPDATA%\cre-skills-plugin
;   2. Runs Install.ps1 to detect and register with Claude Code / Desktop
;   3. Generates an uninstaller that cleans up both registrations
;
; Build (from GitHub Actions or local with Inno Setup 6+):
;   iscc /DSourceDir="C:\path\to\repo" /DAppVersion="2.0.0" scripts\create-exe.iss
;
; Preprocessor variables (passed via /D flags):
;   SourceDir  -- absolute path to the repo checkout
;   AppVersion -- version string (e.g. "2.0.0")
; ──────────────────────────────────────────────────────────────────────

#ifndef SourceDir
  #error "SourceDir must be defined via /DSourceDir=..."
#endif

#ifndef AppVersion
  #define AppVersion "3.0.0"
#endif

[Setup]
AppName=CRE Skills Plugin
AppVersion={#AppVersion}
AppVerName=CRE Skills Plugin v{#AppVersion}
AppPublisher=Mario Urquia
AppPublisherURL=https://github.com/mariourquia/cre-skills-plugin
AppSupportURL=https://github.com/mariourquia/cre-skills-plugin/issues
DefaultDirName={%USERPROFILE}\cre-skills-plugin
DefaultGroupName=CRE Skills Plugin
OutputBaseFilename=cre-skills-v{#AppVersion}-setup
OutputDir={#SourceDir}\dist
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
LicenseFile={#SourceDir}\LICENSE
DisableProgramGroupPage=yes
DisableDirPage=no
UninstallDisplayName=CRE Skills Plugin v{#AppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=CRE Skills Plugin for Claude
WelcomeLabel2=This will install the CRE Skills Plugin v{#AppVersion} on your computer.%n%n112 institutional-grade CRE skills covering deal sourcing, underwriting, capital markets, leasing, asset management, investor relations, development, and more.%n%nClaude Code: 112 skills, 54 agents, hooks, commands.%nClaude Desktop: 21 MCP tools (route, workspace, feedback, customize).%n%nApache License 2.0

; ──────────────────────────────────────────────────────────────────────
; Files -- explicit whitelist (no .git, dist, .local, tests, etc.)
;
; Source layout: all plugin content lives under src/ in the repo.
; We flatten src/ into {app}/ so post-install scripts find files at
; {app}\skills\*, {app}\mcp-server.mjs, etc. (no src\ prefix).
; ──────────────────────────────────────────────────────────────────────

[Files]
; Core plugin directories (from src/)
Source: "{#SourceDir}\src\skills\*"; DestDir: "{app}\skills"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\agents\*"; DestDir: "{app}\agents"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\commands\*"; DestDir: "{app}\commands"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\hooks\*"; DestDir: "{app}\hooks"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\orchestrators\*"; DestDir: "{app}\orchestrators"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\routing\*"; DestDir: "{app}\routing"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\schemas\*"; DestDir: "{app}\schemas"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\src\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs

; Plugin manifest (from src/plugin/ -> .claude-plugin/)
Source: "{#SourceDir}\src\plugin\plugin.json"; DestDir: "{app}\plugin"; Flags: ignoreversion
Source: "{#SourceDir}\src\plugin\.mcp.json"; DestDir: "{app}\plugin"; Flags: ignoreversion

; Calculator scripts (from src/calculators/)
Source: "{#SourceDir}\src\calculators\*"; DestDir: "{app}\calculators"; Flags: ignoreversion recursesubdirs createallsubdirs

; Catalog (from src/catalog/)
Source: "{#SourceDir}\src\catalog\*"; DestDir: "{app}\catalog"; Flags: ignoreversion recursesubdirs createallsubdirs

; MCP server (from src/)
Source: "{#SourceDir}\src\mcp-server.mjs"; DestDir: "{app}"; Flags: ignoreversion

; Windows installer script (post-install)
Source: "{#SourceDir}\scripts\Install.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion

; Verification and utility scripts (useful for manual troubleshooting)
Source: "{#SourceDir}\scripts\verify-install.sh"; DestDir: "{app}\scripts"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\scripts\uninstall.sh"; DestDir: "{app}\scripts"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\scripts\update.sh"; DestDir: "{app}\scripts"; Flags: ignoreversion skipifsourcedoesntexist

; Root files
Source: "{#SourceDir}\registry.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\NOTICE"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\PRIVACY.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\SECURITY.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\CONTRIBUTING.md"; DestDir: "{app}"; Flags: ignoreversion

; Pre-built catalog (optional, speeds up first load)
Source: "{#SourceDir}\dist\catalog.json"; DestDir: "{app}\dist"; Flags: ignoreversion skipifsourcedoesntexist

; ──────────────────────────────────────────────────────────────────────
; Post-install: run Install.ps1 to register with Claude Code / Desktop
; ──────────────────────────────────────────────────────────────────────

[Run]
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -NoProfile -File ""{app}\scripts\Install.ps1"" -InstallDir ""{app}"""; \
    Description: "Configure CRE Skills Plugin (register with Claude Code / Desktop)"; \
    StatusMsg: "Configuring CRE Skills Plugin..."; \
    Flags: postinstall shellexec waituntilterminated

; ──────────────────────────────────────────────────────────────────────
; Uninstall: remove plugin registration and Claude Desktop copy
; ──────────────────────────────────────────────────────────────────────

[UninstallRun]
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -NoProfile -Command ""try {{ & claude plugin remove cre-skills 2>$null }} catch {{ }}; $desktopSkills = Join-Path $env:APPDATA 'Claude\skills\cre-skills-plugin'; if (Test-Path $desktopSkills) {{ Remove-Item -Recurse -Force $desktopSkills }}"""; \
    Flags: runhidden waituntilterminated; \
    RunOnceId: "UnregisterPlugin"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
