#!/bin/bash
wkg="$HOME/Library/Application Support/Notational Velocity/"
noteprefix="notes-" # specify your own noteprefix
tmrow="$wkg/$noteprefix$(date -v+1d "+%Y-%m-%d").txt"
touch "$tmrow"
open -a "FoldingText" "$tmrow"