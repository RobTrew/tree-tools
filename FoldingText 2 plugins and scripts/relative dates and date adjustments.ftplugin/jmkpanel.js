/* ------------------------------------------------------------- *
 * Panel Module for FoldingText 2.0 Plugins
 * by Jamie Kowalski, github.com/jamiekowalski/foldingtext-extra
 *
 * Usage:
 *
 * var Panel = require('./panel.js').Panel;
 *
 * var panel = new Panel({
 *   className: String,
 *   placeholder: String,
 *   onReturn: Function,
 *   onEscape: Function,
 *   onTextChange: Function,
 *   addToDOM: Boolean    // add to DOM immediately? Default true
 * })
 *
 * ------------------------------------------------------------- */

define(function(require, exports, module) {
  'use strict';

	var Extensions = require('ft/core/extensions'),
    editor;          // this variable is assigned in the 'init' function below

  var p = function (opts) {  // Panel constructor; assigned to exports.Panel below

    // class properties
    var commonClassName = 'JKPanel',
      COMMAND_LEFT = 91,
      COMMAND_RIGHT = 93,
      RETURN = 13,     // TODO is Enter key a different code?
      ESC = 27,
      KEY_A = 65,
      KEY_Z = 90,
      debug = false,
      keysDown = {};

    // define default options
    this.options = {
      className: '',
      placeholder: 'enter text...',
      onReturn: function () {},
      onEscape: function () {},
      onTextChange: function () {},
      addToDOM: true
    }

    // copy options from argument
    for (var op in opts) {
      // TODO fails if undefined is changed!
      if ( this.options[op] !== undefined && typeof this.options[op] === typeof opts[op]) {
        this.options[op] = opts[op]
      }
    }

    this.isShown = false;
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

    // this.element = document.createElement('div');
    // this.input = document.createElement('input');

    // set panel attributes
    this.element.style.display = 'none';       // don't show panel at first
    this.element.className = commonClassName;

    this.input.setAttribute('type', 'text');
    this.input.setAttribute('value', '');
    this.input.setAttribute('placeholder', this.options.placeholder);
    if (this.options.className) {
      this.element.classList.add(this.options.className);
    }

    this.element.insertBefore(this.input); // add the input to the panel

    if (debug) console.log(this.input.value)

    this.input.addEventListener('blur', (function(event) {
      this.hide(true);    // close the panel, keep contents
    }).bind(this));

    this.input.addEventListener('keyup', (function(event) { // TODO how to get the panel instance inside here?
      if (debug) console.log(event.which)
      if (debug) console.log(keysDown)

      if (event.which === COMMAND_LEFT) {          // left command key
        keysDown[COMMAND_LEFT] = false;
      } else if (event.which === COMMAND_RIGHT) {  // right command key
        keysDown[COMMAND_RIGHT] = false;
      } else if (event.which === ESC) {            // escape key
        this.options.onEscape(this);
        return;
      }
      if (this.input.value.trim() === this.currentValue) {
        if (debug) console.log('No change');
        return;
      }
      this.currentValue = this.input.value.trim();

      this.options.onTextChange(this);

    }).bind(this))

    // capture paste from menu bar, etc.
    this.input.addEventListener('input', (function(event) {
      this.input.dispatchEvent(new CustomEvent('keyup'));
    }).bind(this));

    this.input.addEventListener('keydown', (function(event) {
      if (event.which === RETURN) {
        this.options.onReturn(this);
        this.input.dispatchEvent(new CustomEvent('blur'));
        event.preventDefault();
      }
      if (event.which === COMMAND_LEFT) {
        keysDown[COMMAND_LEFT] = true;
      } else if ( event.which === COMMAND_RIGHT ) {
        keysDown[COMMAND_RIGHT] = true;
      } else if ( event.which === ESC ) {
        event.preventDefault();
      } else if (keysDown[COMMAND_LEFT] || keysDown[COMMAND_RIGHT]) {
        // Modify behavior of some command combinations

        if ( event.which === KEY_A ) {
          this.input.select();
          event.preventDefault();
        } else if ( event.which === KEY_Z ) {
          event.preventDefault();
        }
      }
    }).bind(this));

    if (this.options.addToDOM) {
      document.body.insertBefore(this.element);
    }
  };

  p.prototype.addToDOM = function () {
    document.body.insertBefore(this.element);
  };
  p.prototype.show = function (strSeln) {
    this.element.style.display = 'block';
    this.input.select();  // select contents, and focus
    // optional strSelection added for modification of selected dates
    if (strSeln) {
      this.input.value = strSeln;
    }
    this.currentValue = this.input.value;
    this.isShown = true;
  };
  p.prototype.hide = function (keepContents) {
    if (! keepContents) {
      this.input.value = '';
    }
    this.currentValue = this.input.value;
    this.element.style.display = 'none';
    editor.focus();
    this.isShown = false;
  };
  p.prototype.toggle = function () {
    if (this.isShown) {
      this.hide();
    } else {
      this.show();
    }
  };
  p.prototype.clear = function () {
    this.input.value = '';
  };

  Extensions.add('com.foldingtext.editor.init', function(ed) {
    editor = ed;    // TODO This is a hack
  });

  exports.Panel = p;

});
