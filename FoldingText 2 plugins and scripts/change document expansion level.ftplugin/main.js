define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions').Extensions;

	// deepest nesting level in this sub-tree ?
	function maxdepth(node) {
		var lngChiln = 0, lstChiln=[],
			lngMax = 0, lngDepth = 0, i = 0;

		if (node.hasChildren()) {
			lstChiln = node.children();
			lngChiln = lstChiln.length;
			for (i = 0; i < lngChiln; i++) {
				lngDepth = maxdepth(lstChiln[i]) + 1;
				if (lngDepth > lngMax) {
					lngMax = lngDepth;
				}
			}
		}
		return lngMax;
	}

	// shallowest fold in the editor's tree ?
	function getFoldLevel(editor) {
		function nestLevel(node) {
			var level = 0;
			while (node.parent) {
				level++;
				node = node.parent;
			}
			return level;
		}
		// what folds have we got ?
		var tree = editor.tree(), folds = editor.folds(),
			lstLevels = [], i=0, lngFolds = folds.length, lngLine;

		// and how deep is the shallowest fold ?
		for (i=0; i < lngFolds; i++) {
			lngLine = folds[i].range().startLine();
			lstLevels.push(nestLevel(tree.lineNumberToNode(lngLine)));
		}
		// null if no folds
		return lstLevels.sort()[0];
	}

	function setFoldLevel(editor, lngLevel) {
		// clear all existing folds
		// and fold all nodes at level N
		var strPath = new Array(lngLevel+1).join('/*'),
			lstNodes = editor.tree().evaluateNodePath(strPath);
		editor.removeFolds(editor.folds());
		editor.collapseNodes(lstNodes, false);
	}

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'expand more',
		description: 'Expand outline one more level',
		performCommand: function (editor) {
			var lngMaxDepth = maxdepth(editor.tree().root),
				lngLevel = getFoldLevel(editor);

			if (lngLevel) { // not null
				if (lngLevel < (lngMaxDepth)) {
					setFoldLevel(editor, lngLevel + 1);
				}
			}
		}

	});

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'collapse more',
		description: 'Collapse outline one more level',
		performCommand: function (editor) {
			var lngLevel = getFoldLevel(editor);
			if (lngLevel) {
				if (lngLevel > 1) {
					setFoldLevel(editor, lngLevel - 1);
				}
			} else { // fold the outer fringe
				setFoldLevel(editor, maxdepth(editor.tree().root) - 1);
			}
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		editor.addKeyMap({
			'Cmd-Alt-=' : 'expand more',
			'Cmd-Alt--' : 'collapse more',
		});
	});


});
