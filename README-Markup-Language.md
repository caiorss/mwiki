# MWiki Markdown/Markup Language Features 

This section describes the MWiki markup language features, which is based on MyST markdown, Obsidian markdown and Media Wiki markup language.

TODO: Add screenshot of wiki syntax code examples.


## Text Formatting 

### Italic Text 

```
  + *text in italic*
```

Rendering:


+ *text in italic*

### Bold Text 

Syntax: 

```
**Bold text here**
```

Example:

```
+ Example of syntax of a **bold text**.
```

Rendering:

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

+ Copyright Symbol ©
+ Copyright Symbol ©
+ Registered Symbol ®
+ Registered Symbol ©
+ Trademark™ symbol
+ Trademark™ symbol
+ The angle is 60° degrees
+ The angle is 60° degrees
+ The price is 30 €
+ The price is 50 £
+ The price is 50 £ (British Pounds)
+ The price is 20 ¥
+ Pilcrow Symbol ¶ or {pagraph}
+ Section Symbol §


## Hyperlinks

### Internal Hyperlinks Links (WikiLinks)

Links to Wiki Pages (also called notes)

```
+ [[Link to internal page]]
```

Rendering: 

+ [[Link to internal page]]


### External Inline Hyperlinks

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


### External Reference-Style Hyperlinks

Example:

```markdown

+ This page presents a study of [control][ceng] engineering and [state-space][ssmodel] models.

[ceng]: https://en.wikipedia.org/wiki/Control_engineering 

[ssmodel]: <https://en.wikipedia.org/wiki/State-space_representation>
      "In control engineering and system identification, a state-space representation is a mathematical model of a physical system specified as a set of input, output, and variables related by first-order differential equations or difference equations. Such variables, called state variables, evolve over time in a way that depends on the values they have at any given instant and on the externally imposed values of input variables. Output variables’ values depend on the state variable values and may also depend on the input variable values."
```

Rendering:


+ This page presents a study of [control][ceng] engineering and [state-space][ssmodel] models.

[ceng]: https://en.wikipedia.org/wiki/Control_engineering 

[ssmodel]: <https://en.wikipedia.org/wiki/State-space_representation>
      "In control engineering and system identification, a state-space representation is a mathematical model of a physical system specified as a set of input, output, and variables related by first-order differential equations or difference equations. Such variables, called state variables, evolve over time in a way that depends on the values they have at any given instant and on the externally imposed values of input variables. Output variables’ values depend on the state variable values and may also depend on the input variable values."

### Special Hyperlinks

 **Hyperlink to Mastodon Handles (User Accounts)**

Syntax:
 
 ```
   @<USERNAME>@<SERVER>
 ```

Creates a hyperlink to a Mastodon user account. For instance, the Mastodon handle (user account)

```
+ @kde@floss.social
```

is rendered to HTML as

```
+  <a href="https://floss.social/@kde" class="link-esternal" ...  >@kde@floss.social</a>
```

