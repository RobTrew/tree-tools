
## OmniFocus to Taskpaper exporters
### Two export scripts
- OmniFocus to .taskpaper file
- OmniFocus to Taskpaper-formatted email (Apple Mail)

## Usage

Select parent items in the right hand content panel of OmniFocus, and run either of the scripts.

The parent items will be exported, together with their whole subtree.

The following flag formats are used in the export of TaskPaper data. 
OmniFocus contexts become Taskpaper tags.

- @start(yyyy-mm-dd) or @start(yyyy-mm-dd hh:mm) - Start date 
- @due(yyyy-mm-dd) or @due(yyyy-mm-dd hh:mm) - Due date
- @mins(nn) - Estimated minutes
- @flag - Flagged


## Note
 
OmniFocus does have a Taskpaper export option, but it's output is non-standard. Top level project tasks, for example, lack a leading tab.

##  View Scripts
[OmniFocus to .taskpaper file](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/TaskPaper%20scripts/OF2TaskPaper-005.applescript)

[OmniFocus to Taskpaper email](https://github.com/RobTrew/tree-tools/blob/master/OmniFocus%20scripts/TaskPaper%20scripts/OF2TaskPaperMail-005.applescript)



