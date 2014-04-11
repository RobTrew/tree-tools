define(function (require) {
	'use strict';

	describe('Expand and collapse', function () {
		var MarkdownTaxonomy = require('ft/taxonomy/markdowntaxonomy').MarkdownTaxonomy,
			Taxonomies = require('ft/core/taxonomies'),
			Editor = require('ft/editor/editor').Editor,
			taxonomy = Taxonomies.taxonomy({
				foldingtext: true,
				multimarkdown: true,
				gitmarkdown: true,
				criticMarkup: true
			}, 'markdown'),
			editor;

		beforeEach(function () {
			editor = new Editor('', taxonomy);
		});

		afterEach(function () {
			editor.removeAndCleanupForCollection();
		});

		it('level of folding should increase in steps', function () {
			var lstFolds = [], i=0;
			editor.setTextContent('# a\n- b\n\t- c\n\t\t- d\n# e\n- f\n\t- g\n\t\t- h');
			editor.performCommand('collapse more');
			editor.performCommand('collapse more');
			for (i = 0; i < 2; i++) {
				lstFolds.push(editor.folds()[i].range().startLine());
			}
			expect(editor.folds().length).toEqual(2);
			expect(lstFolds[0]).toEqual(1);
			expect(lstFolds[1]).toEqual(5);
		});

		it('level of folding should decrease in steps', function () {
			var lstFolds = [], i=0;
			editor.setTextContent('# a\n- b\n\t- c\n\t\t- d\n# e\n- f\n\t- g\n\t\t- h');
			editor.performCommand('collapse more');
			editor.performCommand('collapse more');
			editor.performCommand('collapse more');
			editor.performCommand('expand more');
			editor.performCommand('expand more');
			for (i = 0; i < 2; i++) {
				lstFolds.push(editor.folds()[i].range().startLine());
			}
			expect(editor.folds().length).toEqual(2);
			expect(lstFolds[0]).toEqual(2);
			expect(lstFolds[1]).toEqual(6);
		});


	});


});


