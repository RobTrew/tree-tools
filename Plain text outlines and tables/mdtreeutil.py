#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Pretty-prints MMD tables (included nested/spanning tables),
    or translates in any direction between 3 formats of tabular or nested text.
    1. Parses text as a MMD Table, CSV (excel_tab) lines , or Outline MD/tabbed
    2. writes it to CLIPBOARD or STDOUT (OSX or iOS)
        as a pretty-printed MMD table, CSV rows, or Outline.
    (various sub-options for each format)
"""

SCRIPT_NAME = 'mdtreeutil.py'
DESCRIPTION = 'Prettyprints or converts between MMD tables, \
                            plain text outlines (Markdown / tabbed), and CSV.'
AUTHOR = 'Rob Trew'
VER = '.097'
LICENSE = """Copyright (c) 2013 Robin Trew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

SCRIPT_OPTIONS = """
usage: mdtreeutil.py [-h] [-v] [-stdin] [-stdout] [-tgt {mmdtable,outline,csv}]
                  [-src {mmdtable,outline,csv}] [-pp {mono,mmc_tabs}]
                  [-hl {0,1,2,3,4,5,6}] [-b {-,*,+,none}] [-dlm DELIMITER]
                  [-q {all,nonnumeric,none,excel_tab}]

Prettyprints or converts between MMD tables, plain text outlines (Markdown /
tabbed), and CSV.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -stdin                specify that input should be read from stdin rather
                        than from the clipboard.
  -stdout               specify that output should go to stdout rather than
                        the clipboard
  -tgt {mmdtable,outline,csv}, --targetformat {mmdtable,outline,csv}
                        convert the text to the indicated format and write
                        back to the clipboard or to stdout. Default is
                        mmdtable.
  -src {mmdtable,outline,csv}, --sourceformat {mmdtable,outline,csv}
                        force input text to be interpreted using the indicated
                        format (by default, the text's format will be
                        determined from its contents).
  -pp {mono,mmc_tabs}, --prettyprint {mono,mmc_tabs}
                        choose between monospaced pretty-printing (default)
                        and MMD Composer elastic tab format for MMD tables
  -hl {0,1,2,3,4,5,6}, --hashlevels {0,1,2,3,4,5,6}
                        maximum number of heading hashes for MD outlines.
                        Further outline levels will be tab-indented lists.
                        Specify 0 for plain tabbed outlines.
  -b {-,*,+,none}, --bullet {-,*,+,none}
                        bullet character to use for indented outline lists
                        beyond any maximum hash header level. By default, no
                        bullet will be used if --hashlevels is set to 0.
  -dlm DELIMITER, --delimiter DELIMITER
                        delimiter string to use for CSV. CSV output defaults
                        are csv.excel_tab
  -q {all,nonnumeric,none,excel_tab}, --csvquote {all,nonnumeric,none,excel_tab}
                        quoting pattern for CSV output. CSV output defaults
                        are csv.excel_tab
"""

# FUNCTION
# 1. reads [MMD table / outline / CSV] text in the OSX or iOS clipboard or STDIN
# 2. translates the input to one of 3 formats, with some options

# TYPICAL APPLICATIONS
# 1. Pretty-printing & completing existing MMD tables, preserving any spanning,
# 2. converting between different format of plain text outline,
# 3. copying and pasting in either direction between spreadsheets & MMD tables,
# 4. converting between outline and tabular representations of text nesting.

#  2 options for MMD table (nested/flat) pretty-printing:
## monospaced font MultiMarkdown tables (with text alignments)
## tabbed pretty-printing for MultiMarkdown Composer's elastic tabs.

# TEXT FORMATS THAT CAN BE DETECTED AND PARSED:

# 1. CSV dialects recognised by the Python csv module (for spreadsheet copying)
# 2. Outlines: tab-indented, Markdown/FT (heading levels &  list indentations)
# 3. MMD tables (flat or nested/spanning)

# OUTPUT FORMATS

# 1. CSV (defaults to tab-delimited, for pasting into spreadsheets)
# 2. OUTLINES (defaults to one level of hash heading, then indented lists)
# 3. MMD tables (flat or nested) (defaults to monospaced pretty-printing)

# COMMAND LINE OPTIONS

# SOME LIMITATIONS OF THIS EARLY DRAFT
# Doesn't look for MMD tables within other material
# (assumes the clipboard only contains a single table)

# Handles top down spanning (parent spans children),
# but performs an opinionated normalisation of any children which
# attempt to span parents.
# (Doesn't attempt to parse any cyclic graphs in which
# descendant branches rejoin).


import sys, argparse
import re
from textwrap import dedent
import csv
from StringIO import StringIO

FMT_MMD_TBL = 'mmdtable'
FMT_OUTLN = 'outline'
FMT_CSV = 'csv'

#######################

TBL_MMD_MONO = 'mono'
TBL_MMD_TABBED = 'mmc_tabs'

