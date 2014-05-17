
var dctReportTypes =
{'first report':
	{
		'for':'$tag',
		'in':'fn:tagSet(///*)',
		// each let: item is a key to a function which will be applied to members of the in Array
		// after evaluation, the result of the function will be assigned to the key
		// The function may be a direct function reference or a string
		// any string may be a nodePath containing a nodepath including a $for variable (to expand)
		// or an fn:Function Name
		'let': {'key':'strExpr1', 'key2':'strExpr2'},

		//'group array items which share a value into tuples
		'orderby':'$tag',
		'order':'descending',
		'where':'',
		'return':['### ', 'fn:sentenceCase($tag)', ':\t(',
			'fn:sum($tag)', ' items)\n', {
			'for':'$node',
				'in':'//$tag',
				'return':['- ','$node[text]', '\n']
			}, '\n'
		]
	}
};




//{'$tag':undefined,'lstIn':tree.tags().sort()}

function writeReport(editor, dctSpec) {

	var tree = editor.tree(),
		rgxFnArgs = /^fn:(\w+)\((.*)\)/,
		oMatch = null, lstIn = [],
		dctLet = dctSpec['let'],
		strFn, strArgs,
		varIn, strType, strKey, varLet;
	// prepare the ground
	// and run the process

	// gather the base array, and establish a loop variable
	varIn = dctSpec.in;
	strType = typeof(varIn);
	if (strType === 'string') {
		//could be a function
		if (varIn.slice(0,3) == 'fn:') {
			oMatch = rgxFnArgs.exec(varIn);
			if (oMatch !== null) {
				lstIn = dctViewFunctions[oMatch[1]](oMatch[2]);
			} else { //raise error
				// starts with fn: but doesn't look like function call
			}
		} else {  // evaluate a nodePath
			lstIn = tree.evaluateNodePath(varIn);
		}
	} else if (strType === 'array') {
		lstIn = varIn;
	} else { // raise error
		// unexpected type - expected string or array
		lstIn = [];
	}

	dctLet = dctSpec['let'];
	// for each key in this, we need to establish a pointer to a live function
	for (strKey in dctSpec) {
		varLet = dctSpec[strKey];
		strType = typeof(varLet);
		// or an fn:function to apply
		// or an expression to eval
		// could be a nodePath containing a $value to expand
	}
}




// feed the json object to an instance of an ftView class
// whose prototype contains functions for reading the tree
// the structure is recursive - the return element of an ftView may
// contain an ftView

// name: for use in a UI menu
// for variable : one predeclared (indefinite type, for each ftView object)
// in resolves to an array
// 	 if the 'in': string starts with fn: then call a class function
//		else evaluate it as nodePath through the active tree
// where, if not empty apply as a further nodepath condition ??
// 		may not be necessary, as a final nodePath clause may cover most/all cases ?
// orderby: sort the array, defaulting to ascending unless order:starts with 'd'
// groupby: Supports calcns like: how many nodes are tagged @vertical ?


