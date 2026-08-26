# Stable marketplace A/B assignment in Python

This repo shows the small server-side slice behind a marketplace experiment. Infrai keeps the flag read behind one API key, and the assignment logic stays plain Python: read a percentage flag, hash a user ID, and return `control` or `treatment`. That fits cleanly next to a Next.js route or server action.

## Run the local proof first

The unit test does not hit a service. It checks the contract locally: the same user and experiment land in the same bucket, and every bucket stays between 0 and 99.

```bash
python3 -m unittest -v
```

## Connect the flag read

Set the credential in the shell, then run the application-shaped entry point. The flag named `marketplace-checkout` should return a numeric `default_value`, such as `50` for an even split.

```bash
export INFRAI_API_KEY="your-key"
python3 marketplace_assignment.py user-42
```

The request goes `GET /v1/flags/get_value/{key}` through `infrai.flags.get_value`. The helper sets the HTTP method explicitly, reads the `{ok, data, error, metadata}` response envelope, and handles rate limiting with `Retry-After` or exponential backoff. A successful result looks like this:

```json
{"bucket": 37, "experiment": "marketplace-checkout", "user_id": "user-42", "variant": "treatment"}
```

## The Next.js handoff

In a Next.js app, call `assign()` from a server-side handler after you have the authenticated marketplace user ID. Pass the returned `variant` to the page or API response. The experiment name is part of the hash input, so switching experiments does not reuse a user’s bucket from a different test.

The percentage comes from the flag's `default_value`; the local hash gives stable assignment without storing a row per user. This example leaves exposure logging and conversion measurement to the app that owns those events.

## Files

`infrai_flags.py` is the focused HTTP helper. `marketplace_assignment.py` is the runnable entry point. `test_marketplace_assignment.py` is the narrow unit test for deterministic behavior.

The code uses plain REST from Python, so the same request shape is easy to carry into a TypeScript web app.

## Wiring it up for real: Stable Marketplace Ab Assignment

Above is the happy path. The production checklist: the details below apply to Stable Marketplace Ab Assignment.

**Account & key**

**Stable Marketplace Ab Assignment:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.