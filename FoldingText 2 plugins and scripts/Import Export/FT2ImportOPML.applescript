-- Copyright (C) 2014 Robin Trew
--
-- Permission is hereby granted, free of charge, 
-- to any person obtaining a copy of this software 
-- and associated documentation files (the "Software"), 
-- to deal in the Software without restriction, 
-- including without limitation the rights to use, copy, 
-- modify, merge, publish, distribute, sublicense, 
-- and/or sell copies of the Software, and to permit persons 
-- to whom the Software is furnished to do so, 
-- subject to the following conditions:

-- *******
-- The above copyright notice and this permission notice 
-- shall be included in ALL copies 
-- or substantial portions of the Software.
-- *******

-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
-- EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
-- OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
-- IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
-- DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
-- TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
-- OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

property pTitle : "Import OPML file to FoldingText"
property pVer : "0.1"
property pAuthor : "Robin Trew"

property plngHeaderLevels : 2 -- Make the top N (N ³ 0) levels of the OPML outline into Markdown hash headers 

property pSrcFolder : (path to desktop)

-- NOTE THAT THIS IS A .SCPTD FILE CONTAINING A PYTHON SCRIPT IN THE /CONTENTS/RESOURCES FOLDER 
-- FT2ImportOPML.scptd/Contents/Resources/OPML2FT.py
property pPythonScript : "OPML2FT.py"

on run
	-- CHOOSE AN OPML FILE
	tell application "Finder"
		pSrcFolder
		if exists pSrcFolder then
			set strSrcFolder to POSIX path of pSrcFolder
		else
			set strSrcFolder to POSIX path of (path to home folder)
		end if
	end tell
	
	tell application "FoldingText"
		activate
		set strOPMLFile to (POSIX path of Â
			(choose file with prompt pTitle default location strSrcFolder))
		
		-- REMEMBER THIS FOLDER FOR THE NEXT RUN - VALUES OF APPLESCRIPT PROPERTIES PERSIST BETWEEN RUNS
		set {dlm, my text item delimiters} to {my text item delimiters, "/"}
		set pSrcFolder to POSIX file ((items 1 thru -2 of (text items of strOPMLFile)) as string) as alias
		set my text item delimiters to dlm
		
		if strOPMLFile does not end with ".opml" then
			activate
			display dialog strOPMLFile & return & return & Â
				"File must have .opml extension" buttons {"OK"} default button "OK" with title pTitle & "  ver. " & pVer
			return
		end if
		
		-- GET THE PATH OF THE PYTHON SCRIPT
		set strScript to my GetScript(pPythonScript)
		
		-- GET AN FT TEXT VERSION
		set strTmpPath to POSIX path of (path to temporary items) & "tmp.ft"
		set strCMD to "python " & strScript & " --infile=" & quoted form of strOPMLFile & " --outfile=" & quoted form of strTmpPath
		if plngHeaderLevels > 0 then set strCMD to strCMD & space & "--headlevels=" & (plngHeaderLevels as string)
		try
			do shell script strCMD
		on error
			activate
			display dialog strOPMLFile & return & return & "could not be read as an OPML file" buttons {"OK"} default button "OK" with title pTitle & "  ver. " & pVer
			return
		end try
		set strFT to my readFile(strTmpPath)
		
		-- CREATE A NEW FT DOC CONTAINING THE IMPORTED TEXT
		set oDoc to make new document with properties {text contents:strFT}
		
		activate
	end tell
end run

on GetScript(strFileName)
	return quoted form of (POSIX path of (path to resource strFileName))
end GetScript

on readFile(strPath)
	set oFile to (open for access (POSIX file strPath))
	set strText to (read oFile for (get eof oFile) as Çclass utf8È)
	close access oFile
	return strText
end readFile
