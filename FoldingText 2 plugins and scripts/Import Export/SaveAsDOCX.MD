#### Saving a FoldingText 2 Outline as a .docx MS Word file

- [FoldingText-SaveAs-docx.applescript](./FoldingText-SaveAs-docx.applescript)


This [script]((./FoldingText-SaveAs-docx.applescript)) is an Applescript wrapper for FoldingText 2 which calls:

- Fletcher Penney's MultiMarkdown, and

	[http://fletcherpenney.net/multimarkdown](http://fletcherpenney.net/multimarkdown])

- John MacFarlane's Pandoc.

	[http://johnmacfarlane.net/pandoc](http://johnmacfarlane.net/pandoc)

#### Installation

1. Install Pandoc from [http://johnmacfarlane.net/pandoc/installing.html](http://johnmacfarlane.net/pandoc/installing.html)
2. In Terminal.app, check the path of the pandoc command by entering the command:
	`type -a pandoc`
	
3. In the Applescript, check the property `pstrPandoc` (near the top of the script), and edit its value, if necessary, to match the path returned by `type -a pandoc` e.g:

	`property pstrPandoc : "/usr/local/bin/pandoc"`

4. Install MultiMarkdown from [http://fletcherpenney.net/multimarkdown/install/#macosx](http://fletcherpenney.net/multimarkdown/install/#macosx)
5. In Terminal.app, check the path of the pandoc command by entering the command:
	`type -a multimarkdown`
6. In the Applescript check that the property `pstrMMD` (near the top of the script), and edit its value, if necessary, to match the path returned by `type -a multimarkdown` e.g:

	`property pstrMMD : "/usr/local/bin/multimarkdown"`


You can then run the script from something like [KeyBoard Maestro](http://www.keyboardmaestro.com/main/) or [FastScripts](http://www.red-sweater.com/fastscripts/)

- Hash headers level 1 to N in your FoldingText document will become MS Word outline Heading Levels 1 to N

- Indented list items will be correspondingly indented

- The document can be further styled by changing the MS Word theme.


_Alternatively, to export from FoldingText to MS Word in a way that directly applies CSS stylesheet formatting, and also offers formatted PDF exports, try Brett Terpstra’s excellent [marked2.app](http://marked2app.com)_


