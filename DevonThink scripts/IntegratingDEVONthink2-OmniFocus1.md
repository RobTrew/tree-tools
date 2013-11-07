## Integrating OmniFocus with DEVONthink 

### OF-DT Integration - Version 2  

Contains complete rewrites of:  

1. OpenProjFolderInDevon, and  

2. OpenProjNotesInDevon  

(Removing dependence on parallel folder structures - links between OF projects and documents in DT will be preserved even if the folder nesting is changed in OF and/or DT).   

Version 214 of the Project notes scripts can be used with FoldingText notes (plain text outlines, and MarkDown conventions) as an alternative to OO3 notes.  


[To DEVON INBOX as oo3.zip](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/To%20DEVON%20INBOX%20as%20oo3.zip) 

A droplet to which a set of TXT, RTF or OPML files can be dragged.  

Each file will be converted to OmniOutliner 3 format, and placed in the global DEVONthink 2 Inbox.  

Assumes both DT2 and OO3 are installed on the system.  

Any other files or folders will be passed unmodified to the DEVONthink global Inbox.

#### DEVONthink - OF integration: 4 scripts

Four draft scripts illustrating the integration of OmniFocus (and OmniOutliner Pro) with DEVONthink 2  

[Save2DevonAsTXT](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/Save2DevonAsTXT.scpt.zip) exports whatever is currently selected in OmniFocus (task, project, folder), as a text file, to a corresponding DEVONthink 2 project folder.   

The text file is in TaskPaper format. The DT2 folder has the same path and name as the selected Omnifocus project or folder. This DT2 folder is automatically created, if it does not already exist.  

[Save2DevonAsOO3](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/Save2DevonAs003.scpt.zip) exports whatever is currently selected in OmniFocus (task, project, folder), as an OmniOutliner 3 file, to a corresponding DEVONthink 2 project folder.   

The .oo3 file contains columns for task properties such as Context, Start, Due, Completed, Duration, Flagged. The OmniOutliner checkbox is set according to the OF task Done property. The DT2 folder has the same path and name as the selected Omnifocus project or folder. This DT2 folder is automatically created, if it does not already exist.   

[OpenProjFolderinDevon](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/OpenProjFolderInDevn.scptd.zip) opens a folder, in DEVONthink 2, with a path and name matching that of the currently selected OmniFocus project. (The DT2 folder is automatically created, if it does not already exist).  

[OpenProjNotesinDevon](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/OpenProjNOTESInDevn214.scptd.zip) opens a project notes file (stored in  the matching DEVONthink 2 folder) for the selected OmniFocus project. The notes file is an Omnioutliner 3 document. (The DT2 folder and .oo3 file are automatically created, if they do not already exist)  

[SetDBforOmniFocusFolder](https://github.com/RobTrew/tree-tools/blob/master/DevonThink%20scripts/SetDBforOmniFocusFolder.scpt.zip) allows you to choose which DEVONthink database will be used for the selected OmniFocus folder. The default is “OmniFocus Notes”, but this script will offer you a list of the databases currently open in DT, and will store the path of the database you choose in the invisible note field of the selected OF Folder. The  OpenProjFolderinDevon and OpenProjNotesinDevon scripts will then use the specified database for all projects enclosed by that folder and its child folders. (Except where any of these have been given their own database assignment by this script).  

For a brief account of an approach to  work-flow, see:  

[DEVONthink forum: Applescripts to integrate DT2 with OmniFocus](http://www.devon-technologies.com/scripts/userforum/viewtopic.php?f=20&t=8447&p=39758#p39758)
