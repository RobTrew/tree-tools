property pTitle : "Create a new FoldingText document from the visible (unfolded and unfiltered) lines"property pVer : "0.1"property pAuthor : "Rob Trew"tell application "FoldingText"	set lstDocs to documents	if lstDocs ≠ {} then		set strVisibleLines to ""		tell item 1 of lstDocs			set strVisibleLines to (evaluate script "
			function(editor) {
				var node =	editor.tree().firstLineNode(), 
							lstVisible=[];
				while (node !== null) {
					if (!editor.nodeIsHiddenInFold(node)) {
						lstVisible.push(node.line());
					}
					node = node.nextLineNode();
				}
				return lstVisible.join('\\n');
			}")		end tell				if strVisibleLines ≠ "" then make new document with properties {text contents:strVisibleLines}	end ifend tell