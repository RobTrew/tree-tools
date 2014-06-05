#### A script to Open OPML outlines in FoldingText

- [FT2ImportOPML.scptd](./FT2ImportOPML.scptd)

- [FT2ImportOPML.applescript](./FT2ImportOPML.applescript)
- [OPML2FT.py](./OPML2FT.py)
- [FT2ImportOPML.zip](./FT2ImportOPML.zip)

#### Installation

This is an applescript which uses a Python helper script to convert from OPML to FoldingText Markdown.

It therefore needs:

1. To be saved as a Compiled Script Bundle .scptd
		(not as .applescript or flat .scpt)
2. To have the Python script OPML2FT.py copied into the script bundle's `Contents/Resources` folder. For example as: `FT2ImportOPML.scptd/Contents/Resources/OPML2FT.py`

_To open an .scptd bundle, ctrl-click it, and choose ‘Show Package Contents’_


(Note that if you accidentally to a Save As in a format other than .scptd, the bundle format and the Python script will be lost. 

You will then need to save again as .scptd, and manually place a copy of [OPML2FT.py](./OPML2FT.py) in FT2ImportOPML.scptd/Contents/Resources/)


#### Use
- Run the script from something like [KeyBoard Maestro](http://www.keyboardmaestro.com/main/) or [FastScripts](http://www.red-sweater.com/fastscripts/)
- Choose an OPML file from the File Open dialog which appears.