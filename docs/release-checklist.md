# Release Checklist

Use this checklist before publishing a new version. See also [`docs/install_smoke_test_matrix.md`](install_smoke_test_matrix.md) for the test-coverage matrix and the v4.2.0 release-engineer notes at [`docs/releases/v4.2.0-release-notes.md`](releases/v4.2.0-release-notes.md) for the template.

## Pre-release (repo state)

- [ ] Update version in `.claude-plugin/plugin.json` (single source of truth)
- [ ] Run `python scripts/catalog-build.py` to rebuild catalog from repo state
- [ ] Run `python scripts/catalog-generate.py` to regenerate all public surfaces
- [ ] Run `python scripts/catalog-generate.py --check` to verify zero drift
- [ ] Run `python scripts/catalog-build.py --validate` to verify catalog integrity
- [ ] Run `pytest tests/` (repo-root suite) and `pytest src/skills/residential_multifamily/tests/` (subsystem suite); both must pass
- [ ] Run `node --check` on every `.mjs` file in `src/hooks/`, `src/orchestrators/engine/`, and `scripts/`
- [ ] Run `pytest tests/test_release_version_parity.py -v` to confirm version strings across plugin.json / marketplace.json / catalog.yaml / installer scripts / docs are coherent
- [ ] Update `CHANGELOG.md` with the new version entry (move items from `[Unreleased]`)
- [ ] Write `docs/releases/v<version>-release-notes.md`; keep frontmatter `status: pending` until the tag actually exists
- [ ] Review README for manually-maintained text that references old counts, behavior, or install commands
- [ ] Verify `PRIVACY.md` accurately reflects current feedback/telemetry behavior

## Non-generated surfaces (manual check)

These are not updated by the generator and must be verified manually:

- [ ] GitHub repo "About" description
- [ ] GitHub release title and body match `docs/releases/v<version>-release-notes.md`
- [ ] DMG/EXE installer version strings — `scripts/create-dmg.sh` and `scripts/create-exe.iss` read `APP_VERSION` injected by `release.yml`; verify the workflow tag matches `.claude-plugin/plugin.json`
- [ ] Any blog posts, tweets, or external references

## Tag and publish

- [ ] Create annotated tag: `git tag -a v<version> -m "v<version>"`
- [ ] Push tag: `git push origin v<version>`
- [ ] GitHub Actions `release.yml` builds DMG, EXE, the four target zips, source archives, signs every artifact via cosign, and generates a consolidated SHA256SUMS file
- [ ] The release body is prepended with the ASCII banner from `docs/assets/cre-skills-ascii.txt` and the release-engineer notes from `docs/releases/v<version>-release-notes.md`
- [ ] After the release workflow completes, flip the frontmatter in `docs/releases/v<version>-release-notes.md` from `status: pending` to `status: released` (in a follow-up PR or direct commit)

## Post-release

- [ ] Verify DMG download and install on macOS
- [ ] Verify EXE download and install on Windows
- [ ] Run `claude plugin marketplace add mariourquia/cre-skills-plugin && claude plugin install cre-skills@cre-skills` from a clean environment
- [ ] Verify SessionStart hook fires correctly
- [ ] Run one skill end-to-end to confirm routing works
- [ ] Verify the published release includes the ASCII banner at the top of the body and every expected asset + `.sig` + `.cert` file
