property pTitle : "Batch delete tags from current document"property pVer : "0.2"property pAuthor : "RobTrew"property pDescription : "

	1. Shows a sorted menu of the different kinds of tags in the current document,
	2. allows choice of one or more tag-types (⌘-click to multi-select)
	3. deletes all tags of the chosen type(s).

	(In case of unintentional deletion, use ⌘Z undo)

"property pjsListTags : "

	function(editor) {
		return editor.tree().tags(true).sort();
	}

"property pjsStripTags : "

	function(editor, options) {
		var tree=editor.tree(), lstTags = options.strip;

		tree.nodes().forEach(function (oNode) {
			Object.keys(oNode.tags()).forEach(function(strTag) {
				if (lstTags.indexOf(strTag) !== -1) {
					oNode.removeTag(strTag);
				}
			});
		});
	}
"on run	tell application "TaskPaper"		set lstDocs to documents		if lstDocs ≠ {} then			tell item 1 of lstDocs				set lstTagsFound to (evaluate script pjsListTags)				if lstTagsFound ≠ {} then										-- CHOOSE WHICH TAG-TYPES TO DELETE					set varChoice to choose from list lstTagsFound with title pTitle & tab & pVer with prompt ¬						"Choose tag types to delete" default items {item 1 of lstTagsFound} ¬						OK button name "OK" cancel button name "Cancel" with empty selection allowed and multiple selections allowed					if varChoice = false then return missing value					set lstTagsChosen to varChoice										-- AND DELETE ALL INSTANCES OF THE CHOSEN TAG TYPES					set varResult to (evaluate script pjsStripTags with options {strip:lstTagsChosen})				end if			end tell		end if	end tellend run