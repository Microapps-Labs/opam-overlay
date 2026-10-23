#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
demo_dir=$(mktemp -d)
trap 'rm -rf "$demo_dir"' EXIT HUP INT TERM
mkdir -p "$demo_dir/scripts" "$demo_dir/source/resend-eio"
cat > "$demo_dir/scripts/publish_release.py" <<'PYMETA'
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
PYMETA
cat "$root/scripts/publish_release.py" >> "$demo_dir/scripts/publish_release.py"
cp "$root/release-manifest.json" "$demo_dir/release-manifest.json"
cp "$root/docs/demo/resend-eio.opam" "$demo_dir/source/resend-eio/"
tar -czf "$demo_dir/source.tar.gz" -C "$demo_dir/source" resend-eio
fixture_commit=$(cat "$root/docs/demo/source-commit.txt")
printf 'Local release-generator fixture, no publication\n\n'
printf 'Synthetic version: v0.0.0-demo\nInput: recorded resend-eio source metadata\n\n'
uv run --script "$demo_dir/scripts/publish_release.py" \
  --source Microapps-Labs/resend-eio --tag v0.0.0-demo \
  --commit "$fixture_commit" --archive "$demo_dir/source.tar.gz"
printf '\nGenerated definition lint:\n'
opam lint "$demo_dir/packages/resend-eio/resend-eio.0.0.0-demo/opam"
printf '\nNo source tag, release, dispatch or remote write occurred.\n'
