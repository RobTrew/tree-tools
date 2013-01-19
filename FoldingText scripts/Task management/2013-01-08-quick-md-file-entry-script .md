---

layout: default

title: Quick MD/FT Task/Note Entry Script

description: Uses LaunchBar/Alfred to tasks or notes under specific headings in FoldingText or MarkDown text files 

---

{{page.description}}

### DESCRIPTION

A script which takes a line from LaunchBar / Alfred (text parameters or 'Instant Send' selections), and adds the line (optionally time-stamped in a FoldingText notation like `@added(yyyy-mm-dd HH:MM)`:

1.  To a default (or specified) text file,

2.  under a default or specified (existing or new) Markdown header in that file,

3.  optionally normalising informal date/time tags like @due(tomorrow at 2pm) to @due(2013-01-19 14:00).

![](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/Task%20management/QuickMDEntry_LaunchBar.png)


![](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/Task%20management/QuickMDEntry_Alfred.png)

### USE

- Invoke the script with **Launchbar**, and tap the space-bar to open a text field (or in **Alfre**, type a space after the shortcut, and continue typing),

- enter a string using `>` to separate the text and tags from any header string,

- optionally adding a further `>` to precede any filename string.

***Note:*** header and file name strings are interpreted as case-insensitive substrings or grep patterns, and menus will offer choices if multiple matches are found)

### SYNTAX

 	line of text [@tag ...] [ > header_sub_string ] [ > file_sub_string ]

 	line of text [@tag ...] >*		(choose from menu of headers in default file)
 	line of text [@tag ...] >		(abbreviation for above)

 	line of text [@tag ...] >*>*	(choose from menus of files and headers)
 	line of text [@tag ...] >>		(abbreviation for above)

 	line of text [@tag ...] >>*		(use default header, choose file from menu)
 	

### EXAMPLES

	Write report @tag1 @tag2 > part of heading text

*heading text pattern is case insensitive - menu pops up if not unique*

	Read New York Times @tag3 > pattern

*the pattern is appended to `grep -i '^#\\+ .*` (string in MarkDown header)*

	Buy oranges  >

*choose from menu of headings in the default file.*

	Discard "art of war" and run !!

*no* `>` *– simply append to default heading in default file.*

	Collect argument diagrams >tasks>graph

*send text to Tasks header in file Graphics.txt*

	Collect argument diagrams >>graph

*send text to default header title in file Graphics.txt*

	Collect argument diagrams >>*

*choose a target file from the text files in default folder, use standard header*

	Collect argument diagrams >>

*choose a target file, then choose a header from within it*

	Collect argument diagrams >

*choose a target header from the default file*

	Collect argument diagrams

*send text to default file under default collection header*

### INSTALLATION

- Edit the value of `pDefaultTaskFile` near top of script to specify a full Posix path to an existing FoldingText/Markdown file

	(Use `$HOME` rather than `~` to specify the home folder)

	***Note:*** You may want to specify a file in your NVAlt text files folder, as in *NVAlt > Preference > Notes > Store and Read notes on disk as: > Plain Text Files*

	This will mean that using the  `[ > file_sub_string ]` syntax can find your other NVAlt text files

- Edit the value of `pBackupFolder` to allow for backups when `sed` inserts lines into text files. 

	
- Edit the value of `pDefaultHeader` to the name of a header in the FoldingText/Markdown file.

	This allows for quick entry of tasks without specifying a header

- Edit the value of `pblnFixCR_Delimited_Files` according to your preference.

	(OS X text files should be LF delimited. If this is set to false, the script will warn and exit when it encounters CR-delimited files)

- Optionally install the *parsedatetime* Python module:

	**Either:**

	edit the value of `pblnFixDates` to `false`

	**Or:**

	Install `https://github.com/bear/parsedatetime`



	1. Download and expand `https://github.com/bear/parsedatetime/archive/master.zip`

	2. In Terminal.app cd to the unzipped folder (e.g. type cd + space and drag/drop the folder to the Terminal.app command line, then tap return)

	3. Enter the following command in Terminal.app: `sudo python setup.py install`

### Use with LaunchBar

Save as a .scpt on a path indexed by LaunchBar, and reindex that path.

- Invoke the script and tap spacebar to open a text field.

- Or use the *Instant Send* key trigger to apply to selected text.

### Use with Alfred

- Paste into an Alfred Applescript extension dialog 

- Uncheck `Background`

- Fill other fields and exit dialog

- Follow the action shortcut with a space, and continue typing.


***

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Task%20management/QuickMDEntry.applescript)


- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Task%20management/QuickMDEntry.scpt?raw=true)