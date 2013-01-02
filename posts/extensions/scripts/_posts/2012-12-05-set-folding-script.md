---
layout: default
title: Set Folding Level Script
description: Use this script to set the level of folding in the open FoldingText document.
---

{{page.description}}

This script expands the top N levels of the FoldingText outline, and leaves the lower levels concealed by folding.

![User dialog](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/Expand%20collapse/Expand-to-level-N.png)

A dialog tells the user how many levels there are in the current outline, and invite the user to enter a number.

1. Entering 1 (or less) will completely collapse the outline, folding all the Level 1 lines, leaving the rest concealed.
1. Entering a large number (the maximum number of levels, or more) will completely expand the outline, leaving no lines folded.
1. Entering a number between 1 and the maximum depth will leave the outline consistently folded at a particular level
1. Entering a number with a sign (e.g. +1 -1) will increase or decrease the current degree of folding.



- [**View Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Expand%20collapse/ExpandFT-ToLevelN-008.applescript)
- [**Download Script**](https://github.com/RobTrew/tree-tools/blob/master/FoldingText%20scripts/Expand%20collapse/ExpandFT-ToLevelN-008.scpt?raw=true)