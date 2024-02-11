#!/bin/bash -ex

source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

[ -n "${CONTENT_LENGTH}" ] && dd bs=${CONTENT_LENGTH} > /dev/null

echo -e 'Content-type: text/html\n\n'

echo "test"

cd "$contentsdir"
git pull

## CREATE TIMESTAMP FILES
find posts pages -maxdepth 1 -type d |
	grep / |
	while read d ; do
		[ -f "$contentsdir/$d/main.md" ] &&
			mkdir -p "$datadir/$d" &&
			## ADD TIME FILES
		git log -p "$contentsdir/$d/main.md" |
			grep ^Date |
			awk '{print $2,$3,$4,$5,$6}' |
			date -f - "+%Y-%m-%d %H:%M:%S" |
			awk -v cf="$datadir/$d/created_time" -v mf="$datadir/$d/modified_time" 'NR==1{print > mf}END{print > cf}'
	done


## MAKE SOME SHORTCUT
find posts pages -maxdepth 1 -type d |
	grep / |
	while read d ;do
		[ -f "$contentsdir/$d/main.md" ] || continue

		grep -m 1 '^# ' "$contentsdir/$d/main.md" |
			sed 's/^# *//' |
			awk '{if(/^$/){print "NO TITLE"}else{print}}END{if(NR==0){print "NO TITLE"}}'|
			tee "$datadir/$d/title"|
			sed -r "s;(.*);<a href=\"/\?${d}\"\>\1</a>;" |
			sed "s;s/;=;" > "$datadir/$d/link"
		touch "$datadir/$d/nav"
	done


## MAKE POST LIST
cd "$datadir"
find posts -type f |
	grep created_time |
	xargs  grep -H . |
	sed 's;/created_time:; ;' |
	awk '{print $2,$3,$1}' |
	sort -s -k1,1 |
	cat > "$datadir/post_list"

## MAKE PREV\NEXT NAVIGATION LINK
cat "$datadir/post_list" |
	 while read ymd hms d ;do 
		 grep -C1 $d "$datadir/post_list" | 
			 awk '{print $3}' | 
			 sed -n -e '1p' -e '$p' | 
			 xargs -I@ cat @/link | 
			 awk 'NR<=2{print}END{for(i=NR;i<2;i++)print "LOST TITLE"}'| 
			 sed -e '1s/^/prev:/' -e '2s/^/next:/'|
			 tr '\n' ' ' |
			cat  > "$datadir/$d/nav"
	 done
