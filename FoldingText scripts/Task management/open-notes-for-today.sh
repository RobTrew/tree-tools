#!/bin/bash
wkg="$HOME/Library/Application Support/Notational Velocity/"
noteprefix="notes-" # specify your own noteprefix
dayfile="$wkg/$noteprefix$(date "+%Y-%m-%d").txt"
touch "$dayfile"
open -a "FoldingText" "$dayfile"