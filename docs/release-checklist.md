# Release Checklist

Use this checklist before publishing a new version.

## Pre-Release

- [ ] Update version in `src/plugin/plugin.json`
- [ ] Run `python scripts/catalog-build.py` to rebuild catalog from repo state
- [ ] Run `python scripts/catalog-generate.py` to regenerate all public surfaces
- [ ] Run `python scripts/catalog-generate.py --check` to verify zero drift
- [ ] Run `python scripts/catalog-build.py --validate` to verify catalog integrity
- [ ] Run `pytest tests/` to verify all structural and consistency tests pass
- [ ] Run `node --check` on all `.mjs` files in `src/hooks/` and `scripts/`
- [ ] Verify `node src/routing/skill-dispatcher.mjs --list` returns correct skill count
- [ ] Update `CHANGELOG.md` with version entry
- [ ] Update `docs/install-guide.md` version reference
- [ ] Review README for any manually-maintained text that references old counts or behavior
- [ ] Verify PRIVACY.md accurately reflects current feedback/telemetry behavior

## Non-Generated Surfaces (Manual Check Required)

These are NOT updated by the generator and must be verified manually:

- [ ] GitHub repo "About" description
- [ ] GitHub release title and notes
- [ ] DMG/EXE installer version strings (in `scripts/create-dmg.sh` and `scripts/create-exe.iss`)
- [ ] Any blog posts, tweets, or external references

## Release

- [ ] Create git tag: `git tag v<version>`
- [ ] Push tag: `git push origin v<version>`
- [ ] GitHub Actions will build DMG and EXE installers
- [ ] Create GitHub release with notes from CHANGELOG
- [ ] Attach DMG and EXE artifacts to release

## Post-Release

- [ ] Verify DMG download and install on macOS
- [ ] Verify EXE download and install on Windows
- [ ] Run `claude plugin add github:mariourquia/cre-skills-plugin` from a clean environment
- [ ] Verify SessionStart hook fires correctly
- [ ] Run one skill end-to-end to confirm routing works
