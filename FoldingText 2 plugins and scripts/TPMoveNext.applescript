property pTitle : "Move the @next tag along, leaving @done in its wake"property pVer : "0.5" -- DRAFT ...property pAuthor : "RobTrew"property pblnDebug : false-- ROUGH DRAFT:-- **MOVE** THE @NEXT OR @NOW TAG (edit pstrTag below) ON TO THE NEXT UNCOMPLETED ITEM IN THE PROJECT-- [Marking the current line as @done(yyy-mm-dd hh:mm) ]-- (If all lines under this heading/project are now @done, then mark the heading/project itself as @done)-- (and if there are no lines after this which are not @done, but there are some before, jump to the first of them and place the @next tag there)property pstrTag : "next"property plstExcept : {"done", "wait"}property precOptions : {tag:pstrTag, except:plstExcept}property pstrJS : "
	function(editor, options) {

		// WALK A PROJECT OUTLINE - WHICH IS THE NEXT ELIGIBLE NODE ?
		function nextNode(tree, oCurrent, strWhere, strTag) {
			var	oNext=null, oAncestor,
				strID = oCurrent.id, lstNodes, strPath, i;

			// ANY INCOMPLETE DESCENDANTS ?
			// (if not, mark as done)
			strPath = nextPath(strID, 'descendant', strWhere);
			lstNodes = tree.evaluateNodePath(strPath);
			if (lstNodes.length) {
				oNext = lstNodes[0];
			} else {
				if (oCurrent.type() != 'root') {
					oCurrent.addTag('done', fmtTP(new Date()));

					//ANY FOLLOWING SIBLINGS REMAIN ?
					strPath = nextPath(strID, 'following-sibling', strWhere);
					lstNodes = tree.evaluateNodePath(strPath);
					if (lstNodes.length) {
						oNext = lstNodes[0];
					} else {

						// WHAT IS THE MOST RECENT INCOMPLETE ANCESTOR ?
						strPath = nextPath(strID, 'ancestor', strWhere);
						oAncestor = tree.evaluateNodePath(strPath)[0];
						if (oAncestor !== undefined) {
							oNext = nextNode(tree, oAncestor, strWhere,strTag);
						}
					}
				} else {
					//whole document appears to be complete ... nothing to be done
				}
			}

			return oNext;
		}

		// Assemble node path for next eligible descendant, sibling, or ancestor
		function nextPath(strID, strAxis, strWhere) {
			var strPath = '//@id=' + strID + '/' + strAxis + '::' + strWhere + ')';
			if (strAxis != 'ancestor') {
				strPath += '[0]'; //first found sibling or descendant
			} else {
				strPath += '[-1]'; //last found (most immediate) ancestor
			}
			return strPath;
		}

		// Javascript Date() to FT/TP datetime string
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

		// TAG THE CURRENT LINE AS 'NOW' OR 'NEXT'
		// (AND IF IT'S ALREADY TAGGED NOW/NEXT, TAG IT AS 'DONE' AND MOVE THE @NOW TAG TO THE NEXT
		//  ELIGIBLE LINE UNDER THIS PROJECT/HEADING, OR MARK THE WHOLE PROJECT/HEADING AS 'DONE')
		//debugger;
		var tree = editor.tree(),
			strTag = options.tag, lstExcept = options.except,
			oSelnNode = editor.selectedRange().startNode,
			oCurrent, oNextNode,
			strSelnID = oSelnNode.id,
			strWhere = '(@type!=root and @line:text!=\"\" and not @done and not @' + strTag,
			strAncestors = '//@id=' + strSelnID + '/ancestor-or-self::(not @done and (@type=heading or @type=project or @type=root))[-1]',
			lstAncestors = tree.evaluateNodePath(strAncestors), lstNext,
			strTaggedNext,
			strProjectID=0;

		//ANY CURRENT @NEXT NODE(S) IN THIS PROJECT ?

		if (lstAncestors.length) {
			strProjectID = lstAncestors[0].id;
		}
		//debugger;
		if (strProjectID != '0') {
			strTaggedNext = '//@id=' + strProjectID + '/descendant-or-self::@' + strTag;
		} else {
			strTaggedNext = '//@' + strTag;
		}


		lstNext = tree.evaluateNodePath(strTaggedNext);

		if (lstNext.length) {
			oCurrent = lstNext[0];

			// Clear this and other @next tags in the project
			lstNext.forEach(function(oNode) {
				oNode.removeTag(strTag);
			});

			// add any excluded tags to the list of conditions for @next status
			if (lstExcept.length) {
				lstExcept.forEach(function(strExcept) {
					if (strExcept !== 'done') {
						strWhere += (' and not @' + strExcept);
					}
				});
			}
			// and look for a successor

			oNextNode = nextNode(tree, oCurrent, strWhere, strTag);
			if (oNextNode) {
				oNextNode.addTag(strTag);
			}

		} else {
			oSelnNode.addTag(strTag);
		}
	}
"on run	tell application "TaskPaper"		if not pblnDebug then			set lstDocs to documents			if lstDocs ≠ {} then				tell item 1 of lstDocs					set varResult to (evaluate script pstrJS with options precOptions)				end tell			end if		else			-- debug script automatically refers to the SDK version of the editor			-- which must be open: FoldingText > Help > SDK > Run Editor			set varResult to (debug script pstrJS with options precOptions)		end if		return varResult	end tellend run