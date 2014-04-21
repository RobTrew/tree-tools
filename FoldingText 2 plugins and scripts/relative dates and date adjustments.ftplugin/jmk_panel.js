/* ------------------------------------------------------------- *
 * Panel Module for FoldingText 2.0 Plugins
 * by Jamie Kowalski, github.com/jamiekowalski/foldingtext-extra
 * Use of this code and associated files is permitted without restriction, provided
 * the above attribution and this statement are included in all copies of this code.
 *
 * Usage:
 *
 * The event callback functions are passed the event object and the panel object;
 * but there is no need to capture these in your functions if they are not needed.
 *
 * None of the options are required; define as many functions as you need.
 *
 * Return false from a function to prevent the default behavior (e.g. closing panel
 * on return).
 *
 * var Panel = require('./panel.js').Panel;
 *
 * var panel = new Panel({
 *   className: 'MyPanel',
 *   placeholder: 'type some text...',
 *   onTextChange: function (event, panel) {},
 *   onBlur: function (event, panel) {},
 *   onReturn: function (event, panel) {},
 *   onEscape: function (event, panel) {},
 *   onCommand: function (event, panel) {}, // use event.which to determine which
 *                                          // key other than Command is pressed
 *   ignoreWhiteSpace: true,     // don't get changes in leading/trailing whitespace
 *   addToDOM: true
 * });
 *
 * ------------------------------------------------------------- */

