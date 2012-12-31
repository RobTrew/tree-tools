---
layout: default
title: Autofocus System Script
description: Use this script to implement a version of [Mark Forster's](http://markforster.squarespace.com/autofocus-system/) Autofocus time management system.
---

{{page.description}}

The autofocus system is paper based, but it can be implemented on the computer by using a new heading for each _page_, as shown in this FoldingText document.

    # Autofocus.todo
    
    - item 1
    - item 3

    # Autofocus.todo
    
    - item 2

In this implementation an `Autofocus.todo` heading is created for each page. Use unorderd list syntax for items so that you can get a nice clickable checkbox to cross the items off the list. The process is the same as described on Mark's page, except:

1. Instead of using physical pages add your items to "Autofocus.todo" headings.

2. Instead of physically crossing items of your lists, click the checkbox that's added by .todo mode. That will add the `@done` tag to the item so that it gets visually crossed off.

3. Instead of manually re-entering items that you are not finished with, place your text cursor on the items line, and run the linked to "Re-Enter" script. That will move a copy of the item to the end of your list. And it will automatically create "Autofocus.todo" headings as needed.

- [**View Script**](https://gist.github.com/4075021/)
- [**Download Script**](https://gist.github.com/4075021/download)
