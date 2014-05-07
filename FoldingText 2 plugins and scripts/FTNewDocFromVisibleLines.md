#### Creating a Table of Contents or shorter document with FoldingText filtering & folding

I often need a table of contents, or a shorter and less fully elaborated copy of a larger document.

With FoldingText nodePath filtering (and/or a bit of manual folding for fine-tuning), I can show only the level of detail that I want in FoldingText, and then make a shorter snapshot document (including only the visible lines) by running a [script](./FTNewDocFromVisibleLines.applescript) like the one below (from something like KeyBoard Maestro).

For example, if I use Jamie Kowalski's [Filter plugin](https://github.com/jamiekowalski/foldingtext-extra/tree/master/filter.ftplugin) to show only the top two heading levels in the FoldingText User's Guide, with a query like:

`/@type=heading union /*/@type=heading`

I can then create a new document containing only the following lines:
```
# Welcome to the User's Guide
# Part 1: FoldingText's Story
# Part 2: Markdown text editor
## Formatting Your Document
## Editing Your Document
## Folding Your Document to Hide Details
## Filtering Your Document to Find Things
## Using FoldingText's Command Mode
## Sharing Your Document
# Part 3: Plain Text Productivity
## Modes for Custom Behavior
## Tags and Properties for Metadata
## Node Paths for Filtering
# Part 4: Platform SDK
```

by running:

```
property pTitle : "Create a new FoldingText document from the visible (unfolded and unfiltered) lines"
property pVer : "0.1"
property pAuthor : "Rob Trew"

tell application "FoldingText"
	set lstDocs to documents
	if lstDocs ≠ {} then
		set strVisibleLines to ""
		tell item 1 of lstDocs
			set strVisibleLines to (evaluate script "
			function(editor) {
				var node =	editor.tree().firstLineNode(), 
							lstVisible=[];
				while (node !== null) {
					if (!editor.nodeIsHiddenInFold(node)) {
						lstVisible.push(node.line());
					}
					node = node.nextLineNode();
				}
				return lstVisible.join('\\n');
			}")
		end tell
		
		if strVisibleLines ≠ "" then make new document with properties {text contents:strVisibleLines}
	end if
end tell
```