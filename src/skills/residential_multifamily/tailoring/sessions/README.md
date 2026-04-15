# Sessions (operator-private)

This directory holds session state files produced by the tailoring TUI.

- `tailoring/sessions/{org_id}/{session_id}.yaml` — persisted interview state, written after every answer.
- `tailoring/sessions/{org_id}/{session_id}__summary.md` — human-readable session summary, re-written on every diff preview.

The contents of this directory are ignored by git (see `.gitignore` at this path). The tailoring skill creates session files locally so an interrupted interview can be resumed; it does not commit them. If an operator decides a specific session should be archived under version control, they should either copy the file out of this directory or add a deliberate exception to the repo's top-level `.gitignore`.

Never commit operator-identifying answers from these files without an explicit sign-off; they may contain sensitive thresholds, staffing, and internal policy details.
