#!/usr/local/bin/perl -w
use strict;

my $numArgs = $#ARGV + 1;

if ( $numArgs < 1 ) {
    print
"Arguments expected: <path to Clippings.txt> optional: [English|French|German|Italian]\n\n";
    exit;
}

use Date::Parse;
use Date::Language;

# options "English, French, German, Italian"
# defaults read .GlobalPreferences AppleCollationOrder
my ( $src_path, $query, $language );

$src_path = $ARGV[0];
if ( $numArgs > 1 ) { $query = $ARGV[1]; $query = substr( $query, 0, 64 ); }
else                { $query = '' }
if   ( $numArgs > 2 ) { $language = $ARGV[2] }
else                  { $language = 'English' }

if ( $language =~ m/English|French|German|Italian/ ) { }
else {
    print
"Unknown language: $language - Should be one of English|French|German|Italian\n";
    exit;
}

open( SOURCEFILE, "<", $src_path )
  or die "Could not open file $src_path $!";

my ( $mkd_from, $mkd_to ) = ( 0, 0 );

my $delim = "\t";
my $row   = 0;

my ( $work, $type, $position, $page, $location, $loc_from, $loc_to, $tmp ) =
  ( "", "", "", "", "", "", "", "" );

#my ( $ss, $mm, $hh, $day, $month, $year, $zone ) =
#  ( "", "", "", "", "", "", "" );

my @date;

my $text = "";
my $rec  = "";
my ($time);
my $lang = Date::Language->new($language);

#$row = 1;
while ( my $line = <SOURCEFILE> ) {

    #Strip the BOM bytes used by windows notepad etc
    $line =~ s/^\x{EF}\x{BB}\x{BF}//;

    if ( $line =~ m/^====/ ) {
        $line = "";

        $text =~ s/<br>$//;

        if ( $type ne 'Bookmark' ) {
            if ( $query ne '' ) {
                if ( $work =~ m/Irvine/ ) {

                    # print "\nW:";
                    #                    print unpack( "H*", $work );
                    #                    print "\n";
                    #                    print "\nQ:";
                    #                    print unpack( "H*", $query );
                    #                    print "\n";
                }
                #print "Q:$query\n";
                if ( $work =~ m/\Q$query\U/ ) {

                    # print unpack( "H*", $query );
                    #                     print "\n";
                    print join(
                        $delim,
                        (
                            $type,   $work, $page, $loc_from,
                            $loc_to, $time, $text
                        )
                      ),
                      "\n";
                }
            }
            else {
                print join( $delim,
                    ( $type, $work, $page, $loc_from, $loc_to, $time, $text ) ),
                  "\n";
            }
        }
        $text = "";
        $row  = 0;
        $type = "";
    }
    else { $row += 1 }

    # READ TITLE + HEADER
    if ( $row == 1 ) {

        $line =~ m/^(.*)\s*$/;
        $work = $1;
        $work =~ s/\x0D//g;

    }    # READ ENTRY TYPE, PAGE NUMBER, LOCATION OR RANGE, DATE
    elsif ( $row == 2 ) {

        $line =~
          m/(Highlight|Note|Bookmark)(.*)(Loc\..*\d)\s*\|\s*?Added on (.*)$/;

        ( $type, $page, $location, $time ) =
          ( $1, $2, $3, $lang->str2time($4) );

        if    ( $type =~ m/Note/ )      { $type = "c" }
        elsif ( $type =~ m/Highlight/ ) { $type = "q" }

        if ( $location =~ m/Loc\. (\d*?)-(\d*?)\s*$/ ) {
            ( $loc_from, $loc_to ) = ( $1, $2 );

            # Rebuild end of location range from Loc. 2755-57 format
            $loc_to =
              substr( $loc_from, 0, length($loc_from) - length($loc_to) )
              . $loc_to;

        }
        else {
            if ( $location =~ m/(\d*?)$/ ) {
                $loc_from = $1;
                $loc_to   = $1;
            }
            else { ( $loc_from, $loc_to ) = ( $1, $1 ); }
        }

        if ( $page =~ m/ on Page (\d*?) \| / ) {
            $page = $1;
        }
        else { $page = '' }

    }    # READ THE TEXT
    else {
        $line =~ s/^\s//;
        $line =~ s/\n$/<br>/;
        $line =~ s/\t//;
        $text .= $line;
    }

    # Append to record

}

close(SOURCEFILE);

