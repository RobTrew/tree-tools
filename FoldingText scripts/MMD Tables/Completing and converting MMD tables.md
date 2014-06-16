##Is converted to:

### Convert between MD Outline and Nested MultiMarkdown table formats.

Two Keyboard Maestro macros:
- Convert to, or pretty-print, an MMD table (flat or nested)
- Convert from a (flat or nested) MMD table to an MD outline.

#### Pretty-print as MMD table 
##### (from selected rough table or md outline)
 
- Performs automatic completion and monospaced pretty-printing of an **existing MMD table** containing the cursor,

```
alpha|beta|gamma
1|23|45
7|8|9
```

Is converted to:

```
| alpha | beta | gamma |  
|:-----:|:----:|:-----:|  
|   1   |  23  |   45  |  
|   7   |  8   |   9   |  
```

| alpha | beta | gamma |  
|:-----:|:----:|:-----:|  
|   1   |  23  |   45  |  
|   7   |  8   |   9   |  


- or converts a **Markdown outline** containing the cursor to a nested MMD table.

```
# Three Sections
- Section One
	- 1
	- 4
	- 9
- Section Two
	- 16
	- 25
	- 36
- Section Three
	- 49
	- 64
	- 81
```

Is converted to:

```
|              Three Sections             |||||||||  
|:---:|:--:|:--:|:---:|:--:|:--:|:---:|:---:|:---:|  
| Section One ||| Section Two ||| Section Three |||  
|  1  | 4  | 9  |  16 | 25 | 36 |  49 |  64 |  81 |  
```

|              Three Sections             |||||||||  
|:---:|:--:|:--:|:---:|:--:|:--:|:---:|:---:|:---:|  
| Section One ||| Section Two ||| Section Three |||  
|  1  | 4  | 9  |  16 | 25 | 36 |  49 |  64 |  81 |  




#### Convert (nested or flat) table to outline

- Reverses the kind of outline → nested table conversion above (gives an automatic table → outline conversion)

Place the cursor anywhere in a simple MD outline or a nested MMD table, and run one of these Keyboard Maestro macros.

The **→ Table** script can also be used to pretty-print or complete a partially specified MMD table (nested - with some parent cells spanning child cells - or flat/tabular)

The **→ Outline** script translates the nesting structure of the selected MMD table to an outline combining hash headings with tab-indented lists.


*Example of a source outline and a table generated from that outline (previewed in Marked):*

![HTML table from outline](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/MMD%20Tables/NestedTablePreview.png)


*The outline and the MMD table text version in FoldingText:*

![MMD table from outline](https://raw.github.com/RobTrew/tree-tools/master/FoldingText%20scripts/MMD%20Tables/OutlineAndMMDTable.png)


***

- [Pair of Keyboard Maestro macros](https://github.com/RobTrew/tree-tools/tree/master/FoldingText%20scripts/MMD%20Tables) for conversion MD Outline ⇄ Nested MMD table. 

