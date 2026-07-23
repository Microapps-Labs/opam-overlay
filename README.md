# OlegHQ opam overlay

This is the release repository for the OCaml libraries maintained by OlegHQ
and `nexo-tech/flo`. Add it ahead of the default repository:

```sh
opam repository add oleg-overlay git+https://github.com/OlegHQ/opam-overlay.git --this-switch
opam repository set-repos --this-switch oleg-overlay default
```

Packages are generated from immutable source tags. Do not edit generated
definitions by hand; tag the source repository instead.

## Publishing

Each allowlisted source repository has a `v<opam-version>` tag workflow. It
dispatches this repository, which verifies the source/tag mapping, resolves the
tag to a commit, generates package definitions, checks their checksums and
lints them, then commits a new immutable package version.

The source workflow requires an `OPAM_OVERLAY_DISPATCH_TOKEN` Actions secret
with access only to this repository's dispatch endpoint.
