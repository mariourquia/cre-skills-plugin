#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# Build a signed .dmg installer for cre-skills-plugin
#
# Creates a macOS disk image containing a signed .app bundle.
# User opens DMG, sees "CRE Skills Installer.app" and a README.
# Double-clicking the .app copies files and runs setup in Terminal.
#
# Usage:
#   ./scripts/create-dmg.sh                # builds dist/cre-skills-0.1.0.dmg
#   ./scripts/create-dmg.sh v1.0.0         # custom version in filename
#
# Requirements:
#   - Apple Developer ID certificate in keychain (or --no-sign)
#   - xcrun notarytool credentials (optional, for notarization)
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# ── Parse args ────────────────────────────────────────────────────────

VERSION=""
SIGN_IDENTITY=""
SKIP_SIGN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --version)    VERSION="$2"; shift 2 ;;
        --identity)   SIGN_IDENTITY="$2"; shift 2 ;;
        --no-sign)    SKIP_SIGN=true; shift ;;
        *)            VERSION="$1"; shift ;;
    esac
done

if [ -z "$VERSION" ]; then
    VERSION="0.1.0"
fi

# Strip leading 'v' for filenames
VERSION_CLEAN="${VERSION#v}"

# Auto-detect signing identity if not provided
if [ -z "$SIGN_IDENTITY" ] && [ "$SKIP_SIGN" = false ]; then
    SIGN_IDENTITY=$(security find-identity -v -p codesigning 2>/dev/null \
        | grep "Developer ID Application" \
        | head -1 \
        | sed 's/.*"\(.*\)"/\1/' || true)
    if [ -z "$SIGN_IDENTITY" ]; then
        echo "Warning: No Developer ID found. Building unsigned."
        SKIP_SIGN=true
    fi
fi

DMG_NAME="cre-skills-v${VERSION_CLEAN}"
DIST_DIR="$REPO_ROOT/dist"
STAGING_DIR="$DIST_DIR/.dmg-staging"
APP_NAME="CRE Skills Installer.app"

echo "Building $DMG_NAME.dmg..."
[ "$SKIP_SIGN" = false ] && echo "Signing with: $SIGN_IDENTITY"

# ── Clean ─────────────────────────────────────────────────────────────

rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR/$DMG_NAME" "$DIST_DIR"

# ── Copy project files into hidden .content/ ──────────────────────────

mkdir -p "$STAGING_DIR/$DMG_NAME/.content"
rsync -rlpt \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    --exclude='node_modules' \
    --exclude='dist' \
    --exclude='PLUGIN-BUILD-PLAN.md' \
    --exclude='.venv' \
    --exclude='.claude' \
    --exclude='.claude-plugin' \
    --exclude='*.pyc' \
    --exclude='*.egg-info' \
    --exclude='.pytest_cache' \
    --exclude='.github' \
    --exclude='tests' \
    --exclude='tools' \
    --exclude='builds' \
    --exclude='config' \
    --exclude='.gitleaks.toml' \
    --exclude='.gitignore' \
    --exclude='.local' \
    "$REPO_ROOT/" "$STAGING_DIR/$DMG_NAME/.content/"

chflags hidden "$STAGING_DIR/$DMG_NAME/.content" 2>/dev/null || true

# ── Generate app icon ─────────────────────────────────────────────────
# Creates a blue/steel icon with a building silhouette -- CRE themed.
# Uses pure Python for pixel-perfect PNG output without dependencies.

ICON_DIR="$STAGING_DIR/icon-build"
ICONSET_DIR="$ICON_DIR/AppIcon.iconset"
mkdir -p "$ICONSET_DIR"

ICONSET_DIR="$ICONSET_DIR" python3 << 'ICON_SCRIPT'
import struct, zlib, os, math

def create_png(width, height, pixels):
    """Create a minimal PNG from RGBA pixel data."""
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))

    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter: none
        for x in range(width):
            idx = (y * width + x) * 4
            raw += bytes(pixels[idx:idx+4])

    idat = chunk(b'IDAT', zlib.compress(raw, 9))
    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend

