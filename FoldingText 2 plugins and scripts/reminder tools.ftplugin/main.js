// Interpret date tags:
// 1.	Informal or relative phrases in
//		specified date tags in selected line are converted to ISO
// 2.	The date and other values are returned to any calling Applescript
//		through window.RTpluginReturn, so that a linked Reminder.app
//		can be updated or created.

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions').Extensions,
		dateLogic = require('../smalltime.ftplugin/main.js'),
		Editor;

	function updateAndReadForLink(dctArgs) {

		var	lstResults = translateDateTags(Editor, dctArgs),
			node = lstResults[0], strLine = node.line(),
			strText = node.text(),
			dctReturn = lstResults[1], strTag='', oMatch,
			lstHeat = dctArgs.heat || [], lngHeat = 0, i,
			rgxReminder = /\[[^\]]*\]\((x-apple-reminder:\/\/[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\)/;

		// Find the highest priority/heat tag and return a 1-based index
		lngHeat = lstHeat.length;
		for (i=0; i<lngHeat; i++) {
			strTag = lstHeat[i];
			if (strTag.charAt(0) !== '@') {strTag = ('@' + strTag);}
			if (strLine.indexOf(strTag) !== -1) {
				if (i > 2) {i=2;}
				dctReturn.heat = i+1;
				break;
			}
		}

		// Separate any Reminders UUID from the main text entry
		oMatch = rgxReminder.exec(strText);
		if (oMatch) {
			dctReturn.uuid = oMatch[1];
			dctReturn.text = strText.substring(0, oMatch.index-1);
		} else {
			dctReturn.text = strText;
		}
		// return the harvest for any calling Applescript
		return dctReturn;
	}

	// translate values of specified date tags to ISO (if informal/relative)
	// and return any values for uuid, text, alarm tag, priority,
	// and any other requested date tags
	function translateDateTags(Editor, dctArgs) {
		var lstUpdateTags = ['alarm'],
			tree = Editor.tree(),
			node = Editor.selectedRange().startNode,
			dctReturn = {'uuid':null, 'text':null, 'alarm':null,
				'datetext':null, 'iso':null, 'heat':null},
			dctNodeTags = node.tags(),
			lstNodeTags = Object.keys(dctNodeTags), strKey='', strVal,
			lngSeconds=0, lstKeySet, lngTag,
			strTrans='', dteUpdated, strAlarmKey, blnDelta, i;

		// read any arguments to override defaults for alarm,
		// other date tags, and priority tags
		if (typeof dctArgs !== 'undefined') {
			strAlarmKey = dctArgs.alarm || 'alarm';
			if (strAlarmKey.charAt(0) === '@') {
				strAlarmKey = strAlarmKey.substring(1);
			}
			lstUpdateTags = dctArgs.others || [];
			lstUpdateTags.push(strAlarmKey);
		}
		// strip any leading '@' from date tags to get the key
		lngTag = lstUpdateTags.length;
		for (i=0; i<lngTag; i++) {
			strKey = lstUpdateTags[i];
			if (strKey.charAt(0) === '@') {
				lstUpdateTags[i] = strKey.substring(1);
			}
		}
		// normalise any date or date adjustment phrases in date tags to ISO
		tree.beginUpdates();
		lstNodeTags.forEach(function(strKey) {
			if (lstUpdateTags.indexOf(strKey) !== -1) {
				strVal = dctNodeTags[strKey];
				if (strVal) {
					// compute any deferrals, interpret any informal dates
					dteUpdated = dateLogic.phraseToDate(strVal);
					strTrans = dateLogic.fmtTP(dteUpdated);

					blnDelta = (strVal !== strTrans);
					if (blnDelta) {
						// belt and braces as a workaround to
						// ensure update both of display and of model
						node.addTag(strKey, strTrans);
						dctNodeTags[strKey] = strTrans;
					}
					// collect dates for calling script
					lngSeconds = ~~(dteUpdated.valueOf() / 1000);
					if (strKey !== strAlarmKey) {
						dctReturn[strKey] = lngSeconds;
					} else {
						dctReturn.alarm = lngSeconds;
						dctReturn.datetext = strVal;
						dctReturn.iso = strTrans;
					}
				}

			}
		});
		tree.endUpdates();

		return [node, dctReturn];
	}


	//translate date tag(s) to ISO and return UUID, date(s), priorty, text
	exports.version = 0.2;
	exports.updateAndReadForLink = updateAndReadForLink;

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'translate date tags',
		description: 'convert to ISO absolute',
		performCommand: translateDateTags
	});

	Extensions.add('com.foldingtext.editor.init', function(editor) {
		Editor = editor;

		Editor.addKeyMap({
			"Shift-Cmd-U" : 'translate date tags'
		});
	});

});
