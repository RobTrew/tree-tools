function(editor, options) {
	var	oParser = new DOMParser(),
		oXMLDoc = oParser.parseFromString(options.opml,'text/xml'),
		oOPML = oXMLDoc.childNodes[0],
		oBody = oOPML.lastElementChild, oOutline = oBody.firstElementChild,
		lngMaxHash = options.hashlevels, strMD = '';

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

	while (oOutline !== null) {
		strMD += mdTrans(oOutline, 0);
		oOutline = oOutline.nextElementSibling;
	}
	return strMD;
}
