-- Ver 0.5 Spaces in context names mapped to underscore
-- Ver 0.4 Adapts to the new requirement that all child bullets are preceded by space
-- Ver 0.3  2007 Dec 22
-- Now exports whatever is displayed and selected in right-hand content panel

property pblnToMail : true

on run
	tell application "OmniFocus"
		tell default document
			if number of document window is 0 then
				make new document window with properties {bounds:{0, 0, 1000, 500}}
			end if
		end tell
		
		tell document window 1 of front document
			set lstTrees to selected trees of content
			if (count of lstTrees) = 0 then
				try
					display dialog "Nothing selected in the right-hand panel." & return & return & "Select material to export, and try again." & return
				end try
			else
				-- Generate a TaskPaper string of the selected content
				set blnContext to (selected view mode identifier is not equal to "project")
				set lngIndent to 0
				set strTP to my ExportTrees(lstTrees, lngIndent, blnContext)
				
				if pblnToMail then
					-- Make Mail message
					try
						strTP
						tell application "Mail"
							set oMsg to make new outgoing message with properties {content:strTP & return & return}
							set visible of oMsg to true
							activate
						end tell
					on error
						display dialog "No tasks selected"
					end try
				else
					set oFile to choose file name "Export as:" default name ¬
						"OmniFocus.taskpaper" default location (path to desktop)
					set strFile to (POSIX path of oFile)
					do shell script "echo " & quoted form of strTP & " > " & strFile
				end if
			end if
		end tell
	end tell
end run

on ExportTrees(lstTrees, lngIndent, blnContextView)
	-- if the tree is a task give full detail
	-- else just name and any note
	set strTP to ""
	set strIndent to ""
	
	repeat lngIndent times
		set strIndent to strIndent & tab
	end repeat
	
	tell application "OmniFocus"
		repeat with oTree in lstTrees
			
			set oValue to value of oTree
			set clValue to class of oValue
			if clValue ≠ item then
				set strName to name of oValue
				if length of strName > 0 then set strName to my EscAmpersand(strName)
				
				set strNote to note of oValue
				if length of strNote > 0 then set strNote to my EscAmpersand(strNote)
			else
				set strName to ""
				set strNote to ""
			end if
			
			if (clValue is not equal to task) and (clValue is not equal to inbox task) then
				
				-- Project or Folder
				if clValue is not equal to folder then
					if clValue is not equal to project then
						--Inbox (No details)
						set oWin to first document window of front document
						set strName to name of first selected tree of (sidebar of oWin)
						if strName ≠ "Inbox" then set strName to ""
						set strTP to strTP & strName & ":" & return
					else
						-- Project (Name and possibly note)
						if length of strName > 0 then
							set strTP to strTP & strIndent & strName & ":" & return
							if length of strNote > 0 then ¬
								set strTP to strTP & strIndent & strNote & return
						end if
					end if
				else
					-- Folder (Just name - no note)
					set strTP to strTP & strIndent & strName & ":" & return
				end if
				
			else -- Task (with details from specified columns)
				
				
				-- set recFields to {fldName:name of oValue, fldNote:note of oValue, fldDone:completed of oValue, fldContext:strContext, fldStartDate:start date of oValue, flddueDate:due date of oValue, fldDoneDate:completion date of oValue, fldDuration:estimated minutes of oValue, fldFlagged:flagged of oValue}
				
				
				-- write first line of task, followed by tags
				set lstLines to paragraphs of strName
				
				set strTP to strTP & strIndent & "- " & item 1 of lstLines
				
				-- Add any tags
				set oContext to context of oValue
				if oContext is not equal to missing value then
					set strContext to name of oContext
					set {dlm, my text item delimiters} to {my text item delimiters, space}
					set lstContext to text items of strContext
					set my text item delimiters to "_"
					set strContext to lstContext as string
					set my text item delimiters to dlm
					
					set strTP to strTP & " @" & strContext
				end if
				
				set dteStart to start date of oValue
				if dteStart is not equal to missing value then ¬
					set strTP to strTP & " @start(" & my DateString(dteStart) & ")"
				
				set dteDue to due date of oValue
				if dteDue is not equal to missing value then ¬
					set strTP to strTP & " @due(" & my DateString(dteDue) & ")"
				
				
				set lngDurn to estimated minutes of oValue
				if lngDurn is not equal to missing value then ¬
					set strTP to strTP & " @mins(" & (lngDurn as string) & ")"
				
				
				if flagged of oValue then set strTP to strTP & " @flag"
				
				if completed of oValue then set strTP to strTP & " @done"
				set strTP to strTP & return
				
				-- write any remaining lines of task as note text
				if length of lstLines > 1 then
					repeat with strLine in rest of lstLines
						set strLine to my RTrim(strLine)
						if length of strLine > 0 then
							-- change any trailling : to :-, to avoid misinterpretation as a header
							if last character of strLine ≠ ":" then
								set strTP to strTP & strIndent & strLine & return
							else
								set strTP to strTP & strIndent & strLine & "-" & return
							end if
						end if
					end repeat
				end if
				
				-- append any attached note text
				set lstLines to paragraphs of strNote
				
				repeat with strLine in lstLines
					set strLine to my RTrim(strLine)
					if length of strLine > 0 then
						-- change any trailling : to :-
						if last character of strLine ≠ ":" then
							set strTP to strTP & strIndent & strLine & return
						else
							set strTP to strTP & strIndent & strLine & "-" & return
						end if
					end if
				end repeat
				
			end if
			
			-- if the current node has sub-trees then recurse
			set lstSubTrees to trees of oTree
			if (count of lstSubTrees) > 0 then
				set lngNewIndent to lngIndent + 1
				set strTP to strTP & my ExportTrees(lstSubTrees, lngNewIndent, blnContextView)
			end if
			
		end repeat
	end tell
	return strTP
end ExportTrees

on RTrim(someText)
	local someText
	
	repeat until someText does not end with return
		if length of someText > 1 then
			set someText to text 1 thru -2 of someText
		else
			set someText to ""
		end if
	end repeat
	
	return someText
end RTrim

on DateString(dte)
	-- yyyy-mm-dd hh:mm
	set strDate to ""
	if dte is not equal to missing value then
		set lngMonth to month of dte as integer
		set strMonth to lngMonth as string
		if lngMonth < 10 then set strMonth to "0" & strMonth
		
		set lngDay to day of dte as integer
		set strDay to lngDay as string
		if lngDay < 10 then set strDay to "0" & strDay
		
		set strDate to strDate & (year of dte) & "-" & strMonth & "-" & strDay
		
		set lngHrs to (hours of dte) as integer
		set lngmins to (minutes of dte) as integer
		
		if (lngHrs > 0) or (lngmins > 0) then
			set strHrs to lngHrs as string
			if lngHrs < 10 then set strHrs to "0" & strHrs
			
			set strMins to lngmins as string
			if lngmins < 10 then set strMins to "0" & strMins
			
			set strDate to strDate & " " & strHrs & ":" & strMins
		end if
	end if
	return strDate
end DateString

on EscAmpersand(str)
	set strOldDelim to text item delimiters
	
	set text item delimiters to " @"
	set lstParts to text items of str
	set lngParts to count of lstParts
	if lngParts > 1 then
		
		set strNew to item 1 of lstParts
		repeat with n from 2 to lngParts
			set strNew to strNew & "_@" & item n of lstParts
		end repeat
		set text item delimiters to strOldDelim
		return strNew
	else
		set text item delimiters to strOldDelim
		return str
	end if
end EscAmpersand



