---
layout: default
title: Mark Done Time (and log) Script
description: Marks the selected todo item as @done(yyyy-mm-dd HH:MM), and appends a copy to a log file
---

{{page.description}}

Marks the selected line as done, including a date-time stamp (in FoldingText's default date-time format) in the @done tag.

	@done(yyyy-mm-dd HH:MM)
	
	@done(2012-12-05 21:15)

(Works with FoldingText's .todo mode)

The script also appends a copy of the done item (with any parent node, and with the file name, to a log file).

The log files (one per day – FTDoneYYYY-mm-dd.txt and a working copy called FTDoneToday.txt – are kept by default at ~/FTLog

A companion shell script [FTDoneLog.sh](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Task%20management/FTLogDone.sh) can be used (for example with [Hazel](www.noodlesoft.com/hazel.php)) to further log the done items to [Day One](https://itunes.apple.com/us/app/day-one/id422304217?mt=12) whenever the DoneToday.txt file changes.

In the Day One entries the @done tags are simplified from @done(2012-12-05 21:15) to @done(21:15), as the journal page provides the date.

***

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Task%20management/MarkDoneTime.applescript)
 
- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Task%20management/MarkDoneTime.scpt?raw=true)