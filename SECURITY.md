# GenZify Security Notes

## Scope
GenZify is a public text-conversion frontend backed by a Flask API and an external AI provider.

## Secrets
- Keep NVIDIA_API_KEY in local environment variables or the hosting provider's secret settings.
- Never commit .env files, API keys, access tokens, or production credentials.
- Rotate any credential that may have been exposed; removing a secret from the latest commit does not invalidate it.

## API protection
- Validate request structure and input length before making upstream AI calls.
- Keep rate limiting enabled and configure shared storage for multi-worker production deployments.
- Apply provider-side quota limits or alerts where available.
- Return generic client errors; do not expose exception messages or secrets.
- Do not execute or render model output as trusted HTML or code.

## Browser security
- Keep CORS limited to verified frontend origins.
- Keep the Content Security Policy aligned with the actual frontend and API hosts.
- CORS is a browser policy, not authentication.

## Testing and deployment
- Run the local pytest suite before merging changes.
- Mock external AI calls in automated tests.
- Do not run security tests against production without an explicitly approved, controlled plan.
- Verify headers, CORS, rate limiting, and environment configuration in staging before deployment.
- Do not deploy changes without an explicit approval.

## Reporting
Report suspected vulnerabilities privately to the project maintainer with a concise description, impact, reproduction steps in a local/staging environment, and suggested remediation. Do not include secrets or other users' private data.
