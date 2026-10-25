# GenZify Deployment Security Checklist

## Before deploying
- [ ] Run `python -m pytest backend/test_security.py` from the repository root.
- [ ] Review the branch diff and confirm no secrets are included.
- [ ] Verify the frontend and backend URLs are correct for the intended environment.
- [ ] Run dependency vulnerability scanning and review findings.

## Render backend environment
- [ ] Set `APP_ENV=production`.
- [ ] Set `NVIDIA_API_KEY` in the Render environment settings. Do not commit it.
- [ ] Provision a managed Redis instance and set `REDIS_URL` using its private connection URL.
- [ ] Confirm the Redis URL uses `redis://` or `rediss://` and is reachable from the backend service.
- [ ] Confirm the application fails startup if production Redis configuration is missing.
- [ ] Configure provider-side quotas or alerts where supported.

## Netlify frontend and CORS
- [ ] Confirm `https://genzconverterr.netlify.app` is the intended production frontend origin.
- [ ] Confirm the API host in `frontend/script.js`, `frontend/_redirects`, and `netlify.toml` matches the deployed backend.
- [ ] Confirm CSP `connect-src` permits only required API hosts.
- [ ] Confirm CORS allows only required, trusted browser origins.

## Staging verification
- [ ] Verify the effective HTTPS redirect and security headers.
- [ ] Verify invalid content types and malformed JSON return safe 4xx responses.
- [ ] Verify rate limits are shared across more than one backend worker.
- [ ] Verify upstream timeouts and failures return generic errors.
- [ ] Verify normal conversion and all style choices still work.
- [ ] Verify the fallback UI works when the backend is unavailable.

## Release
- [ ] Review all test results and outstanding risks.
- [ ] Obtain explicit approval before merging or deploying.
- [ ] After approval, deploy to staging first and repeat the checks above.
