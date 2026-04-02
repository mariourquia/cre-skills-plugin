#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
npx --prefix tools tsx tools/build.ts "$@"
