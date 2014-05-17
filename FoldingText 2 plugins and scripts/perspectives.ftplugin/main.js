// Perspectives for FoldingText


define(function(require, exports, module) {
	'use strict';

	var	Extensions = require('ft/core/extensions'),
		dctViewMenu = {
			'Empty view': {
				'for':'$tag',
				'in':[],
				'let':[],
				'groupby':[],
				'orderby':[],
				'where':'true',
				'return':[]
			},

			'Grouped by unknown priority levels':{
				'for':'$line',
				'in':'//*',
				'let': '$level=$line@priority',
				'group':'$level',
				'sort':'$level',
				'order' : 'ascending',
				'return':[
					'### Priority {$level}',
					{'for':'$node',
						'in':'$level',
						'return':'- {$node@text}'
					}
				]
			},

			'Grouped by priority':{
				'for':'$level',
				'in':[1, 2, 3],
				'return':[
					'### Priority {$level}',
					{'for':'$node',
						'in':'//@priority={$level}',
						'return':'- {$node@text}'
					}
				]
			},


			'Grouped by tag':{
				'for':'$tag',
				'in':'fn:tagSet()',
				'return':[
					"### fn:sentenceCase({$tag})",
					{'for':'$node',
						'in':'//@{$tag}',
						'return':'- {$node@text}'
					}
				]
			}

		},

		dctViewFn = {
			'tagSet':function tagSet(editor) {
				return editor.tree().tags(true);
			},
			'sentenceCase': function sentenceCase(editor, strAny) {
				return strAny[0].toUpperCase() + strAny.slice(1).toLowerCase();
			}
		};

		// Group by tag
	function makeViewB(editor) {

		var lstIn = [], strOut='', tree=editor.tree();

		lstIn = dctViewFn['tagSet'](editor);
		lstIn.forEach(function (varTag) {
			var lstIn = tree.evaluateNodePath('//@' + varTag);
			strOut += "### " + dctViewFn['sentenceCase'](varTag) + '\n';
			lstIn.forEach(function(varNode) {
				strOut += "- " + varNode.text() + '\n';
			});
			strOut += '\n';
		});
		//debugger;
		return strOut;
	}

	// evaluate a string or FLWOR dictionary in a FLWOR line return list
	function makeLine(editor, varLine, dctLabels) {
		//debugger;
		var strType = typeof(varLine),
			strDeepType = strType.toString(), strLine;

		if (strType == 'string') {
			strLine = expandDollars(varLine, dctLabels);
			if (strLine.indexOf('fn:') !== -1) {
				strLine = expandFns(editor, strLine);
			}

		} else if (strType == 'object') {
			//debugger;
			// recurse with a child FLWOR to get a string
			strLine = writeReport(editor, varLine, dctLabels);
		}
		return strLine;
	}

	function expandFns(editor, strLine) {

		var rgxFnArgs = /fn:(\w+)\((.*)\)/,
			oMatch=null, strFn='', strArg='',
			strFull = strLine, strMatch, fn,
			strFnResult='';

		oMatch = rgxFnArgs.exec(strFull);
		if (oMatch !== null) {
			strMatch = oMatch[0];
			strFn = oMatch[1];
			strArg = oMatch[2];
			fn = dctViewFn[strFn];

			//debugger;
			if (typeof(fn) !== 'function') {
				strFull = strFull.replace(
					strMatch, strMatch +'=UNKNOWN FUNCTION', 'g');
			} else {
				strFnResult = fn(editor, strArg);
				strFull = strFull.replace(strMatch, strFnResult, 'g');
			}
		}
		return strFull;
	}


	// Can be a string expansion,
	// or getting a reference to an object,
	// and returning one of its attributes as a string.
	function expandDollars(varItem, dctLabels) {
		//debugger;
		var rgxLabel = /(\{(\$.*)\})/,
			rgxNodeAttribute = /^(\$.*)\@(.*)/,
			strNode, oNode, strAttrib,
			oMatch = rgxLabel.exec(varItem),
			oAttribMatch = null,
			strLine = varItem.toString(),
			strMatch, strLabel, varValue;

			// first expand the string before any @
			// then branch on the kind of object which the key returns
			// if there was no @ we should be getting a string
			// if (there is a @) {we try to return an attribute}

			while (oMatch !== null) {
				strMatch = oMatch[1];
				strLabel = oMatch[2];
				//debugger;
				oAttribMatch = rgxNodeAttribute.exec(strLabel);
				if (oAttribMatch !== null) {
					//debugger;
					strNode = oAttribMatch[1];
					oNode= dctLabels[strNode];
					if (typeof(oNode) !== 'undefined') {
						strAttrib=oAttribMatch[2];
						strLine = strLine.replace(strMatch,
							getAttrib(oNode, strAttrib), "gi");
					} else {
						strLine = strLine.replace(strMatch,
							strLabel + '=UNDEFINED LABEL');
					}

				} else {
					varValue = dctLabels[strLabel];
					if (typeof(varValue) !== 'undefined') {
						strLine = strLine.replace(strMatch, varValue, "gi");
					} else {
						strLine = strLine.replace(strMatch,
							strLabel + '=UNDEFINED LABEL');
					}
				}
				oMatch = rgxLabel.exec(strLine);
			}

			return strLine;
	}

	function getAttrib(oNode, strAttrib) {
		var strValue = '';
		if (strAttrib == 'text') {
			strValue = oNode.text();
		} else if (strAttrib == 'line') {
			strValue = oNode.line();
		} else if (oNode.hasTag(strAttrib)) {
			strValue = oNode.tag(strAttrib);
		}
		return strValue;
	}

	function makeView(editor) {
		//debugger;
		// var dctView = dctViewMenu['Grouped by unknown priority levels'],
		// strReport = writeReport(editor, dctView, {});
		var strReport = subGroupView(editor);

		console.log(strReport);
		window.RTReport = strReport;
	}

	function subGroupView(editor) {
		//debugger;
		var tree = editor.tree(),
			strTag = 'due',
			strTag2 = 'priority',
			lstDue = tree.evaluateNodePath('//@' + strTag),
			strReport = '\n', dctGroup = {}, strValue,
			dctTag, dctTag2, lstDueSorted, lstSubDue=[], lstSubSorted;
		//debugger;
		dctGroup[strTag] = {};
		dctTag = dctGroup[strTag];

		// PUT NODES IN VALUE BINS
		lstDue.forEach(function (oNode) {
			strValue = getAttrib(oNode, strTag);
			if (strValue in dctTag) {
				dctTag[strValue].push(oNode);
			} else {
				// first one starts a fresh bin (list)
				dctTag[strValue] = [oNode];
			}
		});

		// SORT THE BINS BY THEIR VALUE (IF REQUESTED)
		lstDueSorted = Object.keys(dctTag);
		lstDueSorted.sort();

		// SUBDIVIDE THESE BINS BY ANOTHER FIELD ('PRIORITY')
		dctGroup[strTag2] = {};
		dctTag2 = dctGroup[strTag2];


		// FOR EACH DAY VALUE,
		lstDueSorted.forEach(function (strDate) {
			// WRITE OUT THE DATE
			strReport += ('### ' + strDate + '\n\n');

			// clear the Priority bins for the new date
			dctTag2 = {};

			// THEN GROUP THE HARVEST (FOR THIS DATE) BY PRIORITY
			lstSubDue = dctTag[strDate]; // list of nodes with same due date
			lstSubDue.forEach(function (oNode) {
				strValue = getAttrib(oNode, strTag2);
				if (strValue) {
					if (strValue in dctTag2) {
						dctTag2[strValue].push(oNode);
					} else {
						// first one starts a fresh bin (list)
						dctTag2[strValue] = [oNode];
					}
				}
			});

			// SORT, IF REQUESTED
			lstSubSorted = Object.keys(dctTag2);
			lstSubSorted.sort();

			// AND WRITE OUT THE LEVEL OF THE PRIORITY
			lstSubSorted.forEach(function (strValue) {
				strReport += ('#### ' + dctViewFn['sentenceCase'](
					editor, strTag2) + ' ' + strValue + '\n');
				// AND THE ASSOCIATED NODES
				dctTag2[strValue].forEach(function (oNode) {
					strReport += ("- " + getAttrib(oNode, 'text') + '\n');
				});
				strReport += '\n';
			});
			strReport += '\n';
		});


		return strReport;
	}


	function groupView(editor) {

		var tree = editor.tree(),
			strTag = 'priority',
			lstPrior = tree.evaluateNodePath('//@' + strTag),
			strReport = '', dctGroup = {}, strValue,
			dctTag, lstSorted;
		//debugger;
		dctGroup[strTag] = {};
		dctTag = dctGroup[strTag];

		// PUT NODES IN VALUE BINS
		lstPrior.forEach(function (oNode) {
			strValue = getAttrib(oNode, strTag);
			if (strValue in dctTag) {
				dctTag[strValue].push(oNode);
			} else {
				dctTag[strValue] = [oNode];
			}
		});

		// SORT THE BINS BY THEIR VALUE (IF REQUESTED)
		lstSorted = Object.keys(dctTag);
		lstSorted.sort();

		// LIST THE BINS AND THEIR CONTENTS
		lstSorted.forEach(function (strValue) {
			strReport += ('### ' + dctViewFn['sentenceCase'](
				editor, strTag) + ' ' + strValue + '\n');
				dctTag[strValue].forEach(function (oNode) {
					strReport += ("- " + getAttrib(oNode, 'text') + '\n');
				});
			strReport += '\n';
		});
		return strReport;
	}

	function writeReport(editor, dctView, dctLabels) {
		//debugger;
		var tree = editor.tree(),
			lstIn = [], strOut='',
			varIn = dctView['in'],
			strExpanded,
			strType, strFn, strArg, strItem,
			rgxIsPath = /^[\/\()]/,
			rgxFnArgs = /^fn:(\w+)\((.*)\)/,
			oMatch, strFor = dctView['for'];


		// CONSTRUCT THE (FLWOR) 'IN' ARRAY
		if (varIn) {
			//debugger;
			strType = typeof(varIn);
			if (strType == 'string') {
				strExpanded = expandDollars(varIn, dctLabels);
				if (rgxIsPath.exec(varIn) !== null) {
					lstIn = tree.evaluateNodePath(strExpanded);
				} else {
					oMatch = rgxFnArgs.exec(varIn);
					if (oMatch !== null) {
						strFn = oMatch[1]; strArg = oMatch[2];
						lstIn = dctViewFn[strFn](editor, strArg);
					}
				}
			} else if (strType == 'object') {
				lstIn = varIn;
			} else {
				// puzzlement -- raise an error
			}
		}

		// ITERATE THROUGH THE (FLWOR) 'IN' ARRAY
		//debugger;
		lstIn.forEach(function (varItem) {
			var varReturn = dctView['return'];
			dctLabels[strFor] = varItem;

			// varReturn should be a list of lines
			// wrap as list if user has supplied a single string
			if (typeof(varReturn) == 'string') {
				varReturn = [varReturn];
			}

			varReturn.forEach(function (varLine) {
				strOut += makeLine(editor, varLine, dctLabels) + '\n';
			});

		});
		return strOut;

	}



	// Next actions //heading//(not @done)[0]/ancestor-or-self::*
	// or just //heading//(not @done)[0]
	function makeViewD(editor) {

		var lstIn = [], strOut='', tree=editor.tree();

		lstIn = tree.evaluateNodePath('//heading');
		lstIn.forEach(function (varProj) {
			var strPath = '//\"' + varProj.text() + '\"/(not @done)[0]',
				lstIn = tree.evaluateNodePath(strPath);
			strOut += varProj.line() + '\n';
			lstIn.forEach(function(varNode) {
				strOut += "- " + varNode.text() + '\n';
			});
			strOut += '\n';
		});

		return strOut;
	}


	// Next actions //heading//(not @done)[0]/ancestor-or-self::*
	// or just //heading//(not @done)[0]
	function makeViewC(editor) {

		var lstIn = [], strOut='', tree=editor.tree();

		lstIn = tree.evaluateNodePath('//heading');
		lstIn.forEach(function (varProj) {
			var strPath = '//\"' + varProj.text() + '\"/(not @done)[0]',
				lstIn = tree.evaluateNodePath(strPath);
			strOut += varProj.line() + '\n';
			lstIn.forEach(function(varNode) {
				strOut += "- " + varNode.text() + '\n';
			});
			strOut += '\n';
		});

		return strOut;
	}


	// // PROPERTIES AND FUNCTION(S) TO EXPORT
	exports.version = 0.1;
	exports.makeView = makeView;


	// // exports.datePhraseToISO = datePhraseToISO; //Phrase to ISO string
	// // exports.phraseToDate = phraseToDate; // Phrase to JS Date()
	// // exports.fmtTP = fmtTP; // JS Date() to ISO string
	// // // search and replace for date phrases enclosed in curly brackets
	// // exports.translatePathDates = translatePathDates;

	Extensions.add('com.foldingtext.editor.commands', {
		name: 'generate Perspective',
		description: 'build a report from a JSON spec',
		performCommand: makeView
	});

	Extensions.add('com.foldingtext.editor.init', function(editor) {
		editor.addKeyMap({
			"Shift-Cmd-T" : 'generate Perspective'
		});
	});

});
