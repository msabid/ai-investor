# Future Live Trading Path

The system already includes a future live-trading pathway, but it is intentionally locked.

To enable real trading later, the following must be completed:

1. Replace `LiveBrokerPlaceholder` with `IBKRBroker`.
2. Add broker position reconciliation.
3. Add duplicate order prevention.
4. Add stale data checks.
5. Add kill-switch enforcement.
6. Add order confirmation logs.
7. Add human approval workflow.
8. Add deployment monitoring.
9. Add paper-trading performance validation.
10. Only then change execution mode from `PAPER` to `LIVE_LOCKED`, and eventually `LIVE`.

Phase 1.5 intentionally supports only paper execution.
