## MWiki Markup Language Reference Card 

MWiki markup language, also known as MWiki wikicode, is a based on Github-flavored Markdown (GFM). The markup language also is inspired by MyST markdown from Jupyter Book project, Obsidian markdown format and Mediawiki's markup language.

## Text Formating 
### Italic Text 

```
   *text in italic*
```

Rendering:


*text in italic*

### Bold Text 

Syntax: 

```
**Bold text here**
```

Example:

```
+ Example of syntax of a **bold text**.
```

+ Example of syntax of a **bold text**.

### Strikethrough Text (Deleted Text) 

Example:

```
+ Example of ~~Deleted text~~ syntax.  
```
Rendering: 

+ Example of ~~Deleted text~~ syntax.  


### Highlighted Text 

A highlighted text must be enclosed by `==`. Example:

```
this ==text will be higlighted== and remaining of the text.  
```

Rendering:

this ==text will be higlighted== and remaining of the text.  

## Typographic Notation 

MWiki can convert ascii notation, such as `(C)` to the copyright unicode symbol, `(TM)` to trademark unicode symbol and other notations to the equivalent unicode symbol.

Example:

```
+ Copyright Symbol (C)
+ Copyright Symbol {C}
+ Registered Symbol (R)
+ Registered Symbol (C)
+ Trademark(TM) symbol
+ Trademark{TM} symbol
+ The angle is 60{deg} degrees 
+ The angle is 60{degrees} degrees 
+ The price is 30 {euros}
+ The price is 50 {pounds}
+ The price is 50 {gbp}  (British Pounds)
+ The price is 20 {yens}
+ Pilcrow Symbol {pilcrow} or {pagraph}
+ Section Symbol  {section}
```

Rendering:

+ Copyright Symbol (C)
+ Copyright Symbol {C}
+ Registered Symbol (R)
+ Registered Symbol (C)
+ Trademark(TM) symbol
+ Trademark{TM} symbol
+ The angle is 60{deg} degrees 
+ The angle is 60{degrees} degrees 
+ The price is 30 {euros}
+ The price is 50 {pounds}
+ The price is 50 {gbp}  (British Pounds)
+ The price is 20 {yens}
+ Pilcrow Symbol {pilcrow} or {pagraph}
+ Section Symbol  {section}

## Hyperlinks 

### Internal Links

*Link to Wiki Page (also called note)

```
+ [[Link to internal page]]
```

Rendering: 

+ [[Link to internal page]]


### External Links

**Raw External Link (1)**

```
+ <https://www.site.com/some/page>
```

Rendering:

+ https://www.site.com/some/page


**Raw External Link (2)**

```
+ <https://www.site.com/some/page>
```

Rendering:

+ <https://www.site.com/some/page>


**External Link with Label**

```
+ [Link label](https://www.site.com/some/page)
```
Rendering:

