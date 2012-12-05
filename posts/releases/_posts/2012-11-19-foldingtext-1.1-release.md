---
layout: default
title: FoldingText 1.1 Release
published: false
description: Highlights include improved AppleScript support and lots of bug fixes.
---

- Welcome text is only shown on the first launch.
- Markdown escape sequences are now highlighted.
- Repeat tags or tags that use reserved words are not highlighted.
- New window location is set from last positioned window.
- Menu item choice changes are used as defaults for new documents.
- Collapsing a childless node will collapse it's parent instead.
- Fixed Items > Change Type > Codeblock now works.
- Fixed Copy as RTF to work correctly with characters such as Æ Ø Å.
- Fixed File path links for absolute and relative paths now work.
- Fixed No longer show spelling errors in smart links.
- Fixed Inline link highlighting that included title attributes.
- Fixed Console.app warnings displayed on FoldingText launch.
- Fixed Finding text in last section works even if it's collapsed.
- Fixed Finding text works correctly when the view is focused in.
- Fixed Bold highlighting now works in tab-indented block-quotes.
- Fixed Internal crashes caused by invalid AppleScript parameters.
- Fixed Cases where link URLs could inadvertently be deleted.

This release also makes lots of changes to expand the AppleScript support. It adds support for more precise selection control, read/write access to the view node path, and the ability to expand and collapse nodes. It also adds an HTTP style interface that's easy to use from other languages and might make more sense to web programmers. See User's Guide > AppleScript Support for more information.

- [**Download FoldingText 1.1**]()