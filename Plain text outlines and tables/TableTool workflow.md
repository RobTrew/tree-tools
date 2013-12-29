### Table Tool Workflow ###


An experimental [workflow](https://github.com/RobTrew/tree-tools/blob/master/Plain%20text%20outlines%20and%20tables/mmd%20-%20TableTool.workflow.zip?raw=true) for tidying spanning (and flat) tables in Fletcher Penney's MultiMarkdown Composer.

MMC 2.6's built-in **Format > Clean up Selected Table(s)** currently works best with non-spanning tables. It removes any spans, normalising a table back to a non-spanning (non-nested) grid.

I happen to use MMD spanning tables quite a lot, so this workflow tidies the selected table:

1. Preserving any spanning, and, 
2. in the interests of laziness and quick typing, also attempting to to correct or complete under-specified tables.

To try it, select a dummy table in MultiMarkDown Composer, and run the Automator Workflow.

#### Examples ####


    1|2|3

→

![Simplest](https://github.com/RobTrew/tree-tools/blob/master/Plain%20text%20outlines%20and%20tables/Simple.png?raw=true)

    Spanning title
    First stage|||second stage|||third stage
    alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota

→

![Spanning](https://github.com/RobTrew/tree-tools/blob/master/Plain%20text%20outlines%20and%20tables/Span.png?raw=true)

    # Totals

    - Q1
	    - 0.8M
    - Q2
	    - 1.2M
    - Q3
	    - 1.0M
    - Q4
	    - 1.5M

→

    | Totals				||||  
    |:----:	|:----:	|:----:	|:----:	|  
    | Q1	| Q2	| Q3	| Q4	|  
    | 0.8M	| 1.2M	| 1.0M	| 1.5M	|  


![Outline to table conversion](https://raw.github.com/RobTrew/tree-tools/master/Plain%20text%20outlines%20and%20tables/Outline2Table.png)
