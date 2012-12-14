---
layout: default
title: Log OmniFocus items done today to DayOne
description: Logs today's OmniFocus done items to DayOne (avoiding duplication)
---

{{page.description}}

Shell script which logs, to the [DayOne](http://dayoneapp.com) application, any OmniFocus tasks which :

1.	Are marked as completed since midnight last night, and
2.	have not yet been logged to DayOne.

- The script directly queries the OmniFocus Sqlite cache, and doesn't require OmniFocus to be running.
- It avoids duplication of items logged earlier, if the script is called several times in one day.
- It can be called automatically from Hazel, whenever a change in the OmniFocus cache is detected, if that suits your workflow.

##Usage:

This script requires installation of the Day One [command line interface](http://dayoneapp.com/tools/).

Hazel settings to monitor changes in the OmniFocus cache folder:
- *~/Library/Caches/com.omnigroup.OmniFocus*
- or *~/Library/Caches/com.omnigroup.OmniFocus.MacAppStore*

(Depending on which version of OmniFocus you are running)

![Hazel settings](https://raw.github.com/RobTrew/tree-tools/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/HazelSettings4DayOneLog.png)

Or, for sparser and more aggregated logging events, combine a delaying rule with one or more fixed time events:

![Two rules](https://raw.github.com/RobTrew/tree-tools/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/ComplementaryRules.png)

![Hazel gaps between logging events](https://raw.github.com/RobTrew/tree-tools/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/HazelLoggingIntervals.png)

![Timed rules to flush the logging buffer](https://raw.github.com/RobTrew/tree-tools/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/TimedRules.png)

- The default output format is broadly that of TaskPaper or FoldingText, but with times only. 
- Works best with Day One Preferences > Appearances:  **+ Markdown** **- Link Twitter @names**
- If you need *Link Twitter names* then it will probably make sense to edit the '@' characters out of the script

```
    Project A:
    - task1 @done(HH:MM)
    - task2 @done(HH:MM)
    - taskN @done(HH:MM)
    
    Project B:
    - taskX @done(HH:MM)
    - taskY @done(HH:MM)
    - taskZ @done(HH:MM)
```
Viewing the results in DayOne:
- When DayOne first opens it defaults to displaying a fresh editing session, and displays a **Done** button at upper right.
- To view the text created by automatic logging events, you will need to click the **Done** button, to exit the current editing session.
- Note that (Ver 3+ of this script) the final colon of the project line is a live link back to the project in OmniFocus.

Logging sound:
- By default the script makes a system 'pop' sound when the **done** log has taken place.
- To suppress this sound, comment out the relevant line near the end of the script (by preceding it with a hash character)
```
   afplay /System/Library/Sounds/Pop.aiff 
```

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/OmniFocusLogDone2DayOne.sh)
