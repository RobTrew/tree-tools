// Paste a full map of FT keyboard assignments as an MMD table
// Shift-Cmd-Ctrl-Alt-K

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions').Extensions,
		pasteboard = require('ft/system/pasteboard'),
		dctShowKeys = {'name':'show map', 'keys':'Shift-Cmd-Ctrl-Alt-K'},
		dctKeys = {};

	function pasteKeyMap(editor) {
		var lstKeys = sortedKeys(editor),
			strHead = '| Key | Assignment |\n|:----|:-----------|\n',
			strKeys = strHead + lstKeys.join('\n');

			editor.replaceSelection('Please wait a moment ...', 'around');
			editor.replaceSelection(strKeys);
			pasteboard.writeString(strKeys);
	}

	function sortedKeys(editor) {
		//debugger;
		var //varMap = editor.reverseKeyMapLookup(),
			lstMaps = editor._keyMaps,
			lngMaps = lstMaps.length, i,
			dctMap = {}, strKey, varVal, lstKeys=[];


		for (i=0; i< lngMaps; i++) {
			dctMap = lstMaps[i];
			for (strKey in dctMap) {
				if (strKey !== 'name') {
					varVal = dctMap[strKey];
					if (!(varVal && typeof(varVal) === 'string')) {
						varVal = typeof(varVal);
					}
					lstKeys.push('| `' + keySymbols(strKey) +
						'` | ' + varVal.split('\n')[0] + ' |');
				}
			}
		}
		lstKeys.sort();
		return lstKeys;
	}

	function keySymbols(strKeys) {
		return strKeys.replace(
			'Shift-', '⇧').replace(
			'Cmd-', '⌘').replace(
			'Ctrl-',  '^').replace(
			'Alt-', '⌥');
	}

	Extensions.add('com.foldingtext.editor.commands', {
		name: dctShowKeys.name,
		description: 'show keyboard assignments',// + ' - ' + keySymbols(
			//dctDeep.keys),
		performCommand: function (editor, pasteboard) {

			pasteKeyMap(editor);
		}
	});

	Extensions.add('com.foldingtext.editor.init', function (editor) {
		dctKeys[dctShowKeys.keys] = dctShowKeys.name;
		editor.addKeyMap(dctKeys);
	});


});


//
