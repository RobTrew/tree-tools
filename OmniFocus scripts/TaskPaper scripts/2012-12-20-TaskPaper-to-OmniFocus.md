---
layout: default
title: TaskPaper to OmniFocus importer
description: A draft Applescript droplet for copying data from Taskpaper-formatted text files to OmniFocus.
---

{{page.description}}

##The code is intended to:

Place Taskpaper projects and their tasks in a date-stamped Omnifocus import folder.
Place any Taskpaper tasks which are not preceded by a project header into the Omnifocus inbox.
Also place tasks in any Taskpaper project named “Inbox:” into the Omnifocus inbox.

In addition to files created with Taskpaper, it should also work with any plain .txt file which conforms to the Taskpaper file format. Apart from context and @done tags, it is intended to correctly interpret tags of the following form:

- @start(yyyy-mm-dd) or @start(yyyy-mm-dd hh:mm) - Start date 
- @due(yyyy-mm-dd) or @due(yyyy-mm-dd hh:mm) - Due date
- @mins(nn) - Estimated minutes
- @flag - Flagged

Note that it runs fairly slowly - when it is finished it will display simple import statistics.

##USAGE:  
- Drag one or more .taskpaper or .txt files onto the droplet, 
- Or select and copy some text (or one or more text files in in the Finder) and then run the script.

(I find it works well in a Keyboard Maestro macro which precedes it with a Copy action, to pick up currently selected text or text files)


- [**View Script**](https://github.com/RobTrew/tree-tools/tree/master/OmniFocus%20scripts/TaskPaper%20scripts)
- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/TaskPaper%20scripts/TaskPaper2OmniFocus.app.zip?raw=true)


