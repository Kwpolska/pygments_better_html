Better line numbers for Pygments HTML
=====================================

This library provides improved line numbers for the Pygments HTML formatter. The `BetterHtmlFormatter` supports two styles:

* `linenos='table'` (the default) — every line of the code is a separate table row (a 2xN table, as opposed to Pygments’ standard 2x1 table) This improves the appearance if the code contains characters with unusual line-height, and allows for the code to be word-wrapped with the numbers kept in the right places.
* `linenos='ol'` — lines are `<li>` elements in an `<ol>` list.

Both styles allow for copy-pasting into a code editor. Directly copy-pasting into Microsoft Word (or similar) might produce something ugly. The first style is inspired by GitHub, and the second can be seen at pastebin.com.

Usage
=====

In most cases, it’s a drop-in replacement for `HtmlFormatter`. Just add the import:

    from pygments_better_html import BetterHtmlFormatter

and when calling `highlight()`, instead of `HtmlFormatter`, pass the `BetterHtmlFormatter` class:

    BetterHtmlFormatter(linenos="table", …other options…)
    BetterHtmlFormatter(linenos="ol", …other options…)

You can see a simple demo in `demo.py`.

Required CSS
------------

To make this work, you will need to add the following CSS:

```css
.highlight { white-space: pre-wrap; }
.highlight table, .highlight tr, .highlight td { border-spacing: 0; border-collapse: collapse; }
.highlight pre { white-space: pre-wrap; line-height: normal; }
.highlighttable td.linenos { vertical-align: top; padding-left: 10px; user-select: none; }
.highlighttable td.code { overflow-wrap: normal; border-collapse: collapse; }
.highlight .lineno.nonumber { list-style: none; }
```

If you’re using ``get_style_defs``, those will be included for you.

Known limitations
=================

* The `anchorlinenos` option is not supported for `linenos='ol'`.

License
=======

Copyright © 2020, Chris Warrick. Licensed under the 3-clause BSD license.

Many parts of the code are taken from Pygments’ original HTMLFormatter, which is copyright © 2006-2019 by the Pygments team, and is licensed under the 2-clause BSD license.
