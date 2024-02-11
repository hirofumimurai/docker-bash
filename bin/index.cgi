#!/bin/bash -euvx
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

#md="$contentsdir/posts/20240205/main.md"

trap 'rm -f $tmp-*' EXIT

### VARIABLE
tmp=/tmp/$$
dir="$(echo ${QUERY_STRING} | tr -dc 'a-zA-Z0-9_=' | sed 's;=;s/;')"
md="$contentsdir/$dir/main.md"
[ -f "$md" ]

### MAKE METADATA
cat << FIN > $tmp-meta.yaml
---
#created_time: $(date -f - < $datadir/$dir/created_time)
created_time: $(cat $datadir/$dir/created_time)
modified_time: $(cat $datadir/$dir/modified_time)
title: $(grep '^#' "$md" | sed 's;^# *;;')
nav: $(cat "$datadir"/$dir/nav)
---
FIN




### MAKE HTML
pandoc --template="$viewdir/template.html" -f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml" | teip -e 'grep -n img' -- bash -c 'sed "s;src=\";src=\"/'$dir'/;"' 
