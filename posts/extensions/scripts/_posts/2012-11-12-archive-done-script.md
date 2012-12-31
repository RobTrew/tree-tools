---
layout: default
title: Archive Done Script
description: Use this script to move completed todo items to the _# Archive_ heading in your document.
---

{{page.description}}

This script is useful if you are using FoldingText to track todos and you need a record of what you've done. It's also intended to be used together with FoldingText's todo mode. You can see how it works in this example document:

    # My.todo
    
    - item 1
    - item 3

Paste that text into a new FoldingText document and each unordered list item will get a checkbox because of .todo mode. Click the checkbox to mark an item as done.

When you are ready to archive a `@done` item place your text cursor on the items line and then run the "Arhchive Done" script. The item will be moved to the `# Archive` heading in your document, the script will create that heading if needed.

You can archive multiple items by selecting them all before running the script.

- [**View Script**](https://gist.github.com/4061766/)
- [**Download Script**](https://gist.github.com/4061766/download)
