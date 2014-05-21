// Adjust the number of outline levels which have hash headings

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions').Extensions;

	function maxhash(tree) {
		var lstHead = tree.evaluateNodePath('//@type=heading'),
			lngHead = 0, lngMax = 0, i, lngLevel;

		if (typeof lstHead !== 'undefined') {
			lngHead = lstHead.length;
			for (i=0; i < lngHead; i++) {
				lngLevel = lstHead[i].typeIndentLevel();
				if (lngLevel > lngMax) {
					lngMax = lngLevel;
				}
			}
		}
		return lngMax;
	}

	// Capture the nesting structure,
	// in case it changes while we adjust heading levels
	function nestedList(lstNodes) {
		var lstNest = [], lngNodes = lstNodes.length, i, node;
		for (i=0; i<lngNodes; i++) {
			node = lstNodes[i];
			if (node.hasChildren()) {
				lstNest.push([node, nestedList(node.children())]);
			} else {
				lstNest.push([node, []]);
			}
		}
		return lstNest;
	}

	function adjustHeaders(tree, lngDelta) {
		var lngMaxHash = maxhash(tree) + lngDelta,
			lstChiln = tree.root.children(),
			lstNest = nestedList(lstChiln);

		if (lngMaxHash < 0) {
			lngMaxHash = 0;
		} else if (lngMaxHash > 6) {
			lngMaxHash = 6;
		}

		// Recursive descent from level 1 (children of root: one hash)
		repaintOutline(tree, lstNest, lngMaxHash, 1);
	}



	function repaintOutline(tree, lstNest, lngMaxHash, lngLevel) {

		var lngNodes = lstNest.length,
			strNewType = 'heading', strOldType = 'unordered',
			lngNewIndent = lngLevel, lngOldIndent,
			lstNode, node, strType, lstChiln, lngChiln, i;

		if (lngLevel > lngMaxHash) {
			strNewType = 'unordered';
			strOldType = 'heading';
			lngNewIndent = (lngLevel - lngMaxHash);
		}


		for (i=0; i<lngNodes; i++) {
			lstNode = lstNest[i];
			node = lstNode[0];
			lstChiln = lstNode[1];
			lngChiln = lstChiln.length;


			// REPAINT THE TYPE AND INDENT OF THIS NODE,
			if (node.type() == strOldType) {
				node.setType(strNewType);
				tree.ensureClassified(node, node);
			}
			strType = node.type();
			if (strType == strNewType) {
				if (node.typeIndentLevel() !== lngNewIndent) {
					node.setTypeIndentLevel(lngNewIndent);
				}
			}

			// AND OF ITS CHILDREN.
			if (lngChiln) {
				repaintOutline(tree, lstChiln, lngMaxHash, lngLevel +1);
			}

		}
	}


	Extensions.add('com.foldingtext.editor.commands', {
		name: 'more heading levels',
		description: 'Increase number of heading levels by 1',
		performCommand: function (editor) {

			adjustHeaders(editor.tree(), 1);
		}
	});


	Extensions.add('com.foldingtext.editor.commands', {
		name: 'fewer heading levels',
		description: 'Decrease number of heading levels by 1',
		performCommand: function (editor) {

			adjustHeaders(editor.tree(), -1);
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		editor.addKeyMap({
			'Shift-Cmd-]' : 'more heading levels',
			'Shift-Cmd-[' : 'fewer heading levels',
		});
	});


});
