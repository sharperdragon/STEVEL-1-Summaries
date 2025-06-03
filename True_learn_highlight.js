// ==UserScript==
// @name         Right-click triggers Alt+H
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Converts right-click to Alt+H on a specific site
// @author       You
// @match        https://example.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    document.addEventListener('contextmenu', function(e) {
        e.preventDefault(); // Block native right-click menu

        // Create and dispatch the Alt+H keyboard event
        const altH = new KeyboardEvent('keydown', {
            key: 'h',
            code: 'KeyH',
            altKey: true,
            bubbles: true,
            cancelable: true
        });

        document.dispatchEvent(altH);
    });
})();