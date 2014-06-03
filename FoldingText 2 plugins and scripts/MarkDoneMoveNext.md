### Move the @next tag on, marking the current line as @done(yyyy-mm-dd hh:mm)

#### Automating @done and @next


When I am working through the finer detail of a project I like to use a @next tag to mark which item I’m on.

I assign a keystroke to:
- Marking the current line as `@done(yyy-mm-dd hh:mm)`,
- and moving the `@next` tag on (to the next item in the current project which is not tagged `@done`).

If we are on the last line of a project:
- The project/heading section itself is flagged as  `@done(yyy-mm-dd hh:mm)` if no uncompleted items remain.
- If any earlier lines remain uncompleted, then the `@next` tag jumps to the first of them.

#### FoldingText 2 and TaskPaper 3 scripts

[FoldingText 2](http://www.foldingtext.com) and [TaskPaper 3](http://oldsupport.foldingtext.com/discussions/development-versions/210-taskpaper-3-dev-build-126) now allow us to do these things in Javascript, which is becoming [Apple’s general direction](https://developer.apple.com/library/prerelease/mac/releasenotes/InterapplicationCommunication/RN-JavaScriptForAutomation/index.html#//apple_ref/doc/uid/TP40014508) in OS X Yosemite too.

We can call the Javascript from an Applescript, and perhaps use that from something like Keyboard Maestro, or we can put it in a pure javascript plugin for FoldingText itself.

Here are two sample scripts, one for [FoldingText 2](http://www.foldingtext.com), and one for [TaskPaper 3](http://oldsupport.foldingtext.com/discussions/development-versions/210-taskpaper-3-dev-build-126) which automate the business of marking a line as `@done(yyy-mm-dd hh:mm)` and moving the `@next` tag to the next line in the project which isn’t completed, and which doesn’t have any other disqualifying tags.

[FTMoveNext.applescript](./FTMoveNext.applescript)
[TPMoveNext.applescript](./TPMoveNext.applescript)

#### Customising the scripts

1. **@next** versus **@now** etc:
	To specify an alternative ‘bookmarking’ tag to `@next`, edit the value of `pstrTag` at the top of the text
2. Other disqualifying tags:
	By default, the script assumes that lines marked `@done` should be skipped by the bookmarking tag (`@next`, `@now` or whatever you have chosen). If you want to specify any other disqualifying tags which should be skipped, like `@wait`, `@tomorrow`, `@snooze` etc, add quoted tag names to the comma-delimited  `plstExcept` list at the top of the script.

#### Experimenting with the new FoldingText debugger

Not that you can run these scripts in a debug mode and trace their execution if you want. To do that:

1. Edit `pblnDebug` at the start of the script to `true`
2. insert the line `debugger;` wherever you want a break-point,
3. and open the SDK version of the editor through _FoldingText > Help > Software Development Kit > Run Editor > Inspector_
4. Paste a bit of text into the SDK editor, and
5. run the script.


You can then:

- Step through the code line by line with F7 or ⌘;
	- (other debugging icons to the left)
	- and watch variables changing their values in the Scope Chain panel to the right.