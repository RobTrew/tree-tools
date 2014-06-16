
### Automatically complete, pretty-print, and convert MultiMarkdown tables in FoldingText

#### Two Keyboard Maestro macros
- Convert to, or pretty-print, an [MMD Table](https://github.com/fletcher/MultiMarkdown/wiki/MultiMarkdown-Syntax-Guide#tables) (flat or nested)
- Convert from a (flat or nested) MMD table to an MD outline.
[FT Table and Outline.kmmacros](./FT%20Table%20and%20Outline.kmmacros)


### Installation
- If you have installed [Github for Mac ](https://mac.github.com) you should be able to open and install the MK Macros by clicking the open button at the top of [this page]((./FT%20Table%20and%20Outline.kmmacros))
- Otherwise save the plist text on that page as a text file with the .kmmacros extension, and open it in KeyBoard Maestro. 
### Use
- Place your cursor anywhere in rough table or MD outline,
- run one of the two macros from KM.

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

![HTML table from outline](./NestedTablePreview.png)


*The outline and the MMD table text version in FoldingText:*

![MMD table from outline](./OutlineAndMMDTable.png)


***

- [Pair of Keyboard Maestro macros](./FT%20Table%20and%20Outline.kmmacros) for table completion, pretty-printing, and conversion MD Outline ⇄ Nested MMD table. 

