# Authentication Service

## Access Tokens

NimbusFlow uses access tokens to authenticate API requests.

Access tokens remain valid for 60 minutes after issuance.

Applications should not request a new access token for every API request.

## Refresh Tokens

Refresh tokens allow applications to obtain a new access token without requiring the user to authenticate again.

Applications should call the `/oauth/token/refresh` endpoint when an access token expires.

Refresh tokens remain valid for 30 days unless revoked.

## Authentication Errors

The API may return the following authentication errors:

- `TOKEN_EXPIRED`: The access token has expired.
- `TOKEN_INVALID`: The token cannot be validated.
- `TOKEN_REVOKED`: The refresh token or access token has been revoked.