CSVDialect = csv.excel_tab

CSV_DELIMITER = csv.excel_tab.delimiter
CSV_QUOTING = csv.excel_tab.quoting
CSV_LINE_TERMINATOR = '\n'

# RULER COLONS none/left/centre/right – binary: 00, 10 , 11 , 01

TBL_ALIGN_NONE = 0
TBL_ALIGN_RIGHT = 1
TBL_ALIGN_LEFT = 2
TBL_ALIGN_MID = 3
TBL_ALIGN_DEFAULT = TBL_ALIGN_MID

TBL_ALIGN_DEFAULTS = [TBL_ALIGN_DEFAULT]
TBL_ALIGN_CHARS = ['', ':', ':']

# Ruler row: -1: no ruler, 0:above top data, 1:below top line,
# 2: below second line, 3: etc

TBL_RULER_ROW = 1
TBL_MARGIN_CHARS = 1

OUTLN_SPACED_HEADINGS = True

ESC_PIPE = '&#124;'

def main():
    """ 1. GET OPTIONS & ANY TEXT,
        2. PARSE THE TEXT TO A TREE,
        3. TRANSLATE THE PARSE TREE TO THE CHOSEN STRING FORMAT,
        4. and WRITE THE TRANSLATION TO CLIPBOARD OR STDOUT.
    """

    # 1. GET OPTIONS & ANY TEXT,
    ns_args = _get_args()

    # in case we are using the clipboard,
    # record any identification of the platform
    if ns_args.stdin:
        str_src = '\n'.join(sys.stdin.readlines())
        var_ios = None
    else:
        dct_clip = _get_clip()
        str_src = dct_clip['text']
        var_ios = dct_clip['ios']

    if str_src == '':
        return

    # 2. PARSE THE TEXT TO A TREE,

    dct_parse = _get_parse(str_src, ns_args)
    if dct_parse == None:
        print 'could not be parsed as ' + ns_args.sourceformat
        return

    # 3.  TRANSLATE THE PARSE TREE TO THE CHOSEN STRING FORMAT,

    str_tgt_format = ns_args.targetformat
    bln_mono = (ns_args.prettyprint != TBL_MMD_TABBED)
    if str_tgt_format == FMT_OUTLN:
        str_new = write_outline(dct_parse, ns_args.hashlevels,
                                ns_args.bullet, OUTLN_SPACED_HEADINGS)
    elif str_tgt_format != FMT_CSV:
        str_new = write_table(dct_parse, True, TBL_MARGIN_CHARS,
                              bln_mono)
    else:
        str_new = write_table(dct_parse, False, TBL_MARGIN_CHARS,
                              bln_mono)

    # 4. and WRITE TRANSLATION TO CLIPBOARD OR STDOUT.

    if ns_args.stdout:
        print str_new
    else:
        _set_clip(str_new, var_ios)

    # end of main()



def _get_args():
    """Return an argument parse object from the command line"""

    o_parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
        description=DESCRIPTION,
        version=VER)

    # From and to CLIPBOARD [default] or STDIO ?
    o_parser.add_argument('-stdin', action='store_true',
        help='specify that input should be read from stdin '
            'rather than from the clipboard.')
    o_parser.add_argument('-stdout', action='store_true',
         help='specify that output should go to stdout '
            'rather than the clipboard')

    # Source and target FORMATS (TABLE/CSV/OUTLINE)

    tpl_formats = (FMT_MMD_TBL, FMT_OUTLN, FMT_CSV)
    str_default = tpl_formats[0]
    o_parser.add_argument('-tgt', '--targetformat', choices=tpl_formats,
         help='convert the text to the indicated format and '
            'write back to the clipboard or to stdout. '
            'Default is ' + str_default + '.',
            default=str_default)
    o_parser.add_argument('-src', '--sourceformat', choices=tpl_formats,
         help='force input text to be interpreted using '
            'the indicated format (by default, the text\'s '
            'format will be determined from its contents).',
            default=None)

    # MMD table format options (monospace,  or for MC elastic tabs)
    lst_prettyprint = [TBL_MMD_MONO, TBL_MMD_TABBED]
    o_parser.add_argument('-pp', '--prettyprint', choices=lst_prettyprint,
         help='choose between monospaced pretty-printing (default) '
                'and MMD Composer elastic tab format for MMD tables',
            default=lst_prettyprint[0])

    # OUTLINE (output) format options
    o_parser.add_argument('-hl', '--hashlevels', choices=range(7),
         help='maximum number of heading hashes for MD outlines. '
            'Further outline levels will be tab-indented lists. '
            'Specify 0 for plain tabbed outlines.',
            type=int, default=1)
    o_parser.add_argument('-b', '--bullet',
        choices=['-', '*', '+', 'none'],
         help='bullet character to use for indented outline lists '
            'beyond any maximum hash header level. '
            'By default, no bullet will be used if --hashlevels is set to 0.',
             default='-')

    # CSV (output) format options
    o_parser.add_argument('-dlm', '--delimiter',
         help='delimiter string  to use for CSV. '
         'CSV output defaults are csv.excel_tab',
             default='\t')
    o_parser.add_argument('-q', '--csvquote',
         help='quoting pattern for CSV output. '
        'CSV output defaults are csv.excel_tab',
             choices=['excel_tab', 'all', 'nonnumeric', 'none'],
            default='excel_tab')

    return o_parser.parse_args()

