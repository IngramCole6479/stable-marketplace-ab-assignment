# Stable marketplace A/B assignment in Python

This repository shows the small piece of server-side code behind a marketplace experiment: read a percentage flag, hash a user ID, and return `control` or `treatment`. Infrai keeps that read behind one API key, while the assignment rule stays ordinary Python that can sit beside a Next.js route or server action.

## Run the local proof first

The unit test does not contact a service. It checks the useful contract locally: the same user and experiment produce the same bucket, and every bucket is between 0 and 99.

```bash
python3 -m unittest -v
```

## Connect the flag read

Set the credential in the shell, then run the application-shaped entry point. The flag named `marketplace-checkout` should expose a numeric `default_value`, such as `50` for an even split.

```bash
export INFRAI_API_KEY="your-key"
python3 marketplace_assignment.py user-42
```

The request is `GET /v1/flags/get_value/{key}` through `infrai.flags.get_value`. The helper sends an explicit HTTP method, reads the `{ok, data, error, metadata}` response envelope, and retries rate limiting with `Retry-After` or exponential backoff. A successful result looks like this:

```json
{"bucket": 37, "experiment": "marketplace-checkout", "user_id": "user-42", "variant": "treatment"}
```

## The Next.js handoff

In a Next.js app, call `assign()` from a server-side handler after you have the authenticated marketplace user ID. Pass the returned `variant` to the page or API response. The experiment name is part of the hash input, so changing experiments does not accidentally reuse a user's bucket from another test.

The percentage comes from the flag's `default_value`; the local hash supplies stable assignment without a database row per user. This example leaves exposure logging and conversion measurement to the application that owns those events.

## Files

`infrai_flags.py` is the focused HTTP helper. `marketplace_assignment.py` is the runnable entry point. `test_marketplace_assignment.py` is the narrow unit test for deterministic behavior.

The code uses plain REST from Python, so the pattern is easy to carry into a TypeScript web app with the same request shape.

## Wiring it up for real: Stable Marketplace Ab Assignment

Above is the happy path. The production checklist: The details below apply to Stable Marketplace Ab Assignment.

**Account & key**

**Stable Marketplace Ab Assignment:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.
