---
layout: default
title: Informal dates and date-change plugin
description: Use this plugin to enter or adjust dates using informal relative phrases
---

{{page.description}}

This plugin presents a small popup in which you can type or edit informal relative dates and date adjustments like `today +7d`, `jul 14`, `tomorrow 2pm`, or `next month`.

- Default keyboard assignment `⌘⇧9` (⌘ + open bracket)
	- or `⌘⌥ '`

You can enter date/times anywhere in your text.
If your cursor is in or next to a tag (with or without a value), 

![cursor in or next to tag](./A%20PlaceCursorInOrNextToTag.png)

this plugin (keyboard shortcut defaults to `⌘⌥ '`) will automatically select any existing tag value, and create value brackets if none exist. As you type an informal phrase into the popup below your cursor, the phrased is translated into an absolute date (and optionally time) in the default yyyy-mm-dd [HH:MM] format

![B InformalPhraseTranslatedLive.png](./B%20InformalPhraseTranslatedLive.png)

When you finish date entry, the selection moves to the right of the translated date.

![C AfterEntry.png](./C%20AfterEntry.png)

If you later return your cursor to the tag (or immediately to the side of it), and use the plugin again, it will automatically select the date/time, 

![D AutoSelectDateTime.png](./D%20AutoSelectDateTime.png)

and you can enter an adjustment like -2d to bring the date ahead a couple of days, or 2w to push it back for two weeks. Again the translations and adjustments take place live, as you type,

![E Adjust.png](./E%20Adjust.png)

and the cursor moves to right of the date when you finish editing with return or ESC.

![F AfterAdjust.png](./F%20AfterAdjust.png)
 

#### Informal and relative date phrases

Symbol | Description | Examples
-------|-------------|---------
`now` | Current system time | `now +8h` _(8 hours from now)_
`today` | Time set to 00:00 | `today +2w` _(in two weeks)_
`yesterday` | Defaults to midnight of yesterday | `yesterday, yesterday 3pm`


Symbol | Format | Examples
-------|--------|---------
_dayname_ | `sun, mon, tue, wed, thu, fri, sat` [or full forms] | `thu 2pm, next sat,  next saturday`
_current time_ | `now` | `now +2h`
_months_ | `jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec` [or full forms] | `jul 14`, `1 may`
_relative_ | next, last, `+[number][unit]`,  `-[number][unit]` | `last month,  next wednesday`
_intervals_ | `m[in], h[our], d[ay], w[eek], [m]o[nth], y[ear]` | `today +1y,  july -1w`
_time settings_ | `H, M, a(m), p(m)` | `2H 3pm 8am 8.30am 16:00` 

Dates | Description | Examples
------|-------------|---------
_ISO_	| yyyy-mm-dd [HH:MM] | `2014-07-14 +6w` (six weeks after that day)
_Informal months_ | Defaults to midnight at the start of the first future month of this name | `aug` _(the first future august – next year's aug if we are already in this year's)_
_Informal days_ | Preceding or following the name of the month, and assumed to be in the future | `feb 12, 12 feb  `  _(next year if the current date is after feb 12)_
_Informal years_ | Before or after the month and day. Assumed to be the first future instance of the date) if omitted |  `12 June, 2015 june 12, june 12 2015`
_Last_ | most recent past instance | `last wednesday, last jan 12, last month` _(midnight at the start of the month before this)_
_Next_ | soonest future instance after the current week | `next friday` _(not the friday at the end of this week, if one remains, but the following friday)_
_Ago_ | Before the current moment (if the unit is hours), otherwise, before midnight last night | `two hours ago`, `3 weeks ago`

#### Installation in FoldingText Dev 2, or TaskPaper Dev 3
- From the application's main menu, choose `File > Open Application Folder`
- Copy the `.ftplugin` folder and its contents into the `Plug-Ins` sub-folder of the application folder
- Close and restart the application