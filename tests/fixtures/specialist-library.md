# IRSpan

A Rust library for tracking source spans through SSA-to-CPS transformations in compiler research prototypes. Intended for compiler implementers already familiar with SSA and CPS.

Use it when your transformation pipeline needs provenance across rewritten blocks. It preserves origin sets; it does not validate program semantics. Unlike a single-location span field, origin sets can represent merged expressions.

## Requirements

Rust 1.82+. No hosted service. This experimental library is not a drop-in replacement for a compiler's existing source map.

## Example

```rust
let combined = OriginSet::merge(left.origin(), right.origin());
assert_eq!(combined.len(), 2);
```

The example shows two input origins retained after a merge. See [API documentation](https://example.org/irspan/api) for full types and integration instructions. That URL is a fictional fixture, not a verified destination.

Apache-2.0. Contributions are currently closed while the API stabilises.
