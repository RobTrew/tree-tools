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

property pTitle : "Import OPML file to FoldingText"
property pVer : "0.1" -- FIRST DRAFT OF VERSION WHICH PARSES AND TRANSLATES IN JS
property pAuthor : "Robin Trew"

property pblnDebug : false

property plngHeaderLevels : 2 -- Make the top N (N ³ 0) levels of the OPML outline into Markdown hash headers 

property precOptions : {hashlevels:plngHeaderLevels}


property pSrcFolder : (path to desktop)

property pstrOPML2MD : "
		function(editor, options) {
			var	oParser = new DOMParser(),
				oXMLDoc = oParser.parseFromString(options.opml,'text/xml'),
				oOPML = oXMLDoc.childNodes[0],
				oBody = oOPML.lastElementChild, oOutline = oBody.firstElementChild,
				lngMaxHash = options.hashlevels, strMD = '';
	
			// Recursive function: walks XML (OPML) parse translating to MD
			function mdTrans(oNode, lngLevel) {
				var dctAttrib = oNode.attributes,
					lstKeys = Object.keys(dctAttrib),
					strKey, strName, strValue, lngNextLevel = lngLevel +1,
					strText = '', strTags = '',
					strOut = '', strPrefix, oChild=null;
	
				if (lngLevel < lngMaxHash) {
					strPrefix = Array(lngLevel +2).join('#') + ' ';
				} else {
					strPrefix = Array(lngLevel-lngMaxHash).join('	') + '- ';
				}
				// get the string of this node
	
				Object.keys(dctAttrib).forEach(function(strKey) {
					strName = dctAttrib[strKey].name;
					if (strName !== 'text') {
						if (strKey !== 'length') {
							strTags += (' @' + strName);
							strValue = dctAttrib[strKey].textContent;
							if (strValue) strTags += ('(' + strValue + ')');
						}
					} else {
						strText = strPrefix + dctAttrib['text'].textContent;
					}
				});
				strOut += (strText + strTags + '\\n');
	
				// and append that of any descendants by recursion
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
			return strMD;
		}
"


on run
	-- CHOOSE AN OPML FILE
	tell application "Finder"
		pSrcFolder
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
