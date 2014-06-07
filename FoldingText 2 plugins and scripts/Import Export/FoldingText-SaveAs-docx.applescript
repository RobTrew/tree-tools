property pTitle : "FoldingText 2  Save As .docx"
property pVer : "0.05"

property pstrOutFormat : "docx"

property pstrDefaultFolder : (path to desktop) -- or (path to home folder) (path to documents folder)

property pstrAttribution : "
This script is an Applescript wrapper which calls:
1. Fletcher Penney's MultiMarkdown 

http://fletcherpenney.net/multimarkdown

2.	John MacFarlane's Pandoc

http://johnmacfarlane.net/pandoc
"

property pblnNotify : false -- Use Growl or Applescript dialog to confirm save

-- 1. Install Pandoc from http://johnmacfarlane.net/pandoc/installing.html
-- 2. In Terminal.app, check the path of the pandoc command by entering the command:
--			type -a pandoc
-- 3. Assign the correct path to the property pstrPandoc below:

property pstrPandoc : "/usr/local/bin/pandoc"

-- 4. Install MultiMarkdown from http://fletcherpenney.net/multimarkdown/install/#macosx
-- 5. In Terminal.app, check the path of the pandoc command by entering the command:
--			type -a multimarkdown
-- 6. Assign the correct path to the property pstrMMD below: 

property pstrMMD : "/usr/local/bin/multimarkdown"


-- SAVES FROM FOLDINGTEXT  to .DOCX
-- (or from any text in the Clipboard, if there is nothing open in FoldingText)
on run
	-- GET THE TEXT OF THE FRONT FOLDINGTEXT DOC
	set strMMD to ""
	tell application id "sevs" to set blnRunning to (count of (processes where its name = "FoldingText")) > 0
	if blnRunning then
		tell application "FoldingText"
			set lstDocs to documents
			if (length of lstDocs) > 0 then
				tell item 1 of lstDocs
					set strMMD to text contents
					set {strSourceType, strSourceName} to {"FoldingText", its name}
				end tell
			end if
		end tell
	end if
	
	-- (OR IF NOTHING IS OPEN IN FOLDINGTEXT, GET ANY TEXT IN THE CLIPBOARD É )
	if strMMD = "" then
		set strMMD to do shell script "pbPaste -Prefer txt"
		if strMMD ­ "" then
			set strSourceType to "Clipboard"
			set strLine to trim(first paragraph of strMMD)
			if strLine ­ "" then
				set strSourceName to strLine & ".txt"
			else
				set strSourceName to "Clipboard.txt"
			end if
		end if
	end if
	if strMMD ­ "" then
		
		-- CHOOSE AN OUTPUT FOLDER AND FILE NAME
		set strOutFile to ChooseFilePathAndSave(strSourceType, pstrDefaultFolder, strSourceName)
		
		-- CHECK THAT IT ENDS WITH THE RIGHT SUFFIX
		set strSuffix to "." & pstrOutFormat
		if not (strOutFile ends with strSuffix) then set strOutFile to strOutFile & strSuffix
		
		set strCmd to "echo " & quoted form of strMMD & " | " & pstrMMD & " | " & pstrPandoc & " -f html -t " & Â
			pstrOutFormat & " -o " & quoted form of strOutFile
		try
			set strResult to do shell script strCmd
		on error errMsg
			set strResult to errMsg
		end try
		if strResult ­ "" then
			tell application id "MACS"
				activate
				display dialog "MM2DOCX error: " & strResult buttons {"OK"} default button "OK" with title pTitle & "  ver. " & pVer
			end tell
			exit repeat
		else
			if pblnNotify then Notify("Markdown to .docx", "", "Saved", strOutFile & linefeed & linefeed & pstrAttribution)
		end if
	else
		if pblnNotify then Notify("Markdown to .docx", "", "No text to save as .docx", "No FoldingText document open," & Â
			linefeed & linefeed & "and no text in clipboard ...")
	end if
end run

-- PUT UP A 'SAVE AS' DIALOG OFFERING A .DOCX VERSION OF THE CURRENT FOLDINGTEXT FILE NAME
-- OR ( CLIPBOARD.DOCX ) IF THERE IS NO TEXT IN AN OPEN FOLDINGTEXT DOCUMENT
on ChooseFilePathAndSave(strSource, strPath, strName)
	tell application "Finder"
		-- OFFER A DEFAULT FOLDER (if a valid one is specified)
		if exists strPath then
			set strOutFolder to strPath
		else
			set strOutFolder to POSIX path of (path to desktop)
		end if
	end tell
	set {dlm, my text item delimiters} to {my text item delimiters, "."}
	set lstParts to text items of strName
	set item -1 of lstParts to pstrOutFormat
	set strOutName to lstParts as string
	set my text item delimiters to dlm
	tell application id "sevs"
		activate
		set oFile to Â
			(choose file name with prompt strSource & ": Save As .docx" default name strOutName default location strOutFolder)
	end tell
	return POSIX path of oFile
end ChooseFilePathAndSave

-- REPORT THROUGH GROWL OR AN APPLESCRIPT DIALOG
on Notify(strAppName, strProcess, strTitle, strMsg)
	tell application "System Events"
		set strGrowlApp to ""
		repeat with oGrowlApp in {"Growl", "GrowlHelperApp"}
			if (count of (every process whose name = oGrowlApp)) > 0 then
				set strGrowlApp to oGrowlApp
				exit repeat
			end if
		end repeat
		if strGrowlApp ­ "" then
			set strScript to "
			tell application \"" & strGrowlApp & "\"
				register as application \"Houthakker scripts\" all notifications {\"" & strProcess & "\"} default notifications {\"" & strProcess & "\"} icon of application \"" & strAppName & "\"
				notify with name \"" & strProcess & "\" title \"" & strTitle & "\" application name \"Houthakker scripts\" description \"" & strMsg & "\"
			end tell"
			strScript
			run script strScript
		else
			activate
			display dialog strMsg buttons {"OK"} default button "OK" with title pTitle & tab & pVer
		end if
	end tell
end Notify

on trim(strText)
	do shell script "echo " & quoted form of strText & " | perl -pi -e 's/^\\s+//; s/\\s+$//'"
end trim


