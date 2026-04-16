"""Install smoke tests.

These tests scaffold the six `gap` cells in
`docs/install_smoke_test_matrix.md`. They are structural today: each
validates the installer *script* responds correctly to the scenario
without executing the install on the runner's host. A full end-to-end
install against a sandbox runner is future work (see
docs/ROADMAP.md v4.3 Install smoke tests).

Test conventions:
- Every file parses the relevant installer script as text, asserting it
  contains the control-flow branches for its scenario.
- Where a `--dry-run` or `--validate` flag exists, we invoke it and
  assert exit code + stdout contract.
- Anything that would require a clean sandbox to exercise end-to-end is
  marked `expectedFailure` until the sandbox runner lands.
"""
