#!/bin/sh
# Ver 0.02
# Lists items done today in the OmniFocus Sqlite cache
OFOC="com.omnigroup.OmniFocus"
if [ ! -d "$HOME/Library/Caches/$OFOC" ]; then OFOC=$OFOC.MacAppStore; fi
OFQUERY="sqlite3 $HOME/Library/Caches/$OFOC/OmniFocusDatabase2"
START_OF_DAY=$(date -v0H -v0M -v0S +%s) #Midnight at the start of today: set the time component to 00:00

# Suggestions welcome here - not sure this simple arithmetic works for New Zealand's DST +1300 UTC
ZONERESET=$(date +%z | awk '
{if (substr($1,1,1)!="+") {printf "+"} else {printf "-"} print substr($1,2,4)}') 
YEARZERO=$(date -j -f "%Y-%m-%d %H:%M:%S %z" "2001-01-01 0:0:0 $ZONERESET" "+%s")
DONE="($YEARZERO + t.dateCompleted)";

# This join includes context & folder, to allow for broader queries
JOIN="(((task tt left join projectinfo pi on tt.containingprojectinfo=pi.pk) t
left join task p on t.task=p.persistentIdentifier)
left join context c on t.context = c.persistentIdentifier)
left join folder f on t.folder=f.persistentIdentifier"

MATCHES="$DONE > $START_OF_DAY"
doneTOTAL=$($OFQUERY "SELECT count(*) FROM $JOIN WHERE $MATCHES;")
printf "DONE TODAY (%s)\n\n" "$doneTOTAL"

$OFQUERY "
SELECT strftime('%w|%m|%d|%Y|%H:%M',$DONE, 'unixepoch'), p.name, t.name
FROM $JOIN WHERE $MATCHES ORDER BY t.datecompleted
" | awk '
BEGIN {FS="\|"; prj=0; str=""}
{
	if (prj!=$6) {prj=$6;
		if (prj!="") {str = "## " prj} 
	}
	if ($7!=prj) {str = str ":\n- " $7 " @done(" $4 "-" $2 "-" $3 " " $5 ")\n"}
	else {{str = str ": @done(" $4 "-" $2 "-" $3 " " $5 ")\n"}}
	print str # GeekTool etc, or use the line below for DayOne
	#print str | "/usr/local/bin/dayone new" # /usr/local/bin/dayone -h for options
}'
