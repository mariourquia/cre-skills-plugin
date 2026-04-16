"""Runtime fallback resolver.

Obj 2b of the hardening roadmap: `reference_manifest.yaml` declares
`fallback_behavior: use_prior_period | use_portfolio_average |
proceed_with_default | refuse | escalate | ask_user`. The manifest
enforces at contract-time (test_reference_manifests). At runtime, when
a read takes a non-refuse fallback, the downstream output cell MUST
carry an explicit confidence / source-class downgrade so the audience
sees that the number is not what the manifest ideally wants.

This module is a pure, deterministic helper. It does NOT fetch files
or call networks. Callers pass in the ref-read outcome plus the
declared fallback; the resolver returns the resolved value (or None
on refuse) together with a source-class tag per the executive output
contract and an audit-log entry ready to append to
`approval_audit_log.jsonl`.

Consumers:
- Workflow executors (e.g. the orchestrator engine) that read ref
  files via adapters.
- Tailoring TUI dry-runs.
- Tests that want to exercise fallback paths deterministically.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional


FallbackBehavior = Literal[
    "refuse",
    "use_prior_period",
    "use_portfolio_average",
    "proceed_with_default",
    "escalate",
    "ask_user",
]

SourceClass = Literal[
    "operator",
    "derived",
    "benchmark",
    "overlay",
    "overlay:fallback",
    "placeholder",
]


@dataclass
class ReadOutcome:
    """What the adapter layer reports for a single ref read.

    `found` True means the primary read succeeded; `value` holds the
    payload. False means the primary read missed and the resolver
    should apply the declared fallback. `fallback_value` may carry a
    candidate for use_prior_period / use_portfolio_average (if the
    caller already has one queued) — if None, the resolver still
    returns a tagged refusal-or-proceed outcome but leaves value None
    for the caller to fill.
    """

    found: bool
    value: Optional[Any] = None
    fallback_value: Optional[Any] = None
    primary_path: str = ""
    fallback_source: str = ""


@dataclass
class ResolverResult:
    value: Optional[Any]
    source_class: SourceClass
    refused: bool
    audit_entry: Dict[str, Any]
    notes: List[str] = field(default_factory=list)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve(
    fallback_behavior: FallbackBehavior,
    outcome: ReadOutcome,
    *,
    workflow_slug: str,
    ref_path: str,
    actor: str = "runtime",
) -> ResolverResult:
    """Resolve a single ref read against its declared fallback.

    Contract:
    - If outcome.found: source_class = "operator" (raw payload came
      from an operator system via an adapter), value = outcome.value.
      No fallback applied. Audit entry still written for traceability.
    - If not found:
      - refuse:                value=None, source_class="placeholder",
                               refused=True. Caller should abort.
      - use_prior_period:      value=outcome.fallback_value (may be
                               None), source_class="overlay:fallback".
      - use_portfolio_average: same as use_prior_period.
      - proceed_with_default:  same shape, caller provides default.
      - escalate:              value=None, source_class="placeholder",
                               refused=True (escalation is a refusal
                               at the resolver layer; orchestrator
                               handles human routing).
      - ask_user:               value=None, source_class="placeholder",
                               refused=True.

    Caller is responsible for checking `refused` and halting, or for
    consuming `value` with the returned `source_class` tag attached to
    the output cell.
    """

    ts = _now_iso()
    base_audit: Dict[str, Any] = {
        "timestamp": ts,
        "event": "ref_read",
        "workflow_slug": workflow_slug,
        "ref_path": ref_path,
        "declared_fallback_behavior": fallback_behavior,
        "actor": actor,
    }

    if outcome.found:
        base_audit.update(
            {
                "outcome": "primary_hit",
                "source_class": "operator",
            }
        )
        return ResolverResult(
            value=outcome.value,
            source_class="operator",
            refused=False,
            audit_entry=base_audit,
        )

    if fallback_behavior == "refuse":
        base_audit.update(
            {
                "outcome": "refused_missing_required_ref",
                "source_class": "placeholder",
            }
        )
        return ResolverResult(
            value=None,
            source_class="placeholder",
            refused=True,
            audit_entry=base_audit,
            notes=[
                f"required ref {ref_path} missing; fallback=refuse; workflow must halt",
            ],
        )

    if fallback_behavior in ("escalate", "ask_user"):
        base_audit.update(
            {
                "outcome": f"refused_for_{fallback_behavior}",
                "source_class": "placeholder",
            }
        )
        return ResolverResult(
            value=None,
            source_class="placeholder",
            refused=True,
            audit_entry=base_audit,
            notes=[
                f"ref {ref_path} missing; fallback={fallback_behavior}; orchestrator takes over",
            ],
        )

    # soft fallback paths: attach overlay:fallback tag and return whatever
    # the caller supplied as fallback_value (may be None — caller fills in).
    base_audit.update(
        {
            "outcome": f"fallback_{fallback_behavior}",
            "source_class": "overlay:fallback",
            "fallback_source": outcome.fallback_source or "caller-supplied",
        }
    )
    return ResolverResult(
        value=outcome.fallback_value,
        source_class="overlay:fallback",
        refused=False,
        audit_entry=base_audit,
        notes=[
            f"primary {ref_path} missing; applied {fallback_behavior}; "
            f"output cell tagged [overlay:fallback] per executive_output_contract.md rule 2",
        ],
    )


def format_cell(value: Any, source_class: SourceClass) -> str:
    """Attach the source-class tag to a rendered value for table output."""
    if value is None:
        return f"REFUSED [{source_class}]"
    return f"{value} [{source_class}]"


__all__ = [
    "FallbackBehavior",
    "SourceClass",
    "ReadOutcome",
    "ResolverResult",
    "resolve",
    "format_cell",
]
