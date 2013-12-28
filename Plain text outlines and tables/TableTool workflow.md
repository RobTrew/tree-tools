### Table Tool Workflow ###


An experimental workflow for tidying spanning (and flat) tables in Fletcher Penney's MultiMarkdown Composer.

MMC 2.6's built-in **Format > Clean up Selected Table(s)** currently works best with non spanning tables. It removes any spans, normalising a table back to a non-spanning (non-nested) grid.
.
I happen to use MMD spanning tables quite a lot, so this workflow tidies the selected table, preserving any spanning and, in the interests of laziness and quick typing, also attempting to to correct or complete under-specified tables.

To try it select a table in MultiMarkDown Composer, and run the Automator Workflow.

#### Examples ####


    1|2|3

→

![Simplest](https://github.com/RobTrew/tree-tools/blob/master/Plain%20text%20outlines%20and%20tables/Spanning.png?raw=true)

    Spanning title
    First stage|||second stage|||third stage
    alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota

→

![Spanning]()

