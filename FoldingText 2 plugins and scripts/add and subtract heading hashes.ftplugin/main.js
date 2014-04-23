// Add or remove a heading hash (selected line)
// (Removing the last hash toggles the line between header
// and unordered list item)

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions');

	function shiftHeader(editor, lngDelta) {
		var oNode = editor.selectedRange().startNode, lngLevel=0;
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
			}
			oNode.setTypeIndentLevel(lngLevel);
		}
	}

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'deeper heading',
		description: 'add a hash prefix',
		performCommand: function (editor) {

			shiftHeader(editor, 1);
		}
	});

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'shallower heading',
		description: 'remove a hash prefix',
		performCommand: function (editor) {

			shiftHeader(editor, -1);
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		editor.addKeyMap({
			'Cmd-H' : 'deeper heading',
			'Shift-Cmd-H' : 'shallower heading',
		});
	});


});
