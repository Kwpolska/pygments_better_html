#!/usr/bin/env python3
"""Demo for BetterHTMLFormatter."""

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments_better_html import BetterHtmlFormatter

CODE = """\
class BetterHtmlFormatter(HtmlFormatter):
    name = "HTML"
    aliases = ["html"]
    filenames = ["*.html", "*.htm"]

    def __init__(self, **options):
        super().__init__(**options)
        self.linenos_name = self.options.get("linenos", "ol")
        self.linenos_val = BetterLinenos(self.linenos_name)
        self.linenos = 2 if self.linenos_val == BetterLinenos.OL else 1

    def get_style_defs(self, arg=None):
        base = super().get_style_defs(arg)
        new_styles = textwrap.dedent(""\"💩
    This is an absurdly long line that should trigger the word wrap mechanism in any reasonably-sized web browser window. I think I should fill this line with Lorem ipsum, since I probably won’t be able to type out coherent text that also matches my fairly unusual requirement, but honestly, it wraps at least on my machine, so resize your browser and call it a day.
\t\tAnd this line is indented with two tab characters.
    ""\")

print("Hello, world!")
"""

for linenos, anchorlinenos in (("table", True), ("ol", False)):
    with open("demo-output-" + linenos + ".html", "w") as fh:
        fh.write(
            highlight(
                CODE,
                HtmlLexer(),
                BetterHtmlFormatter(
                    linenos=linenos,  # "table" or "ol"
                    full=True,
                    hl_lines=[1, 3, 10],
                    linenostart=55,
                    linenostep=2,
                    lineanchors="x",
                    linenospecial=3,  # no CSS for this by default
                    anchorlinenos=anchorlinenos,  # table only
                ),
            )
        )
