# Local output capture

Captured on 2026-10-23 from base source revision `b1d582010539395e171d7228dcb0157231c4851c`, with the example and copy changes in this commit.

The real release generator ran in a temporary copy against source opam metadata and a synthetic v0.0.0-demo version. The generated file passed opam lint with warning 37 because the source metadata lacks dev-repo. No source tag was created and no workflow or release was published.

The PNG is a browser-rendered transcript of the output saved in output.txt, not a fabricated application UI. Reproduce the output with sh docs/demo/run.sh from the repository root. No credentials or client data appear in the capture.
