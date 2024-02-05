#!/bin/bash
source "$(dirname $0)/conf"

md="$contentsdir/posts/20240205/main.md"

pandoc --template="$viewdir/template.html" -f markdown_github+yaml_metadata_block "$md"