+ [Link label](https://www.site.com/some/page)

### Special Links


 **Hyperlink to DOI - Digital Object Identifier (1)**

Syntax:

```
  <doi:$DOI-BIBLIOGRAPHIC-REFERENCE>
```

Example:

```
+ Reference: Time Aware Least Recent Used (TLRU) cache management policy in ICN  <doi:10.1109/ICACT.2014.6779016> 
```

Rendering:

+ Reference: Time Aware Least Recent Used (TLRU) cache management policy in ICN  <doi:10.1109/ICACT.2014.6779016> 

When this DOI hyperlink is rendered, it is expanded to:

```
https://doi.org/10.1109/ICACT.2014.6779016
```

 **Hyperlink to DOI - Digital Object Identifier (2)**

This syntax when rendered yields the raw hyperlink, whose label is the DOI URL.

Syntax:

```
  <r-doi:$DOI-BIBLIOGRAPHIC-REFERENCE>
```

Example:

```
+ Paper: *Time Aware Least Recent Used (TLRU) cache management policy in ICN*
  + <r-doi:10.1109/ICACT.2014.6779016> 
```

Rendering:

+ Paper: *Time Aware Least Recent Used (TLRU) cache management policy in ICN*
  + <r-doi:10.1109/ICACT.2014.6779016> 

**Hyperlink to ArXiv paper**

Syntax:

```
  <arxiv:$ArXivID>
OR:
  <arXiv:$ArXivID>
```

Example:

```
+ See this paper:  <arxiv:1609.06088> - *Time Derivative of Rotation Matrices: a Tutorial*, shiyu zhao, (2016)  
```

Rendering:

+ see this paper:  <arxiv:1609.06088> - *time derivative of rotation matrices: a tutorial*, shiyu zhao, (2016)  


The hyperlink `<arxiv:1609.06088>` when rendered is expanded to following hyperlink.

```
https://arxiv.org/abs/1609.06088
```

**Hyperlink to ArXiv paper (Full Hyperlink)**

Example: 

```
+ *Time Derivative of Rotation Matrices: a Tutorial*, Shiyu Zhao, (2016)  
  + <r-arxiv:1609.06088>
```

Rendering:

+ *Time Derivative of Rotation Matrices: a Tutorial*, Shiyu Zhao, (2016)  
  + <r-arxiv:1609.06088>


**Hyperlink to Semantic Scholar** 

This syntax generates a hyperlink to a research paper listed in Semantic Scholar by its Semantic-Scholar Identifier (ID).

```
<S2CID:$SEMANTIC-SCHOLAR-ID> 

  OR:
 
<r-S2CID:$SEMANTIC-SCHOLAR-ID>  
   => Display hyperlink as Link label
```

Example: 

```

+ See this article: *Secure Distribution of Protected Content in Information-Centric Networking* - <S2CID:198967720>

```

Rendering:

+ See this article: *Secure Distribution of Protected Content in Information-Centric Networking* - <S2CID:198967720>


**Hyperlink to PubMed Paper by PubMed Id (Pmid)**

This type of special short hyperlink allows to create a link to research papers in PubMed Central database by using the PMID - PubMed of the research paper.

Syntax: 

```
  <pmid:$PUB-MED-ID-HERE>
```

Example: 

```
+ Reference: *Teaching population health: a competency map approach to education* <pmid:23524919>
```

Rendering:

+ Reference: *Teaching population health: a competency map approach to education* <pmid:23524919>

The special hyperlink `<pmid:23524919>` is expanded to:

```
https://pubmed.ncbi.nlm.nih.gov/23524919
```

**Hyperlink to PubMed Paper by PubMed Id (Pmid) - (Full Link)**


Example: 

```
+ *Teaching population health: a competency map approach to education* 
  + <r-pmid:23524919>
```

Rendering:

+ *Teaching population health: a competency map approach to education* 
  + <r-pmid:23524919>

 **Hyperlink to Patent**

Syntax:

```
  <patent:$PATENT-NUMBER>
OR
  <r-patent:$PATENT-NUMBER>

```

Exaple:

```markdown
+ Short Link: <patent:US9906369>
+ Full Link: <r-patent:US9906369>
```

Rendering: 

+ Short Link: <patent:US9906369>
+ Full Link: <r-patent:US9906369>


 **Hyperlink to RFC Standard**

Special link to RFC (Request for Comment) technical standards proposed by the IETF (Internet Engineering Task Force).

Syntax: 

```
    <rfc:$RFC-NUMBER> => Short Link
  <r-rfc:$RFC-NUMBER> => Link as label 
```


Example:

```
+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

+ See <r-rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content
```

Rendering:

+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

+ See <r-rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content


 **Hyperlink to PEP (Pyhton Enhancement Proposal)**

Syntax: 

 ```
   <pep:$PEP-NUMBER>
OR:
   <r-pep:$PEP-NUMBER>
 ```

Example:

```
+ See: Python WSGI - Webserver Gateway Interface  <pep:333> 
+ See: Python WSGI - Webserver Gateway Interface  <r-pep:333> 
```

Rendering:

+ See:  Python WSGI - Webserver Gateway Interface  <pep:333> 
+ See: Python WSGI - Webserver Gateway Interface  <r-pep:333> 

 **Hyperlink to Python Package**

Syntax: 

 ```
   <pypi:$PACKAGE-NAME>
OR:
   <r-pypi:$PACKAGE-NAME>
 ```

Example:

```
+ Pyhton <pypi:sqlitedict> package 
+ Python sqltedict package, available at <r-pypi:sqlitedict>
```

Rendering:

+ Pyhton <pypi:sqlitedict> package 
+ Python sqltedict package, available at <r-pypi:sqlitedict>

## Image 
### Internal Image 

The syntax for internal Wiki images is based on Obsidian's markdown syntax for embedding files on pages. It is not necessary to specify the full path or relative path of an image file as it will be displayed regardless of the sub directory it is located within the wiki pages repository. 

Syntax:

```
![[image_file.png]]

Or 

![[relative/path/to/images/image_file_name.png]]
```

### External Image 

Hyperlink to external image. The image URL can be a relative URL as shown in the example below or a URL of type `https://www.site.com/files/image.png `.

Syntax:

```
![$IMAGE-ALT-TEXT-DESCRIPTION]($IMAGE-URL)
```

Example:

```
![Java's Duke Mascot](/static/example_java_duke_mascot.svg)
```

Rendering: 

![Java's Duke Mascot](/static/example_java_duke_mascot.svg)


## Code Blocks 
### Inline code 

Inline code must be surrounded by backtick character (\`).

Example:

```
+ The wiki syntax `<rfc:7231>` is rendered to a hyperlink to 
http 1.1 standard from IETF <rfc:7231>
```

Rendering:

+ The wiki syntax `<rfc:7231>` is rendered to a hyperlink to 
http 1.1 standard from IETF <rfc:7231>

### Code Block 

Example python source code block:

````markdown
```python
# Code for listing root directory 
import os 
for x in os.listdir("/"):
    print(x)
```
````

Rendering:

```python
# Code for listing root directory 
import os 
for x in os.listdir("/"):
    print(x)
```

## Quotes 

 **Quotion Syntax**

Example:

```markdown
> Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984
```

Rendering:

> Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984

 **Quotation Syntax Using Code Block**

Example:


````
```{quote}
Let us change our traditional attitude to the 
construction of programs: Instead of imagining that 
our main task is to instruct a computer what to do, 
let us concentrate rather on explaining to humans 
what we want the computer to do.
  -- Donald E. Knuth, Literate Programming, 1984
```
````

Rendering:

```{quote}
Let us change our traditional attitude to the 
construction of programs: Instead of imagining that 
our main task is to instruct a computer what to do, 
let us concentrate rather on explaining to humans 
what we want the computer to do.
  -- Donald E. Knuth, Literate Programming, 1984
```


## LaTeX Math Equations
### Inline 

```
Let $x \in \mathbb{R}$ be a real number and $f(x) = \sqrt{x^2 - 10}$.
```

Rendering:

Let $x \in \mathbb{R}$ be a real number and $f(x) = \sqrt{x^2 - 10}$.

### Display Mode 

```
$$
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$
```

Rendering:

$$
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$

### Display Mode Without Enumeration 

```
$$
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$
```

Rendering:

$$
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$

### Display Mode using Code Block Syntax 

Example:

````markdown
```{math}
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
```
````

Rendering:

```{math}
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
```

## Table 

Example:

```
|  German        |   English      |
|----------------|----------------|
| Deustch        | German         |
| ja             | yes            |
| nein           | no or not      |
| hallo welt     | hello World    |
| willkomen      | welcome        |
| Hilfe          | Help           |

```

Rendering: 

|  German        |   English      |
|----------------|----------------|
| Deustch        | German         |
| ja             | yes            |
| nein           | no or not      |
| hallo Welt     | hello world    |
| willkomen      | welcome        |
| Hilfe          | Help           |

## Lists 
### Bullet Lists 

Example: 

```
+ Element 1 
+ Element 2 
  + Element 2.1
  + Element 2.2
+ Element 3
  + Element 3.1
  + Element 3.2
     + Element 3.2.1
     + Element 3.3.1
```

Rendering: 

+ Element 1 
+ Element 2 
  + Element 2.1
  + Element 2.2
+ Element 3
  + Element 3.1
  + Element 3.2
     + Element 3.2.1
     + Element 3.3.1
### Ordered List 

Example:

```
1. Element 1
2. Element 2
   1. Element 2.1
   2. Element 2.2 
3. Element 3
   1. Element 3.1
   2. Element 3.2
   3. Element 3.3
      + Element 3.3.1
      + Element 3.3.2
   4. Element 3.4
4. Element 4
```

Rendering:

1. Element 1
2. Element 2
   1. Element 2.1
   2. Element 2.2 
3. Element 3
   1. Element 3.1
   2. Element 3.2
   3. Element 3.3
      + Element 3.3.1
      + Element 3.3.2
   4. Element 3.4
4. Element 4

### Definition Lists 

Example: 

```
HTML 
   : Hypertext Markup Language 

DOM 
   : Domain Object Model 
   : Object that represents a parsed HTML tag in the memory.

WWW
   : World Wide Web 
```

Rendering: 


HTML 
   : Hypertext Markup Language 

DOM 
   : Domain Object Model 
   : Object that represents a parsed HTML tag in the memory.

WWW
   : World Wide Web 


## Admonitions (Callout Boxes) 
### Info Admonition 


```markdown
:::{info}
Give some information to the user.
:::
```

Rendering:

:::{info}
Give some information to the user.
:::


### Tip Admonition 

```
:::{tip}
Try changing `tip` to `warning`!
:::
```

Rendering:

:::{tip}
Try changing `tip` to `warning`!
:::

### Note Admonition 

```
:::{note}
Make sure to check the relative error before stopping 
the iterations.
:::
```

Rendering:

:::{note}
Make sure to check the relative error before stopping 
the iterations.
:::

### Warning Admonition 

```
:::{warning}

Make sure that device is fully charged before installing the firmware. Otherwise, it the device **may not be able to reboot**.
:::
```

Rendering:

:::{warning}

Make sure that device is fully charged before installing the firmware. Otherwise, it the device may not be able to reboot.
:::


### Foldable Admonition

```
:::{note}
:class: dropdown

This is initially hidden, and can be clicked to be opened when you are viewing the content.
:::
```

Rendering:

:::{note}
:class: dropdown

This is initially hidden, and can be clicked to be opened when you are viewing the content.
:::

### Mathematical Definition Admonition 

Example: 

```
:::{def} Inverse Matrix 
:label: inverse-matrix

The inverse matrix $A^{-1}$ of a matrix $A: n \times n$ is defined as a matrix that when multiplied by the square matrix A yields the identity matrix. Note that not always an inverse matrix of a square matrix Q exists. 

$$
  \notag
   A^{-1} A \triangleq A^{-1} \triangleq \mathbf{I}
$$

:::
```

Rendering:

:::{def} Inverse Matrix 
:label: inverse-matrix

The inverse matrix $A^{-1}$ of a matrix $A: n \times n$ is defined as a matrix that when multiplied by the square matrix A yields the identity matrix. Note that not always an inverse matrix of a square matrix Q exists. 

$$
  \notag
   A^{-1} A \triangleq A^{-1} \triangleq \mathbf{I}
$$

:::

### Mathematical Theorem Admonition 

Example:

````
:::{theorem} Chayley-Hamilton Theorem 
:label: theorem-chayley-hamilton

Any n by n matrix A, whose characteristic polynomial is  
$\beta(s) = \det(s  \mathbf{I} - A)$, satisfy its own  
characteristic equation, so

$$ \notag 

   \beta(A) = A^n + a_{n - 1} A^{n - 1} 
       + \cdots + a_1 A + a_0 \mathbf{I} = 0
$$
:::
````

Rendering:

:::{theorem} Chayley-Hamilton Theorem 
:label: theorem-chayley-hamilton

Any n by n matrix A, whose characteristic polynomial is  $\beta(s) = \det(s  \mathbf{I} - A)$, satisfy its own  characteristic equation, so

$$ \notag 

   \beta(A) = A^n + a_{n - 1} A^{n - 1} 
       + \cdots + a_1 A + a_0 \mathbf{I} = 0
$$
:::


## MyST Roles 

The MyST Roles are similar to MyST directives, but they are single line. Exmaple:

Syntax:

```
{rolename}`text content here`
```

### Abbreviation 

This syntax defines abbreviation of acronyms, that is rendered to an `<abbr>` html5 tag. The description of the acronym is shown in a popup window that appears when the user hoovers the mouse on the the abbreviation element.

Syntax:

```
 {abbr}`$ACRONYM  ($DESCRIPTION)`
```

Example:

```markdown
+ This wiki engine provides a syntax closer to {abbr}`MyST (Markedly Structured Text)`.
+ {abbr}`HTML (Hypertext Markup Language)` is a declarative language.
```

Rendering: 

+ This wiki engine provides a syntax closer to {abbr}`MyST (Markedly Structured Text)`.
+ {abbr}`HTML (Hypertext Markup Language)` is a declarative language.


### Math Role for Inline LaTeX

```
+ The math expression  {math}`x^2 - 10x + 20` the previous function.
```

Rendering:

+ The math expression  {math}`x^2 - 10x + 20` the previous function.

###  Subscript  Role  

```
+ Water: H{sub}`2`O 
```

Rendering:

+ Water: H{sub}`2`O

### Superscript Role 

Superscript Roles:

```
+ The 7{sup}`th` element.
```

Rendering:

+ The 7{sup}`th` element.

## Further Reading 

+ https://mystmd.org/guide/admonitions
+ https://mystmd.org/sandbox
   + => Allows testing MyST online without installation.
+ https://myst-parser.readthedocs.io/en/latest/syntax/math.html
+ https://markdown-it-py.readthedocs.io/en/latest/architecture.html
+ https://mystmd.org/guide/glossaries-and-terms
