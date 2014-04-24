property pName : "shallower heading"
property pDescription : "remove a hash prefix"
property pVer : "0.1"
property pPluginLink : "https://github.com/RobTrew/tree-tools/tree/master/FoldingText%202%20plugins%20and%20scripts/add%20and%20subtract%20heading%20hashes.ftplugin"

tell application "FoldingText"
	set lstDocs to documents
	if lstDocs ­ {} then
		tell item 1 of lstDocs
			set varResult to (evaluate script "function(editor, options) {
				return editor.performCommand(options.command);
			}" with options {command:pName})
		end tell
		if varResult = false then
			set strBtnLink to "Go to Plugin page"
			tell (display dialog "Plugin not installed:" & linefeed & linefeed & pName & " Ð " & pDescription & linefeed & linefeed & pPluginLink buttons {strBtnLink, "OK"} default button "OK" with title pName & "  ver. " & pVer)
				if button returned = strBtnLink then Â
					tell me to do shell script "open " & quoted form of pPluginLink
			end tell
		end if
	end if
end tell