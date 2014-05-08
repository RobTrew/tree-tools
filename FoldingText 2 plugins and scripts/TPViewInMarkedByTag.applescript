property pTitle : "View TaskPaper Pespectives in Marked - Example: Actions grouped by Tags"property pVer : "0.1"property pAuthor : "Rob Trew"property pblnDebug : falseproperty pDescription : "

Creates a view, based on the active TaskPaper document,
and displays it in Marked2app.com

The view contains only tagged lines,
and these are grouped under (sorted) tag headings.
"property pGroupPrefix : "###"property pViewFolder : "ViewFolder" -- Name for Perspectives folder to be created in same folder as .TaskPaper docproperty pstrJS : "

function(editor, options) {
	//debugger;
	var	tree = editor.tree(),
		lstTags = tree.tags(true).sort(),
		strHeadPrefix = options.grouplevel,
		strListPrefix = '- ', lstTagged = [],
		lstReport = [], strTag;

	lstTags.forEach(function(strTag) {
		var strTitle = strTag[0].toUpperCase() + strTag.slice(1);
		lstReport.push([strHeadPrefix, strTitle].join(' '));
		lstTagged = tree.evaluateNodePath('//@' + strTag);
		lstTagged.forEach(function(oNode) {
			lstReport.push(strListPrefix + oNode.text());
		});
		lstReport.push(''); // gap before next heading
	});

	return lstReport.join('\\n');
}
"tell application "TaskPaper"	if not pblnDebug then		set lstDocs to documents		if lstDocs ≠ {} then			set strGroupedByTag to ""			tell item 1 of lstDocs				set strGroupedByTag to (evaluate script pstrJS with options {grouplevel:pGroupPrefix})																if strGroupedByTag ≠ "" then					-- make new document with properties {text contents:strGroupedByTag}					set {strName, oFile} to {name, file} of it					if oFile is missing value then						display dialog "The document: " & return & return & strName & ¬							return & return & "needs to be saved before Marked can display perspectives." buttons {"OK"} ¬							default button "OK" with title pTitle & "  ver. " & pVer						return					end if										-- Get a path to a perspectives folder in the same folder as the .TaskPaper document					set strPath to POSIX path of oFile					set {dlm, my text item delimiters} to {my text item delimiters, "/"}					set lstParts to text items of strPath					set item -1 of lstParts to pViewFolder					set strFolderPath to lstParts as string															if my GetFolder(strFolderPath) then						set strFullPath to (lstParts & "TagView.md") as string						set strCmd to "echo " & quoted form of strGroupedByTag & " > " & quoted form of strFullPath						do shell script strCmd						tell application "Marked"							activate							open (POSIX file strFolderPath as alias) -- get Marked to watch the perspectives folder						end tell					end if					set my text item delimiters to dlm				end if			end tell		end if			else -- (interactive debugging in the SDK)		-- The document will be the SDK Debugging Editor default doc		-- (make sure that FoldingText > Help > Software Development Kit > editor is running		-- and that there is at least one 'debugger;' breakpoint line somewhere in the Javascript )		debug script pstrJS with options {grouplevel:pGroupPrefix}	end ifend tellon GetFolder(strPath)	(do shell script ("mkdir -p " & quoted form of strPath & "; echo $?")) = "0"end GetFolder