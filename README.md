Better line numbers for Pygments HTML
=====================================

This library provides improved line numbers for the Pygments HTML formatter. The `BetterHtmlFormatter` supports two styles:

* `linenos="table"` (the default) — every line of the code is a separate table row (a 2xN table, as opposed to Pygments’ standard 2x1 table) This improves the appearance if the code contains characters with unusual line-height, and allows for the code to be word-wrapped with the numbers kept in the right places.
* `linenos="ol"` — lines are `<li>` elements in an `<ol>` list.

Both styles allow for copy-pasting into a code editor. Directly copy-pasting into Microsoft Word (or similar) might produce something ugly. The first style is inspired by GitHub, and the second can be seen at pastebin.com.

The `table` style is more flexible and looks better. The `ol` style is slightly more compatible with broken browsers and minifiers. Pick whichever one works best for you.

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
.highlight table, .highlight tr, .highlight td { border-spacing: 0; border-collapse: separate; padding: 0 }
.highlight pre { white-space: pre-wrap; line-height: normal }
.highlighttable td.linenos { vertical-align: top; padding-left: 10px; padding-right: 10px; user-select: none; -webkit-user-select: none }
.highlighttable td.linenos code:before { content: attr(data-line-number) }
.highlighttable td.code { overflow-wrap: normal; border-collapse: collapse }
.highlighttable td.code code { overflow: unset; border: none; padding: 0; margin: 0; white-space: pre-wrap; line-height: unset; background: none }
.highlight .lineno.nonumber { list-style: none }
```

If you’re using ``get_style_defs``, those will be included for you.

Browser support
===============

All reasonably modern versions of reasonable browsers are supported. Internet Explorer is neither, so it isn’t supported. Firefox, Chrome and Safari are supported. Either mode works with these browsers, although I’ve seen Firefox add extra spaces to the front of lines randomly, and Safari requires an ugly hack for the table mode.

Known limitations
=================

1. The `anchorlinenos` option is not supported for `linenos="ol"`.
2. Third-party minifier tools may destroy your indentation if you use tabs. Spaces use a work-around, described in the following point.
3. Because of overly clever HTML minifiers, `&nbsp;` tags are used for indentation and sequences of whitespace longer than one character. This might break in the event web browsers decide to copy non-breaking spaces as non-breaking instead of regular spaces. Currently, browsers do the right thing on all platforms. It might also lead to degraded apperance in some edge cases (indentation longer than the code box width, or long runs of spaces inside the code).
4. Some completely broken HTML minifiers will remove line numbers, because they are empty tags (that’s the only way to make Safari ignore them on copy-paste). Removing empty tags is just wrong, considering how many browser hacks were built on top of these throughout the years. I saw this issue with HTML Tidy, which is an antique tool detached from reality (even in the HTML5 fork).

If you care about compatiblity with bad tools or unusual scenarios, and don’t mind losing `anchorlinenos`, consider using the `lineos="ol"` mode instead of `lineos="table"`.

Browsers vs code vs minifiers
-----------------------------

Limitations (3) and (4) might be considered bugs in my code and not the minifiers. But note that browsers don’t ignore whitespace when parsing, and although the default `white-space: normal` setting for most tags collapses them, you can use `white-space: pre` or `white-space: pre-wrap` to display them. Those minifiers don’t take the CSS into account, and assume the default behavior, collapsing spaces outside of `<pre>` tags. Which is wrong if you override `white-space` on other elements, and “wasteful” if you do `pre { white-space: normal }` for some unusual reason (yeah, don’t do that.)

Collapsing whitespace could be worked around with a `<pre>` tag around each line of code, but Firefox will add extra newlines when copying (so the actual code is on every other line of the copied text). This is not avoidable and hard-coded (the plaintext conversion does not look at CSS either, and has a special case for `<pre>` since it makes sense for normal use of that tag. And you can’t wrap the entire table in a `<pre>` tag. If I added one, browsers would move it outside of the table to make the HTML valid. But if browsers do that, some of those clever minifiers might fix HTML syntax as well.

I decided to use a different solution, and work around these tools, by using non-breaking spaces for longer runs of spaces. This depends on web browsers replacing those with regular spaces when copying. Luckily, all browsers do this, and considering a 2008 4chan meme (“can’t triforce”, search results might be NSFW), that’s been a thing since forever and is not likely to change.

The selected solution of replacing runs of spaces with non-breaking spaces can lead to the code overflowing the box/adding a horizontal scrollbar. Those will happen only in very specific edge cases, i.e. very narrow windows + very large fonts + large indents + no regular (single) spaces close to the indent.

I also decided not to apply it to tabs (\t, ^I, U+0009 HORIZONTAL TAB), because tab width can be random, and tabs move the caret to a place, not by a set amount (so in `"a\tb"` and `"aa\tb"`, the `"b"` appears in the same place on the line). Which is generally difficult to handle properly, and you should be using spaces to indent your code anyway.

You should also note that GitHub uses both of these techniques, and BitBucket uses the first one. And that it’s easier for everyone to find a better tool if their current tool does stupid stuff.

License
=======

Copyright © 2020-2023, Chris Warrick. Licensed under the 3-clause BSD license.

Many parts of the code are taken from Pygments’ original HTMLFormatter, which is copyright © 2006-2022 by the Pygments team, and is licensed under the 2-clause BSD license.
