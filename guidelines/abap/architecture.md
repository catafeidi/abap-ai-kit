# ABAP object orientation and architecture

Applies to every ABAP project. Style details: `clean-abap.md` (and the full guide in skill
`clean-abap`, chapters Classes, Methods, Error Handling, Testing). Patterns with ABAP code:
cheat sheets `04_ABAP_Object_Orientation` and `34_OO_Design_Patterns` (skill `sap-abap`).

## Principles
- **Classes over function modules and forms** for new logic; function modules only where the
  technology needs them (RFC, update task, classic BAdI shells) and then as a thin shell that
  delegates to a class.
- **Program to interfaces.** Every dependency that touches the outside world (database, RFC,
  HTTP, files, time, user, other components) sits behind an interface. The class receives it in
  the constructor (constructor injection); a factory or a composition root creates the real
  objects. Tests pass doubles.
- **One responsibility per class**; small public interfaces; members `PRIVATE` by default; classes
  `FINAL` unless built for inheritance (prefer composition to inheritance).
- **Layers that only call downward:** entry point (report, RFC shell, HTTP handler, RAP behaviour)
  -> application service / use case -> domain logic -> adapters (persistence, remote calls). Domain
  logic does not know about HTTP, ALV or JSON.
- **Exceptions:** one exception super class per component (`CX_STATIC_CHECK` for expected errors the
  caller must handle, `CX_NO_CHECK` for programming errors), message classes or T100 texts, and
  `previous` kept when you wrap.
- **Immutable values** where possible (`READ-ONLY` attributes set in the constructor, value objects
  for keys and money); avoid global state and static attributes that hold data.
- **No hidden LUW control:** reusable classes do not `COMMIT WORK`; the entry point owns the
  transaction (in RAP the framework does).

## Patterns that pay off in ABAP
| Need | Pattern |
|---|---|
| Choose an implementation by platform / customizing | strategy + factory (or BAdI) |
| One entry point, many operations (HTTP endpoints, commands) | command objects + a dispatcher |
| Replace a dependency in tests | interface + constructor injection (test double) |
| Expensive or remote reads | repository class behind an interface, with a cache if needed |
| Legacy code without seams | extract an interface around the legacy call (adapter), test the new code |
| Notify several consumers | events (`RAISE EVENT` / RAP business events) instead of direct calls |

Avoid: singletons that hold state, utility classes with dozens of static methods, deep
inheritance, "manager" god classes, boolean parameters that switch behaviour.

## For RAP (ABAP Cloud projects)
Follow the RAP reference scenario (SAP Flight reference, see `SOURCES.md`): CDS data model ->
behaviour definition -> behaviour implementation -> projection -> service definition / binding;
determinations and validations instead of logic in the UI; one RAP BO per business object.