def _get_parse(str_src, ns_args):
    """Return {'tree':, 'rulerrow':, 'alignments':} parse
        from text and ArgParse options
    """
    if ns_args.sourceformat != None:
        e_fmt = ns_args.sourceformat
        if e_fmt == FMT_CSV:
            try:
                o_dialect = csv.Sniffer().sniff(str_src)
            except csv.Error:
                return None
    else:
        (e_fmt, o_dialect) = _format_triage(str_src)

    # dct_tree keys are {'tree':, 'rulerrow':, 'alignments':}
    if e_fmt == FMT_CSV:
        if re.match(r'\w', o_dialect.delimiter) != None:
            dct_parse = read_mmd_table(str_src)
        else:
            dct_parse = read_csv(str_src, o_dialect)
    elif e_fmt == FMT_OUTLN:
        dct_parse = read_outline(str_src)
    else:
        dct_parse = read_mmd_table(str_src)

    return dct_parse


def _get_clip():
    """ Return the clipboard text, & whether the platform is iOS
    """
    # which platform - OSX or iOS ?
    try:
        import clipboard
        var_ios = True
    except ImportError:
        import subprocess
        var_ios = False

    # read the clipboard ...
    if var_ios:
        str_src = clipboard.get()
    else:
        proc = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        proc.wait()
        str_src = proc.stdout.read()

    return {'text':str_src, 'ios':var_ios}

def _set_clip(str_text, var_ios):
    """Place text in the OSX or iOS clipboard"""

    # If the platform is already known ...
    if var_ios != None:
        bln_ios = var_ios
    else: # otherwise check the platform,
        try:
            import clipboard
            bln_ios = True
        except ImportError:
            import subprocess
            bln_ios = False

    # and set the clipboard accordingly
    if bln_ios:
        import clipboard
        clipboard.set(str_text)
    else:
        import subprocess
        proc = subprocess.Popen(['pbcopy'],
                stdin=subprocess.PIPE)
        proc.stdin.write(str_text)
        proc.stdin.close()
        proc.wait()


def _format_triage(str_txt):
    """CSV dialect ? Outline ?
        (otherwise treat as aspirant or actual MMD table)
    """

    def _tbl_or_outln(str_txt):
        """Unless it looks like an outline, treat it as a table"""

        rgx_outline = \
            re.compile(r'^(\t|\ {4})'
                    r'|^(\s*)(\d\.'
                    r'|[\-\*\+])\s|^\#+\s+'
                       , re.MULTILINE)
        if rgx_outline.search(str_txt) != None:

            return (FMT_OUTLN, None)
        else:

            return (FMT_MMD_TBL, None)

    # MAIN CODE of _format_triage

    try:
        dialect = csv.Sniffer().sniff(str_txt)
        str_delim = dialect.delimiter

        if str_delim != '\t':
            if (str_delim not in ['|', ' ', '-']) and not str_delim.isalpha():
                return (FMT_CSV, dialect)
            else:
                return _tbl_or_outln(str_txt)
        else:

            # Assume TSV unless there are tabs are followed by pipes
            # or we can see an MMD table ruler

            rgx_tab_pipe = re.compile(r'\t\|', re.MULTILINE)
            rgx_ruler = \
                re.compile(r'^[\|\-\+\:\.]'
                r'[ \t\-\+\|\:\.]*?\|*'
                r'[ \t\-\+\|\:\.]*$'
                           , re.MULTILINE)
            if rgx_tab_pipe.search(str_txt) != None \
                or rgx_ruler.search(str_txt) != None:
                return (FMT_MMD_TBL, None)
            else:
                return (FMT_CSV, dialect)

    except csv.Error:

        return _tbl_or_outln(str_txt)


# MMD TABLE READER

# --> tree of nested cells, list of col alignments, & index of ruler row
# e.g.  lst_tree, lst_align, i_ruler_row = parse_mmd_table(STR_MMD)

