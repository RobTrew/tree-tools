property pTitle : "Timed task from current FoldingText2 line"
property pVer : "0.1"
property pAuthor : "Rob Trew"

property plngMins : 55

property pstrPrefix : "due://x-callback-url/add?title="
property pstrSuffix : "&minslater="

on run
	set varLine to FTLineText()
	if varLine is not missing value then
		set strCmd to "open " & quoted form of (pstrPrefix & encoded(varLine) & pstrSuffix & (plngMins as string))
		do shell script strCmd
	end if
end run

on encoded(strPath)
	do shell script "python -c 'import sys, urllib as ul; print ul.quote(sys.argv[1])' " & Â
		quoted form of strPath
end encoded

on FTLineText()
	tell application "FoldingText"
		set lstDocs to documents
		if lstDocs ­ {} then
			tell item 1 of lstDocs
				set varLine to evaluate script "
					function(editor) {
						return editor.selectedRange().startNode.text();
					}"
			end tell
		else
			set varLine to missing value
		end if
	end tell
	return varLine
end FTLineText