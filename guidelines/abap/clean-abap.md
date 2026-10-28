# Clean ABAP: the working subset

Source of truth: SAP's Clean ABAP guide, bundled at `skills/clean-abap/reference/CleanABAP.md`
(https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md). This page is the subset
that matters most in practice. For exact wording, grep the guide's `###` / `####` headings.

When legacy code around a change uses another convention, keep cosmetic consistency inside that
object, but never at the cost of correctness, safety or readability. New objects follow this page.

## Names
- Descriptive names, no abbreviations, no Hungarian prefixes (`lv_`, `lt_`, `ls_`, `lo_`, `gv_`,
  `mo_`, `iv_`, `rv_`). A project may keep prefixes for legacy objects; it says so in its `AGENTS.md`.
- Booleans read as predicates: `is_`, `has_`, `can_`. A flag with three values is not a boolean.
- Use the terms of the domain and of SAP, not invented words.

## Language
- `NEW #( )`, functional calls `obj->method( )`, string templates, inline declarations at first
  use (not inside a branch when used after it), constructor expressions (`VALUE`, `CORRESPONDING`,
  `COND`, `SWITCH`, `REDUCE`, `FILTER`), table expressions with `line_exists( )`.
- No `CALL METHOD`, `CREATE OBJECT`, `MOVE`, `COMPUTE`, `CONCATENATE` for simple joins, header
  lines, `OCCURS`, `TYPE-POOLS`, `TRANSLATE ... TO UPPER CASE` (use `to_upper( )`).
- `abap_true` / `abap_false` / `abap_bool`, never `'X'` / `space`.

## Constants
- No magic literals; group constants (`CONSTANTS BEGIN OF ...`) or use an interface/enum class.
- Type constants with their real DDIC type.

## Classes and methods
- Small methods that do one thing at one level of abstraction.
- At most about three importing parameters; prefer `RETURNING` over a single `EXPORTING`.
- No boolean input parameter that switches behaviour: split the method.
- Avoid optional parameters that hide complexity.
- Members `PRIVATE` by default, classes `FINAL` unless designed for inheritance; interfaces for
  anything that will be replaced in tests.

## Control flow
- Return early; avoid deep nesting. `CASE` over long `ELSEIF` chains.
- No empty `WHEN OTHERS` or `CATCH` that swallows.

## Error handling
- Class-based exceptions. Do not propagate return codes or `sy-subrc`.
- After a classic function module with `EXCEPTIONS`, evaluate `sy-subrc` and raise.
- Catch specific exceptions, not `cx_root`. Keep `previous`.
- `MESSAGE ... TYPE 'X'` is not control flow.

## ABAP SQL
- Explicit field list, never `SELECT *` in new code. A `WHERE` on key fields.
- `SELECT SINGLE` or `UP TO 1 ROWS` for one row. No `SELECT` in a loop.
- `FOR ALL ENTRIES` only after checking the driver table is not empty.

## Formatting and comments
- Do not align type clauses or assignments to different objects.
- Comments say why, not what. No dividers (`*&---`), no commented-out code, no `BREAK-POINT`.

## Accepted deviations on 7.40
`ENUM` (7.51) and `RAISE EXCEPTION NEW` (7.52) are not available. Use a constants interface or
an enum class, and `RAISE EXCEPTION TYPE`.
