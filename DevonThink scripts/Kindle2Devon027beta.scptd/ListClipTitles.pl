#!/usr/local/bin/perl -w
use strict;

my $numArgs = $#ARGV + 1;

if ( $numArgs < 1 ) {
    print "Arguments expected: <path to Clippings.txt> \n";
    exit;
}

my $src_path;

$src_path = $ARGV[0];

open( SOURCEFILE, "<", $src_path )
  or die "Could not open file $src_path $!";

my ( $mkd_from, $mkd_to ) = ( 0, 0 );

# my $delim = "\t";
my $row = 0;

# my $start = 1;
my $work = "";
my $type = "";

my @date;

# my $text = "";
# my $rec  = "";
# my ( $ss, $mm, $hh, $day, $month, $year, $zone );
my @authors;
my $dump;

my %seen = ();
my @uniq = ();

while ( my $line = <SOURCEFILE> ) {

    #Strip the BOM bytes used by windows notepad etc
    #if ($line =~ s/^\x{EF}\x{BB}\x{BF}//) {print "-->$line"};
    $line =~ s/^\x{EF}\x{BB}\x{BF}//;

    if ( $line =~ m/^====/ ) {

        # ADD THE AUTHOR/TITLE TO THE LIST UNLESS ALREADY SEEN
        if ( $type ne 'Bookmark' ) {

            push( @uniq, $work )
              unless $seen{$work}++;

            # my $dump = unpack( "H*", $work );
            #             push( @uniq, $dump )
            #               unless $seen{$dump}++;
            #
            #             print unpack( "H*", $work )

        }

        $row = 0;
    }
    else { $row += 1 }

    if ( $line =~ m/^(.*\S)\s*$/ ) { $line = $1; }

    # READ TITLE + HEADER
    if ( $row == 1 ) {
        $work = $line;
    }
    elsif ( $row == 2 ) {
        $line =~ m/(Highlight|Note|Bookmark)/;
        $type = $1;
    }

}

# PRINT OUT THE FULL LIST OF TITLE/AUTHORS

foreach (@uniq) {
    print "$_\n";
}

close(SOURCEFILE);

