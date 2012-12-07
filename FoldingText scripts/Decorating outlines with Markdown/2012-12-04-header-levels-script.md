---
layout: default
title: Header Levels Script
description: Use this script to change your outline between list items and heading items.
---

{{page.description}}

This script presents a popup choice of outline levels. You choose the level to which you want to use header items, and the rest of the structure will be formatted as list items.

This script works best when you are only working with list and heading items. Other item types (like example normal paragraphs) are ignored.

Lets see how this script works. Here we start with a simple outline of list items with three levels:

    - one
    	- Two
    		- Three

Choose "Level 1" and your outline will be transformed to:

    # one
    - Two
    	- Three

Choose "Level 2" and your outline will be transformed to:

    # one
    ## Two
    - Three

Choose "No Headers" and your outline will be transformed back to:

    - one
    	- Two
    		- Three

- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Decorating%20outlines%20with%20Markdown/FTHeaderLevels.applescript) 
- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Decorating%20outlines%20with%20Markdown/MakeOrDeepenHeading.scpt?raw=true)