#! /usr/bin/env python

from xml.etree import ElementTree
import os, sys, re, argparse, codecs
from subprocess import Popen, PIPE
import datetime, locale

# Ver .014 fixes note bugs

# Known OPML to Standard maps (possibly with matching translate)
# _status -- > done or flagged ?

# Each map entry gives a key translation, a data transformation function name, a type and a comment
DCT_READ_MAP = {
    '_note':('note', str, None, None), 
    'Duration':('duration', int, 'fn_durn2secs', 'measured in seconds (integer)'),
    '_status':('done', bool, 'fn_oostatus2bool', 'interpret as @done ? @flagged ?'), 
    'ft_type':('mdtype', str, None, 'heading, ordered, unordered, blockquote, \
        codeblock, linkdef, property, line, term, definition, \
        horizontalrule, or empty' )
}
LST_MAP_KEYS = []
LST_SCOPE = globals()

HRS_PER_DAY = 8
DAYS_PER_WEEK = 5

LOCAL_DATE_PATTERN = ''

def main():
    """Read an OPML file, and write it out as FoldingText
    with the top N levels of the outline as hash headers,
    and nested tab-indented unordered (hyphen prefixed) 
    lists beyond"""
    global LST_MAP_KEYS, LST_SCOPE, LOCAL_DATE_PATTERN
       
    os.environ["PYTHONIOENCODING"]='UTF-8'
    # export PYTHONIOENCODING='UTF-8'

    parser = argparse.ArgumentParser()
    parser.add_argument('--infile, -i', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--outfile, -o', nargs='?', default=sys.stdout)
    parser.add_argument('--headlevels, -N', nargs='?', type=int, default=0)

    args = parser.parse_args()
    # print args
    dct_args = vars(args)
           
    lst_nodes = read_opml(dct_args['infile, _i'])
    dct_args['infile, _i'].close()
   
    int_head_levels = dct_args['headlevels, _N']
    str_ft = ft_doc(lst_nodes, int_head_levels, int_head_levels - 1)
    
    if (type(dct_args['outfile, _o']).__name__ != 'file'):
        str_path = os.path.expanduser(dct_args['outfile, _o'])
        tmp_file = codecs.open(str_path, "w", 'UTF-8')
        tmp_file.write(str_ft)
        tmp_file.close()
    else: # Write to stdout. Bug: ASCII codec
        dct_args['outfile, _o'].write(str_ft, )
        dct_args['outfile, _o'].close()


# FT WRITER
def ft_doc(lst, int_headings, int_remaining):
    """Write out the nested list in FoldingText format
    with the top N levels (int_headings) as hash headings
    and any levels below as tab-indented unordered MD lists.
    Recursive.
    Note that in the top level call called int_remaining should be 
    int_headings - 1"""
    str = ''
    
    # set the level of hash headings or tab  indents
    bln_header = (int_remaining >= 0)
    if (bln_header):
        int_level = int_headings - int_remaining
        str_note_indent = '\t'
    else:
        int_level = (0 - int_remaining) - 1
        str_note_indent = '\t' * (int_level + 1)
    
    for peer in lst:
        [str_text, dct_props, lst_chiln] = peer
        lst_keys = dct_props.keys()
        # Apply hash header or tab-indent
        if (bln_header):
            str = ''.join([str, '#' * int_level ,' ', str_text])
        else:
            str = ''.join([str, '\t' * int_level ,'- ', str_text])
        
        # Append any @done tags
        if ('done' in lst_keys):
            str = ''.join([str, ' @done'])
        
        # End the line
        str = ''.join([str, '\n'])
        
        # Add any note, with the right number of tabs before each line
        if ('note' in lst_keys):
            for str_line in dct_props['note'].split('\n'):
                str = ''.join([str, str_note_indent, str_line, '\n'])

        # Recurse with any children
        if (len(lst_chiln) > 0):
            str = ''.join([str, ft_doc(lst_chiln, int_headings, int_remaining - 1)])
    return str
        
    
# OPML READER
def read_opml(f):
    """Read an OPML file into a nested list"""
    global LST_MAP_KEYS, LST_SCOPE
    # str_file = os.path.expanduser(str_bash_path)
    
    # Open and parse it to a tree structure
    # with open(str_file, 'rt') as f:
    tree = ElementTree.parse(f)
          
    root = tree.getroot()
    lst_body = root[1] # body is a list
    
    LST_MAP_KEYS = DCT_READ_MAP.keys()
    # print 'keys:', LST_MAP_KEYS
    LST_SCOPE = globals().copy
   
    [lst_nodes, lng_Next] = opml_to_nodes(lst_body, 0, 0)
    return lst_nodes

# [str_text, dct_props, lst_chiln]
def opml_to_nodes(xml_lst, int_parent, int_level):
    """Maps xml elementTree to normalised nested list"""
    int_index = int_parent + 1
    int_sibindex = 0
    lst = []
    int_next_level = int_level + 1
    for xml_node in xml_lst:
        # Check that this is an OPML node,
        if (xml_node.tag != 'outline'):
            sys.exit(''.join([xml_node.tag, \
            " node found: not expected in an OPML file"]))
        
        # get the indices and the text,
        dct_attrib = xml_node.attrib
        lst_keys = dct_attrib.keys()
        
        # GET THE TEXT
        if ('text' in lst_keys):
            lst_node = [dct_attrib['text']]
        else:
            sys.exit(" text attribute missing in outline node ...")
            
        # BEGIN THE DICTIONARY WITH CALCULATED PROPERTIES,
        dct_props = {'index':int_index, 'index_parent':int_parent, \
            'index_sibling':int_sibindex, 'level_nest':int_level}
        # ADD IMPORTED PROPERTIES,
            # applying any known maps for a given key
            # and any defined translations that key
        dct_tags = {}
        for str_key in lst_keys:
            # print str_key, LST_MAP_KEYS
            if (str_key != 'text'):
                if (str_key in LST_MAP_KEYS):
                    # print "key found"
                    (var_tr_key, var_type, var_tr_fn) = DCT_READ_MAP[str_key][:3]
                    # print (var_tr_key, var_type, var_tr_fn)
                    # translate the key ?
                    if (var_tr_key is not None):
                        str_tr_key = var_tr_key
                    else:
                        str_tr_key = str_key
                        
                    # reformat the value ?
                    if (var_tr_fn is not None):
                        # look for the specified function
                        try:
                            fn_trans = LST_SCOPE()[var_tr_fn]
                        except:
                            sys.exit("Function %s() not implemented" % var_tr_fn)
                        
                        # derive a new value by applying the specified function
                        var_value = fn_trans(dct_attrib[str_key])
                        dct_props[str_tr_key] = var_value
                    else:
                        dct_props[str_tr_key] = dct_attrib[str_key]
                # otherwise just pass both through as tag/value pairs
                else:
                    dct_tags[str_key] = dct_attrib[str_key]
        
        dct_props['tags'] = dct_tags
        lst_node.append(dct_props)
        
            
        # AND TRANSLATE ANY CHILDREN
        if (len(xml_node) > 0):
            [lst_chiln, int_index] = opml_to_nodes(xml_node, int_index, int_next_level)
        else:
            lst_chiln = []
            int_index = int_index + 1
        lst_node.append(lst_chiln)
        lst.append(lst_node)
        
        # and increment the sibling count
        int_sibindex = int_sibindex + 1
            
    return [lst, int_index]


# FIELD TRANSLATION FUNCTIONS - MAY BE SHARED BETWEEN READ CLASSES
def local_datetime_pattern():
    """Get the local date formats"""
    return locale.nl_langinfo(locale.D_FMT), locale.nl_langinfo(locale.T_FMT)

def fn_oostatus2bool(str_status):
    """Convert OmniOutliner checked/unchecked to boolean"""
    return (str_status == 'checked')

def fn_durn2secs(str):
    """Convert strings like 4h into seconds. w|d|h|m|s
        Uses two globals: HRS_PER_DAY and DAYS_PER_WEEK
    """
    lst_parts = re.compile('(w|d|h|m|s)').split(str)
    # print lst_parts
    str_unit = lst_parts[1]
    num_units  = float(lst_parts[0])
    if (str_unit == 's'):
        return num_units
    elif (str_unit == 'm'):
        return int(num_units * 60)
    elif (str_unit == 'h'):
        return int(num_units * 3600)
    elif (str_unit == 'd'):
        return int(num_units * 3600 * HRS_PER_DAY)
    elif (str_unit == 'w'):
        return int(num_units * 3600 * HRS_PER_DAY * DAYS_PER_WEEK)

main()
    