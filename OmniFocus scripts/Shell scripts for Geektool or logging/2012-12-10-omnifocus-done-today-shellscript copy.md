---
layout: default
title: List items completed in OmniFocus since midnight
description: Use this shell script for a Geektool listing, or for logging to DayOne etc.
---

{{page.description}}

Shell script which lists OmniFocus tasks marked as completed since midnight last night.

(The script directly queries the OmniFocus Sqlite cache, and doesn't require OmniFocus to be running).

The default output format is broadly that of TaskPaper or FoldingText:

    DONE TODAY (6)

    Project A:
    - task1 @done(yyyy-mm-dd HH:MM)
    - task2 @done(yyyy-mm-dd HH:MM)
    - taskN @done(yyyy-mm-dd HH:MM)

    Project B:
    - taskX @done(yyyy-mm-dd HH:MM)
    - taskY @done(yyyy-mm-dd HH:MM)
    - taskZ @done(yyyy-mm-dd HH:MM)

Usage:
- For GeekTool, use the simple print at the end of the Awk code
- For DayOne, comment out the simple print line, and uncomment:

    `print str | "/usr/local/bin/dayone new" # /usr/local/bin/dayone -h for options`

- For a PDF version of the man page for the DayOne command line utility:

	`man -t 'dayone' | pstopdf -i -o ~/Desktop/dayone.pdf`


- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/OmniFocusDoneToday.sh)
