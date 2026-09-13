# Discovery runtime harness

`discovery-runtime-harness.mjs` is an unchanged copy of
`27vette:tests/lib/runtime-harness.mjs` at commit
`4fe92a4f078370c478f18484cad31bdafe58ad43`, SHA-256
`3133fdea83e783c312297cc284f2cc015ff8f00f2ed96bf9d3e085a469612ac4`.
This is the exact harness identified by all six retained discovery observations.
It provides stub DOM/network behavior, not application code for deployment.

The discovery probe verifies this hash before exposing its additional inspection
functions. By default it reads this fixture without needing Git or a 27vette
checkout; an explicit reference-repository argument still reads the pinned Git
blob and checks the same hash. The frozen baseline archive and runtime evidence
are not refreshed. Reproduction verifies the current and historical probe hashes
separately, then compares bytes allowing only that probe-identity change and
`compact.submitted_at` timestamps. All other provenance and observations must match.

Run runtime reproduction with Node and tar available:

```sh
python3 -m unittest discover -s tests -p test_model_discovery.py -k every_lane -v
```

Python requirements come from the root `requirements.txt`. The separate extractor
reproduction tests additionally require the ignored manufacturer original as
documented in `sources/README.md`; this fixture does not substitute for that input.
