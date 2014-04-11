define(function (require) {
	'use strict';

	describe('Change number of hash heading levels used', function () {
		var MarkdownTaxonomy = require('ft/taxonomy/markdowntaxonomy').MarkdownTaxonomy,
			Taxonomies = require('ft/core/taxonomies'),
			Editor = require('ft/editor/editor').Editor,
			taxonomy = Taxonomies.taxonomy({
				foldingtext: true,
				multimarkdown: true,
				gitmarkdown: true,
				criticMarkup: true
			}, 'markdown'),
			editor,
			strText = '\n- Top\n\t- A\n\t\t- a\n\t\t- b\n\t- B\n\t\t- c\n\t\t- d\n\t- C\n\t\t- e\n\t\t- f';

		beforeEach(function () {
			editor = new Editor('', taxonomy);
		});

		afterEach(function () {
			editor.removeAndCleanupForCollection();
		});

		it('Should increment number of hashed outline levels', function () {
			var lstFolds = [], i=0;
			editor.setTextContent(strText);
			editor.performCommand('more heading levels');
			editor.performCommand('more heading levels');
			expect(editor.tree().lineNumberToNode(5).line()).toEqual('## B');
			expect(editor.tree().lineNumberToNode(6).line()).toEqual('- c');
		});

		it('Should decrement number of hashed outline levels', function () {
			var lstFolds = [], i=0;
			editor.setTextContent(strText);
			editor.performCommand('more heading levels');
			editor.performCommand('more heading levels');
			editor.performCommand('more heading levels');
			editor.performCommand('fewer heading levels');
			editor.performCommand('fewer heading levels');
			expect(editor.tree().lineNumberToNode(5).line()).toEqual('- B');
			expect(editor.tree().lineNumberToNode(1).line()).toEqual('# Top');
		});

	});


});


