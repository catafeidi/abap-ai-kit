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
