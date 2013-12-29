Draft script for working with nested and tabular plain text

#### NAME

**mdtreeutil** – Markdown tree utility

#### SYNOPSIS

**mdtreeutil.py** [options]

#### DESCRIPTION

**mdtreeutil** can be used to convert or reformat text outlines and MultiMarkdown tables (flat or nested). It can convert in either direction, and with various options, between MMD tables, CSV data, and (tab-indented or MD/FT) text outlines. 
**Note:** By default the script reads from and writes to the (OS X or iOS **clipboard**). Use the -stdin and/or -stdout options to override this.


#### USAGE 
    mdtreeutil.py [-h] [-v] [-stdin] [-stdout] [-tgt {mmdtable,outline,csv}]
                  [-src {mmdtable,outline,csv}] [-pp {mono,mmc_tabs}]
                  [-hl {0,1,2,3,4,5,6}] [-b {-,*,+,none}] [-dlm DELIMITER]
                  [-q {excel_tab,all,nonnumeric,none}]

Prettyprints or converts between MMD tables, plain text outlines (Markdown /
tabbed), and CSV.

##### Optional arguments:
    -h,--help            show this help message and exit
    -v,--version         show program's version number and exit
    -stdin                specify that input should be read from stdin rather
                            than from the clipboard.
    -stdout               specify that output should go to stdout rather than
                            the clipboard
    - tgt {mmdtable,outline,csv},--targetformat {mmdtable,outline,csv}
                            convert the text to the indicated format and write
                            back to the clipboard or to stdout. Default is
                            mmdtable.
    - src {mmdtable,outline,csv},--sourceformat {mmdtable,outline,csv}
                            force input text to be interpreted using the indicated
                            format (by default, the text's format will be
                            determined from its contents).
    - pp {mono,mmc_tabs},--prettyprint {mono,mmc_tabs}
                            choose between monospaced pretty-printing (default)
                            and MMD Composer elastic tab format for MMD tables
    - hl {0,1,2,3,4,5,6},--hashlevels {0,1,2,3,4,5,6}
                            maximum number of heading hashes for MD outlines.
                            Further outline levels will be tab-indented lists.
                            Specify 0 for plain tabbed outlines.
    - b {-,*,+,none},--bullet {-,*,+,none}
                            bullet character to use for indented outline lists
                            beyond any maximum hash header level. By default, no
                            bullet will be used if--hashlevels is set to 0.
    - dlm DELIMITER,--delimiter DELIMITER
                            delimiter string to use for CSV. CSV output defaults
                            are csv.excel_tab
    - q {excel_tab,all,nonnumeric,none},--csvquote {excel_tab,all,nonnumeric,none}
                            quoting pattern for CSV output. CSV output defaults
                            are csv.excel_tab

#### CAUTIONS

1. Early draft
2. The clipboard access only work on iOS and Unix/Linux platforms

#### HISTORY

*Robin Trew Dec 2013*

#### EXAMPLE OF USE ####

See the [Automator Workflow](https://github.com/RobTrew/tree-tools/blob/master/Plain%20text%20outlines%20and%20tables/readme.md) for tidying and completing spanning/simple tables in Fletcher Penney's excellent MultiMarkdown Composer.
