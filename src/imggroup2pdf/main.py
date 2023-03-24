
import sys
import os

from os.path import abspath, dirname, expanduser, join
from io import BytesIO

from rst2pdf.createpdf import (
    OptionParser,
    parse_commandline,
    add_extensions,
    RstToPdf)

DEFAULT_ENTRY: str="""
.. figure:: {}
    :width: 100%

.. raw:: pdf

    PageBreak

"""

def getPDF(images: list[str]) -> int:
    infile: BytesIO = BytesIO()

    for image in images:
        infile.write(DEFAULT_ENTRY.format(image).encode())

    style: str = '--stylesheet-path={}'.format(abspath(dirname(__file__)))

    parser: OptionParser = parse_commandline()
    options, args = parser.parse_args(['-s', 'none.yaml', style])

    options.basedir = os.getcwd()
    options.infile = infile
    options.compressed = False
    options.output = None
    options.outfile = sys.stdout.buffer

    options.fpath = []
    options.inline_footnotes = False

    ssheet = []
    if options.style:
        for l in options.style:
            ssheet += l.split(',')
    else:
        ssheet = []
    options.style = [x for x in ssheet if x]

    spath = []
    if options.stylepath:
        spath = options.stylepath.split(os.pathsep)
    options.stylepath = spath

    add_extensions(options)

    return RstToPdf(
        stylesheets=options.style,
        language=options.language,
        header=options.header,
        footer=options.footer,
        inlinelinks=options.inlinelinks,
        breaklevel=int(options.breaklevel),
        baseurl=options.baseurl,
        fit_mode=options.fit_mode,
        background_fit_mode=options.background_fit_mode,
        smarty=str(options.smarty),
        font_path=options.fpath,
        style_path=options.stylepath,
        repeat_table_rows=options.repeattablerows,
        footnote_backlinks=options.footnote_backlinks,
        inline_footnotes=options.inline_footnotes,
        real_footnotes=options.real_footnotes,
        def_dpi=int(options.def_dpi),
        basedir=options.basedir,
        show_frame=options.show_frame,
        splittables=options.splittables,
        blank_first_page=options.blank_first_page,
        first_page_on_right=options.first_page_on_right,
        breakside=options.breakside,
        custom_cover=options.custom_cover,
        floating_images=options.floating_images,
        numbered_links=options.numbered_links,
        raw_html=options.raw_html,
        section_header_depth=int(options.section_header_depth),
        strip_elements_with_classes=options.strip_elements_with_classes,
    ).createPdf(
        text=options.infile.getvalue().decode(),
        source_path="<stdin>",
        output=options.outfile,
        compressed=options.compressed,
    )
