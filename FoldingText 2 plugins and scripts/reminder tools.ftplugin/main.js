// Interpret date tags:
// 1.	Informal or relative phrases in
//		specified date tags in selected line are converted to ISO
// 2.	The date and other values are returned to any calling Applescript
//		through window.RTpluginReturn, so that a linked Reminder.app
//		can be updated or created.


define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions'),
		dateLogic = require('../smalltime.ftplugin/smalltime.js'),
		Editor;

	// translate values of specified date tags to ISO (if informal/relative)
	// and return any values for uuid, text, alarm tag, priority,
	// and any other requested date tags
	function translatedDateTags(Editor, dctArgs) {
		var lstUpdateTags = ['alarm'],
			tree = Editor.tree(),
			node = Editor.selectedRange().startNode,
			dctReturn = {'uuid':null, 'text':null, 'alarm':null,
				'datetext':null, 'iso':null, 'heat':null},
			dctNodeTags = node.tags(), strLine = node.line(),
			lstNodeTags = Object.keys(dctNodeTags), strKey='', strVal,
			lngSeconds=0, lstKeySet, strTag, lngTag,
			strTrans='', dteUpdated, strAlarmKey, blnDelta,
			rgxReminder = /\[[^\]]*\]\((x-apple-reminder:\/\/[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\)/, oMatch,
			lstHeat=[], lngHeat = 0, i;

		// read any arguments to override defaults for alarm,
		// other date tags, and priority tags
		if (typeof dctArgs !== 'undefined') {
			strAlarmKey = dctArgs.alarm || 'alarm';
			if (strAlarmKey.charAt(0) === '@') {
				strAlarmKey = strAlarmKey.substring(1);
			}
			lstUpdateTags = dctArgs.others || [];
			lstUpdateTags.push(strAlarmKey);
			lstHeat = dctArgs.heat || [];
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

		// Find the highest priority/heat tag and return a 1-based index
		lngHeat = lstHeat.length;
		for (i=0; i<lngHeat; i++) {
			strTag = lstHeat[i];
			if (strTag.charAt(0) !== '@') {strTag = ('@' + strTag);}
			if (strLine.indexOf(strTag) !== -1) {
				dctReturn.heat = i+1;
				break;
			}
		}

		// Separate any Reminders UUID from the main text entry
		oMatch = rgxReminder.exec(node.line());
		if (oMatch) {
			dctReturn.uuid = oMatch[1];
			dctReturn.text = node.text().substring(0, oMatch.index-2);
		} else {
			dctReturn.text = node.text();
		}
		// Use a global to return the harvest to any calling Applescript
		window.RTpluginReturn = dctReturn;
	}


	Extensions.add('com.foldingtext.editor.commands', {
		name: 'interpret date tags',
		description: 'translate to ISO absolute',
		performCommand: translatedDateTags
	});

	Extensions.add('com.foldingtext.editor.init', function(editor) {
		Editor = editor;

		Editor.addKeyMap({
			//open bracket with Cmd held down
			"Shift-Cmd-U" : 'interpret date tags'
		});
	});

});