def read_mmd_table(str_src):
    """ Parse text to three elements:
        1. tree of nested cells,
        2. index of ruler row,
        3. list of col alignments

        {'tree': lst_tree,
        'rulerrow': i_ruler_row,
        'alignments': lst_align}
    """

    rgx_ruler_part = re.compile(r'^[\:\-. \t]+$')

    def _get_align(str_text):
        """ Interpret alignment colons in MMD ruler segment
        """
        if rgx_ruler_part.match(str_text) != None:
            if str_text[0] != ':':
                if str_text[-1] != ':':
                    return TBL_ALIGN_NONE
                else:
                    return TBL_ALIGN_RIGHT
            else:
                if str_text[-1] != ':':
                    return TBL_ALIGN_LEFT
                else:
                    return TBL_ALIGN_MID
        else:
            return None

    def _rows_to_tree(lst_table):
        """ Translate a list of row lists to a tree of cells
        """

        id_cell = 0
        lst_tree = [{
            'id': id_cell,
            'parent': None,
            'level': 0,
            'text': '',
            'chiln': [],
            }]

        # first add index ids to the table

        id_cell += 1
        for i_row in range(len(lst_table)):
            lst_row = lst_table[i_row]
            lst_table[i_row] = [(id_cell + i, str_text, lng_leaves)
                                for (i, (str_text, lng_leaves)) in
                                enumerate(lst_row)]
            id_cell += len(lst_row)

        # then create a list of tree nodes using these indices

        for (i_row, lst_row) in enumerate(lst_table):
            lst_level = i_row + 1
            for (id_cell, str_text, lng_leaves) in lst_row:
                lst_tree.append({
                    'id': id_cell,
                    'level': lst_level,
                    'text': str_text,
                    'chiln': [],
                    })

        # bottom up, add each node to the child id list of its parent

        for i_row in reversed(range(1, len(lst_table))):
            lst_parents = lst_table[i_row - 1]
            lng_parents = len(lst_parents)
            lst_chiln = lst_table[i_row]

            i_parent = 0
            (id_parent, _, lng_p_leaves) = lst_parents[i_parent]
            lng_leaves_used = 0
            dct_parent = lst_tree[id_parent]
            lst_level = i_row + 1

            for (id_child, _, lng_c_leaves) in lst_chiln:
                dct_parent['chiln'].append(id_child)
                dct_node = lst_tree[id_child]
                dct_node['parent'] = id_parent
                dct_node['level'] = lst_level
                lng_leaves_used += lng_c_leaves

                # if the parental leaf quota is full, move on to the next parent

                if lng_leaves_used >= lng_p_leaves:
                    i_parent += 1
                    if i_parent < lng_parents:
                        (id_parent, _, lng_p_leaves) = \
                            lst_parents[i_parent]
                        dct_parent = lst_tree[id_parent]
                        lng_leaves_used = 0

        # finally, treat level 1 nodes as children of the virtual root

        dct_root = lst_tree[0]
        for id_child in [tpl[0] for tpl in lst_table[0]]:
            dct_root['chiln'].append(id_child)
            lst_tree[id_child]['parent'] = 0

        return lst_tree

    # MAIN CODE of read_mmd_table
    # segment at two levels: line and pipe

    lst_split = [l.split('|') for l in [l.strip() for l in
                 str_src.splitlines() if l != '']]

    # get lines as lists of (text, leafwidth) tuples

    lst_all = []
    for lst_line in lst_split:
        (lst_parse, str_word, lng_leaves) = ([], '', 0)

        # nodes are 1 leaf wide unless followed by non-segmenting pipes
        # except at end

        if lst_line[-1] == '':
            lst_line = lst_line[:-1]
        for str_token in lst_line:
            if str_token != '':
                if str_word != '':
                    lst_parse.append((str_word.strip(), lng_leaves))
                (str_word, lng_leaves) = (str_token.strip(), 1)
                if str_word == '':
                    str_word = ' '  # distinguish gap from span
            else:
                lng_leaves += 1

        lst_parse.append((str_word.strip(), lng_leaves))
        lst_all.append(lst_parse)

    # find, parse and extract any ruler line

    lng_lines = len(lst_all)
    bln_found = False
    if lng_lines > 0:
        for i_ruler_row in range(0, lng_lines):
            lst_align = []
            for (str_text, lng_leaves) in lst_all[i_ruler_row]:

                var_result = _get_align(str_text)

                if var_result != None:
                    bln_found = True
                    lst_align.append(var_result)
                else:
                    lst_align = []  # this is not the line we're looking for
                    break
            if lst_align != []:
                del lst_all[i_ruler_row]  # ruler parsed - clear the decks
                break

        if not bln_found:
            if lng_lines > 1:
                i_ruler_row = TBL_RULER_ROW
            else:
                i_ruler_row = 0

        lst_tree = _rows_to_tree(lst_all)
        var_result = {'tree': lst_tree, 'rulerrow': i_ruler_row,
                'alignments': lst_align}
    else:
        var_result = None

    # read_mmd_table() returns
    return var_result


# END OF MMD TABLE READER

# TABLE WRITER

