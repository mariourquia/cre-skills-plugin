"""Runtime helpers for the residential_multifamily subsystem.

These modules run at workflow-execution time (as opposed to test-time
contract validation). They are light-touch — no network, no external
deps beyond pyyaml — so they can be invoked from any environment that
runs the subsystem's packs.
"""
