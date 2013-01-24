---
layout: default
title: Copy Outline as Nested MMD Table Script
description: Copies the selected outlines as a nested MMD table which you can paste elsewhere.
---

{{page.description}}

Select the top level node(s) of one or more FoldingText outlines and run this script. 

The script will create a nested MultiMarkdown table with the same structure as the outline(s), placing the lines of MMD text in the clipboard, so that you can paste it elsewhere.

This version excludes any subtrees hidden by folding. To make a copy which always includes the full subtree, edit a property at the top of the script:

`property pblnSkipHidden : false`

*Example of a source outline and the table generated from that outline by this script (previewed in Marked):*

![HTML table from outline](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/MMD%20Tables/NestedTablePreview.png)


*The outline and the MMD table text version in FoldingText:*

![MMD table from outline](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/MMD%20Tables/OutlineAndMMDTable.png)


***

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/MMD%20Tables/Tree2MMDTable.applescript)
 
- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/MMD%20Tables/Tree2MMDTable.scpt?raw=true)