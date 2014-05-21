// Add or remove a heading hash (selected lines)
// (Removing the last hash toggles the line between header
// and unordered list item)

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions').Extensions,
		dctDeep = {'name':'deeper heading', 'keys':'Shift-Ctrl-]'},
		dctShallow = {'name':'shallower heading', 'keys':'Shift-Ctrl-['},
		dctKeys = {};

	function shiftLevels(editor, lngDelta) {
		var rngSeln = editor.selectedRange(),
			lstNodes = rngSeln.nodesInRange(),
			oLastNode = null,
			tree = editor.tree(),
			lngShift = 0, lngLevel = 0,

			rngShifted;

		lstNodes.forEach(function(oNode) {
			lngLevel = oNode.typeIndentLevel() + lngDelta;
			if (lngLevel > 6) {
				lngLevel = 6;
			} else if (lngLevel < 1) {
				oNode.setType('heading');
				lngLevel = 1;
			}
			oNode.setTypeIndentLevel(lngLevel);
		});
		oLastNode = lstNodes[lstNodes.length -1];
		rngShifted = tree.createRangeFromNodes(
				lstNodes[0], 0, oLastNode, -1);
		editor.setSelectedRange(rngShifted);

	}

	//function keySymbols(strKeys) {
	//	return strKeys.replace(
	//		'Shift-', '⇧').replace(
	//		'Cmd-', '⌘').replace(
	//		'Ctrl-',  '^').replace(
	//		'Alt-', '⌥');
	//}

	Extensions.add('com.foldingtext.editor.commands', {
		name: dctDeep.name,
		description: 'add a hash prefix',// + ' - ' + keySymbols(
			//dctDeep.keys),
		performCommand: function (editor) {

			shiftLevels(editor, 1);
		}
	});

	Extensions.add('com.foldingtext.editor.commands', {
		name: dctShallow.name,
		description: 'remove a hash prefix',// + ' - ' + keySymbols(
			//dctShallow.keys),
		performCommand: function (editor) {

			shiftLevels(editor, -1);
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		dctKeys[dctDeep.keys] = dctDeep.name;
		dctKeys[dctShallow.keys] = dctShallow.name;
		editor.addKeyMap(dctKeys);
	});


});
