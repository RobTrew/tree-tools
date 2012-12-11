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

Hazel settings:

![Hazel settings](https://raw.github.com/RobTrew/tree-tools/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/HazelSettings4DayOneLog.png)

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

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/Shell%20scripts%20for%20Geektool%20or%20logging/OmniFocusLogDone2DayOne.sh)
