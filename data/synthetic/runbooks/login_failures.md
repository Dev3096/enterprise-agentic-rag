# Authentication Failure Runbook

## TOKEN_EXPIRED Errors

When elevated `TOKEN_EXPIRED` errors are detected:

1. Check the currently deployed authentication-service version.
2. Review authentication-related incidents from the previous seven days.
3. Verify whether refresh-token validation errors have increased.
4. Compare the failure rate before and after the latest deployment.

If the failure began immediately after deployment, consider rolling back the authentication service while the root cause is investigated.