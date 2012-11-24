property pTitle : "Test informal dates for FT"
property pVer : "0.03"

property pstrExample : "wednesday at 4pm"

property pOK : "OK"
property pCancel : "Cancel"


property pblnSeconds : false

-- To install Mike Taylor and Darshana Chhajed's Python parsedatetime module:
-- 	Visit https://github.com/bear/parsedatetime
--  		(Licence: https://github.com/bear/parsedatetime/blob/master/LICENSE.txt)
--	Download and expand https://github.com/bear/parsedatetime/archive/master.zip
--	in Terminal.app cd to the unzipped folder 
--	(e.g. type cd + space and drag/drop the folder to the Terminal.app command line, then tap return)
--	sudo python setup.py install

on run
	set {strPhrase, blnEsc} to {pstrExample, false}
	repeat until blnEsc
		set strDefault to TimeString(strPhrase)
		if pblnSeconds then
			set strSeconds to "Exclude seconds"
		else
			set strSeconds to "Include seconds"
		end if
		try
			tell (display dialog "Result:" & tab & strDefault default answer strPhrase buttons {pCancel, strSeconds, pOK} Â
				cancel button pCancel default button pOK with title pTitle & "  ver. " & pVer)
				set {strButton, strPhrase} to {button returned, text returned}
				if strButton ­ pOK then set pblnSeconds to not pblnSeconds
			end tell
		on error
			set blnEsc to true
		end try
	end repeat
end run

on TimeString(strPhrase)
	-- get a list of  Y,m,d,h,m,s integers from a Python parsedatetime natural language parse
	set lstDateTime to ParseTime(strPhrase, pblnSeconds)
	
	-- left pad any single digits with a zero
	repeat with i from 2 to length of lstDateTime
		set item i of lstDateTime to PadNum(item i of lstDateTime, 2)
	end repeat
	
	-- delimit YYYY-mm-dd with hyphens
	set {dlm, my text item delimiters} to {my text item delimiters, "-"}
	set strDate to (items 1 thru 3 of lstDateTime) as string
	
	-- delimit HH:MM:SS with colons
	set my text item delimiters to ":"
	set strDate to strDate & space & (items 4 thru -1 of lstDateTime) as string
	set my text item delimiters to dlm
	return strDate
end TimeString

-- Use Mike Taylor and Darshana Chhajed's Python parsedatetime module 
-- to get a parse of a natural language expression as a series of integers {year, month, day, hour, minute}
-- (defaults, if parse fails, to current time)
on ParseTime(strPhrase, blnSeconds)
	if blnSeconds then
		set strUpTo to 6
	else
		set strUpTo to 5
	end if
	set str to do shell script "python -c 'import sys, parsedatetime as pdt; print pdt.Calendar().parse(sys.argv[1])[0][0:" & strUpTo & "]' " & Â
		quoted form of strPhrase
	return run script "{" & (text 2 thru -2 of str) & "}"
end ParseTime

-- Left pad with zeroes to get a fixed digit length
on PadNum(lngNum, lngDigits)
	set strNum to lngNum as string
	set lngGap to (lngDigits - (length of strNum))
	repeat while lngGap > 0
		set strNum to "0" & strNum
		set lngGap to lngGap - 1
	end repeat
	return strNum
end PadNum
