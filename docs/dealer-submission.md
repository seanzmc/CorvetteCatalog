# Dealer submission integration

The consumer form prepares a dealer order from its confirmed release-backed
session, collects contact details and preserves the existing Stingray Chevrolet
submission contract. Local preview is the default. Live delivery is an explicit
server option; no dealer requests are made by the Python service.

## Run

Use a completed release built with this runtime:

```sh
python3 -m catalog.consumer_server --store PATH --release CONTENT_ID
```

“Preview dealer submission” displays the prepared payload without loading
Turnstile or contacting the dealership. Contact details stay in page memory and
request-local variables; they are not written to the catalog or a local outbox.

For a qualified host and authorized real delivery, add
`--enable-dealer-submissions`. The browser then uses the existing public Turnstile
site key and posts directly to
`https://stingraychevroletcorvette.com/wp-json/corvette-build/v1/submit`.
The existing WordPress receiver remains responsible for validating the token and
processing the order. Production host allowlisting, CORS, receiver verification
and actual delivery are separate deployment checks. This local loopback server
is not a public hosting configuration.

## Preserved contract

The reference is `27vette/form-app/app.js`: `compactOrder`,
`dealerSubmissionPayload`, `plainTextOrderSummary` and `postDealerSubmission`.
The six base-build observations in `tests/fixtures/dealer-baseline.json` retain
source hashes and executed outputs from its read-only runtime harness.

The submitted object has exactly these seven fields:

| Field | Meaning |
| --- | --- |
| `model` | Existing model registry key, including `grandSport` and `grand_sport_x` |
| `customer` | Required name/email; optional phone/address/comments |
| `vehicle` | Body style, uppercase trim label, display name and numeric starting price |
| `sections` | Ordered nonempty recap sections with `{rpo, label, price}` items |
| `msrp` | Formatted total including destination and applicable required charges |
| `plain_text_summary` | The existing escaped HTML fragment despite its legacy field name |
| `turnstile_token` | Browser security-check token verified by the existing receiver |

Section order and labels follow the accepted catalog presentation. Within a
section, items use stable catalog order rather than the old selection-insertion
order. All prices come from actual evaluator charge owners. Zero prices remain
zero; a no-separate-charge reference does not acquire an invented price. A code
marked non-emitting is blank in a routed recap item; equipment with no recap
route stays out of the dealer summary. For example, R8C remains a $1,695 delivery
choice while its included CFX reference is not emitted as an order code.

Standard equipment remains a separate consumer rollup. The recap includes
selections, their connected additions and every actual charge. A zero-price
configuration-only item does not populate the Required Charges section. Paid
seat and component owners are counted once. In particular, a purchased AE4 seat
alongside R6X remains visible and charged even when legacy interior component
copy omitted that owner. Accepted current prices and copy take precedence over
retained source presentation amounts; fractional-dollar edits retain cents.

## Confirmation and failure behavior

`/api/dealer/review` and `/api/dealer/prepare` require a current session version.
Pending changes, incomplete builds, stale versions and caller-supplied order
contents are refused. The prepare response associates the payload and its hash
with the release, revision and confirmed version; those internal fields do not
change the dealer wire format.

The contact dialog requires name and email, disables duplicate requests while
sending, and locks the same build after a positive receipt. Changing the
confirmed build clears that receipt. Failures preserve contact details and reset
the security check. Expired or failed security checks cannot enable submission.
A malformed response cannot be mistaken for success. Delivery has a 30-second
response timeout and no automatic retry; ambiguous delivery tells the user to
check with the dealership before retrying.

Only live mode loads the security script and permits the specific dealer and
Turnstile origins in the content security policy. The script/frame allowances
follow [Cloudflare's Turnstile CSP guidance](https://developers.cloudflare.com/turnstile/reference/content-security-policy/).
No new package, database schema or public dealer endpoint is introduced.

## Verification

`PYTHONPATH=tests python3 -m unittest test_dealer -v` covers six captured base-build
contracts, all 32 body/trim configurations, paid interior ownership, package and
reference-code semantics, edited prices/copy, contact escaping, stale/pending/
incomplete refusal, and completed-release packaging in preview/live modes.
Release packaging tests isolate the expensive semantic audit; real release
qualification and affected-flow browser checks are recorded in the PR.

The migration sprint browser checks intercept every external dealer and
Turnstile request. They exercise contact entry, security expiry, rejected and
malformed responses, network failure, duplicate submission, receipt reopening,
preview-only operation and responsive layout. They do not prove an actual
WordPress receipt, a dealership notification, production deployment or canonical
cutover. The workbook remains canonical.
