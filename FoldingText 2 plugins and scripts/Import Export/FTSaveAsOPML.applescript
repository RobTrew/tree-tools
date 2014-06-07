-- Copyright (C) 2014 Robin Trew---- Permission is hereby granted, free of charge, -- to any person obtaining a copy of this software -- and associated documentation files (the "Software"), -- to deal in the Software without restriction, -- including without limitation the rights to use, copy, -- modify, merge, publish, distribute, sublicense, -- and/or sell copies of the Software, and to permit persons -- to whom the Software is furnished to do so, -- subject to the following conditions:-- *******-- The above copyright notice and this permission notice -- shall be included in ALL copies -- or substantial portions of the Software.-- *******-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, -- EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES -- OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. -- IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, -- DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, -- TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE -- OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.property pTargetApp : "FoldingText"property pTitle : "Export OPML from " & pTargetAppproperty pVer : "0.1"property pAuthor : "Robin Trew"property pSite : "Originally published on https://github.com/RobTrew/tree-tools"property pblnDebug : false-- Edit the following to false to use this script for exporting only selected lines and their descendantsproperty pblnWholeDocument : falseproperty pOutFolder : (path to desktop) -- edit this to "" to default to the same folder as the FT/TP fileproperty pstrDefaultTitle : "Exported from " & pTargetApp -- edit to "" to use the title of the FT documentproperty precOptions : {title:pstrDefaultTitle, wholedoc:pblnWholeDocument}property pstrJS : "

		function(editor, options) {
	
			// FIND THE ROOT NODES AMONG THE SELECTED LINES
			// (Ignoring any children of lines already seen)
			function selectedRoots() {
				var lstRoots = [], lstSeen = [];
	
				editor.selectedRange().forEachNodeInRange(function(oNode) {
					if (oNode.type() !== 'empty') {
						if (lstSeen.indexOf(oNode.parent.id) == -1) {
							lstRoots.push(oNode);
						}
						lstSeen.push(oNode.id);
					}
				});
				return lstRoots;
			}
	
			// TRANSLATE A SET OF ROOTS AND THEIR DESCENDANTS INTO OPML
			function opmlTranslation(lstRoots, strTitle) {
	
				var lstOPMLHead = [
						'<?xml version=\"1.0\" encoding=\"utf-8\"?>',
						'<opml version=\"1.0\">',
						'  <head>',
						'    <title>' + strTitle + '</title>',
						'    <expansionState>'],
					lstOPMLPostExpand = [
						'</expansionState>',
						'  </head>',
						'  <body>'],
					lstOPMLTail = [
						'  </body>',
						'</opml>'],
					strNodeStart = '<outline ',
					strLeafClose = '/>',
					strParentClose = '>',
					strOutlineClose = '</outline>',
					strOPML = lstOPMLHead.join('\\n');


				// WRITE OUT A SINGLE NODE AS OPML, AND RECURSE WITH ITS CHILDREN
				function opmlOutline(oNode, strIndent) {
					var	strOut = strIndent + strNodeStart + 'text=\"' + quoteAttr(oNode.text()) + '\"',
						dctTags = oNode.tags(),
						blnChiln = oNode.hasChildren(),
						strKey, strValue, strDeeper = strIndent + '  ';
	
					// add @key(values) as attributes
					for (strKey in dctTags) {
						strValue = oNode.tag(strKey);
						if (!strValue) strValue = 1;
						strOut += (' ' + strKey + '=\"' + quoteAttr(strValue) + '\"');
					}
	
					// recurse with any children before closing the <outline>
					if (blnChiln) {
						strOut += (strParentClose + '\\n');
						oNode.children().forEach(function(oChild) {
							strOut += opmlOutline(oChild, strDeeper);
						});
						strOut += (strIndent + strOutlineClose + '\\n');
					} else {
						strOut += (strLeafClose + '\\n');
					}
					return strOut;
				}
				// ASSEMBLE THE OPML HEADER, 
				strOPML += ('0' + lstOPMLPostExpand.join('\\n') + '\\n');

				// RECURSE THROUGH THE TREE
				lstRoots.forEach(function (oNode) {
					strOPML += opmlOutline(oNode, '    ');
				});

				// AND APPEND THE OPML TAIL
				strOPML += (lstOPMLTail.join('\\n') + '\\n')
				return strOPML;
			}

			// Attribute-quoting code adapted from:
			// http://stackoverflow.com/questions/7753448/how-do-i-escape-quotes-in-html-attribute-values/9756789
			function quoteAttr(s) {
			    return ('' + s) /* Forces the conversion to string. */
			        .replace(/&/g, '&amp;') /* This MUST be the 1st replacement. */
			        .replace(/'/g, '&apos;') /* The 4 other predefined entities, required. */
			        .replace(/\"/g, '&quot;')
			        .replace(/</g, '&lt;')
			        .replace(/>/g, '&gt;')
			        ;
			}

			// MAIN
	
			var lstRoots;

			// EXPORT WHOLE DOC ?
			if (options.wholedoc) {
				lstRoots = editor.tree().evaluateNodePath('/*');
			} else { //JUST THE SELECTED LINE(S) AND ALL ITS/THEIR DESCENDANTS
				lstRoots = selectedRoots();
			}
			return opmlTranslation(lstRoots, quoteAttr(options.title));
		}
"on run	tell application "FoldingText"		if not pblnDebug then			set lstDocs to documents			if lstDocs ≠ {} then				tell item 1 of lstDocs					-- PROMPT FOR AN EXPORT AS FILE PATH					try						set {strBaseName, strFTPath} to {name, POSIX path of ((its file) as alias)}					on error						activate						display dialog pTargetApp & " file not yet saved: " & return & return & ¬							"Save before exporting to OPML." buttons {"OK"} default button "OK" with title pTitle & "  ver " & pVer						return					end try					set strOutPath to my ChooseFilePathAndSave(it, strFTPath, strBaseName, "opml", pblnWholeDocument)										-- AND IF WE HAVE A DESTINATION, WRITE OPML TO IT					if strOutPath is not missing value then						set recOptions to precOptions						if title of recOptions = "" then ¬							set title of recOptions to name of it												-- TRANSLATE TO AN OPML STRING						set varResult to (evaluate script pstrJS with options recOptions)						if (class of varResult is text) and (varResult ≠ "") then														-- AND WRITE IT OUT							my WriteText2Path(varResult, strOutPath)						end if					end if				end tell								set varResult to strOutPath			end if		else			-- debug script automatically refers to the SDK version of the editor			-- which must be open: (FT2/TP3) > Help > SDK > Run Editor						set varResult to (debug script pstrJS with options precOptions)		end if		return varResult	end tellend run-- SAVE A STRING TO A TEXT FILEon ChooseFilePathAndSave(oApp, strPath, strBaseName, strExtn, blnWholeDoc)	tell application "Finder"		-- OFFER A DEFAULT FOLDER (if a valid one is specified)		if exists pOutFolder then			set strOutFolder to POSIX path of pOutFolder		else			-- OR OFFER THE FOLDER CONTAINING THE .OO3 FILE			set lngName to length of strBaseName			set strOutFolder to text 1 thru ((-lngName) - 1) of strPath		end if	end tell	set {dlm, my text item delimiters} to {my text item delimiters, "."}	set strStem to first text item of strBaseName	set my text item delimiters to dlm		if blnWholeDoc then		set strTitle to "Export " & pTargetApp & " document to OPML"	else		set strTitle to "Export selected lines and their descendants from " & pTargetApp & " to OPML"	end if		tell oApp		activate		set strOutPath to missing value		try			set strOutPath to (POSIX path of ¬				(choose file name with prompt strTitle default name strStem & "." & strExtn default location strOutFolder))		end try	end tell	return strOutPathend ChooseFilePathAndSaveon WriteText2Path(strText, strPosixPath)	set f to (POSIX file strPosixPath)	open for access f with write permission	write strText as «class utf8» to f	close access fend WriteText2Path