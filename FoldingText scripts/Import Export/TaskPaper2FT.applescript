-- Simple conversion of Taskpaper projects to FoldingText headers-- Open a copy of a Taskpaper file in FoldingText and run this script

tell application "FoldingText"	tell front document		update nodes at path "//matches ':\\s*$'" with changes {|type|:"heading"}	end tellend tell