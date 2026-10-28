# ABAP Unit testing

Reference: `skills/sap-abap/references/cheat-sheets/14_ABAP_Unit_Tests.md`.

- Test classes `FOR TESTING RISK LEVEL HARMLESS DURATION SHORT`, local to the class under test
  (test include), one test method per behaviour, names that state the behaviour
  (`returns_empty_for_unknown_key`).
- Given / when / then structure; one reason to fail per test.
- Replace dependencies through interfaces and constructor injection (test doubles,
  `cl_abap_testdouble`, or local fake classes). For SQL use the test environments
  (`cl_osql_test_environment`, `cl_cds_test_environment`) where the release has them.
- Use published vectors for crypto, encoding and protocol code (FIPS, RFC, vendor test vectors).
- Cover negative cases: initial input, empty tables, exceptions raised and their texts.
- A test that only passes against one system's data is not a unit test; mark live checks as
  integration checks and keep them out of the unit test suite.
- Run the tests and report the real result. Do not claim coverage you did not run.
- New class on some releases: if ATC says "class not found" right after the first activation,
  activate the class a second time (the first activation writes cross-references only for the
  test include).

## RAP business objects (EML tests)
- Test save validations with `MODIFY ENTITIES` followed by
  `COMMIT ENTITIES IN SIMULATION MODE RESPONSE OF <bo> FAILED DATA(failed) REPORTED DATA(reported)`:
  every save-phase check runs, nothing is written, so the failing and the valid path both get a
  test. Type the responses as `RESPONSE FOR FAILED LATE <bo>` / `REPORTED LATE`.
- Do not test through draft actions: `EXECUTE Prepare` from a test does not reliably run the
  validations, and `EXECUTE Activate` can end in `BEHAVIOR_CONTRACT_VIOLATION`.
- `MODIFY ENTITIES ... IN LOCAL MODE` is only allowed inside the BO's own handlers; a shared helper
  called from elsewhere dumps. Use a plain `MODIFY` there (authorization is then enforced).
- EML derived types cannot be written inline in method signatures: declare them first
  (`TYPES ty_result TYPE STRUCTURE FOR READ RESULT <bo>\<entity>`).
- Messages: text with `%msg->if_message~get_text( )`, number with
  `%msg->if_t100_message~t100key-msgno`.
- `GET PERMISSIONS ONLY INSTANCE FEATURES` can return no row for a fresh instance: assert "no
  disabled row", not "row 1 enabled".
- "Activated successfully" can still leave the test include inactive, and the unit test run then
  reports no classes or misses methods: check the inactive objects and syntax-check the include
  before trusting a green run.
