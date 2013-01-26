#!/bin/bash
wkg="$HOME/Library/Application Support/Notational Velocity/"
noteprefix="notes-" # specify your own noteprefix
ystday="$wkg/$noteprefix$(date -v-1d "+%Y-%m-%d").txt"
touch "$ystday"
open -a "FoldingText" "$ystday"