property pTitle : "FoldingText Report - Group lines by Tags"property pVer : "0.1"property pAuthor : "Rob Trew"property pblnDebug : falseproperty pDescription : "

Creates a new report, based on the active FoldingText document.
The new document contains only tagged lines,
and these are grouped under (sorted) tag headings.
"property pGroupPrefix : "##"property pstrJS : "

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
		lstReport.push('\\n');
	});

		return lstReport.join('\\n');
}
"tell application "FoldingText"	if not pblnDebug then		set lstDocs to documents		if lstDocs ≠ {} then			set strGroupedByTag to ""			tell item 1 of lstDocs				set strGroupedByTag to (evaluate script pstrJS with options {grouplevel:pGroupPrefix})			end tell						if strGroupedByTag ≠ "" then				make new document with properties {text contents:strGroupedByTag}			end if		end if			else -- (interactive debugging in the SDK)		-- The document will be the SDK Debugging Editor default doc		-- (make sure that FoldingText > Help > Software Development Kit > editor is running		-- and that there is at least one 'debugger;' breakpoint line somewhere in the Javascript )		debug script pstrJS with options {grouplevel:pGroupPrefix}	end ifend tellstrGroupedByTag