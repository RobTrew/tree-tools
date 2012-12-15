#!/bin/sh
# 
# Rob Trew www.complexpoint.net
# https://github.com/RobTrew/tree-tools
#
# Ver 0.03
# Logs today's FoldingText DONE items 
# (From "$DONE_LOG_FOLDER/FTDoneToday.txt" see MarkDoneTime.scpt)
# in DAYONE, 
# Avoiding duplication if called several times in one day
# ( Maintains a text file list of which items have already been logged today )

# Requires installation of the [DayOne Command Line Interface](http://dayoneapp.com/tools/)
# For more details of the dayone command line tool, try:
# man -t 'dayone' | pstopdf -i -o ~/Desktop/dayone.pdf

# Can be used with [HAZEL](http://www.noodlesoft.com/hazel.php) rules like:
## Watch:   DONE_TODAY_FILE (see below)
##  Date Last Modified is after Date last Matched
##  <AND> Date last Matched is not in the last 5 mins

# (The delay reduces the number of log events, 
# allowing time for a small set of actions within one project to be marked as done, 
# without undue fragmentation into separate DayOne Log events)

# PROJECT_PREFIX="## " # Edit this to an empty string (see next line) for unbolded Day-One project lines.
PROJECT_PREFIX="" # Edit this to "## " (see previous line) for **bolded** Day-One project lines.

DONE_LOG_FOLDER="$HOME/FTLog"
if [ ! -d "$DONE_LOG_FOLDER" ]; then mkdir $DONE_LOG_FOLDER; fi
DONE_TODAY_FILE="$DONE_LOG_FOLDER/FTDoneToday.txt"
LOGGED_TODAY_FILE="$DONE_LOG_FOLDER/FTLoggedToday.txt"
LOG_NOW_FILE="$DONE_LOG_FOLDER/FTJustDone.txt"
DAY1_ENTRY="$DONE_LOG_FOLDER/Day1Entry.txt"
TODAY="@done($(date "+%Y-%m-%d")"

# WHAT, IF ANYTHING, NEEDS TO BE LOGGED
if ! [[ -f $DONE_TODAY_FILE ]]; then
    exit 1
fi
# IF SOME THINGS HAVE ALREADY BEEN LOGGED TODAY,
# IS THERE ANYTHING OUTSTANDING ?
if [ -f $LOGGED_TODAY_FILE ]; then
    if grep -q $TODAY $LOGGED_TODAY_FILE; then # Find items in the full DONE list which have NOT yet been logged
       awk 'FNR==NR{old[$0];next};!($0 in old)' $LOGGED_TODAY_FILE $DONE_TODAY_FILE > $LOG_NOW_FILE
    else # nothing yet logged from today
        cp -f $DONE_TODAY_FILE $LOG_NOW_FILE
        rm $LOGGED_TODAY_FILE # No longer needed
    fi
else # NOTHING YET LOGGED, SO PREPARE TO LOG IT ALL
   cp -f $DONE_TODAY_FILE $LOG_NOW_FILE
fi

# PUSH THE 'TO LOG' LIST THRU SED (reduce @done(%Y-%m-%d %H%M) to @done(%H%M)) 
# AND AWK TO A SIMPLY FORMATTED FILE (done items listed under parents)
if [ -s $LOG_NOW_FILE ] ; then
cat $LOG_NOW_FILE | sed -e "s/@done([0-9-]* /@done(/g" | \
awk -v d1_entry=$DAY1_ENTRY -v prj_prfx="$PROJECT_PREFIX" '
function rtrim(s) { sub(/[ \t]+$/, "", s); return s }
BEGIN {FS="\~\|\~"; prj=0}
{
  if (prj!=$3) {prj=$3;
        if (prj!="") {
            if (prj !~ /^#/) {if (prj_prfx!="") {prj= prj_prfx prj}}
            if (prj !~ /:$/) {print "\n" rtrim(prj) ":" >> d1_entry}
            else {print "\n" prj >> d1_entry}
        } 
    }
  if ($5!=prj) { print $5 >> d1_entry }
}'

# IF THERE'S ANYTHING IN THE FORMATTED FILE, SEND IT TO DAY ONE
if [ -s $DAY1_ENTRY ] ; then
# cat $DAY1_ENTRY # debugging
cat $DAY1_ENTRY | /usr/local/bin/dayone new
rm $DAY1_ENTRY
fi

# AND ADD WHAT WE'VE JUST LOGGED TO THE LIST OF THINGS LOGGED TODAY
cat $LOG_NOW_FILE >> $LOGGED_TODAY_FILE  # Append the list of logged tasks to avoid duplication
rm $LOG_NOW_FILE
# rm $LOGGED_TODAY_FILE # debugging

# THEN MAKE A NOISE TO CONFIRM THAT SOMETHING WAS LOGGED ...
afplay /System/Library/Sounds/Pop.aiff
fi