def draw_icon(size):
    """Draw a building/skyscraper silhouette icon at given size."""
    pixels = [0] * (size * size * 4)
    cx, cy = size / 2, size / 2
    r_outer = size * 0.44

    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx * dx + dy * dy)

            # Background circle with steel-blue gradient
            if dist <= r_outer:
                t = dist / r_outer
                r = int(30 + (60 - 30) * (1 - t))
                g = int(60 + (110 - 60) * (1 - t))
                b = int(100 + (170 - 100) * (1 - t))

                # Subtle top-light effect
                light = max(0, -dy / r_outer) * 0.25
                r = min(255, int(r + light * 60))
                g = min(255, int(g + light * 80))
                b = min(255, int(b + light * 100))

                # Anti-alias edge
                if dist > r_outer - 1.5:
                    alpha = max(0, min(255, int(255 * (r_outer - dist) / 1.5)))
                else:
                    alpha = 255

                pixels[idx] = r
                pixels[idx + 1] = g
                pixels[idx + 2] = b
                pixels[idx + 3] = alpha

            # Draw building silhouette (white on blue)
            in_building = False
            s = size  # shorthand

            # Normalize coordinates to 0..1 range centered at icon center
            nx = (x - cx) / (r_outer * 0.85)
            ny = (y - cy) / (r_outer * 0.85)

            # Ground line
            if abs(ny - 0.45) < 0.02 and abs(nx) < 0.55:
                in_building = True

            # Tall center tower (skyscraper)
            if -0.10 < nx < 0.10 and -0.42 < ny < 0.45:
                in_building = True
            # Tower cap/antenna
            if -0.03 < nx < 0.03 and -0.52 < ny < -0.42:
                in_building = True

            # Left building (medium height)
            if -0.32 < nx < -0.12 and -0.18 < ny < 0.45:
                in_building = True

            # Right building (medium-tall)
            if 0.12 < nx < 0.30 and -0.28 < ny < 0.45:
                in_building = True

            # Far left small building
            if -0.48 < nx < -0.34 and 0.05 < ny < 0.45:
                in_building = True

            # Far right small building
            if 0.32 < nx < 0.48 and 0.10 < ny < 0.45:
                in_building = True

            # Window grid on center tower
            if -0.10 < nx < 0.10 and -0.42 < ny < 0.45:
                # Horizontal window rows every ~0.08 units
                wy = (ny + 0.42) % 0.09
                wx = (nx + 0.10) % 0.07
                if 0.02 < wy < 0.07 and 0.015 < wx < 0.055:
                    in_building = False  # Cut out windows (show bg)

            # Window grid on left building
            if -0.32 < nx < -0.12 and -0.18 < ny < 0.45:
                wy = (ny + 0.18) % 0.10
                wx = (nx + 0.32) % 0.08
                if 0.03 < wy < 0.08 and 0.02 < wx < 0.06:
                    in_building = False

            # Window grid on right building
            if 0.12 < nx < 0.30 and -0.28 < ny < 0.45:
                wy = (ny + 0.28) % 0.09
                wx = (nx - 0.12) % 0.07
                if 0.025 < wy < 0.065 and 0.015 < wx < 0.055:
                    in_building = False

            if in_building and dist <= r_outer * 0.92:
                pixels[idx] = 240
                pixels[idx + 1] = 245
                pixels[idx + 2] = 255
                pixels[idx + 3] = 255

    return create_png(size, size, pixels)

# Generate all required iconset sizes
sizes = {
    'icon_16x16.png': 16,
    'icon_16x16@2x.png': 32,
    'icon_32x32.png': 32,
    'icon_32x32@2x.png': 64,
    'icon_128x128.png': 128,
    'icon_128x128@2x.png': 256,
    'icon_256x256.png': 256,
    'icon_256x256@2x.png': 512,
    'icon_512x512.png': 512,
}

