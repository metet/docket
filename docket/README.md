# Docket store — Docket's own development

This store is where Docket's design is worked out, using Docket. It is the
protocol's first real store and its own dogfood test.

Because the store lives *inside the spec repo*, the normative documents are not
copied here — they are one level up:

- Protocol: [`../PROTOCOL.md`](../PROTOCOL.md)
- Parties:  [`../PARTIES.md`](../PARTIES.md)

`INDEX.md` is generated. Regenerate with `tools/docket-index`, validate with
`tools/docket-lint`. Never hand-edit either the index or an existing filing.