def write_table(
    dct_tree,
    bln_MMD,
    lng_margin,
    bln_monofont,
    ):
    """ Write out the data tree in some tabular format:
        either in one of two flavours of MultiMarkdown table
        prettyprinting (1. monospaced fonts 2. elastic tabbing),
        or in a CSV dialect (defaults to csv.excel-tab).
    """

    def _measure_tree(i_root, lng_margin):
        """ Flag each node with its leaf width,
            and its character width,
            ensuring that parents are as wide
            as their child ranges, and vice versa
        """

        # How wide is the text of the current node ?

        dct_root = lst_nodes[i_root]
        lng_chars = len(dct_root['text'])

        # and how many children does it have ?

        lst_chiln_ids = dct_root['chiln']
        lng_chiln = len(lst_chiln_ids)

        # what is its leafwidth in nodes, and childspan width in characters ?

        lng_chiln_chars = 0
        if lng_chiln < 1:
            lng_leaves = 1
        else:
            lng_leaves = 0
            for i_child_id in lst_chiln_ids:
                (lng_leaf_count, lng_char_count) = \
                    _measure_tree(i_child_id, lng_margin)
                lng_leaves += lng_leaf_count
                lng_chiln_chars += lng_char_count

        # what is the node's own width ?
        # (text including spaces and span pipe(s),
        # or child range, whichever is larger)
        # (note - the span pipe count is the terminal leaf count)

        lng_width = max(lng_chars + (lng_margin * 2) + lng_leaves,
                        lng_chiln_chars)

        # record the measurements in the node itself

        dct_root.update([('width', lng_width), ('leaves', lng_leaves),
                        ('chilnwidth', lng_chiln_chars)])

        # _measure_tree() returns the subset needed for recursion

        return (lng_leaves, lng_width)

    def _pad_tree(i_root, lng_space):
        """ Add width to ensure that child ranges
            are as big as their parents
        """

        def _share_list(lng_spaces, lng_chiln):
            """ Integer division of spaces between N child nodes
            """

            (lng_div, lng_mod) = (lng_spaces / lng_chiln, lng_spaces
                                  % lng_chiln)
            return [(lng_div + 1 if i < lng_mod else lng_div) for i in
                    xrange(lng_chiln)]

        # MAIN CODE of pad_tree()

        dct_root = lst_nodes[i_root]

        # is there any space to allocate top+down- ?

        if lng_space > 0:
            dct_root['width'] += lng_space

        # does this node have any children ?

        lst_chiln_ids = dct_root['chiln']
        lng_chiln = len(lst_chiln_ids)
        if lng_chiln > 0:

            # is there a gap to be padded ?

            lng_gap = dct_root['width'] - dct_root['chilnwidth']

            if lng_gap > 0:
                lst_space_shares = _share_list(lng_gap, lng_chiln)
                for (i_id, lng_share) in zip(lst_chiln_ids,
                        lst_space_shares):
                    _pad_tree(i_id, lng_share)
            else:
                for i_id in lst_chiln_ids:
                    _pad_tree(i_id, 0)

        # pad_tree() returns

        return 0

    def _col_widths(i_root):
        """ A list of the widths (in characters)
            of each column in the tree/table.
        """

        dct_node = lst_nodes[i_root]

        if dct_node['leaves'] < 2:
            return [dct_node['width']]

        # otherwise, get a list of column widths for each child,

        lst_widths = []
        for i_child_id in dct_node['chiln']:
            lst_widths += _col_widths(i_child_id)

        # _col_widths() returns

        return lst_widths

    def _get_tree_rows():
        """ A tabular representation of the tree in lst_nodes
            (in which shallow tree leaves have empty descendants
            down to the full tabular dept)
        """

        def _extend_depth(lng_depth):
            """ Extend descendants of any shallow leaves to full depth
                matching the width of the node they descend from
            """

            # find leaves which are shallower than lng_rows

            lst_leaves = [dct for dct in lst_nodes if len(dct['chiln'])
                          == 0 and dct['level'] < lng_depth]
            for dct_node in lst_leaves:

                # extend leaf descendants to the reqired depth,
                # giving them single spaces as texts

                lst_level = dct_node['level']
                while lst_level < lng_depth:
                    lst_level += 1
                    id_next = len(lst_nodes)
                    lst_nodes.append({
                        'id': id_next,
                        'text': '',
                        'chiln': [],
                        'level': lst_level,
                        'width': dct_node['width'],
                        'leaves': 1,
                        })
                    dct_node['chiln'].append(id_next)
                    dct_node = lst_nodes[id_next]

            # _extend_depth returns

            return 0

        def _fill_tree_rows(i_node):
            """ Recurse through tree appending each node id
                to the appropriate row list
            """

            dct_node = lst_nodes[i_node]
            lst_chiln = dct_node['chiln']
            if lst_chiln != []:
                lst_rows[dct_node['level']] += lst_chiln
                for i_child in lst_chiln:
                    _fill_tree_rows(i_child)

            # _fill_tree_rows returns

            return 0

        # MAIN CODE of _get_tree_rows() begins

        lng_rows = max([dct_node['level'] for dct_node in lst_nodes])
        _extend_depth(lng_rows)

        lst_rows = [[] for _ in xrange(lng_rows)]
        _fill_tree_rows(0)

        # _get_tree_rows() returns

        return (lng_rows, lst_rows)

    def _align_cell(
        str_text,
        lng_chars,
        lng_margin,
        e_align,
        ):
        '''Align text left/right/center within allocated space'''

        lng_txt_chars = lng_chars - lng_margin * 2
        str_mgn = r" " * lng_margin
        if e_align & TBL_ALIGN_RIGHT:
            if e_align & TBL_ALIGN_LEFT:
                str_al = str_text.center(lng_txt_chars)
            else:
                str_al = str_text.rjust(lng_txt_chars)
        else:
            str_al = str_text.ljust(lng_txt_chars)

        # _align_cell() returns

        return str_mgn + str_al + str_mgn

    def _mk_mmd_table(lng_margin, bln_monofont):
        """ Assemble the rows (and any ruler)
            of a multimarkdown table, as a
            list of MMD-formatted lines
        """

        def _mk_mmd_rows(lng_margin, lst_align):
            """ make a list of mmd-formatted row strings
                (excluding any ruler)
            """

            # MAIN CODE OF _mk_mmd_rows begins
            # get a tabular representation of the tree

            (lng_rows, lst_rows) = _get_tree_rows()

            lst_lines = []
            for i_row in xrange(lng_rows):
                str_row = '|'

                lng_col = 0
                for dct_cell in [lst_nodes[id_cell] for id_cell in
                                 lst_rows[i_row]]:
                    lng_leaves = dct_cell['leaves']
                    lng_space = dct_cell['width'] - lng_leaves
                    if bln_monofont:
                        str_row = ''.join([str_row,
                                _align_cell(dct_cell['text'],
                                lng_space, lng_margin,
                                lst_align[lng_col]), lng_leaves * '|'])
                    else:
                        str_row = ''.join([str_row, ' ', dct_cell['text'
                                ], lng_leaves * '\t', lng_leaves * '|'])

                    lng_col += lng_leaves

                # append two trailling space for better MD viewer compatibility

                lst_lines.append(''.join([str_row, '  \n']))

            # mk_mmd_rows() returns

            return lst_lines

        def _mmd_ruler(lst_col_spec):
            """ The MMD ruler string for a list of widths & alignments
            """

            def _mmd_ruler_part(lng_chars, e_align):
                """ Read any left and/or right colons from bits of e_align
                """

                str_left = TBL_ALIGN_CHARS[e_align & TBL_ALIGN_LEFT]
                str_right = TBL_ALIGN_CHARS[e_align & TBL_ALIGN_RIGHT]
                lng_colons = len(str_left + str_right)
                if bln_monofont:
                    return ''.join([str_left, '-' * max(lng_chars
                                   - lng_colons, 0), str_right, '|'])
                else:
                    return ''.join([str_left, '-' * max(lng_chars
                                   - lng_colons, 0), str_right, '\t|'])

            # MAIN CODE OF _mmd_ruler()

            return '|' + ''.join([_mmd_ruler_part(lng_chars - 1,
                                 lng_align) for (lng_chars,
                                 lng_align) in lst_col_spec]) + '  \n'

        # MAIN CODE of _mk_mmd_table begins

        _measure_tree(i_root, lng_margin)
        _pad_tree(i_root, 0)
        lst_col_widths = _col_widths(i_root)

        # get an alignments list which is the same length as the columns list
        # truncating or duplicating the last value as necessary

        lst_align = dct_tree['alignments']  # length may not match column count

        # ensure that there is at least one member of the list

        if lst_align == []:
            lst_align = TBL_ALIGN_DEFAULTS

        # make sure that the length of the alignments list
        # matches the column count

        (lng_cols, lng_align) = (len(lst_col_widths), len(lst_align))
        lng_gap = lng_cols - lng_align
        if lng_gap != 0:
            if lng_gap > 0:

                # pad the align list out with duplicates of its last member

                lst_align += [lst_align[-1] for _ in xrange(lng_gap)]
            else:

                # truncate the align list to the number of columns

                del lst_align[lng_cols:]

        lst_col_spec = zip(lst_col_widths, lst_align)
        lst_rows = _mk_mmd_rows(lng_margin, lst_align)

        # build a new ruler, if required

        str_ruler = _mmd_ruler(lst_col_spec)
        lng_ruler = dct_tree['rulerrow']
        if lng_ruler >= 0:

            # install it in the specified row

            lst_rows.insert(dct_tree['rulerrow'], str_ruler)

        # _mk_mmd_table() returns

        return lst_rows

    # MAIN CODE of write_table

    lst_nodes = dct_tree['tree']
    i_root = 0

    if bln_MMD:

        # translate the tree to a MultiMarkdown table
        # with pretty-printing (of spanning cols etc)
        # either for monospaced fonts
        # or for MultiMarkdown Composer's style of elastic tabbing.

        lst_rows = _mk_mmd_table(lng_margin, bln_monofont)
        str_table = ''.join(lst_rows)
    else:

          # CSV
        # Prepare the tabular model of the tree,

        _measure_tree(i_root, 0)
        _, lst_table = _get_tree_rows()

        lst_matrix = []
        for row in lst_table:
            lst_spans = [[dct['text']] + [''] * (dct['leaves'] - 1)
                         for dct in [lst_nodes[i] for i in row]]
            lst_matrix.append([cell for lst_group in lst_spans
                              for cell in lst_group])

        # and write it out to a CSV string

        o_string = StringIO()
        o_writer = csv.writer(o_string, dialect=CSVDialect,
                              delimiter=CSV_DELIMITER,
                              quoting=CSV_QUOTING,
                              lineterminator=CSV_LINE_TERMINATOR)
        o_writer.writerows(lst_matrix)
        str_table = o_string.getvalue()
        o_string.close()

    # write_table() returns

    return str_table