In other words, @kde@floss.social is rendered as hyperlink (link for short) to the [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(social_network)) user account of the [KDE project](https://en.wikipedia.org/wiki/KDE) project.

+ [@kde@floss.social](https://floss.social/@kde)


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

 **Hyperlink to Patents**

Syntax:

```
  <patent:$PATENT-NUMBER>
OR
  <r-patent:$PATENT-NUMBER>

```

Exaple:

```markdown
+ Short Link 1: <patent:US9906369>
+ Full Link 1:  <r-patent:US9906369>
+ Short Link 2: <patent:7,139,686>
+ Full Link 2:  <r-patent:7,139,686>
```

Rendering: 


+ Short Link: [Patent USUS9906369](https://patents.google.com/patent/USUS9906369)
+ Full Link: https://patents.google.com/patent/USUS9906369
+ Short Link 2: [Patent US7139686](https://patents.google.com/patent/US7139686)
+ Full Link 2: https://patents.google.com/patent/US7139686



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


 **Hyperlink to CVE - Common Vulnerability Exposures**

This special link syntax allows creating hyperlinks to the CVE (Common Vunerability Exposures) database given a CVE identifier.

Syntax:

```md
 <cve:$CVE_NUMBER>
or
 <CVE:$CVE_NUMBER>
```

Example: the link shortcut

```md
+  <cve:CVE-2024-53104> 
```

is equivalent to the hyperlink 

```md
+ [CVE-2024-53104](https://www.cve.org/CVERecord?id=CVE-2024-53104) 
```

and is rendered to html as 

+  [CVE-2024-53104](https://www.cve.org/CVERecord?id=CVE-2024-53104) 


**Hyperlink to Subreddit**

Syntax:

```
<rd:/r/$NAME-OF-SUBREDDIT>

or

<reddit:/r/$NAME-OF-SUBREDDIT>
```

Example:

```markdown
+ C++ Subreddit <rd:/r/cpp> 
+ <reddit:/r/smalltalk>
```

Rendering:

+ C++ Subreddit [/r/cpp](https://old.reddit.com/r/cpp)
+ [/r/smalltalk](https://old.reddit.com/r/smalltalk) 

The hyperlink `<rd:/r/cpp>` is a hyperlink to

+ https://old.reddit.com/r/cpp 

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


## Embed Uploaded Video Files

MP4 or WEBM video files can be embedded in the current page by using the syntax. 

```
![[video-file-to-be-embedded.mp4]]
```

or

```
![[video-file-to-be-embedded.webm]]
```

Embedded video files are rendered as [\<video\>](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video) html5 embedded element with controls for playing the video, including button for start playing the video, button for stopping the video and so on.

NOTE: It is possible to upload video files directly in the wiki editor by clicking at the button with label 'Link to Uploaded File' in the editor toolbar section 'insert'.


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


## Math and LaTeX Equations
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

### Cross Reference to LaTeX Equations

Equation cross referencing allows linking previously stated equations in paragraphs, mathematical proofs or defintions. This feature reduces the text verbosity and makes it easier to readers to follow the mathematical reasoning. Note that this feature is provided by MathJax LaTeX rendering engine.

Syntax Example:

````markdown

Pendulum position vector $\mathbf{r}(t)$.

$$
  \label{eq_pendulum_position_vector}
  \mathbf{r}(t) = \ell \sin \theta(t) \mathbf{e}_x + \ell \cos \theta(t) \mathbf{e}_y
$$


The velocity of a point mass, a body with negligible dimensions, is given by

$$
   \label{eq_def_velocity}
   \mathbf{v}(t) = \frac{d \mathbf{r}}{dt} = \dot{\mathbf{r}}(t)
$$


Compute the velocity of the pendulum point-mass by replacing $\eqref{eq_pendulum_position_vector}$  in $\eqref{eq_def_velocity}$.

$$
   \mathbf{v}(t) = \frac{d}{dt} [ \ell \sin \theta(t) \mathbf{e}_x + \ell \cos \theta(t) \mathbf{e}_y ]
$$
````

Rendering output:

![](images/latex-equation-cross-reference.png)


In the rendering output, the velocity equation has the number 8.3, which means that it is the 3rd equations of the current wiki page section 8. The last text displays links to the position and velocity equations, which an user can click to go to the referenced equations.


### Latex Macros

It is possible to define LaTeX macros for writing math expressions in a more concise way
by using a code block similar to the example below on the top of the page. This special 
code block is not rendered, it is processed by MathJax or other LaTeX rendering engines.


````markdown
```{latex_macro}
% Logical AND 
\DeclareMathOperator{\\and}{ \\wedge }
% Logical OR
\DeclareMathOperator{\\or}{ \\vee }

 % ---- OR add your OWN LaTeX Macros here ------%%

```
````

After adding the previous macro to the top of the page, one can write logical expressions $\neg (p \wedge q)$, which means not (p and q) or NAND(p, q), in the following form:

```
$$
\neg (p \and q) \equiv \neg p \or q
$$
```


### Graphs with Graphviz 

MWiki has a GraphViz rendering engine, which can render Graphviz [DOT](https://graphviz.org/doc/info/lang.html) markup language to an image diagrams of a graph.

Example this GraphViz code block in DOT language

````{markdown}
```{dot}
graph {
    0 -- 1;
    0 -- 2;
    0 -- 3;
    0 -- 4;
    1 -- 2;
    1 -- 3;
    1 -- 4;
    2 -- 3;
    2 -- 4;
    3 -- 4;
}
```
````

is rendered to

![](images/graphviz-dot.jpg)


**See also:**

+ *GraphViz Pocket Reference*
  + https://graphs.grevian.org/example
+ *Graphviz (dot) examples*
  + https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
    


### Pseudocode of Algorithm

This wiki also supports LaTeX pseudocode of algorithms compatible with LaTeX algorithmic package. The implementation of this feature relies on [pseudocode-js](https://saswat.padhi.me/pseudocode.js/) and [MathJax](https://www.mathjax.org/) JavaScript libraries.

Example:

````latex
```{pseudo}
\begin{algorithm}
\caption{Buble Sort Algorithm}
\begin{algorithmic}
\PROCEDURE{BubbleSort}{$A, n$}
   \STATE $B = $ \CALL{CopyArray}{$A, n$}
   \STATE $\:$ \textit{// i = 0, 1, ..., n - 1}
   \FOR{$i = 0$ \TO  $i < n$}
       \STATE $\:$ \textit{// j = 0, 1, ..., n - 2 }
       \FOR{$j = 0$ \TO $j < n - 1$}
           \IF{$B[j] > B[j+1]$}
               \STATE swap $B[j]$ with $B[j+1]$
           \ENDIF
       \ENDFOR
   \ENDFOR
   \RETURN{$B$}
\ENDPROCEDURE
\end{algorithmic}
\end{algorithm}
```
````

Rendering:


![](images/bubble-sort-agorithm.png)

## Tables 

Example:

```
|  German          |   English         |
|------------------|-------------------|
| Deutsch          | German            |
| ja               | yes               |
| jetzt            | now               |
| nein             | no or not         | 
| hallo Welt       | hello World       |
| hallo Leute      | hello people      |
| willkomen        | welcome           |
| Hilfe            | Help              |
| die Zeit         | time              | 
| die Einstellugen | settings (plural) |
| die Kunst        | art               |
| die Freiheit     | freedom, liberty  |
| die Menschen     | people            |
| die Wirtschaft   | the economy       |
| das Ding         | thing, stuff      |
| das Miteglied    | member            | 
```

Rendering: 

|  German          |   English         |
|------------------|-------------------|
| Deutsch          | German            |
| ja               | yes               |
| jetzt            | now               |
| nein             | no or not         | 
| hallo Welt       | hello World       |
| hallo Leute      | hello people      |
| willkomen        | welcome           |
| Hilfe            | Help              |
| die Zeit         | time              | 
| die Einstellugen | settings (plural) |
| die Kunst        | art               |
| die Freiheit     | freedom, liberty  |
| die Menschen     | people            |
| die Wirtschaft   | the economy       |
| das Ding         | thing, stuff      |
| das Miteglied    | member            | 


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

````markdown
:::{theorem} Determinant of Orthogonal Matrix  

The determinant of a **orthogonal matrix** $Q \in \mathbb{R}^{n \times n}$ of n rows and n columns is always 1.

$$
 \notag 
  \det(Q) = 1
$$


```{proof}

$$
\notag 
\begin{split}
      \det (Q Q^T)      &= \det(Q) \det(Q^{T}) 
   \\ \det (Q Q^T)      &= \det(Q) \det(Q) 
   \\ \det (Q Q^{-1})   &= \det(Q) \det(Q) 
   \\ \det (\mathbf{I}) &= \det(Q)^2
   \\  1                &= \det{Q}^2
   \\  \det(Q)          &= 1
\end{split}
$$
```
% --- end determinant proof ---

:::
````

Rendering:


:::{theorem} Determinant of Orthogonal Matrix  

The determinant of a **orthogonal matrix** $Q \in \mathbb{R}^{n \times n}$ of n rows and n columns is always 1.

$$
 \notag 
  \det(Q) = 1
$$


```{proof}

$$
\notag 
\begin{split}
      \det (Q Q^T)      &= \det(Q) \det(Q^{T}) 
   \\ \det (Q Q^T)      &= \det(Q) \det(Q) 
   \\ \det (Q Q^{-1})   &= \det(Q) \det(Q) 
   \\ \det (\mathbf{I}) &= \det(Q)^2
   \\  1                &= \det{Q}^2
   \\  \det(Q)          &= 1
\end{split}
$$
```
% --- end determinant proof ---

:::

### Example of solved exercise 

````{markdown}
:::{example} Chain Rule for Derivative Multi-Variate Functions

Let the function f be $f(x, y) = x^2/A^2 + y^2/B^2 - C$.  Find the derivative of f with respect to t. And x and y are functions of t, $x = x(t) = A \cos t$ and $y = y(t) = B \sin t$. 


```{solution}   
$$
 \notag 
\begin{split}
  \frac{df}{dt} 
    &= \frac{\partial f}{\partial x} \frac{dx}{dt}  
    + \frac{\partial f}{\partial y} \frac{dy}{dt}  \\

    &=  \frac{\partial}{\partial x} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \cos t)
       \\ & +  \frac{\partial}{\partial y} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \sin t)  \\

    &=  (2x/A^2) (-A \sin t) + (2y/B^2) (A \cos t) \\ 
    &=  -2x \sin(t) / A + 2y \cos(t) / B \\
    &=  -2(A  \cos(t)) \sin(t) / A + 2(B  \sin(t)) \cos(t) / B \\
    &=  -2 \cos t  \sin t  + 2 \sin t  \cos t \\ 
    &=  0 
\end{split}
$$
```
:::
````

Rendering:

:::{example} Chain Rule for Derivative Multi-Variate Functions

Let the function f be $f(x, y) = x^2/A^2 + y^2/B^2 - C$.  Find the derivative of f with respect to t. And x and y are functions of t, $x = x(t) = A \cos t$ and $y = y(t) = B \sin t$. 


```{solution}   
$$
 \notag 
\begin{split}
  \frac{df}{dt} 
    &= \frac{\partial f}{\partial x} \frac{dx}{dt}  
    + \frac{\partial f}{\partial y} \frac{dy}{dt}  \\

    &=  \frac{\partial}{\partial x} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \cos t)
       \\ & +  \frac{\partial}{\partial y} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \sin t)  \\

    &=  (2x/A^2) (-A \sin t) + (2y/B^2) (A \cos t) \\ 
    &=  -2x \sin(t) / A + 2y \cos(t) / B \\
    &=  -2(A  \cos(t)) \sin(t) / A + 2(B  \sin(t)) \cos(t) / B \\
    &=  -2 \cos t  \sin t  + 2 \sin t  \cos t \\ 
    &=  0 
\end{split}
$$
```
:::

## MyST Roles 

The MyST Roles are similar to MyST directives, but they are single line. Exmaple:

Syntax:

```
{rolename}`text content here`
```

### Underline text 

Makes a any text underline.

Example:

```
{u}`underline text`
```

Rendering:

+ {u}`underline text`


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

### Embed Youtube Youtube Video

Embed Youtube video given its ID (Unique Identifier) or URL.

Syntax: 

```
{youtube}`<VIDEO-URL-OR-ID>`
```

Example: Embed video [3 Hours of Most Common Logical Fallacies to Fall Asleep To](https://www.youtube.com/watch?v=bNE4uBMsnP0&t=30s)

```
{youtube}`https://www.youtube.com/watch?v=bNE4uBMsnP0`

or

{youtube}`bNE4uBMsnP0`
```


## Frontmatter (Page Metadata)

The frontmatter is a YAML section at the beginning of MWiki *.md page file within two triple dashes (---), which contains machine-readable metadata of the current wiki page, including, authors, tags, date, description, abbreviations, page settings and other data.


Example: consider the wiki page file

+ 'NAS - Network Attached Storage Device.md'

whose content is

```md
---
author:  John Doe
date:    2022-06-10
description: Survey of NAS - Network Attached Storage devices for reliable backup, data replication and file sharing.

---

Describe what is a NAS 

+ S.M.A.R.T monitoring of disks.
+ SMB file sharing - SAMBA implementation 

...

![[picture-of-synology-nas.png]]

```

### Abbreviations

The frontmatter can be used for defining abbreviations of common words. Consider a wiki page whose the frontmatter is

```
---
author:      John Doe
date:        2022-06-10
description: Survey of NAS - Network Attached Storage devices for reliable backup, data replication and file sharing.
abbreviations:
   NAS:  Network Attached Storage Device
   RAID: Redudant Array of Inexpensive Disks
   NFS:  Network File System 
   SMB:  Server Message Block (Windows shares, also known as network shares)
---
```

Any word defined in the 'abbreviations' section of a YAML frontmatter of a particular wiki page file, it is replaced by the `<abbr>` html5 element. 

For instance if a text of this wiki page is 

```
Most NAS devides provide Web UI for quickly 
creating SMB network shares, windows shared folders.
```

Then, it will be rendered to html as 

```html
Most <abbr title="Network Attached Storage Device">NAS</abbr>  
devides provide Web UI for quickly creating 
<abbr title="Server Message Block">SMB</abbr> network shares, 
windows shared folders.
```

When the mouse is over any abbr text, which has black dashes below it, a pop up window is appears displaying the meaning of the abbreviation. This feature also works on mobile devices, including phones and tablets.

### Wordlinks

The wordlinks feature allows quickly creating hyperlinks for words defined in the **wordlinks** section of a frontmatter of a wiki page. This feature is useful for creating hyperlinks to dictionry definitions or Wikipedia articles related to a particular word. For instance consider the following frontmatter of a Wiki page *.md file.


```md
---
description: Wiki page (note) description here.

abbreviations:
    GUI: Graphics User Interface

wordlinks:
   ZFS:      https://hyperlink-to-wikipedia-of-ZFS
   TrueNAS:  https://link-to-wikipedia-of-TrueNAS

---
```

Whenever the word ZFS appears in any MWiki, paragraph, quote or bullet list, it is replaced by a hyperlink whose label is the word 'ZFS' and the URL is the corresponding URL to this word defined wordlist YAML dictionary. 

For instance, the wiki text 

```md
The file system ZFS is awesome!
```

is rendered to HTML as 

```html
The file system
<a href=" https://hyperlink-to-wikipedia-of-ZFS" ...>ZFS</a>
is awesome.
```

The advantage of this feature allows users to turn words of a MWiki page into hyperlinks without modifying the text or defining the hyperlink multiple times as 

+  `[word](http://hyperlink-of-this-word)`

## Further Reading 

+ https://mystmd.org/guide/admonitions
+ https://mystmd.org/sandbox
   + => Allows testing MyST online without installation.
+ https://myst-parser.readthedocs.io/en/latest/syntax/math.html
+ https://markdown-it-py.readthedocs.io/en/latest/architecture.html
+ https://mystmd.org/guide/glossaries-and-terms