define(function(require, exports, module) {
	'use strict';

	var Extensions = require('ft/core/extensions'),
		editor; // assigned in the 'init' function below


	// Panel constructor; assigned to exports.Panel below
	var p = function (opts) {

		var COMMAND_LEFT = 91,
			COMMAND_RIGHT = 93,
			RETURN = 13,
			ESC = 27,
			KEY_A = 65,
			KEY_Z = 90,
			debug = false,
			no_op = function () {}, // no-op function to use as default
			performDefault;

		// define default options
		this.options = {
			className: 'JKPanel',
			placeholder: 'enter text...',
			onTextChange: no_op,
			onBlur: no_op,
			onReturn: no_op,
			onEscape: no_op,
			onCommand: no_op,
			ignoreWhiteSpace: true,
			addToDOM: true
		};

		// copy options from argument
		for (var op in opts) {

			if ( this.options[op] === undefined ) {
				console.log('JKPanel: \'' + op + '\' is not a valid option. Ignoring.');
			} else if ( typeof this.options[op] !== typeof opts[op] ) {
				console.log( 'JKPanel: Option \'' + op + '\' must be of type ' +
					typeof this.options[op] + '. Reverting to default.' );
			} else {
				this.options[op] = opts[op];
			}
		}

		this.isShown = false;    // TODO hide this property
		this.currentValue = '';

		// add unsettable properties
		Object.defineProperty(
			this,
			'element',
			{ value: document.createElement('div') }
		);
		Object.defineProperty(
			this,
			'input',
			{ value: document.createElement('input') }
		);

		// set panel attributes
		this.element.style.display = 'none';       // don't show panel at first

		this.input.setAttribute('type', 'text');
		this.input.setAttribute('value', '');
		this.input.setAttribute('placeholder', this.options.placeholder);
		if (this.options.className) {
			this.element.classList.add(this.options.className);
		}

		this.element.insertBefore(this.input); // add the input to the panel


		// EVENTS

		// when editor is clicked, etc.
		this.input.addEventListener('blur', (function(event) {
			if (this.options.onBlur && this.options.onBlur !== no_op) {
				performDefault = this.options.onBlur(event, this);
			}
			if (performDefault !== false) {     // panel's default behavior
				this.hide(true);    // close the panel, keep contents
			}
		}).bind(this));

		// capture changes to input
		this.input.addEventListener('input', (function(event) {
			if (debug) console.log( 'input change event: \'' + this.input.value + '\'' );

			if (this.options.ignoreWhiteSpace) {
				if ( this.input.value.trim() === this.currentValue ) {
					if (debug) console.log( 'No change' );

				} else {
					if (debug) console.log( 'Text changed' );
					this.currentValue = this.input.value.trim();

					if (this.options.onTextChange && this.options.onTextChange !== no_op) {
						this.options.onTextChange(event, this);
					}
				}
			} else {
				if (this.options.onTextChange && this.options.onTextChange !== no_op) {
					this.options.onTextChange(event, this);
				}
			}

		}).bind(this));

		// capture keyups (for command keys, etc.)
		this.input.addEventListener('keyup', (function(event) {
			if (debug) console.log('keyup: ' + event.which);
			if (debug) console.log(this.keysDown);

			if (event.which === COMMAND_LEFT) {          // left command key
				this.keysDown[COMMAND_LEFT] = false;
			} else if (event.which === COMMAND_RIGHT) {  // right command key
				this.keysDown[COMMAND_RIGHT] = false;
			}

		}).bind(this));

		// capture keydowns (for command keys, etc.)
		this.input.addEventListener('keydown', (function(event) {
			if (debug) console.log('keydown: ' + event.which);

			if (event.which === RETURN) {                  // return key pressed

				if (this.options.onReturn && this.options.onReturn !== no_op ) {
					performDefault = this.options.onReturn(event, this);
				}
				if (performDefault !== false) {      // panel's default behavior
					this.input.dispatchEvent(new CustomEvent('blur'));
					event.preventDefault();
				}

			} else if ( event.which === COMMAND_LEFT ) {     // command keys pressed
				this.keysDown[COMMAND_LEFT] = true;
			} else if ( event.which === COMMAND_RIGHT ) {
				this.keysDown[COMMAND_RIGHT] = true;
			} else if ( event.which === ESC ) {            // escape key pressed

				if ( this.options.onEscape && this.options.onEscape !== no_op ) {
					this.options.onEscape( event, this );
				}
				if ( performDefault !== false ) {        // panel's default behavior
					this.hide(false);
					event.preventDefault();
				}

			} else if ( this.keysDown[COMMAND_LEFT] || this.keysDown[COMMAND_RIGHT] ) {
				// Modify behavior of some command combinations

				if ( this.options.onCommand && this.options.onCommand !== no_op ) {
					performDefault = this.options.onCommand( event, this );
				}
				if (performDefault !== false ) {
					if ( event.which === KEY_A ) {           // Command + A
						this.input.select();
						event.preventDefault();
					} else if ( event.which === KEY_Z ) {    // Command + Z
						event.preventDefault();
					}
				}

			}
		}).bind(this));

		// Add panel to DOM

		if ( this.options.addToDOM ) {
			document.body.insertBefore( this.element );
		}
	};

	Object.defineProperty( p.prototype, 'keysDown', { value: {} } );

	p.prototype.addToDOM = function () {
		document.body.insertBefore( this.element );
	};
	p.prototype.show = function ( text, selection, selectionEnd ) {
		if ( text || text === '' ) {
			this.input.value = text;
		}
		this.element.style.display = 'block';
		this.input.focus();

		if (! selection || selection === 'around' ) {
			this.input.select();          // select contents
		} else if ( selection === 'start' ) {
			this.input.setSelectionRange(0, 0);
		} else if ( selection === 'end' ) {
			var length = this.input.value.length;
			this.input.setSelectionRange(length, length);
		} else if (typeof selection === 'number' ) {
			var end = selectionEnd || selection;
			this.input.setSelectionRange(selection, end);
		} else if ( selection === 'preserve' ) {
			// do nothing
		} else {
			this.input.select();          // select for other values
		}

		if ( this.options.ignoreWhiteSpace ) {
			this.currentValue = this.input.value.trim();
		}
		this.isShown = true;
	};
	p.prototype.hide = function ( keepContents ) {
		if ( !keepContents ) {
			this.input.value = '';
		}
		if ( this.options.ignoreWhiteSpace ) {
			this.currentValue = this.input.value.trim();
		}
		this.element.style.display = 'none';
		editor.focus();
		this.isShown = false;
	};
	p.prototype.toggle = function ( keepContents, text ) {
		if ( this.isShown ) {
			this.hide( keepContents );
		} else {
			this.show( text );
		}
	};
	p.prototype.clear = function () {
		this.input.value = '';
	};
	p.prototype.value = function () {
		if ( this.options.ignoreWhiteSpace ) {
			return this.input.value.trim();
		} else {
			return this.input.value;
		}
	};

	Extensions.add('com.foldingtext.editor.init', function( ed ) {
		editor = ed;
	});

	exports.Panel = p;

});