# END OF MMD TABLE WRITER

# OUTLINE READER

def read_outline(str_src):
    """ Parse the text to three elements:
        1. a simple tree structure
        (A list of node dictionaries, in which each node
        has the indexes of its parent and children)
        2/3 defaults for ruler row and alignments.
    """

    def _parse_text(str_src):
        """ Return the text tree component of the parse
        """

        def _mdoutline_to_tabbed(str_in):
            """ Normalise an MD outline to a simple
                 tabindented outline
            """

            rgx_hdr = re.compile(r'^(#+)\s+')
            rgx_pfx = re.compile(r'^(\s*)(\d\.|[\-\*\+]\s)')
            rgx_4s = re.compile(r'\ {4}')

            lst_lines = [_ for _ in dedent(str_in).splitlines() if _
                         != '']

            lng_prev = 0
            for (i, str_line) in enumerate(lst_lines):
                o_match = rgx_hdr.match(str_line)
                if o_match != None:

                    # hashes to (hashcount - 1) * tabs

                    lng_prev = len(o_match.group(1))
                    lst_lines[i] = rgx_hdr.sub('\t' * (lng_prev - 1),
                            str_line)
                else:

                    # strip md list prefixes, normalise 4 spaces to tabs,
                    # and add extra tabs for parental hash levels

                    lst_lines[i] = lng_prev * '\t' + rgx_4s.sub('\t',
                        rgx_pfx.sub('\\1', str_line))

            # _mdoutline_to_tabbed() returns

            return lst_lines

        # MAIN CODE OF _parse_text(str_src)

        lst_nodes = [{
            'id': 0,
            'parent': None,
            'level': 0,
            'indents': 0,
            'text': '',
            'chiln': [],
            }]
        lst_tabbed = _mdoutline_to_tabbed(str_src)
        rgx_tabs = re.compile('^\t*')
        #rgx_soh = re.compile('\x01')
        for (i_line, str_line) in enumerate(lst_tabbed):
            o_match = rgx_tabs.match(str_line)
            lng_tabs = len(o_match.group())
            str_text = str_line.strip().replace('|', ESC_PIPE)
            # the SOH character has been intruding here
            # and confusing the charwidth count. Whence ?
            # ANSWER a double slash editor error in a regex \\1 \1
            # str_text = rgx_soh.sub('', str_text)
            lst_nodes.append({'id': i_line + 1, 'indents': lng_tabs,
                             'text': str_text})

        # ensure that the minimum indent is zero
        # (in case of hash headers with shortest > #)

        lng_mgn = min(dct['indents'] for dct in lst_nodes[1:])
        if lng_mgn > 0:
            for dct in lst_nodes:
                dct['indents'] -= lng_mgn

        # parse_text() returns

        return lst_nodes

    def _add_parent_child(lst_nodes):
        """ Add parent and ChildIDs to each node
        """

        # The parent of Level 1 headers (and pre-header full-left lines)
        # is the virtual root.

        lst_parents = [0]
        for dct_node in lst_nodes[1:]:
            dct_node['chiln'] = []
            lst_id = dct_node['id']

            lst_level = dct_node['indents'] + 1

            # RECORD the nesting level

            dct_node['level'] = lst_level

            # and look for its current parent
            # (ensuring that there is a parent for this level)

            while len(lst_parents) < lst_level:
                lst_parents.append(lst_parents[-1])
            id_parent = lst_parents[lst_level - 1]

            # RECORD parent-child relationship

            dct_node['parent'] = id_parent
            lst_nodes[id_parent]['chiln'].append(lst_id)

            # UPDATE current level-parent list (unless this is an empty line)

            if len(lst_parents) <= lst_level:
                lst_parents.append(lst_id)
            else:
                lst_parents[lst_level] = lst_id

        # _add_parent_child() returns

        return lst_nodes

    # MAIN CODE read_outline()

    return {'tree': _add_parent_child(_parse_text(str_src)),
            'rulerrow': TBL_RULER_ROW, 'alignments': TBL_ALIGN_DEFAULTS}


