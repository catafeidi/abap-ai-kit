# SAP Fiori launchpad content

How an app reaches users. Applies to the ABAP front-end server launchpad. In SAP Build Work Zone
the target mapping comes from the inbounds in the app's `manifest.json`, and catalogs, spaces and
roles are content of the site manager.

## The chain
`app (BSP / repository)` -> **target mapping** (semantic object + action -> app, parameters) ->
**tile** (static or dynamic, points to the semantic object and action) -> **business catalog**
(holds tiles and target mappings: what a user is *allowed* to start) -> **space / page** (what a
user *sees*; replaces the older groups) -> **business role** (PFCG role with the catalogs and
spaces) -> user.

## Rules
- **One intent per app function:** semantic object + action named after the business object and
  what is done (`SalesOrder-display`); reuse a standard SAP semantic object when it exists.
- **Catalogs grant, spaces arrange:** put tiles and target mappings in business catalogs; arrange
  them for users in spaces and pages. Groups only on releases without spaces.
- **Roles are the only assignment** to users; never assign catalogs to users directly.
- **Choose the layer by how the content is delivered:**
  - delivered with a product, an add-on or to several clients: the **configuration layer** (CONF,
    cross-client, workbench transport);
  - specific to one customer client: the **customizing layer** (CUST, client-specific, customizing
    transport).
  Content in CUST overrides CONF for that client. Customers adapting SAP's delivered (CONF) catalogs
  in CUST is normal; for your own content pick one layer per catalog and keep to it.
- **Maintain with the content tools** of your release (launchpad content manager and designer for
  catalogs, the space / page apps for spaces), not by editing tables.
- **Transport every object** (app, catalog, target mapping, space, page, role) in the same release
  path as the app; record in the notes which request carries which object.
- **Test as a user with only the business role**, not as a developer with full authorisation: the
  tile shows, the app starts, the OData service is authorised (PFCG start authorisation for the
  service).
