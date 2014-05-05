property pTitle : "Toggle @done in selected FT lines, updating any linked Reminder"
property pVer : "0.4"
property pAuthor : "Rob Trew"

on run
	tell application "FoldingText"
		set lstDocs to documents
		if lstDocs ­ {} then
			tell item 1 of lstDocs
				set lstUpdates to (evaluate script "
					function (editor) {
						var tree = editor.tree(),
						range = editor.selectedRange(),
						rgxLink = /\\[[^\\]]*\\]\\((x-apple-reminder:\\/\\/[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\\)/,
						match = null, strUUID = '',
						lstNodes = range.nodesInRange(), lstResult=[];
	
						tree.beginUpdates();
						lstNodes.forEach(function (node) {
							match = rgxLink.exec(node.line());
							if (match !== null) {
								strUUID = match[1];
							} else {
								strUUID = '';
							};

							if (node.tag('done') == undefined) {
								node.addTag('done', new Date().format('isoDate'));
								lstResult.push([strUUID, true]);
							} else {
								node.removeTag('done');
								lstResult.push([strUUID, false]);
							}
						});
						tree.endUpdates();
						tree.ensureClassified(lstNodes[0], lstNodes[-1]);
						return lstResult;
					}
				")
			end tell
			
			if lstUpdates ­ {} then
				lstUpdates
				tell application "Reminders"
					repeat with oDelta in lstUpdates
						set {strUUID, blnDone} to oDelta
						if strUUID ­ "" then
							try
								set oRem to reminder id strUUID
								set completed of oRem to blnDone
							on error
								display dialog strUUID & linefeed & linefeed & Â
									"not found ..." buttons {"OK"} default button "OK" with title pTitle & "  ver. " & pVer
							end try
						end if
					end repeat
				end tell
			end if
		end if
	end tell
	
end run
