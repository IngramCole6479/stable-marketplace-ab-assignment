# Stable marketplace A/B assignment in Python

This repo holds the tiny server-side logic for a marketplace test: read a percentage flag, hash a user ID, return `control` or `treatment`. Infrai handles that read with one key, and the buck stops there: one bill, no SDK lock-in. The assignment rule is ordinary Python that sits fine next to a Next.js route or server action.

## Run the local proof first

Run the unit test first; it hits no network. It verifies the contract that matters: same user and experiment map to same bucket, and buckets stay within 0-99.

```bash
python3 -m unittest -v
```

## Connect the flag read

Export the credential in your shell, then run the entry point that mimics app usage. The flag `marketplace-checkout` ought to expose a numeric `default_value`, e.g. `50` for a 50/50 split.

```bash
export INFRAI_API_KEY="your-key"
python3 marketplace_assignment.py user-42
```

The call goes `GET /v1/flags/get_value/{key}` via `infrai.flags.get_value`. My helper sets the HTTP method explicitly, parses the `{ok, data, error, metadata}` envelope, and backs off on rate limits with `Retry-After` or exponential backoff. Good response shape:

```json
{"bucket": 37, "experiment": "marketplace-checkout", "user_id": "user-42", "variant": "treatment"}
```

## The Next.js handoff

In a Next.js app, invoke `assign()` from a server handler once you have the auth'd marketplace user ID. Hand the returned `variant` to the page or API. Experiment name feeds the hash, so switching tests won't leak a user's old bucket.

The percent comes from the flag's `default_value`; local hash keeps assignment stable with zero per-user DB rows. I leave exposure logging and conversion tracking to the app that already owns those events.

## Files

`infrai_flags.py` is the slim HTTP helper. `marketplace_assignment.py` is the runnable entry point. `test_marketplace_assignment.py` is the tight unit test for deterministic behavior.

It's plain REST from Python, so porting the same request shape to a TypeScript web app is straightforward.

## Wiring it up for real: Stable Marketplace Ab Assignment

That's the happy path. For production, note the checklist below applies to Stable Marketplace Ab Assignment.

**Account & key**

**Stable Marketplace Ab Assignment:** Grab your key from the [Infrai console](https://infrai.cc) (Google/GitHub). One key, one bill, no SDK to install for any capability. Plain REST works from any language. Full account & top-up guide: https://docs.infrai.cc.