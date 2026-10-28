# ABAP security

Applies to every ABAP project. Review points are repeated in `code-review.md` (Security).

## Input that reaches SQL or dynamic code
- Prefer static Open SQL with host variables (`@lv_value`); they are never injectable.
- Dynamic `WHERE`, field lists, table names or `ORDER BY` built from input: whitelist the names
  (check against DDIC or a fixed list) and escape values with `cl_abap_dyn_prg`
  (`escape_quotes`, `quote`, `check_column_name`, `check_table_name_str`, `check_whitelist_tab`).
  Never concatenate raw input into a condition.
- No `GENERATE SUBROUTINE POOL`, `INSERT REPORT`, dynamic `CALL FUNCTION` / `CALL METHOD` /
  `SUBMIT` with names from input unless whitelisted.

## Authorization
- Every entry point (RFC, HTTP handler, report, RAP action) checks authority before it reads or
  changes data with `AUTHORITY-CHECK OBJECT ...`. Evaluate `sy-subrc` right after the check; a
  missing check of `sy-subrc` is a defect.
- ABAP for Cloud Development: `AUTHORITY-CHECK OBJECT` is allowed, with the object name as a
  literal and no `FOR USER` (current user only). Prefer the declarative checks: CDS access control
  (CDS roles) for reads through CDS views, RAP authorization control in the behavior definition
  for RAP business objects (cheat sheet `25_Authorization_Checks`).
- Check with the activity actually performed (`ACTVT` 03 for display, 02 change, 01 create, 06
  delete); `DUMMY` only where the field really does not matter.
- `CLIENT SPECIFIED` / `USING CLIENT` only with a documented reason; never let input choose the
  client.
- RFC-enabled modules are reachable from outside: treat their parameters as untrusted input and
  check `S_RFC` plus the business authorization.

## Files, URLs and output
- File names from input: build the path with logical file names (`FILE_GET_NAME`,
  `FILE_VALIDATE_NAME`) or validate against a base directory; reject `..`, absolute paths and
  unexpected characters (directory traversal).
- HTTP handlers: set the content type explicitly, escape output for its context
  (`escape( val = ... format = cl_abap_format=>e_html_text / e_json_string / e_url )`), never echo
  input into HTML, keep error responses free of stack traces, SQL texts and internal names.
- Outbound HTTP: destinations or communication arrangements, never hard-coded URLs or
  credentials; TLS certificate checks stay on.

## Secrets and data
- No passwords, keys or tokens in source, tables readable by everyone, logs or messages; use SSF,
  secure store or the destination service.
- Personal and customer data only as far as the function needs it; mask it in logs and
  application logs; delete temporary data (buffers, files) after use.
- Log security-relevant events (refused authorization, unusual input) to the application log
  without the secret values.

## Checks
- ATC / Code Vulnerability Analyzer where licensed (security checks); abaplint rules `sql_escape_*`
  style checks are limited, so review dynamic SQL by hand.
- Unit tests for the negative paths: refused authorization, malicious input, path traversal.
