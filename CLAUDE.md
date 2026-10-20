# CLAUDE.md

Lab exercise for PGR301 that demonstrates feature management with [Unleash](https://unleash.io) by toggling between a mock sentiment response and a live AWS Comprehend call inside an AWS Lambda function. Deployed with AWS SAM.

## Repository layout

- `hello_world/app.py` — Lambda handler. Reads `UNLEASH_API_TOKEN` from env, checks a feature flag, and either returns a mocked positive sentiment or calls `comprehend.detect_sentiment` on the request body.
- `hello_world/requirements.txt` — Python dependencies for the function.
- `template.yaml` — SAM template. Defines the `HelloWorldFunction` (python3.9, x86_64), the `POST /sentiment` API event, and the `ComprehendFullAccess` policy. The Unleash token is injected via the `UNLEASH_API_TOKEN` env var.
- `event.json` — API Gateway proxy event used by `sam local invoke`. The text to analyze lives in the `body` field.
- `events/` — Additional sample events.
- `tests/` — Unit tests for the handler.

## Common commands

Build and invoke locally (uses Docker; `--use-container` matches the Lambda runtime):

```shell
sam build --use-container
sam local invoke -e event.json
```

Deploy to AWS (first time uses `--guided` to create `samconfig.toml`):

```shell
sam deploy --guided
```

Subsequent deploys: `sam deploy`.

## Configuration knobs students must set

- `template.yaml`: replace the `UNLEASH_API_TOKEN` placeholder value with the token handed out in class.
- `hello_world/app.py`: change the toggle name in `client.is_enabled('...')` to the flag the student created in Unleash (names are globally shared, so each student uses a personal suffix like `glenn_toggle`).

## Behavior

- Toggle **off** → handler short-circuits and returns `{"sentiment": "positive"}` (no confidence score).
- Toggle **on** → handler calls AWS Comprehend's `detect_sentiment` on `event["body"]` and returns the mapped label plus the confidence score.

Running against AWS Comprehend requires valid AWS credentials (`aws configure`, region `eu-west-1`).

## Unleash instance

Hosted at `https://eu.app.unleash-hosted.com/eubb1043/`. Toggles live under the "Default" project. The lab also walks through a Randomized 50% rollout strategy.

## Notes for Claude

- This is teaching material: keep the README approachable for students and preserve the step-by-step flow.
- The example toggle name in the README (`glenn_toggle`) is intentional — do not rename it to match whatever is in `app.py` without checking, since `app.py` carries the instructor's working value and the README documents the student-facing example.
- Do not commit real Unleash tokens or AWS credentials. The `UNLEASH_API_TOKEN` value in `template.yaml` must stay a placeholder in version control.
