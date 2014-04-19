---
layout: default
title: Informal dates and date-change plugin
description: Use this plugin to enter or adjust dates using informal relative phrases
---

{{page.description}}

This plugin presents a small popup in which you can type or edit informal relative dates and date adjustments like `today +7d`, `jul 14`, `tomorrow 2pm`, or `next month`.

- Default keyboard assignment `⌘⌥ '`

You can enter date/times anywhere in your text.
If your cursor is in or next to a tag (with or without a value), 
![cursor in or next to tag](./A%20PlaceCursorInOrNextToTag.png)
this plugin (keyboard shortcut defaults to `⌘⌥ '`) will automatically select any existing tag value, and create value brackets if none exist. As you type an informal phrase into the popup below your cursor, the phrased is translated as you type into an absolute date (and optionally time) in the default yyyy-mm-dd [HH:MM] format
![B InformalPhraseTranslatedLive.png](./B%20InformalPhraseTranslatedLive.png)
When you finish date entry, the selection moves to the right of the translated date.
![C AfterEntry.png](./C%20AfterEntry.png)
If you later return your cursor to the tag (or immediately to the side of it), and use the plugin again, it will automatically select the date/time, 
![D AutoSelectDateTime.png](./D%20AutoSelectDateTime.png)
and you can enter an adjustment like -2d to bring the date ahead a couple of days, or 2w to push it back for two weeks. Again the translations and adjustments take place live, as you type,
![E Adjust.png](./E%20Adjust.png)
and the cursor moves to right of the date when you finish editing with return or ESC.
![F AfterAdjust.png](./F%20AfterAdjust.png)

<table>
<colgroup>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
</colgroup>

<thead>
<tr>
	<th style="text-align:left;">Symbol</th>
	<th style="text-align:left;">Description</th>
	<th style="text-align:left;">Examples</th>
</tr>
</thead>

<tbody>
<tr>
	<td style="text-align:left;"><code>now</code></td>
	<td style="text-align:left;">Current system time</td>
	<td style="text-align:left;"><code>now +8h</code> <em>(8 hours from now)</em></td>
</tr>
<tr>
	<td style="text-align:left;"><code>today</code></td>
	<td style="text-align:left;">Time set to 00:00</td>
	<td style="text-align:left;"><code>today +2w</code> <em>(in two weeks)</em></td>
</tr>
<tr>
	<td style="text-align:left;"><code>yesterday</code></td>
	<td style="text-align:left;">Defaults to midnight of yesterday</td>
	<td style="text-align:left;"><code>yesterday, yesterday 3pm</code> </td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
</colgroup>

<thead>
<tr>
	<th style="text-align:left;">Symbol</th>
	<th style="text-align:left;">Format</th>
	<th style="text-align:left;">Examples</th>
</tr>
</thead>

<tbody>
<tr>
	<td style="text-align:left;"><em>dayname</em></td>
	<td style="text-align:left;"><code>sun, mon, tue, wed, thu, fri, sat</code> [or full forms]</td>
	<td style="text-align:left;"><code>thu 2pm, next sat,  next saturday</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>current time</em></td>
	<td style="text-align:left;"><code>now</code></td>
	<td style="text-align:left;"><code>now +2h</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>months</em></td>
	<td style="text-align:left;"><code>jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec</code> [or full forms]</td>
	<td style="text-align:left;"><code>jul 14</code>, <code>1 may</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>relative</em></td>
	<td style="text-align:left;">next, last, <code>+[number][unit]</code>, <code>-[number][unit]</code></td>
	<td style="text-align:left;"><code>last month,  today +2w</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>intervals</em></td>
	<td style="text-align:left;"><code>m[in], h[our], d[ay], w[eek], [m]o[nth], y[ear]</code></td>
	<td style="text-align:left;"><code>today +1y,  july -1w</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>time settings</em></td>
	<td style="text-align:left;"><code>H, M, a(m), p(m)</code></td>
	<td style="text-align:left;"><code>2H 3pm 8am 8.30am 16:00</code> </td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
</colgroup>

<thead>
<tr>
	<th style="text-align:left;">Dates</th>
	<th style="text-align:left;">Description</th>
	<th style="text-align:left;">Examples</th>
</tr>
</thead>

<tbody>
<tr>
	<td style="text-align:left;"><em>ISO</em></td>
	<td style="text-align:left;">yyyy-mm-dd [HH:MM]</td>
	<td style="text-align:left;"><code>2014-07-14 +6w</code> <code>(six weeks after that day)</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>Informal months</em></td>
	<td style="text-align:left;">Defaults to midnight at the start of the first future month of this name</td>
	<td style="text-align:left;"><code>aug</code> <em>(the first future august – next year&#8217;s aug if we are already in this year&#8217;s)</em></td>
</tr>
<tr>
	<td style="text-align:left;"><em>Informal days</em></td>
	<td style="text-align:left;">Preceding or following the name of the month, and assumed to be in the future</td>
	<td style="text-align:left;"><code>feb 12, 12 feb</code> <em>(next year if the current date is after feb 12)</em></td>
</tr>
<tr>
	<td style="text-align:left;"><em>Informal years</em></td>
	<td style="text-align:left;">Before or after the month and day. Assumed to be the first future instance of the date) if omitted</td>
	<td style="text-align:left;"><code>12 June, 2015 june 12, june 12 2015</code></td>
</tr>
<tr>
	<td style="text-align:left;"><em>Last</em></td>
	<td style="text-align:left;">most recent past instance</td>
	<td style="text-align:left;"><code>last wednesday, last jan 12, last month</code> <em>(midnight at the start of the month before this)</em></td>
</tr>
<tr>
	<td style="text-align:left;"><em>Next</em></td>
	<td style="text-align:left;">soonest future instance after the current week</td>
	<td style="text-align:left;">next friday (not the friday at the end of this week, if one remains, but the following friday)</td>
</tr>
</tbody>
</table>




 

#### MMD table format


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
_relative_ | next, last, `+[number][unit]`,  `-[number][unit]` | `last month,  today +2w`
_intervals_ | `m[in], h[our], d[ay], w[eek], [m]o[nth], y[ear]` | `today +1y,  july -1w`
_time settings_ | `H, M, a(m), p(m)` | `2H 3pm 8am 8.30am 16:00` 

Dates | Description | Examples
------|-------------|---------
_ISO_	| yyyy-mm-dd [HH:MM] | `2014-07-14 +6w` `(six weeks after that day)`
_Informal months_ | Defaults to midnight at the start of the first future month of this name | `aug` _(the first future august – next year's aug if we are already in this year's)_
_Informal days_ | Preceding or following the name of the month, and assumed to be in the future | `feb 12, 12 feb  `  _(next year if the current date is after feb 12)_
_Informal years_ | Before or after the month and day. Assumed to be the first future instance of the date) if omitted |  `12 June, 2015 june 12, june 12 2015`
_Last_ | most recent past instance | `last wednesday, last jan 12, last month` _(midnight at the start of the month before this)_
_Next_ | soonest future instance after the current week | next friday (not the friday at the end of this week, if one remains, but the following friday)