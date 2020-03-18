# -*- coding: utf-8 -*-
"""Better HTML formatter for Pygments.

Copyright © 2020, Chris Warrick.
License: 3-clause BSD.
Portions copyright © 2006-2019, the Pygments authors. (2-clause BSD).
"""

__all__ = ["BetterHtmlFormatter"]
__version__ = '0.1.0'

import enum
import textwrap
import warnings

from pygments.formatters.html import HtmlFormatter


class BetterLinenos(enum.Enum):
    TABLE = "table"
    OL = "ol"


class BetterHtmlFormatter(HtmlFormatter):
    r"""
    Format tokens as HTML 4 ``<span>`` tags, with alternate formatting styles.

    * ``linenos = 'table'`` renders each line of code in a separate table row
    * ``linenos = 'ol'`` renders each line in a <li> element (inside <ol>)

    Both options allow word wrap and don't include line numbers when copying.
    """

    name = "HTML"
    aliases = ["html"]
    filenames = ["*.html", "*.htm"]

    def __init__(self, **options):
        """Initialize the formatter."""
        super().__init__(**options)
        self.linenos_name = self.options.get("linenos", "ol")
        self.linenos_val = BetterLinenos(self.linenos_name)
        self.linenos = 2 if self.linenos_val == BetterLinenos.OL else 1

    def get_style_defs(self, arg=None):
        """Generate CSS style definitions.

        Return CSS style definitions for the classes produced by the current
        highlighting style. ``arg`` can be a string or list of selectors to
        insert before the token type classes.
        """
        base = super().get_style_defs(arg)
        new_styles = textwrap.dedent(
            """\
            .%(cls)s { white-space: pre-wrap; }
            .%(cls)s table, .highlight tr, .highlight td { border-spacing: 0; border-collapse: collapse; }
            .%(cls)s pre { white-space: pre-wrap; line-height: normal; }
            .%(cls)stable td.linenos { vertical-align: top; padding-left: 10px; user-select: none; }
            .%(cls)stable td.code { overflow-wrap: normal; border-collapse: collapse; }
            .%(cls)s .lineno.nonumber { list-style: none; }"""
            % {"cls": self.cssclass}
        )
        return base + "\n" + new_styles

    def _wrap_tablelinenos(self, inner):
        lncount = 0
        codelines = []
        for t, line in inner:
            if t:
                lncount += 1
            codelines.append(line)

        fl = self.linenostart
        mw = len(str(lncount + fl - 1))
        sp = self.linenospecial
        st = self.linenostep
        la = self.lineanchors
        aln = self.anchorlinenos
        nocls = self.noclasses
        if sp:
            lines = []

            for i in range(fl, fl + lncount):
                if i % st == 0:
                    if i % sp == 0:
                        if aln:
                            lines.append('<a href="#%s-%d" class="special">%*d</a>' % (la, i, mw, i))
                        else:
                            lines.append('<span class="special">%*d</span>' % (mw, i))
                    else:
                        if aln:
                            lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                        else:
                            lines.append("%*d" % (mw, i))
                else:
                    lines.append("")
            ls = "\n".join(lines)
        else:
            lines = []
            for i in range(fl, fl + lncount):
                if i % st == 0:
                    if aln:
                        lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                    else:
                        lines.append("%*d" % (mw, i))
                else:
                    lines.append("")

        yield 0, '<div class="%s"><table class="%stable">' % (
            self.cssclass,
            self.cssclass,
        )
        for ln, cl in zip(lines, codelines):
            if nocls:
                yield 0, (
                    '<tr><td class="linenos linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><code>'
                    + ln
                    + '</code></td><td class="code"><code>'
                    + cl.rstrip("\n")
                    + "</code></td></tr>"
                )
            else:
                yield 0, (
                    '<tr><td class="linenos linenodiv"><code>'
                    + ln
                    + '</code></td><td class="code"><code>'
                    + cl.rstrip("\n")
                    + "</code></td></tr>"
                )
        yield 0, "</table></div>"

    def _wrap_inlinelinenos(self, inner):
        # Override with preferred method
        return self._wrap_ollineos(self, inner)

    def _wrap_ollinenos(self, inner):
        lines = inner
        sp = self.linenospecial
        st = self.linenostep or 1
        num = self.linenostart

        if self.anchorlinenos:
            warnings.warn("anchorlinenos is not supported for linenos='ol'.")

        yield 0, "<ol>"
        if self.noclasses:
            if sp:
                for t, line in lines:
                    if num % sp == 0:
                        style = "background-color: #ffffc0; padding: 0 5px 0 5px"
                    else:
                        style = "background-color: #f0f0f0; padding: 0 5px 0 5px"
                    if num % st != 0:
                        style += "; list-style: none"
                    yield 1, '<li style="%s" value="%s">' % (style, num,) + line + "</li>"
                    num += 1
            else:
                for t, line in lines:
                    yield 1, (
                        '<li style="background-color: #f0f0f0; padding: 0 5px 0 5px%s" value="%s">'
                        % (("; list-style: none" if num % st != 0 else ""), num)
                        + line
                        + "</li>"
                    )
                    num += 1
        elif sp:
            for t, line in lines:
                yield 1, '<li class="lineno%s%s" value="%s">' % (
                    " special" if num % sp == 0 else "",
                    " nonumber" if num % st != 0 else "",
                    num,
                ) + line + "</li>"
                num += 1
        else:
            for t, line in lines:
                yield 1, '<li class="lineno%s" value="%s">' % (
                    "" if num % st != 0 else " nonumber",
                    num,
                ) + line + "</li>"
                num += 1

        yield 0, "</ol>"

    def format_unencoded(self, tokensource, outfile):
        """Format code and write to outfile.

        The formatting process uses several nested generators; which of
        them are used is determined by the user's options.

        Each generator should take at least one argument, ``inner``,
        and wrap the pieces of text generated by this.

        Always yield 2-tuples: (code, text). If "code" is 1, the text
        is part of the original tokensource being highlighted, if it's
        0, the text is some piece of wrapping. This makes it possible to
        use several different wrappers that process the original source
        linewise, e.g. line number generators.
        """
        source = self._format_lines(tokensource)
        if self.hl_lines:
            source = self._highlight_lines(source)
        if not self.nowrap:
            if self.linenos_val == BetterLinenos.OL:
                source = self._wrap_ollinenos(source)
            if self.lineanchors:
                source = self._wrap_lineanchors(source)
            if self.linespans:
                source = self._wrap_linespans(source)
            if self.linenos_val == BetterLinenos.TABLE:
                source = self._wrap_tablelinenos(source)
            if self.linenos_val == BetterLinenos.OL:
                source = self.wrap(source, outfile)
            if self.full:
                source = self._wrap_full(source, outfile)

        for t, piece in source:
            outfile.write(piece)
