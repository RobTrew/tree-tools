property pTitle : "Open FoldingText file in Marked"
property pVer : "0.03"
property pAuthor : "Robin Trew"

property pblnPositionWindows : true -- Set this to false to disable the window positioning at the end of the script

on run
	tell application "FoldingText"
		set lstDocs to documents
		if lstDocs = {} then return
		set {strName, oFile} to {name, file} of item 1 of lstDocs
		activate
		if oFile is missing value then
			display dialog "The document: " & return & return & strName & Â
				return & return & "needs to be saved before Marked can preview it." buttons {"OK"} Â
				default button "OK" with title pTitle & "  ver. " & pVer
			return
		end if
	end tell
	
	---- Marked
	tell application "Marked"
		activate
		open oFile
	end tell
	
	-- Try to position windows left and right (to disable this, if it doesn't suit your workflow or your screen setup,
	-- set pblnPositionWindows at the top of the script to false )
	if pblnPositionWindows then
		set lngWidth to word 3 of (do shell script "defaults read /Library/Preferences/com.apple.windowserver | grep -w Width")
		set lngHeight to word 3 of (do shell script "defaults read /Library/Preferences/com.apple.windowserver | grep -w Height")
		set lngHalf to lngWidth / 2
		set lngHeight to lngHeight - 22
		
		tell application "System Events"
			tell process "FoldingText" to tell window 1 to set {position, size} to {{lngHalf, 22}, {lngHalf, lngHeight}}
			tell process "Marked" to tell window 1 to set {position, size} to {{0, 22}, {lngHalf, lngHeight}}
		end tell
	end if
end run
