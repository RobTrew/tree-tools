### Python parser for TaskPaper and FoldingText formats

Parses [TaskPaper](www.hogbaysoftware.com) or [FoldingText](www.FoldingText.com) plain text documents to a list of dictionaries using the same node attributes as Jesse Grosjean's reference parser at [https://www.npmjs.org/package/foldingtext](https://www.npmjs.org/package/foldingtext).

Source: [ft_tp_parse_019.py](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/ft_tp_parse_019.py)

#### Goal

This parser aims to produce the same output as the www.foldingtext.com reference parser, and later versions will be adjusted to match any further changes in that parser.

Best practice is to use the [www.foldingtext.com](www.foldingtext.com) reference parser directly. This is available in a draft command line form for TaskPaper 3.0 at [https://www.npmjs.org/package/foldingtext)](https://www.npmjs.org/package/foldingtext).

The reference parser (implemented in Javascript by Hog Bay Software and www.foldingtext.com, and copyright Jesse Grosjean) additionally provides a powerful hierarchical query language, documented at [http://www.foldingtext.com/sdk/nodepaths/](http://www.foldingtext.com/sdk/nodepaths/)

This python parser has the following limitations:

1. It is a provisional draft,
2. it provides no query language,
3. and it only parses node types, tags, nesting, and ft mode flags.
	(it attempts no parsing of inline Markdown formatting)

This is intended simply as a stop-gap for contexts in which the use of Javascript is inconvenient, or where there is a need for a simple light-weight parse which is compatible with the output of the reference parser produced by Jesse Grosjean, [www.HogBaySoftware.com](www.HogBaySoftware.com) and [www.foldingtext.com](www.HogBaySoftware.com)

#### Output

The parse translates the lines of the utf8 input text to a list of dictionaries, each of which has the following keys, (shown below with their correspondence to elements in the official www.foldingtext.com Javascript reference parser)

Python dictionary key | Matching element in the official reference parser
---|---
'id' | node.id
'parentID' | node.parent.id
'text' | node.text() [with any tags, .mode indicators, and syntactic markers removed]
'line' | node.line() [full text line, including prefixes and tags etc. but without LF]
'lineNumber' | node.lineNumber()
'nestedLevel' | nestedLevel(node) [Top level nodes have nestedLevel = 1]
'tagNames' | Object.keys(node.tags()) [list in sequence of textual occurence]
'tags' | node.tags() [dictionary of key:value pairs]
'textIndex' | node.lineTextStart() [the line's starting character position in the text]
'type' | node.type() [see FoldingText and TaskPaper node type strings below]
'typeIndentLevel' | node.typeIndentLevel() [number of leading hashes, or tab-count +1]
'childIndex' | node.indexToSelf() [position in sequence of peers]
'mode' | node.mode() [any special mode of FoldingText, e.g. .todo]
'modeContext' | node.modeContext() [any parentally inherited special mode of FT]
'chiln' | [list of child ids, first & last matching .firstChild.id and .lastChild.id]
'path' | [list: ancestral sequence of node.indexToSelf() indices]


#### Parses the following elements of FoldingText and TaskPaper documents:
- @key(value) tags,
- outline nesting levels,
- parent-child relationships, and
- node types:
	- **FoldingText**:
		TYP_ROOT = 'root'
		TYP_HEAD = 'heading'
		TYP_UNORD = 'unordered'
		TYP_ORD = 'ordered'
		TYP_BODY = 'item'
		TYP_QUOTE = 'blockquote'
		TYP_CODE = 'codeblock'
		TYP_LINK = 'linkdef'
		TYP_PROP = 'property'
		TYP_TERM = 'term'
		TYP_DEFN = 'definition'
		TYP_RULE = 'horizontalrule'
		TYP_EMPTY = 'empty'
	- **TaskPaper**:
		TYP_PROJ = 'project'
		TYP_TASK = 'task'
		TYP_NOTE = 'note'	(temporarily '_comment_' in current build of TaskPaper 3.0)


NB the parser leaves in-line Markdown formatting unparsed.

#### The parser provides two module level Python functions:

1. `is_tp(str_text)`

	Returns True if the text appears to be in TaskPaper format.
	(Otherwise, the www.FoldingText.com FoldingText MD format is assumed)

2. `get_ft_tp_parse(str_text, bln_is_tp)`

	Depending on the boolean value of `bln_is_tp`, parses the text either as [TaskPaper 3.0](http://support.foldingtext.com/discussions/development-versions) format or as [FoldingText 2.0](http://support.foldingtext.com/discussions/development-versions) format, generating a list of Python dictionaries, one for each line of the text, with the key/value pairs indicated above.
#### Source

Source: [ft_tp_parse_019.py](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/ft_tp_parse_019.py)