iconset = os.environ['ICONSET_DIR']
for name, sz in sizes.items():
    png = draw_icon(sz)
    with open(os.path.join(iconset, name), 'wb') as f:
        f.write(png)
ICON_SCRIPT

# Convert iconset to icns
ICONSET_DIR="$ICONSET_DIR" iconutil -c icns "$ICONSET_DIR" -o "$STAGING_DIR/AppIcon.icns" 2>/dev/null && {
    echo "Icon generated"
} || {
    echo "Warning: iconutil failed, using default icon"
}

# ── Build .app bundle (in isolated temp dir, then move in) ────────────
# Building the .app away from the rsync'd .content/ avoids inheriting
# extended attributes that break codesign.

APP_BUILD_DIR="$STAGING_DIR/.app-build/$APP_NAME"
mkdir -p "$APP_BUILD_DIR/Contents/MacOS"
mkdir -p "$APP_BUILD_DIR/Contents/Resources"
APP_DIR="$APP_BUILD_DIR"

# Copy icon if generated
if [ -f "$STAGING_DIR/AppIcon.icns" ]; then
    cp "$STAGING_DIR/AppIcon.icns" "$APP_DIR/Contents/Resources/AppIcon.icns"
fi

# Info.plist
cat > "$APP_DIR/Contents/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>install</string>
    <key>CFBundleIdentifier</key>
    <string>com.cre-skills.installer</string>
    <key>CFBundleName</key>
    <string>CRE Skills Installer</string>
    <key>CFBundleDisplayName</key>
    <string>CRE Skills Installer</string>
    <key>CFBundleVersion</key>
    <string>${VERSION_CLEAN}</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION_CLEAN}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHumanReadableCopyright</key>
    <string>Apache License 2.0 - CRE Skills Plugin ${VERSION_CLEAN}</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
</dict>
</plist>
PLIST

# The executable -- copies project to writable location, then installs
cat > "$APP_DIR/Contents/MacOS/install" << 'LAUNCHER'
#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# CRE Skills Installer
# Copies plugin to ~/cre-skills-plugin, then runs setup in Terminal.
# ──────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
CONTENT_DIR="$SCRIPT_DIR/.content"
INSTALL_DIR="$HOME/cre-skills-plugin"

if [ ! -d "$CONTENT_DIR" ]; then
    osascript -e 'display alert "CRE Skills Installer" message "Could not find installer files. Please run from the mounted disk image." as critical buttons {"OK"} default button "OK"'
    exit 1
fi