# END OF OUTLINE READER

# OUTLINE WRITER

def write_outline(
    dct_parse,
    lng_max_hash,
    str_bullet,
    bln_space_b4hash,
    ):
    """ Translate a list of indexed node dictionaries
        (which include child id lists) into a text
        outline, either with plain tab-indents or as
        some markdown permutation, if lng_max_hash > 0
    """

    def _flag_table_padding():
        """ Flag empty cells which just pad out tables
            below shallow outline leaves.
            We don't need to include these in outlines
        """

        for dct_leaf in [dct_node for dct_node in lst_tree
                         if dct_node['chiln'] == [] and dct_node['text'
                         ] == '']:
            dct_leaf['padding'] = bln_padding = True
            id_parent = dct_leaf['parent']
            while bln_padding and id_parent != None:
                dct_parent = lst_tree[id_parent]
                bln_padding = dct_parent['text'] == ''
                if bln_padding:
                    dct_parent['padding'] = True
                    id_parent = dct_parent['parent']

    def _sub_outln(dct_node):
        """ Recursive closure
            yielding sub-outline for given node
        """

        if 'padding' in dct_node:
            return ''
        else:
            lst_level = dct_node['level']

            if lng_max_hash > 0:  # MARKDOWN outline
                if lst_level > lng_max_hash:
                    str_indent = (lst_level - lng_max_hash - 1) * '\t'
                    if str_bullet != '':
                        str_prefix = ''.join([str_bullet, ' '])
                    else:
                        str_prefix = ''
                else:
                    if bln_space_b4hash:
                        str_preline = '\n'
                    else:
                        str_preline = ''
                    str_indent = ''.join([str_preline, lst_level * '#',
                            ' '])
                    str_prefix = ''
            else:

                  # PLAIN TAB-INDENTED outlne

                str_indent = '\t' * (lst_level - 1)
                if str_bullet != '':
                    str_prefix = ''.join([str_bullet, ' '])
                else:
                    str_prefix = ''

            str_tree = ''.join([str_indent, str_prefix, dct_node['text'
                               ], '\n'])
            for id_child in dct_node['chiln']:
                str_tree = ''.join([str_tree,
                                   _sub_outln(lst_tree[id_child])])

        # _sub_outln() returns (2nd potential return)

        return str_tree

    # MAIN CODE of write_outline()

    lst_tree = dct_parse['tree']
    _flag_table_padding()
    str_out = ''
    for id_line in lst_tree[0]['chiln']:
        str_out = ''.join([str_out, _sub_outln(lst_tree[id_line])])

    # write_outline() returns

    return str_out.lstrip('\n')


