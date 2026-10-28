# ABAP Cheat Sheets — Router Index

Full upstream copy of `SAP-samples/abap-cheat-sheets` (main). Before writing or reviewing
ABAP for a topic below, READ the matching file in this folder and align to it.

> **Release caveat:** These sheets target ABAP Cloud / latest release. The primary target
> system here is **7.40** (classic). Cross-check any construct against the Version
> Compatibility table in `../../SKILL.md`. On 7.40: no `FINAL(...)`, no `@( expr )` host
> expressions, no `UNION`/CTE `WITH`, no `IS INSTANCE OF`/`CASE TYPE OF`, no test seams,
> no `utclong`, no enumerated types. Use `DATA(...)`, `@var`, typed `CAST` + catch, etc.

## Topic → file

| When working on… | Trigger keywords | File |
|---|---|---|
| Internal tables | itab, READ/LOOP/MODIFY/DELETE, keys, table expr | `01_Internal_Tables.md` |
| Structures | BEGIN OF, work area, CORRESPONDING, MOVE-CORRESPONDING | `02_Structures.md` |
| ABAP SQL | SELECT/INSERT/UPDATE/MODIFY/DELETE, joins, aggregates, `@` | `03_ABAP_SQL.md` |
| OO (classes/interfaces) | CLASS, METHODS, INTERFACES, events, friends, visibility | `04_ABAP_Object_Orientation.md` |
| Constructor expressions | VALUE, NEW, CONV, COND, SWITCH, REDUCE, FILTER, CORRESPONDING, REF, CAST | `05_Constructor_Expressions.md` |
| Dynamic programming | field-symbols, data refs, RTTI/RTTC, ASSIGN, CREATE DATA | `06_Dynamic_Programming.md` |
| String processing | string templates, find/replace, `\|...\|`, condense, segment | `07_String_Processing.md` |
| EML / RAP behavior | MODIFY ENTITIES, READ ENTITIES, COMMIT ENTITIES, EML | `08_EML_ABAP_for_RAP.md` |
| Bits and bytes | xstring, bit ops, hex | `09_Bits_and_Bytes.md` |
| SQL hierarchies | HIERARCHY, hierarchical data | `10_ABAP_SQL_Hierarchies.md` |
| Internal table grouping | LOOP AT ... GROUP BY, GROUP SIZE | `11_Internal_Tables_Grouping.md` |
| AMDP | AMDP, SQLScript methods, BY DATABASE PROCEDURE | `12_AMDP.md` |
| Program flow / control | IF/CASE/DO/WHILE/LOOP, CHECK, EXIT, RETURN, control structures | `13_Program_Flow_Logic.md` |
| **Unit tests** | ABAP Unit, FOR TESTING, cl_abap_unit_assert, test doubles, seams, LOCAL FRIENDS | `14_ABAP_Unit_Tests.md` |
| CDS view entities | DEFINE VIEW ENTITY, annotations, associations, DCL | `15_CDS_View_Entities.md` |
| Data types & objects | TYPES, DATA, CONSTANTS, generic types, built-in types | `16_Data_Types_and_Objects.md` |
| SAP LUW | COMMIT/ROLLBACK WORK, update FMs, transactional, CALL FUNCTION IN UPDATE TASK | `17_SAP_LUW.md` |
| Dynpro | classic screens, PBO/PAI, screen fields | `18_Dynpro.md` |
| ABAP for Cloud Dev | released APIs, ABAP Cloud restrictions, if_oo_adt_classrun | `19_ABAP_for_Cloud_Development.md` |
| Selection screens / lists | PARAMETERS, SELECT-OPTIONS, WRITE, classic lists | `20_Selection_Screens_Lists.md` |
| XML / JSON | sXML, CALL TRANSFORMATION, /ui2/cl_json, serialize/deserialize | `21_XML_JSON.md` |
| Released ABAP classes | released APIs, cl_abap_*, xco_*, whitelist | `22_Released_ABAP_Classes.md` |
| Date and time | sy-datum, cl_abap_*_utilities, xco time, timestamps | `23_Date_and_Time.md` |
| Built-in functions | strlen, find, replace, numeric/table built-ins | `24_Builtin_Functions.md` |
| Authorization checks | AUTHORITY-CHECK, authorization objects | `25_Authorization_Checks.md` |
| ABAP Dictionary | DDIC, tables, data elements, domains, structures, CDS entities | `26_ABAP_Dictionary.md` |
| Exceptions | TRY/CATCH/CLEANUP, RAISE EXCEPTION, cx_*, RESUMABLE | `27_Exceptions.md` |
| Regular expressions | REGEX, PCRE, FIND ... REGEX, cl_abap_regex/matcher | `28_Regular_Expressions.md` |
| Numeric operations | arithmetic, rounding, decfloat, packed, overflow | `29_Numeric_Operations.md` |
| Generative AI | ABAP + GenAI, ISLM, AI SDK | `30_Generative_AI.md` |
| WHERE conditions | WHERE, logical operators in SQL/itab, ranges | `31_WHERE_Conditions.md` |
| Performance | performance, PACKAGE SIZE, secondary keys, buffering | `32_Performance_Notes.md` |
| Release news | version differences, "since 7.xx", new syntax | `33_ABAP_Release_News.md` |
| OO design patterns | singleton, factory, strategy, DI, decorator | `34_OO_Design_Patterns.md` |
| BAdIs | GET BADI, CALL BADI, enhancement, BAdI definition | `35_BAdIs.md` |
| RAP BDL | behavior definition, managed/unmanaged, determinations, validations, actions | `36_RAP_Behavior_Definition_Language.md` |
| Logical expressions | IS, boolc/xsdbool, predicate functions, ternary-like COND | `37_Logical_Expressions_and_Functions.md` |

## How to use per task
1. Identify the topic(s) the change touches (a change can touch several — e.g. a class
   method with SQL + exceptions → sheets 04, 03, 27).
2. Read the matching file(s) here.
3. Write/review to match the documented idioms, then downgrade any 7.5x+ syntax for 7.40.
4. If your code diverges from the sheet, either fix it or state why explicitly.

## Clean ABAP (style guide)

`../clean-abap/CleanABAP.md` is a copy of SAP's Clean ABAP guide
(https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md). It is the default
coding standard (a project may tighten it in its AGENTS.md). Before writing or reviewing ABAP, read the sections
that match the change (grep the `###` and `####` headings: Names, Constants, Classes,
Methods, Error Handling, Comments, Formatting, Testing). Rules that are easy to miss:
do not align type clauses; do not align assignments to different objects; group constants;
own exception super class; members PRIVATE by default; FINAL unless designed for
inheritance. On 7.40 two rules cannot be followed and are accepted deviations: `ENUM`
(7.51) and `RAISE EXCEPTION NEW` (7.52).
