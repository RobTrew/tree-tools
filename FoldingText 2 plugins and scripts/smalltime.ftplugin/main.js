// Function datePhraseToISO(strPhrase) → yyyy-mm-dd [HH:MM] (unless 00:00)
// Author: Rob Trew Ver 0.2 2014 MIT License

// A small sublanguage for informal and relative dates
// not a full NLP parser

define(function(require, exports, module) {
	'use strict';

	// informal phrases like 'now +7d', 'thu', jan 12 2pm' to ISO string
	// yyyy-mm-dd [HH:MM] (unless 00:00)
	// returns strPhrase itself if can not be parsed
	function datePhraseToISO(strPhrase, iWeekStart) {
		if (typeof iWeekStart === "undefined" || iWeekStart === null) {
			iWeekStart = 1; //Monday=1 (or Sunday=0)
		}
		var dte = phraseToDate(strPhrase, iWeekStart);
		if (dte) {
			if (isNaN(dte)) {
				return strPhrase;
			} else {
				return fmtTP(dte);
			}
		} else {
			return strPhrase;
		}
	}

	// Javascript Date() to ISO date string
	function fmtTP(dte) {
		if (dte) {
			var strDate = [dte.getFullYear(),
					('0' + (dte.getMonth()+1)).slice(-2),
					('0'+ dte.getDate()).slice(-2)].join('-'),
				strTime = [('00'+dte.getHours()).slice(-2),
					('00'+dte.getMinutes()).slice(-2)].join(':');
			if (strTime !== '00:00') {
				return [strDate, strTime].join(' ');
			} else {
				return strDate;
			}
		} else {
			return '';
		}
	}

	// preprocess a nodePath to translate curly-bracketed date phrases to ISO
	function translatePathDates(strPath) {
		return strPath.replace(/{[^}]+}/g, datePhraseToISO(strPath));
	}

	// if a time specified for today has already passed, assume tomorrow
	function adjustDay(dteAnchor) {
		if (dteAnchor < new Date()) {
			if (dteAnchor > (new Date().setHours(0,0,0,0))) {
				dteAnchor.setDate(dteAnchor.getDate() +1);
			}
		}
	}

	// informal phrases like 'now +7d', 'thu', jan 12 2pm' to .js Date()
	function phraseToDate(strPhrase, iWeekStart) {
		if (typeof iWeekStart === "undefined" || iWeekStart === null) {
			iWeekStart = 1; //Monday
		}

		var DAY_MSECS = 86400000, WEEK_MSECS = 604800000,
			lstAnchors = ['now', 'toda','tomo', 'yest',
				'yesterday', 'today', 'tomorrow'],
			lstDate = ['y', 'w', 'd', 'year', 'yr', 'week',
				'wk','day', 'month', 'o'],
			lstTime = ['h', 'hr', 'hour', 'm', 'min', 'minute'],
			lstAmPm = ['am', 'pm', 'a', 'p'], lstSign = ['+', '-'],
			dctMonths = {'jan':0, 'feb':1, 'mar':2, 'apr':3, 'may':4, 'jun':5,
				'jul':6, 'aug':7, 'sep':8, 'oct':9, 'nov':10, 'dec':11},
			dctShift = {'next':1, 'last':-1, 'ago':0},
			dctNum = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4,
				'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10,
				'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14,
				'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18,
				'nineteen':19, 'twenty':20, 'thirty':30, 'forty':40,
				'fifty':50, 'sixty':60, 'seventy':70, 'eighty': 80,
				'ninety':90},
			dctOrd = {'first':1, 'second':2, 'third':3, 'fifth':5,
				'eighth':8, 'twelfth':12},
			lstNth = ['st','nd','rd','th'],
			dctAnchor = extractISODate(strPhrase),
			dteAnchor = dctAnchor['date'],
			rDelta = 0, dteResult = null,
			lstTokens = tokens(dctAnchor['rest']),
			lngTokens = lstTokens.length, blnOrd = false,
			strBase = '', strAffix = '',
			strTkn = '', strLower = '', iToday, iWkDay, iDay,
			lngSign =+1, rQuant = 0, strUnit='d', i,
			blnDate = false, blnNewQuant = false, strAbbrev ='',
			blnNewUnit = false, blnPostColon = false, blnNextLast = false;

		// Closure - shares core variables with parent function phraseToDate
		function upDate(strUnit) {
			var lngYear, strMonth='', iMonth=-1,
				dteToday=null, dteNow=null, rYearDelta=0;
			rQuant *= lngSign;
			switch (strUnit) {
			case 'w':
				if (blnNextLast) {
					iToday = (iToday || new Date().getDay());
					rDelta += (((7 - (iToday * lngSign))+(iWeekStart * lngSign)) * (DAY_MSECS * lngSign));
				} else {
					rDelta += (rQuant * WEEK_MSECS);
				} break;
			case 'd':
				if (blnOrd) {
					if (rQuant < dteAnchor.getDate()) {
						dteAnchor.setMonth(dteAnchor.getMonth() + 1);
					}
					dteAnchor.setDate(rQuant);
				} else {
					rDelta += (rQuant * DAY_MSECS);
				} break;
			case 'h': // add quantity of hours
				if (!blnDate) {dteAnchor = new Date(); blnDate = true;}
				rDelta += (rQuant * 3600000); break;
			case 'H': // set the clock hour
				dteAnchor.setHours(~~rQuant);
				adjustDay(dteAnchor); break;
			case 'm': // add quantity of minutes
				if (!blnDate) {dteAnchor = new Date(); blnDate = true;}
				rDelta += (rQuant * 60000); break;
			case 'M': // set the clock minutes
				dteAnchor.setMinutes(~~rQuant);
				adjustDay(dteAnchor); break;
			case 'o': // month(s)
				if ((rYearDelta = ~~(rQuant / 12)) !== 0) {
					dteAnchor.setFullYear(dteAnchor.getFullYear()+rYearDelta);
				}
				dteAnchor.setMonth(dteAnchor.getMonth() + (~~rQuant) % 12);
				if (blnNextLast) {dteAnchor.setDate(1);}
				break;
			case 'y':
			case 'Y':
				if (rQuant > 31) { // just 2019 vs jul 17
					dteAnchor.setFullYear(~~rQuant);
				} else {
					dteAnchor.setFullYear(dteAnchor.getFullYear() + ~~rQuant);
				} break;
			case 'a':
				if (!blnPostColon) {
					dteAnchor.setHours(~~rQuant);
					adjustDay(dteAnchor);
				}
				break;
			case 'p':
				if (blnPostColon) {
					if (dteAnchor.getHours() < 12) {
						dteAnchor.setHours(dteAnchor.getHours() + 12);
						adjustDay(dteAnchor);
					}
				} else  {
					if (rQuant < 12) {
						dteAnchor.setHours(~~rQuant + 12);
					} else {
						dteAnchor.setHours(~~rQuant);
					}
					adjustDay(dteAnchor);
				} break;
			default:
				if (strUnit.length >= 3) {
					if (strUnit in dctMonths) {
						dteAnchor.setMonth(dctMonths[strUnit]);
						if (rQuant <= 31) {
							if (rQuant) {
								dteAnchor.setDate(rQuant);
							} else {
								dteAnchor.setDate(1);
							}
						} else {
							dteAnchor.setFullYear(rQuant);
							dteAnchor.setDate(1);
						}
						dteToday = new Date(); dteToday.setHours(0,0,0,0);
						if (dteAnchor < dteToday) {
							dteAnchor.setFullYear(dteAnchor.getFullYear()+1);
						}
					}
				}
			}
			blnNewUnit = blnNewQuant = false; blnNextLast = false; rQuant = 0;
			blnDate = true; lngSign = 1; //scope of sign limited to one number
		}

		if (lngTokens) { // get a base date,
			if (dteAnchor) {
				blnDate = true;
			} else {
				dteAnchor = new Date();
			}
			dteAnchor.setHours(0,0,0,0);
		}
		for (i=0; i<lngTokens; i++) { // tokens adjust the Anchor date or Delta
			strTkn = lstTokens[i]; strBase = strAffix = '';
			if (strTkn) {
				blnOrd = false; strAffix = '';
				strLower = strTkn.toLowerCase();
				if (strLower.length > 1) {
					strAffix = strLower.slice(-2);
					if (strAffix === 'th') {strBase = strLower.slice(0,-2);}
				}

				// normalise any numeric
				//debugger;
				if (strLower in dctNum) {
					strLower = dctNum[strLower].toString();
				} else if (strLower in dctOrd) {
					strLower = dctOrd[strLower].toString();
					blnOrd = true;
				} else if (strBase && strBase in dctNum) {
					strLower = dctNum[strBase].toString();
					blnOrd = true;
				}

				if (strLower.slice(-1) === 's') {
					strLower = strLower.slice(0,-1);
				}
				strAbbrev = strLower.slice(0,4);
				if (!isNaN(strLower)) {
					rQuant += parseFloat(strLower);
					blnNewQuant = true;
					if (rQuant > 2000 && rQuant < 2500) {
						if (blnNewUnit) {
							upDate(strUnit);
						} else {
							strUnit = 'y'; blnNewUnit = true;
						}
					}
				} else if (lstNth.indexOf(strLower) !== -1) {
					blnOrd = true;
				} else if (lstDate.indexOf(strLower) !== -1) {
					if (strLower !== 'month') {
						strUnit = strTkn[0];
					} else {
						strUnit = 'o';
					}
					blnDate = blnNewUnit = true;
				} else if (strLower.substring(0,3) in dctMonths) {
					strUnit = strLower.substring(0,3);
					blnDate = blnNewUnit = true;
				} else if (lstTime.indexOf(strLower) !== -1) {
					strUnit = strTkn[0];
					blnNewUnit = true;
				} else if (lstAnchors.indexOf(strAbbrev) !== -1) {
					blnDate = true;
					if (strAbbrev !== 'now') {
						if (strAbbrev !== 'toda') {
							strUnit = 'd'; rQuant = 1;
							blnNewUnit = blnNewQuant = true;
							if (strAbbrev !== 'tomo') {
								lngSign = -1;
							}
						}
					} else {
						dteAnchor = new Date();
					}
				} else if ((iWkDay = weekDay(strLower)) !== -1) {
					iToday = (iToday || new Date().getDay());
					strUnit = 'd';
					blnNewUnit = blnNewQuant = true;
					if (iWkDay > iToday) {
						rQuant = iWkDay - iToday;
					} else {
						rQuant = 7 - (iToday - iWkDay);
					}
					if (blnNextLast && (iToday !== iWkDay)) {
						rQuant += 7 * lngSign; lngSign=1;
					}
				} else if (lstSign.indexOf(strTkn) !== -1) {
					if (strTkn == '+') {
						lngSign = 1;
					} else {
						lngSign = -1;
					}
				} else if (strTkn == ':' || strTkn == '.') {
					blnPostColon = true; upDate('H'); strUnit = 'M';
					rQuant = 0;
					blnNewQuant = false; blnNewUnit = true;
				} else if (strLower in dctShift) {
					if (dctShift[strLower]) { // unles 'ago'
						blnNextLast = blnNewQuant = true; rQuant = 1;
						if (strTkn !== 'next') {lngSign = -1;}
					} else if (rDelta > 0) { // 'ago: reflect around now'
						rDelta = -rDelta;
						dteAnchor = new Date();
						if (strUnit !== 'h') {dteAnchor.setHours(0,0,0,0);}
					}
				} else if (lstAmPm.indexOf(strLower) !== -1) {
					strUnit = strTkn[0];
					blnNewUnit = blnNewQuant = true;
				}
				if (blnNewUnit && blnNewQuant) {
					upDate(strUnit);
				}
			} else {strLower = '';}
		}
		// No more tokens. Default unit and quantity is 1 day
		if (blnNewUnit && !blnNewQuant) {
			rQuant = 1; upDate(strUnit);
		} else if (!blnNewUnit && blnNewQuant) {
			upDate('d');
		}
		if (blnDate) {
			dteResult = new Date(dteAnchor.valueOf() + rDelta);
		} else {
			dteResult = dteAnchor;
		}
		return dteResult;
	}
	// separate any token which looks like yyyy-mm-dd from the rest
	function extractISODate(strDate) {
		var match = /((\d{4})-(\d{2})-(\d{2}))/.exec(strDate),
			lngYear, lngMonth, lngDay,
			dte = null, strRest = strDate, iMatch;

		if (match !== null) {
			lngYear = parseInt(match[2],10);
			lngMonth = parseInt(match[3],10) -1; //zero based
			lngDay = parseInt(match[4],10);
			dte = new Date(lngYear, lngMonth, lngDay);
			iMatch = match.index;
			strRest = strDate.substring(0, iMatch) + ' ' +
				strDate.substring(iMatch+10);
		}
		return {'date':dte, 'rest':strRest.trim()};
	}

	// English weekday name to JS index into the week
	function weekDay(strTkn) {
		var lstDays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
			lstFullDays = ['sunday', 'monday', 'tuesday', 'wednesday',
			'thursday', 'friday', 'saturday'],
			iDay = lstDays.indexOf(strTkn.slice(0,3));
		if (iDay !== -1) {
			if (lstFullDays[iDay].slice(0,strTkn.length) !== strTkn) {
				return -1; //month != monday
			}
		}
		return iDay;
	}

	// informal date phrase to array of tokens
	function tokens(strWords) {
		var lstWords = strWords.split(/\s*\b\s*/),
			rgxNum = /^\d+/, match,
			lngWords = lstWords.length, strWord, strNum,
			lstTokens = [], i, strRest='';
		for (i=0; i<lngWords; i++) {
			strWord = lstWords[i].trim();
			if (strWord) {
				match = rgxNum.exec(strWord);
				if (match !== null) {
					strNum = match[0]; lstTokens.push(strNum);
					strRest = strWord.substring(strNum.length);
					if (strRest) {lstTokens.push(strRest);}
				} else {
					lstTokens.push(strWord);
				}
			}
		}
		return lstTokens;
	}

	// PROPERTIES AND FUNCTION(S) TO EXPORT
	exports.version = 0.2;
	exports.datePhraseToISO = datePhraseToISO; //Phrase to ISO string
	exports.phraseToDate = phraseToDate; // Phrase to JS Date()
	exports.fmtTP = fmtTP; // JS Date() to ISO string
	// search and replace for date phrases enclosed in curly brackets
	exports.translatePathDates = translatePathDates;


});
