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

```
**This is a bold text**
```

**This is a bold text**

#### Highlighted Text 

A highlighted text must be enclosed by `==`. Example:

```
this ==text will be higlighted== and remaining of the text.  
```

Rendering:

this ==text will be higlighted== and remaining of the text.  

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


 **Hyperlink to DOI - Digital Object Identifier**

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

**Hyperlink to ArXiv paper**

Syntax:

```
  <arxiv:$ArXivID>
```

Example:

```
+ See this paper:  <arxiv:1609.06088> - *Time Derivative of Rotation Matrices: a Tutorial*, shiyu zhao, (2016)  
```

Rendering:

+ See this paper:  <arxiv:1609.06088> - *Time Derivative of Rotation Matrices: a Tutorial*, shiyu zhao, (2016)  


The hyperlink `<arxiv:1609.06088>` when rendered is expanded to following hyperlink.

```
https://arxiv.org/abs/1609.06088
```

**Hyperlink to PubMed Paper**

Syntax: 

```
  <pubmed:$PUB-MED-ID-HERE>
```

Example: 

```
+ Reference: *Teaching population health: a competency map approach to education* <pubmed:23524919>
```

Rendering:

+ Reference: *Teaching population health: a competency map approach to education* <pubmed:23524919>

The special hyperlink `<pubmed:23524919>` is expanded to:

```
https://pubmed.ncbi.nlm.nih.gov/23524919
```


 **Hyperlink to Patent**

```
  <patent:US9906369>
```

This link syntax is rendered as a hyperlink to the patent number US9906369 provided by Google's patent.

```
  https://patents.google.com/patent/US9906369
```

Rendering: 

 <patent:US9906369>


 **Hyperlink to RFC Standard**

Special link to RFC (Request for Comment) technical standards proposed by the IETF (Internet Engineering Task Force).

Example:

```
+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content
```

Rendering:

+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

The special hyperlink `<rfc:7231>` is expanded to the URL

```
 https://datatracker.ietf.org/doc/html/rfc7231
```

 **Hyperlink to PEP (Pyhton Enhancement Proposal)**

Syntax: 

 ```
   <pep:$PEP-NUMBER>
 ```

Example:

```
+ See: Python WSGI - Webserver Gateway Interface  <pep:333> 
```

Rendering:

+ See:  Python WSGI - Webserver Gateway Interface  <pep:333> 

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

### Quotes 

Example:

```markdown
> Donald E. Knuth on Literate Programming, 1984Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984
```

Rendering:

> Donald E. Knuth on Literate Programming, 1984Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984

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
| hallo welt     | hello world    |
| willkomen      | welcome        |
| Hilfe          | Help           |

```

Rendering: 

|  German        |   English      |
|----------------|----------------|
| Deustch        | German         |
| ja             | yes            |
| nein           | no or not      |
| hallo welt     | hello world    |
| willkomen      | welcome        |
| Hilfe          | Help           |

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

### Math Role for Inline LaTeX

```
+ The math expression  {math}`x^2 - 10x + 20` the previous function.
```

Rendering:

+ The math expression  {math}`x^2 - 10x + 20` the previous function.

###  Subscript  Role  

```
+ H{sub}`2`O 
```

Rendering:

+ H{sub}`2`O, and 4{sup}`th` of July

### Superscript Role 

Superscript Roles:

```
+ Happy  4{sup}`th` of July
```

Rendering:

+ Happy  4{sup}`th` of July


## Further Reading 

+ https://mystmd.org/guide/admonitions
+ https://mystmd.org/sandbox
   + => Allows testing MyST online without installation.
+ https://myst-parser.readthedocs.io/en/latest/syntax/math.html
+ https://markdown-it-py.readthedocs.io/en/latest/architecture.html
+ https://mystmd.org/guide/glossaries-and-terms
