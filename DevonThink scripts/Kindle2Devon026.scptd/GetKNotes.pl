#!/usr/local/bin/perl -w
use strict;
use HTML::TokeParser;

# Get an HTML file from the command line
my $numArgs = $#ARGV + 1;
if ( $numArgs < 1 ) {
    print "Arguments expected: <html file>\n";
    exit;
}
my $html = $ARGV[0];

# Define field delimiter
my $delim = "~|~";

my ( $p, $tag, $token, @parts );
my ( $id, $title, $author, $location, $quote, $comment, $klink, $editlink );

# Read the HTML file
$p = HTML::TokeParser->new( shift || $html );

# Extract the fields common to each record:
# TITLE
while ( $tag = $p->get_tag('div') ) {
    if ( $tag->[1]{class} eq 'title' ) {
        $title = $p->get_trimmed_text;
        last;
    }
}

# AUTHOR
while ( $tag = $p->get_tag('div') ) {
    if ( $tag->[1]{class} eq 'author' ) {
        $author = $p->get_trimmed_text;
        $author =~ s/^by //;
        last;
    }
}

# LOOK FOR HIGHLIGHTS FLAGGED AS PERSONAL (RATHER THAN POPULAR)
while ( $tag = $p->get_tag('div') ) {
    if ( $tag->[1]{class} eq 'highlightRow personalHighlight' ) {

        # COLLECT THE NOTES
        while ( $tag = $p->get_tag('span') ) {

            # Get the QUOTE
            if ( $tag->[1]{class} =~
                m/(^highlight|^overlappingPopularHighlight)/ )
            {
                $quote = $p->get_trimmed_text;

                # get the KINDLE LINK
                if ( $token = $p->get_tag('a') ) {
                    $klink = $token->[1]{href};

                    # Parse LOCATION from the link
                    # @parts = split( /[=&]/, $klink );
                    #            $location = $parts[5];
                    $klink =~ m/=(\d{1,})$/;
                    $location = $1;
                }

                # and the COMMENT
                while ( $tag = $p->get_tag('p') ) {
                    if ( $tag->[1]{class} =~ m/^editNote/ ) {

                        # get the comment itself
                        while ( $tag = $p->get_tag('span') ) {
                            if ( $tag->[1]{class} eq 'noteContent' ) {
                                $comment = $p->get_trimmed_text;
                                last;
                            }
                        }

                        # get the ONLINE EDIT LINK
                        if ( $token = $p->get_tag('a') ) {
                            $editlink = $token->[1]{href};
                        }
                        @parts = split( /[=&]/, $editlink );
                        $id = $parts[1];

                    }
                    last;
                }
                print join(
                    $delim,
                    (
                        $id,    $title . ", " .  $author, $location,
                        $quote, $comment, $editlink
                    )
                  ),
                  "\n";
                last;
            }
        }

    }
}