# CSV READER

def read_csv(str_src, o_dialect):
    """ Parse string to a tree, using the dialect identified
         csv library sniffer.
    """

    # splitlines() avoids an excel clipboard newline issue

    lst_lines = str_src.splitlines(False)

    # detect whether we have a header

    bln_header = csv.Sniffer().has_header('\n'.join(lst_lines))

    # and segment and parse the rows and columns

    o_rdr = csv.reader(lst_lines, o_dialect)
    lst_rows = [row for row in o_rdr]
    lng_cols = len(lst_rows[0])

    # each cell of the top row is a child of the virtual root

    id_cell = lng_cols + 1
    lst_tree = [{
        'id': 0,
        'parent': None,
        'level': 0,
        'text': '',
        'chiln': range(1, id_cell),
        }]

    for (i_cell, str_cell) in enumerate(lst_rows[0]):
        lst_tree.append({
            'id': i_cell + 1,
            'parent': 0,
            'level': 1,
            'text': str_cell.strip(),
            'chiln': [],
            })

    # each cell on any further row is a child of the cell above it

    for (i_row, lst_row) in enumerate(lst_rows[1:]):
        for (i_cell, str_cell) in enumerate(lst_row):

            # enter id of this cell in the child list of the cell above

            id_parent = id_cell - lng_cols
            lst_tree[id_parent]['chiln'] = [id_cell]
            lst_tree.append({
                'id': id_cell,
                'parent': id_parent,
                'level': i_row + 2,
                'text': str_cell.strip(),
                'chiln': [],
                })
            id_cell += 1

    if bln_header:
        lng_ruler = TBL_RULER_ROW
    else:

          # no ruler, just paste mmd table lines

        lng_ruler = -1

    return {'tree': lst_tree, 'rulerrow': lng_ruler,
            'alignments': TBL_ALIGN_DEFAULTS}


# END OF CSV READER

# CSV WRITING
    # CSV writing is handled by the same write_table() function (above)
    # as MMD_TBL writing
# END OF CSV WRITING

    # IF NOT USED AS LIBRARY, TRANSLATE ANY CLIPBOARD TEXT

if __name__ == '__main__':
    main()