# Copy to writable location (~/cre-skills-plugin)
if [ -d "$INSTALL_DIR" ]; then
    response=$(osascript -e '
        display dialog "CRE Skills Plugin is already installed." & return & return & "Location: ~/cre-skills-plugin" & return & return & "Would you like to reinstall?" buttons {"Cancel", "Reinstall"} default button "Reinstall" with icon caution with title "CRE Skills Installer"
    ' 2>/dev/null | grep "Reinstall" || true)
    if [ -z "$response" ]; then
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# Show progress dialog while copying
osascript -e 'display notification "Copying files to ~/cre-skills-plugin..." with title "CRE Skills Installer"' 2>/dev/null || true
cp -R "$CONTENT_DIR" "$INSTALL_DIR"

# Open Terminal and run the installer from the writable copy
osascript << EOF
tell application "Terminal"
    activate
    do script "clear && bash '$INSTALL_DIR/Install.command'"
end tell
EOF
LAUNCHER
chmod +x "$APP_DIR/Contents/MacOS/install"

# ── Create README ─────────────────────────────────────────────────────

cat > "$STAGING_DIR/$DMG_NAME/README.txt" << README

    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║     CRE Skills Plugin for Claude                 ║
    ║     Installer  v${VERSION_CLEAN}                         ║
    ║                                                  ║
    ╠══════════════════════════════════════════════════╣
    ║                                                  ║
    ║   Double-click the app to install.               ║
    ║                                                  ║
    ║   What it does:                                  ║
    ║     - Installs to ~/cre-skills-plugin            ║
    ║     - Detects Claude Code -> registers plugin    ║
    ║     - Detects Claude Desktop -> copies skills    ║
    ║     - 105 institutional-grade CRE skills         ║
    ║                                                  ║
    ║   Requirements:                                  ║
    ║     - Claude Code CLI or Claude Desktop          ║
    ║     - macOS 12+                                  ║
    ║                                                  ║
    ║   After install, start Claude and try:           ║
    ║     /cre-skills:deal-quick-screen                ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝

    Alternative: Claude Code CLI (marketplace)
      claude plugin marketplace add mariourquia/cre-skills-plugin
      claude plugin install cre-skills@cre-skills

    113 skills | 54 agents | 6 workflow chains | 12 calculators
    Deal sourcing, underwriting, capital markets, leasing,
    asset management, investor relations, and more.

    github.com/mariourquia/cre-skills-plugin

README

# ── Sign the .app bundle ──────────────────────────────────────────────

if [ "$SKIP_SIGN" = false ]; then
    echo "Stripping extended attributes..."
    xattr -cr "$STAGING_DIR" 2>/dev/null || true
    xattr -d com.apple.FinderInfo "$APP_DIR" 2>/dev/null || true
    xattr -d "com.apple.fileprovider.fpfs#P" "$APP_DIR" 2>/dev/null || true
    find "$APP_DIR" -exec xattr -c {} \; 2>/dev/null || true
    dot_clean -m "$APP_DIR" 2>/dev/null || true

    echo "Signing .app bundle..."
    codesign --force --sign "$SIGN_IDENTITY" \
        --options runtime --timestamp \
        "$APP_DIR/Contents/MacOS/install" 2>&1 || true
    codesign --force --sign "$SIGN_IDENTITY" \
        --options runtime --timestamp \
        "$APP_DIR" 2>&1 || true

    echo "Verifying signature..."
    codesign -dvv "$APP_DIR" 2>&1 | grep -E "Authority|Identifier|TeamIdentifier"
fi

# ── Move signed .app into DMG staging ─────────────────────────────────

mv "$APP_BUILD_DIR" "$STAGING_DIR/$DMG_NAME/$APP_NAME"

# ── Build DMG ─────────────────────────────────────────────────────────

hdiutil create \
    -volname "$DMG_NAME" \
    -srcfolder "$STAGING_DIR/$DMG_NAME" \
    -ov \
    -format UDZO \
    "$DIST_DIR/$DMG_NAME.dmg" \
    -quiet

# ── Sign the DMG itself ───────────────────────────────────────────────

if [ "$SKIP_SIGN" = false ]; then
    echo "Signing DMG..."
    codesign --force --sign "$SIGN_IDENTITY" --timestamp \
        "$DIST_DIR/$DMG_NAME.dmg" 2>&1 || true
fi

# ── Clean staging ─────────────────────────────────────────────────────

rm -rf "$STAGING_DIR"

echo ""
echo "Created: $DIST_DIR/$DMG_NAME.dmg"
SIZE=$(du -h "$DIST_DIR/$DMG_NAME.dmg" | cut -f1 | tr -d ' ')
echo "Size: $SIZE"
[ "$SKIP_SIGN" = false ] && echo "Signed: $SIGN_IDENTITY"
echo ""
echo "DMG contents visible to user:"
echo "  CRE Skills Installer.app  (double-click to install)"
echo "  README.txt                (instructions)"
echo ""
if [ "$SKIP_SIGN" = false ]; then
    echo "Notarize for full Gatekeeper bypass:"
    echo "  xcrun notarytool submit $DIST_DIR/$DMG_NAME.dmg \\"
    echo "    --apple-id YOUR_APPLE_ID \\"
    echo "    --team-id YOUR_TEAM_ID \\"
    echo "    --password APP_SPECIFIC_PASSWORD \\"
    echo "    --wait"
    echo "  xcrun stapler staple $DIST_DIR/$DMG_NAME.dmg"
fi
