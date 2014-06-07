-- Copyright (C) 2014 Robin Trew
--
-- Permission is hereby granted, free of charge, 
-- to any person obtaining a copy of this software 
-- and associated documentation files (the "Software"), 
-- to deal in the Software without restriction, 
-- including without limitation the rights to use, copy, 
-- modify, merge, publish, distribute, sublicense, 
-- and/or sell copies of the Software, and to permit persons 
-- to whom the Software is furnished to do so, 
-- subject to the following conditions:

-- *******
-- The above copyright notice and this permission notice 
-- shall be included in ALL copies 
-- or substantial portions of the Software.
-- *******

-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
-- EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
-- OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
-- IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
-- DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
-- TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
-- OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

property pTitle : "Import OPML outline into FoldingText"
property pVer : "0.2" -- FIRST DRAFT OF VERSION WHICH PARSES AND TRANSLATES IN JS
property pAuthor : "Robin Trew"

property pblnDebug : false

property plngHeaderLevels : 2 -- Make the top N (N ³ 0) levels of the OPML outline into Markdown hash headers 
property pstrNoteIndent : tab & tab -- relative to preceding unordered list item (2 tabs or 1) (_note attribute of outline item)

-- Ver 0.2 any "_note" attributes imported as body text


property precOptions : {hashlevels:plngHeaderLevels, noteindent:pstrNoteIndent}
property pSrcFolder : (path to desktop)

property pstrOPML2MD : "
	function(editor, options) {
		var	oParser = new DOMParser(),
			oXMLDoc = oParser.parseFromString(options.opml,'text/xml'),
			oBody = oXMLDoc.documentElement.lastElementChild,
			oOutline = oBody.firstElementChild,
			lngMaxHash = options.hashlevels,
			strNoteIndent = options.noteindent,
			strMD = '';

		// RECURSIVE FUNCTION: WALKS XML (OPML) PARSE TRANSLATING TO MD
		function mdTrans(oNode, lngLevel) {
			var dctAttrib = oNode.attributes,
				lstKeys = Object.keys(dctAttrib),
				strKey, strName, strValue, lngNextLevel = lngLevel +1,
				strText = '', strTags = '', strNote= '', strIndent = '',
				strOut = '', strPrefix, strTabs='', oChild=null;

			// # Hash headings down to options.hashlevels,
			// and tab indented unordered lists thereafter
			if (lngLevel < lngMaxHash) {
				strPrefix = Array(lngLevel +2).join('#') + ' ';
			} else {
				strTabs = Array(lngLevel-lngMaxHash).join('\\t');
				strPrefix =  strTabs + '- ';
			}

			// MD TRANSLATION OF THIS NODE
			lstKeys.forEach(function(strKey) {
				strName = dctAttrib[strKey].name;
				if (strName !== undefined) {
					if (strName !== 'text') {
						if (strName !== 'length') {
							if (strName !== '_note') {
								strTags += (' @' + strName);
								strValue = dctAttrib[strKey].textContent;
								if (strValue) strTags += ('(' + strValue + ')');
							} else strNote = dctAttrib[strKey].textContent;
						}
					} else strText = strPrefix + dctAttrib['text'].textContent;
				}
			});
			// NODE TEXT AS HASH HEADER OR UNORDERED LIST ITEM
			strOut += (strText + strTags + '\\n');

			// AND ANY _NOTE ATTRIBUTE TEXT AS BODY
			if (strNote) {
				strIndent = strTabs;
				if (lngLevel >= lngMaxHash)  strIndent = strTabs + strNoteIndent;
				strOut += (strIndent + strNote.split('\\n').join('\\n' + strIndent) + '\\n');
			}

			// WITH MD TRANSLATIONS OF ALL/ANY DESCENDANT NODES
			if (oNode.childElementCount > 0) {
				oChild = oNode.firstElementChild;
				while (oChild !== null) {
					strOut += mdTrans(oChild, lngNextLevel);
					oChild = oChild.nextElementSibling;
				}
			}
			return strOut;
		}

		// MAIN
		while (oOutline !== null) {
			strMD += mdTrans(oOutline, 0);
			oOutline = oOutline.nextElementSibling;
		}
		editor.setTextContent(strMD);
	}
"


on run
	-- CHOOSE AN OPML FILE
	tell application "Finder"
		if exists pSrcFolder then
			set strSrcFolder to POSIX path of pSrcFolder
		else
			set strSrcFolder to POSIX path of (path to home folder)
		end if
	end tell
	
	tell application "FoldingText"
		activate
		set strOPMLFile to (POSIX path of Â
			(choose file with prompt pTitle default location strSrcFolder))
		
		-- REMEMBER THIS FOLDER FOR THE NEXT RUN - VALUES OF APPLESCRIPT PROPERTIES PERSIST BETWEEN RUNS
		set {dlm, my text item delimiters} to {my text item delimiters, "/"}
		set pSrcFolder to POSIX file ((items 1 thru -2 of (text items of strOPMLFile)) as string) as alias
		set my text item delimiters to dlm
		
		if strOPMLFile does not end with ".opml" then
			activate
			display dialog strOPMLFile & return & return & Â
				"File must have .opml extension" buttons {"OK"} default button "OK" with title pTitle & "  ver. " & pVer
			return
		end if
		set strOPML to my readFile(strOPMLFile)
		
		-- CREATE A NEW FT DOC CONTAINING THE IMPORTED TEXT
		if pblnDebug then
			set varResult to (debug script pstrOPML2MD with options precOptions & {opml:strOPML})
		else
			tell (make new document) --with properties {text contents:strOPML})
				set varResult to (evaluate script pstrOPML2MD with options precOptions & {opml:strOPML})
			end tell
			activate
		end if
		varResult
	end tell
end run


on readFile(strPath)
	set oFile to (open for access (POSIX file strPath))
	set strText to (read oFile for (get eof oFile) as Çclass utf8È)
	close access oFile
	return strText
end readFile
