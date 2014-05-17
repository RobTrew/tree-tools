// Add or remove a heading hash (selected line)
// (Removing the last hash toggles the line between header
// and unordered list item)

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions'),
		dctDeep = {'name':'deeper heading', 'keys':'Shift-Ctrl-]'},
		dctShallow = {'name':'shallower heading', 'keys':'Shift-Ctrl-['},
		dctKeys = {};

	function shiftHeader(editor, lngDelta) {
		var rngSeln = editor.selectedRange(),
			tree = editor.tree(),
			oNode = rngSeln.startNode,
			lngShift = 0, lngLevel = 0,
			lngChar = rngSeln.location() - oNode.lineTextStart(),
			rngShifted;

		if (oNode.type() !== 'heading') {
			oNode.setType('heading');
			oNode.setTypeIndentLevel(1);
		} else {
			lngLevel = oNode.typeIndentLevel() + lngDelta;
			if (lngLevel > 6) {
				lngLevel = 6;
			} else if (lngLevel < 1) {
				oNode.setType('unordered');
				lngLevel = 1;
			} else {
				lngShift = lngDelta; // cursor position adjustment after change
			}
			oNode.setTypeIndentLevel(lngLevel);
		}
		if (lngChar < 0) {lngChar = 0;}
		rngShifted = tree.createRangeFromLocation(
			oNode.lineTextStart() + lngChar + lngShift, rngSeln.length());
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

			shiftHeader(editor, 1);
		}
	});

	Extensions.add('com.foldingtext.editor.commands', {
		name: dctShallow.name,
		description: 'remove a hash prefix',// + ' - ' + keySymbols(
			//dctShallow.keys),
		performCommand: function (editor) {

			shiftHeader(editor, -1);
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		dctKeys[dctDeep.keys] = dctDeep.name;
		dctKeys[dctShallow.keys] = dctShallow.name;
		editor.addKeyMap(dctKeys);
	});


});
