#!/usr/bin/env python

# Copyright (C) 2012 Robin Trew

# Permission is hereby granted, free of charge, 
# to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), 
# to deal in the Software without restriction, 
# including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons 
# to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice 
# shall be included in ALL copies 
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Read OmniFocus Sqlite & export to OPML/ITM(z)/TXT/MD/FT 022"""

STR_AUTHOR = "Robin Trew 2012"
STR_PUB = "Orginally published on http://forums.omnigroup.com"
STR_VER = "022"

import os, sys, sqlite3, re, codecs, uuid, time
import plistlib, optparse, zipfile, zlib
from datetime import datetime
import xml.etree.ElementTree as ET

from xml.sax.saxutils import quoteattr, escape, unescape
from cStringIO import StringIO
from tokenize import generate_tokens

FLAG_DEBUG = 0

def get_options():
    """Parse the command line options"""
    psr = optparse.OptionParser()
    psr.add_option('--root', '-a', default = None, \
        help = 'Specify a sub-tree by the OmniFocus id of its root node.\n\
Defaults to None.')
    psr.add_option('--format', '-x', default = 'txt', \
        help = 'Set the export format [itmz | itm | opml | txt | md | ft].\n\
Defaults to tab-indented text. md is simple Markdown, ft is Markdown with\n\
the addition of FoldingText\'s .todo mode tags for checkboxes and\n\
struck-through done items')
    psr.add_option('--output', '-o', default = 'current_tasks', \
        help = 'Set the export filepath.\n\
Defaults to file named current_tasks')
    psr.add_option('--collapse', '-c', type = 'string', default = '2,4', \
        help = 'List the outline levels to collapse.\n\
Defaults to 2,4')
    psr.add_option('--template', '-m', type = 'string', default = '', \
        help = 'The pathname of an .itm or .itmz template for iThoughtsHD.\n\
Defaults to same directory as script.')
    psr.add_option('--links', '-l', action = 'store_true', default = False, \
        help = 'Include OmniFocus task/folder links.\n\
Defaults to false')
    psr.add_option('--notes', '-n', action = 'store_true', default = False, \
        help = 'Include OmniFocus notes.\n\
Defaults to false')
    psr.add_option('--recurinfo', '-r', action = 'store_true', default = False,\
        help = 'Add any repetition information to start of notes.\n\
Defaults to false')
    psr.add_option('--folders', '-f', type = 'string', dest = 'folder_SQL', \
        help = 'SQL clause[s] to limit which FOLDERS are exported.\n\
Defaults to effectiveActive=1')
    psr.add_option('--singlelists', '-s', type = 'string', \
        dest = 'singles_SQL', \
        help = 'SQL clause[s] to limit which SINGLE ACTION LISTS \
            are exported.\n\
Defaults to status=active, folderEffectiveActive=1, dateCompleted is null')
    psr.add_option('--projects', '-p',  type = 'string', \
        dest = 'project_SQL', \
        help = 'SQL clause[s] to limit which PROJECTS are exported.\n\
Defaults to status=active, folderEffectiveActive=1, dateCompleted is null \n\
Use a comma for AND (OR is not supported) e.g.\n\
-p \'childrenCount > 0, blockedByFutureStartDate = 0\'')
    psr.add_option('--tasks', '-t',  type = 'string', dest = 'task_SQL', \
        help = 'SQL clause[s] to limit which TASKS are exported.\n\
Defaults to dateCompleted is null, effectiveContainingProjectInfoActive=1')
    psr.add_option('--inbox', '-i',  type = 'string', dest = 'inbox_SQL', \
        help = 'SQL clause[s] to limit which INBOX TASKS are exported.\n\
Defaults to all inbox tasks')
    return psr.parse_args()
    
def main():
    """Read from OmniFocus cache into a nested list,
    then write out in itm, itmz, opml, txt, md, or ft"""
    
    # READ THE DEFAULTS OR COMMAND LINE SWITCHES
    (options, _) = get_options()
    parse_sql_options(options)

    #options.root = 'eIxpzmSr8oJ'
    lst_tree = build_tree(options.root)
    
    str_export = translate_tree(lst_tree, options)
    
    # Write out the specified file and format (or print to screen for debugging)
    
    if (FLAG_DEBUG == 0):
        # Get path and output file names
        (str_dir, str_file) = os.path.split(options.output)
        
        # Use the Desktop if no folder specified
        if (str_dir == ''):
            str_dir = os.path.expanduser('~/Desktop')
        
        # Using a datestamp filename if none specified
        if (str_file == ''):
            str_file = today.strftime('%Y-%h-%d-%Hh%Mm%Ss')
                
        # Get path of final output
        str_suffix = options.format        
        str_out_path = ''.join([str_dir, '/', str_file, '.', str_suffix])
         
        bln_itmz = (str_suffix == 'itmz') 
        if (bln_itmz):
            # Write to a map.itm then zip in the case of .itmz 
            str_tmp_path = ''.join([str_dir, '/map.itm'])
            tmp_file = codecs.open(str_tmp_path, "w", 'UTF-8')
        else:
            tmp_file = codecs.open(str_out_path, "w", 'UTF-8')
        tmp_file.write(str_export)
        tmp_file.close()
        
        if (bln_itmz):
            zip_archive = zipfile.ZipFile(str_out_path, 'w', zipfile.ZIP_DEFLATED)
            os.chdir(str_dir)
            zip_archive.write('map.itm')
            zip_archive.close()
            os.remove(str_tmp_path) # remove the map.itm file
    else:
        #print str_export
        print 'Done'
        #print options.root
        
# DEFAULT DATA TO EXPORT 
CLAUSES_FOLDER = \
    {'effectiveActive':{'logic':'=', 'value':1}}
CLAUSES_SINGLES_HOLDER = \
    {'status':{'logic':'=', 'value':'active'}, \
    'folderEffectiveActive':{'logic':'=', 'value':1}, \
    'dateCompleted':{'logic':'is', 'value':None}}
CLAUSES_PROJECT = \
    {'status':{'logic':'=', 'value':'active'}, \
    'folderEffectiveActive':{'logic':'=', 'value':1}, \
    'dateCompleted':{'logic':'is', 'value':None}}
CLAUSES_TASK = {\
    'dateCompleted':{'logic':'is', 'value':None}, \
    'effectiveContainingProjectInfoActive':{'logic':'=', 'value':1}}
CLAUSES_INBOX = {\
    'dateCompleted':{'logic':'is', 'value':None}}    

OPTS_FILTERS = []

ROOT_COL = None
ROOT_SHAPE = None
LST_COLORS = []
LST_SHAPES = []
    
REPN_PREFIX = 'Repeats: '

DCT_PLIST = \
    {'InheritShape': True, 'Rainbow': True, 'ShowCallouts': True, \
    'MapLayout': 1, 'CanvasStyle': 2, 'Theme': {\
    'level0': {'fillColour': '', 'shape': 4, 'fontSize': 0, 'textStyle': 1}, \
    'level1': {'fillColour': '', 'shape': 4, 'fontSize': 0, 'textStyle': 0}, \
    'level2': {'fillColour': '', 'shape': 4, 'fontSize': 0, 'textStyle': 0}}, \
    'DropShadow': False, 'ShowCompletedTasks': True, 
    'MapData': '&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;\
iThoughtsRelative version="2.0"&gt;&lt;topics&gt;&lt;\
topic refid="1" txt="Template" topcol="FDF6E3" shape="3" &gt;&lt;\
topic refid="2" txt="" shape="4" topcol="B2FFB2"&gt;&lt;/topic&gt;&lt;\
topic refid="10" txt="" shape="4" topcol="B2FFFF"&gt;&lt;/topic&gt;&lt;\
topic refid="11" txt="" shape="4" topcol="B2D9FF"&gt;&lt;/topic&gt;&lt;\
topic refid="12" txt="" shape="4" topcol="B2B2FF"&gt;&lt;/topic&gt;&lt;\
topic refid="13" txt="" shape="4" topcol="D9B2FF"&gt;&lt;/topic&gt;&lt;\
topic refid="14" txt="" shape="4" topcol="FFB2FF"&gt;&lt;/topic&gt;&lt;\
topic refid="16" txt="" shape="4" topcol="FFB2D9"&gt;&lt;/topic&gt;&lt;\
topic refid="9" txt="" shape="4" topcol="B2FFD9"&gt;&lt;/topic&gt;&lt;\
topic refid="7" txt="" shape="4" topcol="D9FFB2"&gt;&lt;/topic&gt;&lt;\
topic refid="6" txt="" shape="4" topcol="FFFFB2"&gt;&lt;/topic&gt;&lt;\
topic refid="5" txt="" shape="4" topcol="FFD9B2"&gt;&lt;/topic&gt;&lt;\
topic refid="4" txt="" shape="4" topcol="FFB2B2"&gt;&lt;/topic&gt;&lt;\
/topic&gt;&lt;/topics&gt;&lt;relationships&gt;&lt;/relationships&gt;&lt;\
/iThoughtsRelative&gt;',\
    'ContentOffset': '{0, 0}', 'MapViewStyle': 1, 'InheritColour': True, \
    'ShowUnfocusedTopics': True, 'Assets': [], 'ShowTaskBadge': True, \
    'Level1LinkTapered': True, 'MapAutoAlign': 1, 'RadialLayout': 0, \
    'LevelNLinkStyle': 3, 'Level1LinkStyle': 3, 'ReadOnly': False, \
    'ZoomScale': 1.0}

# position of fields in the nodes
FLD_NODE_TYPE = 0
FLD_PARENT_ID = 1
FLD_ID = 2
FLD_NAME = 3
FLD_NOTE = 4
FLD_START = 5
FLD_DUE = 6
FLD_DONE = 7
FLD_REPN_STRING = 8
FLD_CHILN = 9

INT_ALL_FIELDS = 10

# types of OmniFocus object
OF_INBOX = 0
OF_FOLDER = 1
OF_SINGLES_HOLDER = 2
OF_PROJECT = 3
OF_TASK = 4

# OPML FRAGMENTS
OPML_NODE_START = '<outline '
OPML_LEAF_CLOSE = '/>'
OPML_PARENT_CLOSE = '</outline>'
OPML_HEAD_TO_EXPAND = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<opml version=\"1.0\">\n<head>\n<title>OmniFocus Active Tasks</title>\n\
<expansionState>'
OPML_HEAD_FROM_EXPAND = '</expansionState>\n</head>\n<body>\n'
OPML_TAIL = '</body></opml>'
OPML_INDENT = ''

# ITM FRAGMENTS
ITM_HEAD = '&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n\
&lt;iThoughtsRelative version="2.0"&gt;\n&lt;topics&gt;'
ITM_TAIL = '&lt;/topics&gt;&lt;relationships/&gt;&lt;/iThoughtsRelative&gt;\n'
ITM_NODE_START = '\n&lt;topic '
ITM_CLOSE_TAG = '&gt;'
ITM_LEAF_CLOSE = '&gt;&lt;/topic&gt;'
ITM_PARENT_CLOSE = '&lt;/topic&gt;'
ITM_INDENT = ''

# TXT INDENT
TXT_INDENT = '\t'

ITM_REFID = 1
        
def translate_tree(lst, options):
    """Choose between itm, opml and text rendering of the tree"""
        
    fmt = options.format.lower()
    if (fmt == 'itmz') or (fmt == 'itm'):
        return itm_doc(lst, options)
    elif (fmt == 'opml'):
        return opml_doc(lst, options.links, options.notes, options.recurinfo)
    elif (fmt == 'txt'):
        return txt_doc(lst, '', options.links, options.notes, \
            options.recurinfo)
    elif (fmt in ('md','ft')):
        bln_ft = (fmt == 'ft')
        return md_doc(lst, '', options.links, options.notes, \
            options.recurinfo, bln_ft)
    else:
        return "Format not found: ", fmt
            
def build_tree(var_root):
    """Read the specified OFOC data into a tree (nested list)"""
    (var_root_parent, flat_of) = get_flat_omnifocus(var_root)
    
    lst_clean = strip_note_xml(list(flat_of))
    dict_parents = get_parent_posns(lst_clean)
    
    #print var_root_parent
    flat_to_nested(lst_clean, dict_parents, var_root_parent)

    # Enclose the data tree in a virtual root node of the right length
    lst_root = list([None] * FLD_CHILN)
    lst_root.append(lst_clean)
    lst_root[FLD_NAME] = 'Focus'
    return [lst_root]
    
def txt_doc(lst, str_indent, bln_links, bln_notes, bln_recurinfo):
    """Traverse tree to build nested TXT outline"""
    
    tr_msg = re.compile('message:%3C(.*)%3E')

    str_out = ""
    str_deeper = ''.join([str_indent, TXT_INDENT])
    for peer in lst:
        [iobj_type, _, str_id, str_name, str_note, int_start, int_due, \
            int_done, str_repn] = peer[FLD_NODE_TYPE:FLD_CHILN]
        str_out = ''.join([str_out, str_indent, escape(str_name)])
        if (bln_recurinfo != 0) and (str_repn is not None):
            str_out = ''.join([str_out, '\n', str_deeper, str_repn])
        if (bln_links != 0) and (str_id is not None):
            str_out = ''.join([str_out, '\n', str_deeper, txt_of_link(str_id)])
        if bln_notes and (str_note is not None):
            str_out = ''.join([str_out, '\n', \
                tr_msg.sub('message://%3C\\1%3E', escape(peer[FLD_NOTE]))])

        if (len(peer) >= INT_ALL_FIELDS):
            str_out = ''.join([str_out, '\n', \
                txt_doc(peer[FLD_CHILN], str_deeper, bln_links, bln_notes, \
                    bln_recurinfo)])
        else:
            str_out = ''.join([str_out, '\n'])
    return str_out
    
def md_doc(lst, str_indent, bln_links, bln_notes, bln_recurinfo, bln_ft):
    """Traverse tree to build a markdown document with hashes to 
    project level, hyphens beyond (except for notes) and tab-indenting
    from the 2nd level of tasks.
    Optionally adding .ft '.todo' after projects, and ' @done' after
    any completed items"""

    tr_msg = re.compile('message:%3C(.*)%3E')
    tr_hash = re.compile('(#*[!#])') # space before hash any sequence in data
    tr_suffix = re.compile('(\.\S{2,8}$)')
        
    str_out = ''
    
    for peer in lst:
        [iobj_type, _, str_id, str_name, str_note, int_start, int_due, \
            int_done, str_repn] = peer[FLD_NODE_TYPE:FLD_CHILN]
        #print iobj_type, str_name    
        if ((iobj_type <= OF_PROJECT) and (iobj_type is not None)):
            str_prefix = '# '
            str_this_indent = str_indent
            str_next_indent = ''.join([str_indent, '#'])
        elif (iobj_type == OF_TASK):
            # BUT TASKS JUST INHERIT, PASSING AN ADDITIONAL TAB 
            # TO THEIR CHILDREN
            str_prefix = '- '
            if ('#' in str_indent):
                str_this_indent = ''
            else:
                str_this_indent = str_indent
            str_next_indent = ''.join([str_this_indent, '\t'])
        else:
            str_next_indent = ''
            str_prefix = ''
            str_this_indent = ''
                  
        if ('#' in str_indent):
            str_deeper = '\t'
        else:
            str_deeper = ''.join([str_this_indent, '\t'])
        
        str_out = ''.join([str_out, str_this_indent, str_prefix, \
            tr_hash.sub(' \\1', escape(str_name))])
        if (bln_ft):
            if (iobj_type in (OF_PROJECT, OF_INBOX)):
                str_out = ''.join([str_out, '.todo'])
            if (int_done != None):
                str_out = ''.join([str_out, ' @done'])

        if (bln_recurinfo != 0) and (str_repn is not None):
            str_out = ''.join([str_out, '\n', str_deeper, str_repn])

        if (bln_links != 0) and (str_id is not None):
            str_out = ''.join([str_out, '\n', str_deeper, txt_of_link(str_id)])

        if bln_notes and (str_note is not None):
            str_out = ''.join([str_out, '\n', str_deeper, \
                tr_suffix.sub('\\1 ', tr_hash.sub(' \\1', \
                tr_msg.sub('<message://%3C\\1%3E>', escape(peer[FLD_NOTE]))))])

        if (len(peer) >= INT_ALL_FIELDS):
            str_out = ''.join([str_out, '\n', \
                md_doc(peer[FLD_CHILN], str_next_indent, \
                    bln_links, bln_notes, bln_recurinfo, bln_ft)])
        else:
            str_out = ''.join([str_out, '\n'])
    return str_out

def txt_of_link(str_id):
    """Build a LINK from an OmniFocus id""" 
    return ''.join(['<omnifocus:///task/', str_id, '>'])
    
def opml_doc(lst, bln_links, bln_notes, bln_recurinfo):
    """Assemble an OPML document"""
    return ''.join([OPML_HEAD_TO_EXPAND, '0', OPML_HEAD_FROM_EXPAND, \
    opml_from_tree(lst, OPML_INDENT, bln_links, bln_notes, bln_recurinfo), \
        OPML_TAIL])
    
def opml_from_tree(lst, str_indent, bln_links, bln_notes, bln_recurinfo):
    """Traverse tree to build nested opml outline"""

    tr_msg = re.compile('message:%3C(.*)%3E')

    str_out = ""
    str_deeper = ''.join([str_indent, OPML_INDENT])
    for peer in lst:
        [iobj_type, _, str_id, str_name, str_note, int_start, int_due, \
            int_done, str_repn] = peer[FLD_NODE_TYPE:FLD_CHILN]
        str_out = ''.join([str_out, str_indent, OPML_NODE_START, \
            opml_attr('text', escape(quoteattr(str_name)))])
        if (bln_links != 0) and (str_id is not None):
            str_out = ''.join([str_out, opml_of_link(str_id)])
        if (bln_recurinfo and (str_repn is not None)):
            if (str_note is None):
                str_note = str_repn
            else:
                str_note = ''.join([str_repn, '    ', str_note])
        if bln_notes and (str_note is not None):
            str_out = ''.join([str_out, opml_attr('_note', \
            tr_msg.sub('message://%3C\\1%3E', escape(quoteattr(str_note))))])

        if (len(peer) >= INT_ALL_FIELDS):
            str_out = ''.join([str_out, '>\n', \
                opml_from_tree(peer[FLD_CHILN], str_deeper, bln_links, \
                    bln_notes, bln_recurinfo), \
                    str_indent, OPML_PARENT_CLOSE, '\n'])
        else:
            str_out = '%s%s\n' % (str_out, OPML_LEAF_CLOSE)
    return str_out
    
def opml_of_link(str_id):
    """Build a LINK attribute from an OmniFocus id"""
    return ''.join(['LINK', '=\"', 'omnifocus:///task/', str_id, '\" '])
    
def opml_attr(str_name, str_value):
    """Build OPML attribute pairings"""
    # return '%s=%s '  % (str_name, str_value)
    return ''.join([str_name, '=', str_value, ' '])
        
def itm_doc(lst_tree, options):
    """translate the tree data into iThoughtsHD .itm text"""
    
    global DCT_PLIST, LST_COLORS, LST_SHAPES
    
    # Update the PLIST dictionary from any specified template
    str_template_path = options.template
    if (str_template_path != ''):
        dct_template = get_template_dct(str_template_path)
        if (dct_template != None):
            DCT_PLIST = dct_template
    # Read in the colours and shapes for the top-level branches
    LST_COLORS = get_template_top_attribs(DCT_PLIST, 'topcol')
    LST_SHAPES = get_template_top_attribs(DCT_PLIST, 'shape')
        
    #Build the escaped topics XML
    str_topics = itm_content(lst_tree, options)
    
    # WRAP THE TOPICS IN A PLIST FILE (STRING VALUE OF MAPDATA KEY)
    # PLACE A SPLICE MARKER IN THE THE PLIST DICTIONARY
    str_cut_here = str(uuid.uuid4())
    DCT_PLIST['MapData'] =  str_cut_here
    str_plist = plistlib.writePlistToString(DCT_PLIST)
    # Extract the plist text before the MapData
    posn_found = str_plist.find(str_cut_here) 
    str_plist_head = str_plist[:posn_found] 
    # and after the map data
    posn_found += len(str_cut_here)
    str_plist_tail = str_plist[posn_found:] 
    
    str_export = ''.join([str_plist_head, str_topics, str_plist_tail])
    return str_export
    
def get_template_top_attribs(dct, str_attrib):
    """Read root node and top level branch attributes
    from iThoughts template data"""
    
    if (dct is not None):
        dom_root = ET.fromstring(unescape(dct['MapData']))
        try:
            var_root = dom_root[0][0].attrib[str_attrib]
        except KeyError:
            var_root = None
        try:
            return  [var_root] + [child.attrib[str_attrib] \
                for child in dom_root[0][0]]
        except KeyError:
            return var_root + [] # Not all templates will define topcol for these topics
    else:
        return []
        

        

def get_template_dct(str_path):
    """Find a an iThoughts plist in an .itm file
    or in a zipped .itmz file"""

    # if no pth component, assume the same path as the script
    if (str_path.count('/') < 1):
        str_path = ''.join([os.path.dirname(sys.argv[0]),'/',str_path])

    if (os.path.isfile(str_path)):
        if (str_path[-1].lower() == 'z'):
            if (zipfile.is_zipfile(str_path)):
                zf = zipfile.ZipFile(str_path, 'r')
                lst_map = zf.namelist()
                if (len(lst_map) > 0):
                    str_map_file = 'map.itm'
                    if (lst_map[0] == str_map_file):
                        data = zf.read(str_map_file)
                        dct = plistlib.readPlistFromString(data)
                        return dct
        else:   
            dct = plistlib.readPlist(str_path)
            return dct
    else:
        sys.exit('Template not found: ' + str_path)
        
def parse_sql_options(options):
    """Capture any SQL options passed at the command line"""
    
    global OPTS_FILTERS
    OPTS_FILTERS = []
    for (str_scope, str_sql) in [('f', options.folder_SQL), \
        ('p', options.project_SQL), ('t', options.task_SQL), \
        ('i', options.inbox_SQL)]:
        if (str_sql != None):
            dct_clauses =  parse_clauses(str_scope, str_sql)
            OPTS_FILTERS = OPTS_FILTERS + dct_clauses


def parse_clauses(str_scope, str_clauses):
    """Read SQL clause sequence into a
        list of {scope, col, logic value} dictionary items
    """
    lst_dict = []
    lst_clauses = re.split(',| and ', str_clauses)
    for clause in lst_clauses:
        lst_tokens = get_tokens(clause)
        lst_dict.append(build_dct(str_scope, lst_tokens))
    return lst_dict

def get_tokens(str_clause):
    """Get a list of tokens from a an SQL clause
        ignoring spaces and parentheses"""

    return list(token[1] for token 
        in generate_tokens(StringIO(str_clause).readline)
        if (token[1] not in ('', ' ','(', ')')))

def build_dct(str_scope, lst_tokens):
    """ try to match tokens to {scope, col, logic value} pattern
        halting the script with an error message on failure.
        Simple error checking for token count and recognised operators"""
    str_expected = 'Expected [column operator value], or a simple [0|1]\n\
        \nTokens found:'
    set_known_ops = ('is', '=', '==', \
        '!=', '<>', '<', '<=', '>', '>=','like')
    int_tokens = len(lst_tokens)
    if (int_tokens > 0):
        if (int_tokens > 4): # too many
            sys.exit(''.join(['SQL clause not understood - ', \
            'too many tokens ...\n\n', \
            str_expected, str(lst_tokens)]))
        else:
            if (int_tokens > 3): # 4 tokens or 1 expected
                str_op1 = lst_tokens[1].lower()
                str_op2 = lst_tokens[2].lower()
                str_op = ''.join([str_op1, ' ', str_op2])
                if (str_op == 'is not') or ((str_op1 == 'not') and \
                    (str_op2 == 'like')):
                    dct_clause = {'scope':str_scope, 'col':lst_tokens[0], \
                        'logic':str_op, 'value':lst_tokens[3]}
                else:
                    sys.exit(''.join(['SQL clause not understood - ', \
                    'too many tokens, or unrecognized operator ...\n\n', \
                    str_expected, str(lst_tokens)]))
            else:
                if (int_tokens > 2): # 3 tokens
                    str_op = lst_tokens[1].lower()
                    if (str_op in set_known_ops):
                        dct_clause = {'scope':str_scope, 'col':lst_tokens[0], \
                            'logic':str_op, 'value':lst_tokens[2]}
                    else:
                        sys.exit(''.join(['SQL clause not understood - ', \
                        'unrecognized operator ...\n\n', \
                        str_expected, str(lst_tokens), \
                        '\n\nOperators understood: ', str(set_known_ops)]))
                else:
                    if (int_tokens > 1): # 2 tokens
                        sys.exit(''.join(['SQL clause not understood - ', \
                        'unexpected number of tokens, ', \
                        'or unrecognized operator ...\n\n',\
                        str_expected, str(lst_tokens)]))
                    else:
                        str_token = lst_tokens[0] # single token
                        if (str_token in ['0', '1']):
                            dct_clause = {'scope':str_scope, 'col':None, \
                                'logic':None, 'value':str_token}
                        else:
                            sys.exit(''.join(['SQL clause not understood - ', \
                            'Unrecognized single token ...\n\n',\
                            str_expected, str(lst_tokens)]))
        return dct_clause            
    else: # no tokens
        return None

def opt_update():
    """Update the SQL query elements with any command line options"""

    dct_tables = {\
        'f':CLAUSES_FOLDER, \
        's':CLAUSES_SINGLES_HOLDER, \
        'p':CLAUSES_PROJECT, \
        't':CLAUSES_TASK, \
        'i':CLAUSES_INBOX }
     
    for opt in OPTS_FILTERS:
        for tbl_code in list(opt['scope']):
            dct_tables[tbl_code][opt['col']] = \
                {'logic':opt['logic'], 'value':opt['value']}
                    
def itm_content(lst, options):
    """Assemble an iThoughtsHD ITM document"""
    global ITM_REFID
    ITM_REFID = 0
    year_zero = ofoc_year_zero()
    
    lst_fold = [int(x) for x in options.collapse.split(',')]
    bln_links = options.links
    bln_notes = options.notes
    bln_repn = options.recurinfo
    
    return ''.join([ITM_HEAD, \
        itm_from_tree(lst, year_zero, '', bln_links, bln_notes, bln_repn, 
            lst_fold, 0), ITM_TAIL])
        
def itm_from_tree(lst, year_zero, str_indent, bln_links, bln_notes, \
        bln_repn, lst_fold, int_level):
    """Traverse tree to build nested iThoughts ITM topic outline"""
    global ITM_REFID
    
    str_out = ""
    if (ITM_INDENT != ''):
        str_deeper = ''.join([str_indent, ITM_INDENT])
    else:
        str_deeper = ''
        
    # decrement the fold levels for the next generation
    #nxt_levels = map(lambda x: x-1, lst_fold)
    nxt_levels = [x - 1 for x in lst_fold]
    
    # Prepare to apply any custom color or shape if this is level 0
    if (int_level == 0):
        lng_colors = 1
        lng_shapes = 1
        iColor = 0
        iShape = 0
    # Prepare to apply any custom colors or shapes if this is level 1
    elif (int_level == 1):
        lng_colors = len(LST_COLORS) - 1
        lng_shapes = len(LST_SHAPES) - 1
        iColor = 1
        iShape = 1
    else:
        lng_colors = 0
        lng_shapes = 0
        
    for peer in lst:
        str_line = ''
        ITM_REFID = ITM_REFID + 1
        
        [iobj_type, _, str_id, str_name, str_note, int_start, int_due, int_done, \
            str_repn] = peer[FLD_NODE_TYPE:FLD_CHILN]
        
        str_line = ''.join([str_line, str_indent, ITM_NODE_START, \
            'uuid=\"', str(uuid.uuid4()).upper(), '\" refid=\"', \
            str(ITM_REFID), '\" txt=', escape(quoteattr(str_name)), ' '])
        # Handle note, optionally with any Repetition String prepended
        if (bln_repn) and (str_repn is not None):
            if (str_note != None):
                str_note = ''.join([REPN_PREFIX, str_repn, '\n', str_note])
            else:
                str_note = ''.join([REPN_PREFIX, str_repn])
                 
        if (str_note is not None):
            str_line = ''.join([str_line, 'note=', \
                escape(quoteattr(str_note)), ' '])
        if (1 in lst_fold):
            str_line = ''.join([str_line, 'folded=\"1\" '])
        if (int_start is not None):
            str_line = ''.join([str_line, 'start=\"', \
            time.strftime('%d%m%y %H%M%S', \
                time.gmtime(year_zero + int_start)), '\" '])
        if (int_due is not None):
            str_line = ''.join([str_line, 'due=\"', \
            time.strftime('%d%m%y %H%M%S', \
                time.gmtime(year_zero + int_due)), '\" '])
        if (bln_links) and (str_id is not None):
            str_line = ''.join([str_line, of_link(str_id, \
                (peer[0] != OF_FOLDER))])

        if (lng_colors > 0):
            var_color = LST_COLORS[iColor]
            if (var_color is not None):
                str_line = ''.join([str_line, 'topcol=', '\"', var_color ,'\" '])
            iColor = iColor + 1
            # if we just used the last color in the palette, restart
            if ((lng_colors - iColor) < 0):
                iColor = 1

        if (lng_shapes > 0):
            var_shape = LST_SHAPES[iShape]
            if (var_shape is not None):
                str_line = ''.join([str_line, 'shape=', '\"', var_shape ,'\" '])
            iShape = iShape + 1
            # if we just used the last shape in the set, restart
            if ((lng_shapes - iShape) < 0):
                iShape = 1 
       
        if (len(peer) >= INT_ALL_FIELDS):
            str_line = ''.join([str_line, ITM_CLOSE_TAG, \
                itm_from_tree(peer[FLD_CHILN], year_zero, str_deeper, \
                bln_links, bln_notes, bln_repn, nxt_levels, int_level+1), str_indent, \
                    ITM_PARENT_CLOSE])
        else:
            str_line = ''.join([str_line, ITM_LEAF_CLOSE]) 
            
        str_out = ''.join([str_out, str_line])
    return str_out
         
def of_link(str_id, bln_not_folder):
    """Build a link to a folder or task from an OmniFocus id"""
    if (bln_not_folder):
        return ''.join(['link=\"omnifocus:///task/', str_id, '\" '])
    else:
        return ''.join(['link=\"omnifocus:///folder/', str_id, '\" '])
    
def ofoc_year_zero():
    """Get Jan 1 2001 in seconds"""
    str_zone = time.strftime("%z")
    int_zone = ((int(str_zone[:3]) * 3600) + (int(str_zone[3:]) * 60))
    return int(time.mktime(time.strptime("1 Jan 01", "%d %b %y")) + int_zone)
    
def get_flat_omnifocus(var_root):
    """Read Omnifocus cache data into flat ordered list"""
    # Where is the ofoc cache ?
    ofoc = os.path.expanduser('~/Library/Caches/com.omnigroup.OmniFocus')
    if not os.path.exists(ofoc):
        ofoc = ofoc + '.MacAppStore'

    cache_db = ofoc +  '/OmniFocusDatabase2'

    # Prepare to query the ofoc cache
    con = sqlite3.connect(cache_db)
    csr = con.cursor()
    
    # Set up a temporary table reducing folders projects
    # and tasks to one record type (including parent)
    str_fld_defns = 'objtype integer, parent text, persistentIdentifier text, \
        name text, noteXMLData blob, rank integer, \
        effectiveDateToStart timestamp, effectiveDateDue timestamp, dateCompleted timestamp, \
        repnString text'
    csr.execute('CREATE TEMP TABLE fpt_active (' + str_fld_defns + ')')

    # SPECIFY THE DATA
    # Gather active folders, projects and tasks into a single table
     
    base_fields = ('parent', 'persistentIdentifier', 'name', 'noteXMLData', \
        'rank', 'effectiveDateToStart', 'effectiveDateDue', 'dateCompleted', \
        'repetitionMethodString  || \';\'  || repetitionRuleString')
        
    # UPDATE THE QUERY OPTIONS FROM ANY SWITCHES
    opt_update()

    # FOLDERS   
    str_fields = '%s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL ' % \
        ((OF_FOLDER, ) + base_fields[:-4])
    (tpl, str_clauses) = build_query(CLAUSES_FOLDER)
    
    str_sql = ''.join(['INSERT INTO fpt_active SELECT ', str_fields, \
            ' FROM Folder WHERE ', str_clauses])
    csr.execute(str_sql, tpl)
    
    # SINGLES HOLDERS
    str_fields = '%s, folder, %s, %s, %s, %s, %s, %s, %s, %s ' \
    % ((OF_SINGLES_HOLDER, ) + base_fields[1:])
    (tpl, str_clauses) = build_query(CLAUSES_PROJECT)
    #print (tpl, str_clauses)
    
    #print (tpl, str_clauses), '\n\n'
    #sys.exit("PROJECT inspection")
    csr.execute(''.join(['INSERT INTO fpt_active SELECT ', str_fields, \
        ' FROM (task t join projectinfo p on t.projectinfo = p.pk) \
        WHERE (containsSingletonActions = 1) and ', str_clauses]), tpl)
        
    # PROJECTS
    str_fields = '%s, folder, %s, %s, %s, %s, %s, %s, %s, %s' \
        % ((OF_PROJECT, ) + base_fields[1:])
    (tpl, str_clauses) = build_query(CLAUSES_PROJECT)
   
    csr.execute(''.join(['INSERT INTO fpt_active SELECT ', str_fields, \
        ' FROM (task t join projectinfo p on t.projectinfo = p.pk) \
        WHERE (containsSingletonActions = 0) and ', str_clauses]), tpl)
    
    # TASKS
    str_fields = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % ((OF_TASK, ) + \
        base_fields)
    (tpl, str_clauses) = build_query(CLAUSES_TASK)
    
    csr.execute(''.join(['INSERT INTO fpt_active SELECT ', str_fields, \
    ' FROM task WHERE projectInfo is null and inInbox = 0 and ', \
        str_clauses]), tpl)

    # INBOX
    (tpl, str_clauses) = build_query(CLAUSES_INBOX)
    
     # An invented INBOX root node, if we are showing the inbox
    if (tpl, str_clauses) != (('0',), ' ?'):
        csr.execute('INSERT INTO fpt_active \
            SELECT ?, NULL, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL ', \
            (OF_INBOX, 'Inbox', 'Inbox'))

    # and all the inbox tasks
    str_fields = '%s, \"Inbox\", %s, %s, %s, %s, %s, %s, %s, %s' % \
        ((OF_TASK, ) + base_fields[1:])
    csr.execute(''.join(['INSERT INTO fpt_active SELECT ', str_fields, \
        ' FROM task WHERE inInbox = 1 and ', str_clauses]), tpl)

    # Set up recursive building of temporary table to get nested folder order
    csr.execute('CREATE TEMP TABLE Nested_Order (' + str_fld_defns + ')')
    csr.execute('PRAGMA recursive_triggers = TRUE')
    str_fields = 'objtype, %s, %s, %s, %s, %s, %s, %s, %s, repnString' % \
        base_fields[:-1]
    csr.execute('CREATE TEMP TRIGGER order_Folders AFTER INSERT \
    ON Nested_Order \
    BEGIN \
        INSERT INTO Nested_Order SELECT ' + str_fields + ' \
            FROM fpt_active \
        WHERE fpt_active.parent = new.persistentIdentifier ORDER BY rank; \
    END')

    # Identify the parent, in case of a selected node
    if var_root is None:
        var_root_parent = None
    else:
       tpl = (var_root, )
       csr.execute('SELECT parent FROM fpt_active WHERE persistentIdentifier = ?', tpl)
       var_root_parent = csr.fetchone()[0]

    # Launch recursive process from top level objects
    # to build a temporary ordered table
    
    if (var_root is None):
        tpl = (None, )
        csr.execute('INSERT INTO Nested_Order SELECT ' + str_fields + ' \
            FROM fpt_active WHERE parent is ? ORDER BY rank', tpl)
    else:
        tpl = (var_root, )
        csr.execute('INSERT INTO Nested_Order SELECT ' + str_fields + ' \
            FROM fpt_active WHERE persistentIdentifier is ? ORDER BY rank', tpl)
    
    # Harvest the recursively ordered temporary table
    csr.execute('SELECT objtype, parent, persistentIdentifier, name, \
        CAST(noteXMLData as text), effectiveDateToStart, effectiveDateDue, dateCompleted, \
        repnString FROM Nested_Order')
    flat_of = csr.fetchall()
    csr.execute('DROP TABLE fpt_active')
    csr.execute('DROP TABLE Nested_Order')
    return (var_root_parent, flat_of)

def build_query(dct):
    """Build SQL with '?' and value tuples from clause dictionary"""
    if (dct is not {}):
        str_clauses = ''
        tpl_values = ()
        bln_start = True
        #print dct
        for str_field, dct_op_val in dct.iteritems():
            if (str_field is not None):
                if (bln_start):
                    str_open = ' ('
                    bln_start = False
                else:
                    str_open = ' and ('
                str_clauses = ''.join([str_clauses, str_open, str_field, ' ', \
                    dct_op_val['logic'], ' ?)'])
                var_val = dct_op_val['value']
                if (str(var_val).lower() == 'null'):
                    var_val = None
                tpl_values = tpl_values + (var_val, )
            else: # simple 1 or 0 (ALL records or NO records) ...
                # trumps all other clauses, so lets exit the loop
                str_clauses = ' ?'
                tpl_values = (dct_op_val['value'],)
                break
        return (tpl_values, str_clauses)
    else:
        return ((), " 1")

def flat_to_nested(lst, dict_parents, var_root_parent):
    """Bottom-up folding of ordered list into nested list"""

    for i in reversed(xrange(len(lst))):
        lst_node = lst[i]
        id_parent = lst_node[FLD_PARENT_ID]
        if (id_parent != var_root_parent):
            lst_parent = lst[dict_parents[id_parent]]
            # Move this node to the start of its parent's
            # children, creating a child list if needed
            if (len(lst_parent) < INT_ALL_FIELDS):
                lst_parent.append([lst_node])
            else:
                lst_parent[FLD_CHILN].insert(0, lst_node)
            lst.pop(i)

def get_parent_posns(lst):
    """Build a dictionary of the parent locations"""
    
    set_parent = set()
    dict_parent = {}
    # from bottom to top of the ordered node list
    for i in reversed(xrange(len(lst))):
        lst_node = lst[i]
        id_node = lst_node[FLD_ID]
        if (id_node in set_parent):
            dict_parent[id_node] = i 
        set_parent.add(lst_node[FLD_PARENT_ID])            
    return dict_parent

# Convert the captured flat_of from tuples to list format,
# convert the notes from XML to text,
# and escape both notes and text
def strip_note_xml(lst):
    """Extract note text from xml, preserving link urls"""
    
    # Match a link value pair
    keep_links = \
        (re.compile('<value\\ key=\\"link\\">[^a-z/]*([^<]*)</value>')).sub
    # Match remaining value pairs
    strip_values = (re.compile('<value.*?value>')).sub
    # Match remaining tags
    strip_tags = (re.compile('<.*?>')).sub
    # Flip (link)[link_name] to [link_name](link)
    flip_link_parts = (re.compile('(\(.*?\))(\[.*?\])')).sub
    
    for i in range(len(lst)):
        lst_node = list(lst[i])
        var_note = lst_node[FLD_NOTE]
        if var_note is not None:
            lst_node[FLD_NOTE] = \
            flip_link_parts('\\2\\1', strip_tags('', \
                strip_values('', keep_links('(\\1)', var_note))))
        lst[i] = lst_node
    return lst

main()

