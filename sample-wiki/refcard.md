---
title:          MWiki Syntax Reference Card
description:    Notes, examples and documentation about MWiki markup language syntax and constructs. This markup language borrow constructs and syntax from Mediwiki, Obsidian and MyST markdown markup languages.
latex_renderer: mathjax

references:

  - id:        lamport1994
    type:      book
    title:     "LaTeX: a document preparation system"
    year:      1994
    publisher: Addison-Wesley
    edition:   2nd
    author:
        - Leslie Lamport
    url:        https://www.latex-project.org/
    #    - family: Leslie
    #     given:  Lamport

  - id: lesk1997
    type: inproceedings
    title: Computer Typesetting of Technical Journals on  UNIX
    author:
        - Michael Lesk
        - Brian Kernighan
    booktitle: "Proceedings of American Federation of Information Processing Societies: 1977 National Computer Conference"
    pages:    879--888
    year:     1977
    address:  Dallas, Texas

  - type:   online
    id:     brownAngVelocity2017
    author: David Brown
    year:   2017
    title:  Angular Velocity Conversions
    access: 2025-12-29
    url:    https://davidbrown3.github.io/euler-angle-rates.html
    url_archive: https://web.archive.org/web/20201214131302/https://davidbrown3.github.io/euler-angle-rates.html
    abstract: "A common requirement when modelling a dynamics system is the tracking of a bodies orientation. A common way to express orientation is through the use of Euler Angles; a sequence of 3 rotations, starting from some base inertial frame to the moving body. These are also commonly intrinsic, meaning that each sequential rotation is about the previous rotated co-ordinate system, rather than the inertial co-ordinate system. These rotation angles are denoted as: (...)"

  - type:          online
    id:            enwiki:1318221113
    author_type:   organization
    author:        Wikipedia contributors
    title:         Angular velocity tensor
    access:        2025-12-28
    url:    https://en.wikipedia.org/w/index.php?title=Angular_velocity_tensor&oldid=1318221113

  - id: StepneyVerlan2018
    type:  proceedings
    year:   2018
    editor:
        - given: Susan
          family: Stepney
        - given: Sergey
          family: Verlan
    publisher: Springer
    title: "Proceedings of the 17th International Conference on Computation and Natural Computation, Fontainebleau, France"
    series: "Lecture Notes in Computer Science"
    volume: 10867
    address: Cham, Switzerland

  - id: bennet2018
    type:   techreport
    title:  Wasatch Solar Project Final Report
    author:
       - given: Vicki
         family: Bennett
       - given: Kate
         family: Bowman
       - given: Sarah
         family: Wright
    institution:  Salt Lake City Corporation
    address:  Salt Lake City, UT
    number:   DOE-SLC-6903-1
    year:     2018
    month:    sep

  - id:        rempel1956
    type:      phdthesis
    title:     Relaxation Effects for Coupled Nuclear Spins
    school:    Stanford University
    address:   Stanford, CA
    year:      1956
    author:
        - given:  Robert Charles
          family: Rempel

  - id:          blonski2017
    type:        article
    author_type: many
    author:
        - family: Błoński
          given: Piotr
    year:      2017
    title:     Doping with Graphitic Nitrogen Triggers Ferromagnetism in Graphene
    url:       https://stringr.tidyverse.org
    journal:    Journal of the American Chemical Society
    volume:    139
    number:    8
    pages:     3171–3180
    doi:       10.1021/jacs.6b12934
    pmid:      28110530
    url:       http://dx.doi.org/10.1021/jacs.6b12934
    eprint:    http://dx.doi.org/10.1021/jacs.6b12934

  - id:        knuth1986
    type:      book
    title:     The TeX Book
    year:      1986
    publisher: Addison-Wesley Profession
    author: Donald E. Knuth
    #    - family: Knuth
    #      given:  Donald E.



  - id:        lamport2025
    type:      online
    title:     "LaTeX Project Website"
    year:      2025
    access:    2025-05-29
    author:   Leslie Lamport
    #    - given: Leslie
    #      family:  Lamport
    url:        https://www.latex-project.org/

  - id:        knitr2015
    type:      book
    title:     Dynamic Documents with R and knitr
    publisher: Chapman and Hall/CRC
    year:      2015
    edition:   2nd
    isbn:      978-1498716963
    # address:   Boca Raton, Florida
    url:       https://yihui.org/knitr/

  - id:        rstring2025
    type:      manual
    year:      2025
    note:      R package version 1.5.2
    title:     StringR R Package
    url:       https://stringr.tidyverse.org
    author:
        - given:   Hadley
          family:  Wickham

  - id: WatsonCrick1953
    type: article
    author:
        - family: Watson
          given: J. D.
        - family: Crick
          given: F. H. C.
    issued:
      date-parts:
      - - 1953
        - 4
        - 25
    title: 'Molecular structure of nucleic acids: a structure for deoxyribose nucleic acid'
    title-short: Molecular structure of nucleic acids
    container-title: Nature
    volume: 171
    issue: 4356
    page: 737-738
    DOI: 10.1038/171737a0
    URL: https://www.nature.com/articles/171737a0
    language: en-GB



---


## Frontmatter (Page Metadata)

The frontmatter is a [YAML](https://en.wikipedia.org/wiki/YAML) section at the beginning of MWiki *.md page file within two triple dashes (---), which contains machine-readable metadata of the current wiki page, including, authors, tags, date, description, abbreviations an dother page settings.


Example: consider the wiki page file

+ `NAS - Network Attached Storage Device.md`

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


### Content Language

The html lang attribute `<html attr="en">` is used to indicate the content language to web browsers, screen readers and search engines. The lang attribute is the ISO code of the default content language, which is set by the administrator in the settings form. If the content language is not the same as the default one, it is possible to override the content laguage code of the current document using the **language** frontmatter directive.

```yaml
language: <ISO-LANGUAGE-CODE-OF-CURRENT-DOCUMENT>
```

For instance, if the current document language is Spanish, the lang attribute can be overriden using the following directive in the frontmatter, where 'es' is the ISO language code of the Spanish language.

```yaml
language: es
```

### Alternative Document Title 

By default, the title of a wiki page is the same as the related mardown file name without the .md file extension. However, it is possible to change a wiki page title by adding the directive 

```yaml
title:  Name of New title here 
```

to the document frontmatter.

### Section (Heading) Enumeration 

Section enumeration is disabled by default. It can be enabled by adding the following directive to the document frotmatter.

```yaml
section_enumeration: on
```

It can also be explicit disabled by adding

```yaml
section_enumeration: off 
```

or

```yaml
section_enumeration: off
```

### LaTeX renderer

The directive *latex_renderer* allows overriding the default latex rendering engine, that can be changed in the settings page.

Use KaTeX rendering engine:

```yaml
latex_renderer: katex
```

Use MathJax rendering engine:

```yaml
latex_renderer: mathjax 
```


### Equation Enumeration 

Equation enumeration can be enabled using

```yaml
equation_enumeration_enabled: on
```

or disabled by using this directive set to off. If enumeration is disabled, only referenced equations will get an enumeration on the left side of the equation (LaTeX display mode).

```yaml
equation_enumeration_enabled: off  
```


The frontmatter directive 'equation_enumeration_style' allows changing the equation enumeration style.

```yaml
equation_enumeration_style: <style>
```

The following enumeration styles supported:

+ cont or continous  
  + Example: 1, 2, ..., 50
+ section (default)
  + Example:  2.1, 2.10, ..., 2.10, 3.1, 3.2, ..., 3.25
+ subsection  
  + Example: 1.2.1, 1.2.2, ..., 1.2.15, 1.3.1, ..., 1.3.15, ....

More details are provided about this feature in the LaTeX section of this document.


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


## Comments 

### Single Line Comment

Any line starting with '%' percent sign is regarded as single line comment and not rendered. NOTE: It is the same comment syntax of MyST markdown used by Jupyter Book project.

Example:

````{markdown}
% single line comment 
  % Other single line comment

Write something here. This line will be rendered.

% Single line comments are not rendered.
````

Redering:

:::{info} Rendering Result

% single line comment 
  % Other single line comment

Write something here. This line will be rendered.

% Single line comments are not rendered.


:::


### Multi Line Comment 

Mutli line comments are code blocks with `{comment}` tag.

````markdown

Line here.

```{comment}
The multi line comments syntax reuses 
  the syntax of code blocks.
and are not rendered by the markdown processor.
```

Some text after.

````

:::{info} Rendering Result

Line here.

```{comment}
The multi line comments syntax reuses 
  the syntax of code blocks.
and are not rendered by the markdown processor.
```

Some text after.

:::


Multi line comments can also be written using the command **on** for rendering the markdown code enclosed in the comment block without needing to delete the `{comment}` tag and the backticks surrounding the code.


````markdown

Line here.

```{comment} on 
The multi line comments syntax reuses 
  the syntax of code blocks.
and are not rendered by the markdown processor.
```

Some text after.

````

The tag `{command}` can also be written as `{command} off` for enabling the rendering/display of the enclosed code.


## Text Formating 
### Italic Text 

```
  + *text in italic*
```

Rendering:


+ *text in italic*

### Bold Text 

Syntax: 

```markdown 
**Bold text here**
```

Example:

```
+ Example: this is a **bold text**.
```

Rendering:

+ Example: this is a **bold text**.

### Bold Italic Text

Example: 

```markdown
+ A ***bold and italic*** text.
```

Rendering:

+ A ***bold and italic*** text.

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
+ Copyright Symbol {C}
+ Registered Symbol {R}
+ Trademark{TM} symbol
+ The angle is 60{deg} degrees 
+ The angle is 60{degrees} degrees 
+ The price is 30 {euros}
+ The price is 50 {pounds}
+ The price is 50 {gbp}  (British Pounds)
+ The price is 20 {yens}
+ Pilcrow Symbol {pilcrow} or {pagraph}
+ Section Symbol  {section}
+ First item - 1{st} item
+ Second item - 2{nd} item
+ Third item - 3{rd} item
+ Fourth item - 4{th} item 
+ Fifth item - 5{th} item
```

Rendering:

+ Copyright Symbol {C}
+ Registered Symbol {R}
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
+ First item - 1{st} item
+ Second item - 2{nd} item
+ Third item - 3{rd} item
+ Fourth item - 4{th} item 
+ Fifth item - 5{th} item
  
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

 **Hyperlink to Patent**

Syntax:

```
  <patent:$PATENT-NUMBER>
OR
  <r-patent:$PATENT-NUMBER>

```

Example:

```markdown
+ Short Link 1: <patent:US9906369>
+ Full Link 1:  <r-patent:US9906369>
+ Short Link 2: <patent:7,139,686>
+ Full Link 2:  <r-patent:7,139,686> 
```

Rendering: 

+ Short Link: <patent:US9906369>
+ Full Link: <r-patent:US9906369>
+ Short Link 2: <patent:7,139,686>
+ Full Link 2:  <r-patent:7,139,686> 


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

This special link syntax allows creating hyperlinks to the CVE (Common Vulnerability Exposure) database given the CVE unique identifier.

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

+ C++ Subreddit <rd:/r/cpp>
+ <reddit:/r/smalltalk>

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
![Java's Duke Mascot](/mwiki/static/example_java_duke_mascot.svg)
```

Rendering: 

![Java's Duke Mascot](/mwiki/static/example_java_duke_mascot.svg)

### External using Relative URL

The `@root` directive is replaced by MWiki root URL. This feature is useful if MWiki root URl changes, for instance, if is hosted in the URl `https://somedomain.com/p/mwiki`, the MWiki root URL is `/p/mwiki`, so the URL of the Java's Duke mascot image would no longer be

+ `/static/example_java_duke_mascot.svg`

Instead it would be 

+ `/p/mwiki/static/example_java_duke_mascot.svg`

By using the directive `@root`, no matter MWiki's root URL, it will not be necessary to change the image URL in the construct for external images as shown below.

Example:

```
![Java's Duke Mascot](@root/static/example_java_duke_mascot.svg)
```

Rendering: 

![Java's Duke Mascot](@root/static/example_java_duke_mascot.svg)



## Figures 

Figures are images with metadata, including automatic enumeration with optional attributes such as caption (also known as label), unique identifier and alt text (alternative text) for better accessibility.

### Figure of external image

A figure of an external image uses URL (Universal Resource Locator) for external images possibly loaded from other websites. In the following example the image `example_java_duke_mascot.svg` is loaded from a external URL of a ficticious web site `https://some-web-site.com`.

Example:

````markdown
```{figure} /mwiki/static/example_java_duke_mascot.svg
:width: 200px
:alt: Java duke mascot, one of the symbols of the Java programming language.

Java's Duke mascot
```
````

Rendering:


```{figure} /mwiki/static/example_java_duke_mascot.svg
:height: 200px
:alt: Java duke mascot, one of the symbols of the Java programming language.

Java's Duke mascot
```

Or relative to current MWiki's root URL:


````markdown
```{figure} @root/static/example_java_duke_mascot.svg
:width: 200px
:alt: Java duke mascot, one of the symbols of the Java programming language.

Java's Duke mascot
```
````

Rendering:

```{figure} @root/static/example_java_duke_mascot.svg
:width: 200px
:alt: Java duke mascot, one of the symbols of the Java programming language.

Java's Duke mascot
```

### Figure of Internal Image

Example: 

````markdown
```{figure} ![[logo-java-coffee-cup.png]]
:name: unique-identifier-of-the-image-optional
:height: 200px
:alt: An iconic symbol of the Java programming language. Note the alt text should provide a detailed description of the image for better accessibility.

Java coffee cup symbol. 
```
````


Note that internal images can be uploaded by copying and pasting images to the MWiki code editor or by manual upload using the editor button with label 'Link to Uploaded File'. 


Uploading images by copying and pasting images:

Now when an user pastes an image from the clipboard in the wiki editor with Ctrl+V or by clicking with mouse right button for opening the context menu and clicking at paste, the image is uploaded to the server and the editor inserts the following template code for a figure containing a reference to the pasted image `pasted-image-1754432753336.jpg`.

````markdown
```{figure} ![[pasted-image-1754432753336.jpg]]
:name: 
:alt: Optional Alt text (alternative) text for accessibility

Optional Figure caption here.
```
````

Then, then user can change the label/caption, optional alt text, optiona name (unique) identifier for cross referencing and also add the attributes `:width: 150px` or `height: 100px`.


## Videos

### Embed Youtube Video 

Embed Youtube video given its ID (Unique Identifier) or URL.

Syntax: 

```
{youtube}`<VIDEO-URL-OR-ID>`
```

**Example**

Embed video *3 Hours of Most Common Logical Fallacies to Fall Asleep To*, whose URL is 

+ https://www.youtube.com/watch?v=bNE4uBMsnP0


Code example:

```
{youtube}`https://www.youtube.com/watch?v=bNE4uBMsnP0`

or

{youtube}`bNE4uBMsnP0`
```
### Embed Uploaded Video Files

MP4 or WEBM video files can be embedded in the current page by using the syntax. 

```
![[video-file-to-be-embedded.mp4]]
```

or

```
![[video-file-to-be-embedded.webm]]
```

Embedded video files are rendered as [{r}`<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video) html5 DOM element with controls for playing the video, including button for start playing the video, button for stopping the video and so on.

NOTE: It is possible to upload video files directly in the wiki editor by clicking at the button with label 'Link to Uploaded File' in the editor toolbar section 'insert'.


### Video Blocks

Video blocks `{video}` are similar to `{figure}` blocks, they allow embeding videos with metadata.

Syntax for internal videos uploaded to the Wiki. This code is auomtically inserted in the editor after successful upload of a webm or mp4 video.

````markdown
```{video}  ![[name-of-internal-video.webm]]
:name: Unique ID - Identifier.
:alt: Alt text, video description optional metadata.
    
Video caption (also known as label)
```
````

Syntax for external videos.


````markdown
```{video}  https://somedomain.com/files/video.mp4
:name: Unique ID - Identifier.
:alt: Alt text, video description optional metadata.

Video caption (also known as label)
```
````

**Example**

Sample code:

````markdown
```{video}  ![[pendulum-with-viscuous-fricition-simulation.mp4]]

Simulation (animation) of simple pendulum with viscous friction using Runge Kutta 4{th} order method
```
````

Rendering:

```{video}  ![[pendulum-with-viscuous-fricition-simulation.mp4]]

Simulation (animation) of simple pendulum with viscous friction using Runge Kutta 4{th} order method
```


  
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


## Mathematics

### LaTeX renderer (Frontmatter)

The frontmatter's directive *latex_renderer* allows overriding the default rendering engine, that can be changed in the settings page.

Use KaTeX rendering engine:

```yaml
latex_renderer: katex
```

Use MathJax rendering engine:

```yaml
latex_renderer: mathjax 
```

### Equation Enumeration Style (Frontmatter)

MWiki supports the following LaTeX equation enumeration styles

+ cont or continous 
  + Schema: `<equaiton-number>`
  + Example: 20
  + Description:  In this style, equations are enumerated in the order that they are defined without regarding section or subsection numner. For instance, 1, 2, 3,... 25. It might be a good choice for documents with a small number of equations, for instance, less than 100.
+ section  (default)
  + Schema: `<section-number>.<equation-number>`
  + Example: 3.2
  + Description: Equation are enumerated according to their section without considering subsections, for instance, equationsof section 3 are enumerated as 3.1, 3.2, 3.20 until section 4 is defined. Then, equations of section 4 are enumerated as 4.1, 4.2, ..., 4.15 and so on. This style might be a good fit for documents with less than 100 equations per section.
+ subsection  
  + Example:  5.4.20
  + Schema: `<section-number>.<subsection-number>.<equation-number>`
  + Description: Equation are enumerated according to the section and subsection that they are defined. For instance, equations of subsection 3 of section 5 are enumerate 5.3.1, 5.3.2, ..., until the next section or subsection is defined. If there exists the subsection 4 of section 5, then the equations of this subsection will be enumerated as 5.4.1, 5.4.2, ..., 5.4.10 and etc.


The enumeration style can be changed by adding the next line to the document front-matter as shown in the following code example. Note that the front-matter is a human-readable human configuration in the markdown code between the lines containing '---' (three dashes) at the beginning of the page. The enumeration on the left side of each display mode LaTeX equation will only be visible if the directive *equation_enumeration_enabled* is set to **on**, otherwise if it is set to **off**, only equations referenced by `\eqref{labelOfEquation}` will have their enumeration visible.


Front-matter example:

````markdown
```
---
description: Description of the document

equation_enumeration_style:   subsection
equation_enumeration_enabled: on 
  ... ... ... ... ... 
  ... ... ... ... ... 
---
```
````

Example consider the remaining of the page source code below after the front-matter.

+ If **equation_enumeration** is set to **section** (default), the number of equation A is set to 1.1, the number of the equation B is set to 1.2, the number of equation C is set to 1.3, the number of D is set to 1.4
+ If **equation_enumeration** is set to **subsection**, the number of equation A is set to 1.1, the number of equation B is set to 1.2, the number of equation C is set to 1.1.1, the number of D is set to 1.1.2, F's number is set to 2.1.1 and G's number is set to 2.1.2. This enumeration style is best suitable for documents with many equations per section.
+ If the directive **equation_enumeration_enabled** is set to **on**, the enumeration of all equations will be visible, unless there is a `\notag` in the equation LaTeX code.
+ If the directive **equation_enumeration_enabled** is set to **off**, only the enumeration of referenced equations will be visible.

Remaining of the wiki page source after the front-matter.

````markdown
## Section 1 

Introduction ....

$$
   % equation (A)
   f(x) = x^2 - 2x + 10
$$

Root of the equation

$$
   % equation (B)
   x = ....
$$


### Subsection 1.1

Quadratic formula.

$$
   % equation (C)
   x = \frac{-b \pm \sqrt{b^2 - 4ac}}
$$

Cubic function 

$$
  % equation (D)
  f(x) = x^3
$$

## Section 2

### Section 2.1

Equation 1 of section 2.1

$$
  % Equation (F)
  y = 2 x + 10
$$

Equation 2 of section 2.2

$$
  % Equation (G)
   b = y - 10
$$

````


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



### Cross Reference To LaTeX Equations

Example:

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

Redering:

:::{note} Rendering Output

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
:::


### Latex Macros

It is possible to define LaTeX macros for writing math expressions in a more concise way
by using a code block similar to the example below on the top of the page. This special 
code block is not rendered, it is processed by MathJax or other LaTeX rendering engines.


````markdown
```{macros}
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

 
### Special Math Blocks

#### Proof

The block {proof} is used for adding a mathematical proof without cluttering the text.

Example: Proof of orthogonal matrix theorem, that states that if a matrix is orthogonal, then $\det Q = 1$.

````latex
```{proof}
According to the defintion, if a $n \times n$ real matrix is orhtogonal, $Q Q^T = \mathbf{I}$, where $\mathbf{I}$ is a identity matrix, so

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

Hence, if a matrix $Q$ is orthogonal, $\det Q = 1$.
```
````

Rendering:

```{proof}
According to the defintion, if a $n \times n$ real matrix is orhtogonal, $Q Q^T = \mathbf{I}$, where $\mathbf{I}$ is a identity matrix, so

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

Hence, if a matrix $Q$ is orthogonal, $\det Q = 1$.
```

#### Derivation 

The {derivation} is similar to the {proof} foldable block. However, {derivation} is intended for writing derivations of mathematical formulas, the steps to to find or deduce a particular mathematical formula or algorithm. The term *derivation* is more used in physics and engineering than the term *proof*.

Example: 

````markdown
If a body-attached frame with origin in the mass center of a rigid body is aligned to is principal axes of inertia, then the mass moment of inertia tensor will be a diagonal matrix and the products of inertia will be zero. As a result, the Euler's equation for motion for the rigid body rotational motion become

$$
\begin{split}
  \\ I_x \dot{\omega}_x + \omega_y \omega_z (I_z - I_y) &= \tau_x
 \\ I_y \dot{\omega}_y + \omega_x \omega_z (I_x - I_z)
    &= \tau_y
 \\ I_z \dot{\omega}_z + \omega_x \omega_y (I_y - I_x)
    &= \tau_z
\end{split}
$$

```{derivation}
The Euler's equation of motion that relates the torque $\bs{\tau}$, angular velocity $\bs{\omega}$ and angular accleration $\bsdot{\omega}$ is given by

$$
\notag
\mathcal{I} \bsdot{\omega} 
    + \bs{\omega} \times \mathcal{I} \bs{\omega}
    = \bs{\tau}
$$

Express the cross product operator $\times$ as the cross-product matrix operator $\skew{}$.

$$
\notag
\mathcal{I} \bsdot{\omega} + \skew{\bs{\omega}} \mathcal{I} \bs{\omega} = \bs{\tau}
$$
 
  ... ... ... ... ... 

Thus, the equations of motions, for a body frame aligned to the principal axes of inertia, are

$$
\notag
\begin{split}
  \\ I_x \dot{\omega}_x + \omega_y \omega_z (I_z - I_y) &= \tau_x
 \\ I_y \dot{\omega}_y + \omega_x \omega_z (I_x - I_z)
    &= \tau_y
 \\ I_z \dot{\omega}_z + \omega_x \omega_y (I_y - I_x)
    &= \tau_z
\end{split}
$$
```

````

**Rendering:**

If a body-attached frame with origin in the mass center of a rigid body is aligned to is principal axes of inertia, then the mass moment of inertia tensor will be a diagonal matrix and the products of inertia will be zero. As a result, the Euler's equation for motion for the rigid body rotational motion become

$$
\begin{split}
  \\ I_x \dot{\omega}_x + \omega_y \omega_z (I_z - I_y) &= \tau_x
 \\ I_y \dot{\omega}_y + \omega_x \omega_z (I_x - I_z)
    &= \tau_y
 \\ I_z \dot{\omega}_z + \omega_x \omega_y (I_y - I_x)
    &= \tau_z
\end{split}
$$

```{derivation}
The Euler's equation of motion that relates the torque $\bs{\tau}$, angular velocity $\bs{\omega}$ and angular accleration $\bsdot{\omega}$ is given by

$$
\notag
\mathcal{I} \bsdot{\omega} 
    + \bs{\omega} \times \mathcal{I} \bs{\omega}
    = \bs{\tau}
$$

Express the cross product operator $\times$ as the cross-product matrix operator $\skew{}$.

$$
\notag
\mathcal{I} \bsdot{\omega} + \skew{\bs{\omega}} \mathcal{I} \bs{\omega} = \bs{\tau}
$$
 
  ... ... ... ... ... 

Thus, the equations of motions, for a body frame aligned to the principal axes of inertia, are

$$
\notag
\begin{split}
  \\ I_x \dot{\omega}_x + \omega_y \omega_z (I_z - I_y) &= \tau_x
 \\ I_y \dot{\omega}_y + \omega_x \omega_z (I_x - I_z)
    &= \tau_y
 \\ I_z \dot{\omega}_z + \omega_x \omega_y (I_y - I_x)
    &= \tau_z
\end{split}
$$
```

#### Solution 

The solution block is intended for providing solutions of exercises, questions or worked examples.

**Example:**

````markdown
Fit the line $p(x) = \beta_0 + \beta_1 x$ for (1, 2.2), (0.8, 2.4) and (0, 4.25) [(src)](https://people.sc.fsu.edu/~jpeterson/linear_least_squares.pdf).


```{solution}
Define the parameters vector $\mathbf{\beta}$ and $\mathbf{y}$ 

$$
\notag
   \mathbf{\beta} = 
      \begin{bmatrix} \beta_0 \\ \beta_1 \end{bmatrix}
   \quad 
   \mathbf{y} = 
      \begin{bmatrix} 2.2 \\ 2.4 \\ 4.25 \end{bmatrix}
$$

Compute the *design matrix* $X$

$$
\notag

X = \begin{bmatrix}
           1  & x_1
        \\ 1  & x_2
        \\ 1  & x_2
    \end{bmatrix}
    
   = \begin{bmatrix}
           1 & 1
        \\ 1 & 0.8
        \\ 1 & 0
     \end{bmatrix}
$$

Find the solution of $X \mathbf{\beta} = \mathbf{y}$ by determining the least square solution, which can be computed by solving the system of normal equations $(X^T X) \mathbf{\beta} = X^T \mathbf{y}$.

$$
\notag

X' = X^T X 
   = \begin{bmatrix}
            3.0  & 1.8
        \\  1.8  & 1.64
     \end{bmatrix}

\quad

\mathbf{y}' = X^T \mathbf{y} = \begin{bmatrix} 8.85 \\ 4.12 \end{bmatrix}

$$

Solve the system of normal equations $X' \mathbf{\beta} = \mathbf{y}'$.

$$
\notag

 \mathbf{\beta} 
   = \begin{bmatrix} 4.225 \\ -2.125 \end{bmatrix}
$$

So, the line that best fit those data points is

$$
\notag 

p(x) = 4.225 + (-2.125) x
$$
```

````

**Rendering**

Fit the line $p(x) = \beta_0 + \beta_1 x$ for (1, 2.2), (0.8, 2.4) and (0, 4.25) [(src)](https://people.sc.fsu.edu/~jpeterson/linear_least_squares.pdf).


```{solution}
Define the parameters vector $\mathbf{\beta}$ and $\mathbf{y}$ 

$$
\notag
   \mathbf{\beta} = 
      \begin{bmatrix} \beta_0 \\ \beta_1 \end{bmatrix}
   \quad 
   \mathbf{y} = 
      \begin{bmatrix} 2.2 \\ 2.4 \\ 4.25 \end{bmatrix}
$$

Compute the *design matrix* $X$

$$
\notag

X = \begin{bmatrix}
           1  & x_1
        \\ 1  & x_2
        \\ 1  & x_2
    \end{bmatrix}
    
   = \begin{bmatrix}
           1 & 1
        \\ 1 & 0.8
        \\ 1 & 0
     \end{bmatrix}
$$

Find the solution of $X \mathbf{\beta} = \mathbf{y}$ by determining the least square solution, which can be computed by solving the system of normal equations $(X^T X) \mathbf{\beta} = X^T \mathbf{y}$.

$$
\notag

X' = X^T X 
   = \begin{bmatrix}
            3.0  & 1.8
        \\  1.8  & 1.64
     \end{bmatrix}

\quad

\mathbf{y}' = X^T \mathbf{y} = \begin{bmatrix} 8.85 \\ 4.12 \end{bmatrix}

$$

Solve the system of normal equations $X' \mathbf{\beta} = \mathbf{y}'$.

$$
\notag

 \mathbf{\beta} 
   = \begin{bmatrix} 4.225 \\ -2.125 \end{bmatrix}
$$

So, the line that best fit those data points is

$$
\notag 

p(x) = 4.225 + (-2.125) x
$$
```

#### Example Block

Example:


````markdown
The product of two complex numbers $z_1 = a_1 + j b_1$ and 
$z_2 = a_2 + j b_2$ is

$$
z = (a_1 a_2 - b_1 b_2) + j(a_1 b_2 + a_2 b_1)
$$

Where $j = \sqrt{-1}$ is the imaginay root.

```{example}
The product of $z_1 = 5 + j2$ and $z_2 = 3 + j4$  is

$$
z_1 z_2 = (5 * 3 - 2 * 4) + j (5 * 4 + 2 * 3)
$$

$$
z_1 z_2  = 7 + 26j
$$

```
````

**Rendering**

The product of two complex numbers $z_1 = a_1 + j b_1$ and 
$z_2 = a_2 + j b_2$ is

$$
z = (a_1 a_2 - b_1 b_2) + j(a_1 b_2 + a_2 b_1)
$$

Where $j = \sqrt{-1}$ is the imaginay root.

```{example}
The product of $z_1 = 5 + j2$ and $z_2 = 3 + j4$  is

$$
z_1 z_2 = (5 * 3 - 2 * 4) + j (5 * 4 + 2 * 3)
$$

$$
z_1 z_2  = 7 + 26j
$$

```

   
### Definition Admonition 

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
 
### Theorem Admonition 

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
  
### Worked examples

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

### Embedded Jupyter Notebook

Example:

```markdown
![[SimplePendulum.ipynb]]
```

Rendering:

![[SimplePendulum.ipynb]]   

NOTE: that the editor has a button, which allows uploading Jupyter notebooks and inserting alink to the file name at current cursor position.  
## Table 

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


### List of Checkboxes / List of Tasks

Example:

```markdown
+ [x] Implement full text search.
+ [ ] Implement a revision control system.
```

Rendering:

+ [x] Implement full text search.
+ [ ] Implement a revision control system.



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


## Footnotes 

### Footnote Reference 

Syntax 1: Compatible with MyST markdown and Obsidian markdown.

```markdown
+ The motor speed is 300 rmp^[revolutions per minute].
```

Rendering:

+ The motor speed is 300 rmp^[revolutions per minute].

Syntax 2: Only used by MWiki, but it does not conflict with any markdown syntax such as `[label](http://some-site.com)`.

```markdown
+ Ship speed is about 30 knots^{Nautical miles per hour}.
```

Rendering:
+ Ship speed is about 30 knots^{Nautical miles per hour}.

### Footnotes listing

The following code lists all footnotes of current wiki page.

````markdown
```{footnotes}
```
````

Rendering:

```{footnotes}
```

## Citations and List of References

MWiki supports citations based on IEEE style with the following syntax based on Pandoc's citation markup language.

```
$[@CITATION_KEY1; CITATION_KEY2 ; CITATION_KEY3, locator3 ....]
```

**Example:**

```markdown
The molecular structure is (...) $[@blonski2017 ; @enwiki:1318221113]

The systems equation $[@knuth1986; @lamport1994; @lamport2025; @lesk1997] of motion are given by $[@knitr2015, pages:20-25; @rstring2025, chap:10; @rempel1956 ; @bennet2018; @StepneyVerlan2018]

  ... .... ... ... ... ...

According to $[@brownAngVelocity2017], the system's governing equations are given by $[@knitr2015, p:10 eq:20].
```

:::{info} Rendering

The molecular structure is (...) $[@blonski2017 ; @enwiki:1318221113]

The systems equation $[@knuth1986; @lamport1994; @lamport2025; @lesk1997] of motion are given by $[@knitr2015, pages:20-25; @rstring2025, chap:10; @rempel1956 ; @bennet2018; @StepneyVerlan2018]

  ... .... ... ... ... ...

According to $[@brownAngVelocity2017], the system's governing equations are given by $[@knitr2015, p:10 eq:20].

::: 


### Citation Locators

The following citation locators are supported:

| Name       | Syntax                  |  Example          |
| ---------- | ----------------------- | ----------------- |
| Page       | `p:<page-number>`       | `p:10`            |
| Page Range | `p:<page-range>`        | `p:10-20`         |
| Chapter    | `ch:<chapter>`          | `ch:6`            |
| Section    | `sec:<section>`         | `sec:4`           |
| Appendix   | `appendix:<appendix>`   | `appendix:A`      |
| Table      | `table:<table-number>`  | `table:4`         |
| Table      | `tbl:<table-number>`    | `tbl:4`           |
| Figure     | `fig:<figure-number>`   | `fig:10`          |
| Algorithm  | `algorithm:<algorithm>` | `algorithm:10.2`  |
| Algorithm  | `alg:<algorithm>`       | `alg:10.5`        |
| Equation   | `eq:<equation>`         | `eq:1.2.25`       |
| Equation   | `equation:<equation>`   | `equation:1.2.25` |

Usage example: indicate that the citation refers to equation 2.5.10 of a reference, whose citation key is doeJohn1995

```
It can be shown that the mass moment of inertia becomes $[@doejohn1995, eq:2.5.10] ...
```

It is rendered to

+ It can be shown that the mass moment of inertia becomes [10, eq.(2.5.10)]




### List of References

The directive {references} can be used for generating the list cited references in the document as shown in the following example. 

````markdown
```{references}
:style: mwiki
```
````

:::{info} List of references rendering

```{references}
:style: mwiki
```
:::

It is possible to generate the list of references in IEEE style using 

````markdown
```{references}
:style: ieee
```
````

:::{info} List of references rendering in IEEE style

```{references}
:style: ieee
```

:::

### Bibliographic Database

The citation key is a unique identifier of each reference entry in the YAML front matter. Example of bibliographic references database of the front matter in this docuement.

```yaml
references:

  - id:        lamport1994
    type:      book
    title:     "LaTeX: a document preparation system"
    year:      1994
    publisher: Addison-Wesley
    edition:   2nd
    author:
        - Leslie Lamport
    url:        https://www.latex-project.org/
    #    - family: Leslie
    #     given:  Lamport

  - id: lesk1997
    type: inproceedings
    title: Computer Typesetting of Technical Journals on  UNIX
    author:
        - Michael Lesk
        - Brian Kernighan
    booktitle: "Proceedings of American Federation of Information Processing Societies: 1977 National Computer Conference"
    pages:    879--888
    year:     1977
    address:  Dallas, Texas

  - type:   online
    id:     brownAngVelocity2017
    author: David Brown
    year:   2017
    title:  Angular Velocity Conversions
    access: 2025-12-29
    url:    https://davidbrown3.github.io/euler-angle-rates.html
    url_archive: https://web.archive.org/web/20201214131302/https://davidbrown3.github.io/euler-angle-rates.html
    abstract: "A common requirement when modelling ..."

  - type:          online
    id:            enwiki:1318221113
    author_type:   organization
    author:        Wikipedia contributors
    title:         Angular velocity tensor
    access:        2025-12-28
    url:    https://en.wikipedia.org/w/index.php?title=Angular_velocity_tensor&oldid=1318221113

  - id: StepneyVerlan2018
    type:  proceedings
    year:   2018
    editor:
        - given: Susan
          family: Stepney
        - given: Sergey
          family: Verlan
    publisher: Springer
    title: "Proceedings of the 17th International Conference on Computation and Natural Computation, Fontainebleau, France"
    series: "Lecture Notes in Computer Science"
    volume: 10867
    address: Cham, Switzerland

  - id: bennet2018
    type:   techreport
    title:  Wasatch Solar Project Final Report
    author:
       - given: Vicki
         family: Bennett
       - given: Kate
         family: Bowman
       - given: Sarah
         family: Wright
    institution:  Salt Lake City Corporation
    address:  Salt Lake City, UT
    number:   DOE-SLC-6903-1
    year:     2018
    month:    sep

  - id:        rempel1956
    type:      phdthesis
    title:     Relaxation Effects for Coupled Nuclear Spins
    school:    Stanford University
    address:   Stanford, CA
    year:      1956
    author:
        - given:  Robert Charles
          family: Rempel

  - id:          blonski2017
    type:        article
    author_type: many
    author:
        - family: Błoński
          given: Piotr
    year:      2017
    title:     Doping with Graphitic Nitrogen Triggers Ferromagnetism in Graphene
    url:       https://stringr.tidyverse.org
    journal:    Journal of the American Chemical Society
    volume:    139
    number:    8
    pages:     3171–3180
    doi:       10.1021/jacs.6b12934
    pmid:      28110530
    url:       http://dx.doi.org/10.1021/jacs.6b12934
    eprint:    http://dx.doi.org/10.1021/jacs.6b12934

  - id:        knuth1986
    type:      book
    title:     The TeX Book
    year:      1986
    publisher: Addison-Wesley Profession
    author: Donald E. Knuth
    #    - family: Knuth
    #      given:  Donald E.



  - id:        lamport2025
    type:      online
    title:     "LaTeX Project Website"
    year:      2025
    access:    2025-05-29
    author:   Leslie Lamport
    #    - given: Leslie
    #      family:  Lamport
    url:        https://www.latex-project.org/

  - id:        knitr2015
    type:      book
    title:     Dynamic Documents with R and knitr
    publisher: Chapman and Hall/CRC
    year:      2015
    edition:   2nd
    isbn:      978-1498716963
    # address:   Boca Raton, Florida
    url:       https://yihui.org/knitr/

  - id:        rstring2025
    type:      manual
    year:      2025
    note:      R package version 1.5.2
    title:     StringR R Package
    url:       https://stringr.tidyverse.org
    author:
        - given:   Hadley
          family:  Wickham

  - id: WatsonCrick1953
    type: article
    author:
        - family: Watson
          given: J. D.
        - family: Crick
          given: F. H. C.
    issued:
      date-parts:
      - - 1953
        - 4
        - 25
    title: 'Molecular structure of nucleic acids: a structure for deoxyribose nucleic acid'
    title-short: Molecular structure of nucleic acids
    container-title: Nature
    volume: 171
    issue: 4356
    page: 737-738
    DOI: 10.1038/171737a0
    URL: https://www.nature.com/articles/171737a0
    language: en-GB
```

### Further Reading


+ *Citation*, Quarto Docs
  + https://quarto.org/docs/authoring/citations.html
+ *Citation Metadata*, Quarto Docs
  + https://quarto.org/docs/reference/metadata/citation.html
+ *Citations*, Pandoc Manual
  + https://pandoc.org/MANUAL.html#citations
+ *Citation Style Language*
  + https://citationstyles.org/authors/
+ *Citations & Footnotes*
  + https://www.datanovia.com/guide/tools/quarto/citations-and-footnotes.html
+ *CSL 1.0.2 Specification*
  + https://docs.citationstyles.org/en/stable/specification.html#csl-1-0-2-specification
+ *Primer — An Introduction to CSL*, Rintze M. Zelle, PhD
  + https://docs.citationstyles.org/en/stable/primer.html   
+ *Chicago Manual of Style 18th Edition*, Purdue University
  + https://owl.purdue.edu/owl/research_and_citation/chicago_manual_18th_edition/cmos_formatting_and_style_guide/chicago_manual_of_style_18th_edition.html
  + *Please note that although these resources reflect the most recent updates in the The Chicago Manual of Style (18th edition) concerning documentation practices, you can review a full list of updates concerning usage, technology, professional practice, etc. at The Chicago Manual of Style Online.*
+ *Institute of Electrical and Electronics Engineers - IEEE*, Wikipedia
  + https://en.wikipedia.org/wiki/Institute_of_Electrical_and_Electronics_Engineers
+ *Association for Computing Machinery - ACM*, Wikipedia
  + https://en.wikipedia.org/wiki/Association_for_Computing_Machinery
+ *Research and Citation*, Purdue University
  + https://owl.purdue.edu/owl/research_and_citation/index.html
+ *STEM Citation Styles*, University of Nebraska at Omaha
  + https://libguides.unomaha.edu/c.php?g=1439199
+ *Computer Science Research Guide*
  + https://dal.ca.libguides.com/csci/writing/examples
+ *IEEE Reference Style*  
  + https://owl.purdue.edu/owl/research_and_citation/chicago_manual_18th_edition/cmos_formatting_and_style_guide/chicago_manual_of_style_18th_edition.html
+ *IEEE Style - Research and Citation*, Purdue University
  + https://owl.purdue.edu/owl/research_and_citation/ieee_style/index.html
+ *In-Text Citation - IEEE Style - Research and Citation*, Purdue University
  + https://owl.purdue.edu/owl/research_and_citation/ieee_style/in-text_citation.html
+ *Reference List - IEEE Style - Research and Citation**, Purdue University
  + https://owl.purdue.edu/owl/research_and_citation/ieee_style/reference_list.html
  + *References should be provided on a separate page at the end of your paper, with the title “References” at the top of the page. They should be listed and numbered in order of citation, not alphabetically. The numbers should be flush against the left margin, and separated from the body of the reference.*
+ *How to format your references using the Proceedings of the IEEE citation style*
  + https://paperpile.com/s/proceedings-of-the-ieee-citation-style/
+ *Citation Styles by Discipline: STEM*
  + https://paperpile.libguides.com/c.php?g=1226166&p=8971526
+ *Computer Science Style Guide Suggestions*
  + https://dal.ca.libguides.com/csci/writing/examples
+ *Citing Sources: Which citation style should I use?*
  + https://guides.lib.uw.edu/research/citations/citationwhich
+ *Citation*, Brown University Library
  + https://libguides.brown.edu/citations/styles
+ *Online Bibtex Converter*
  + https://asouqi.github.io/bibtex-converter/
  + NOTE: This tool allows converting bibtex to many reference formats, including, APA, Havard, IEE, Elsevier, Springer, ACM, ACS, and MLA.
+ *The 14 BibTeX entry types*, Bibtex
  + https://www.bibtex.com/e/entry-types/
+ *Bibtex bibliography styles*, Overleaf
  + https://www.overleaf.com/learn/latex/Bibtex_bibliography_styles
+ *Bibliography management with bibtex*, Overleaf
  + https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex
+ *Tame the BeaST: The B to X of BibTeX by Nicolas Markey [PDF]*
  + https://www.bibtex.com/g/bibtex-format/
+ *Using bibtex: a short guide by Martin J. Osborne*
  + https://www.economics.utoronto.ca/osborne/latex/BIBTEX.HTM
+ *BibTeXing by Oren Patashnik [PDF]*
  + http://mirror.kumi.systems/ctan/biblio/bibtex/base/btxdoc.pdf
+ *LaTeX Document Preparation System*, Georgia State University
  + https://research.library.gsu.edu/latex/bibtex
+ *BibTeX for LaTeX Guide*, Texas A&M University
  + https://libguides.tamusa.edu/c.php?g=1441028&p=10703447
+ *BibTeX for LaTeX*
  + https://library-guides.imperial.ac.uk/c.php?g=719784&p=5221129 
+ *A BibTEX Guide via Examples*, Ki-Joo Kim (2004)
  + http://www-hep.colorado.edu/~jcumalat/4610_fall_10/bibtex_guide.pdf 
+ *How does BibTex Works - BibTeX*, Purdue University
  + https://guides.lib.purdue.edu/bibtex/basics  
+ *How to Cite a Website in LaTeX Using BibTeX and BibLaTeX*, bibtex\.eu
  + https://bibtex.eu/faq/how-can-i-use-bibtex-to-cite-a-website/
+ *How to Cite a Website in LaTeX Using BibTeX*
  + https://www.getbibtex.com/blog/posts/how-to-cite-website-in-latex-using-bibtex
  + *Learn how to properly cite online sources in LaTeX using BibTeX, with ready-to-use examples and templates.* 
+ *BibTeX generic citation style Referencing Guide*
  + https://citationsy.com/styles/bibtex      
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

Make sure that device is fully charged before installing the firmware. Otherwise, the device may not be able to reboot.
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


 

  
## MyST Roles 

The MyST Roles are similar to MyST directives, but they are single line. Exmaple:

Syntax:

```
{rolename}`text content here`
```

### Raw Text 

This MyST role renders a text to itself without the text being interpreted to anything and without any escape character.


Syntax:

````markdown
{r}`enclosed text` or {raw}`enclosed text`
````

Example: 
```markdown
+ {r}`<a href="https://site.com">label</a>`
```

Rendering:

+ {r}`<a href="https://site.com">label</a>`

Note that the markdown rendered to the enclosed text within backticks "`" and not interpreted as a hyperlink.

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


### Text Notes 

This MyST role (not available by default in MyST) allows adding notes to text that are displayed in a popup window in a similar way to the abbr MyST role for abbreviations.

Syntax:

````markdown
{note}`[TERM or SENTENCE] ([NOTE])`
````

For instance, consider the following markdown code 

````markdown
+ A python {note}`dictionary (This data structure is a hash table)` has type Dict[key, value].
````

which is rendered as 

+ A python {note}`dictionary (This data structure is a hash table)` has type Dict[key, value].

The term "dictionary" is displayed with underline dots. When the user clicks at this text, a popup window containing the note "This data structure is a hash table" is shown to the user.

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


## Flashcards

MWiki supports basic flashcards, for instance, the following syntax defines a German-to-English flashcard deck. Where, each element of the array entries is a flashcard. The German Article+Word "der Tag" is the front side of the first flashcard. The backside of this card is corresponding english word "day". 

````markdown
```{flashcard}
{
     "title":  "Vocabulary German/English"
   , "entries": [
           ["der Tag",    "day"]
        ,  ["heute", "today"]
        ,  ["die Woche", "Week"]
        ,  ["der Monat", "Month"]
        ,  ["der Wochentag", "weekday or day of week"]
        ,  ["der Diestang",  "Tuesday"]
        ,  ["der Mittwoch", "Wednesday"]
        ,  ["die Sicht", "View"]
        ,  ["mehr Bilder", "More pictures"]
        ,  ["das Unternehmen", "business, company, firm"]
        ,  ["die Wirklichkeit", "relity"]
        ,  ["die Hauptsache", "the main thing"]
        ,  ["die Ausgabe", "Issue/edition"]
        ,  ["die Verzauberte Ausgabe", "enchanted edition"]
        ,  ["die Gemütlich Ausgabe", "cozy (confortable) edition"]
        ,  ["die Letzte Ausgabe", "Latest Issue/Edition"]
        ,  ["die Richtige vorige Ausgabe", "Correct previous issue/edition"]
        ,  ["die Vorherige Ausgabe", "Previous Issue"]
        ,  ["seher gut", "very good or very well"]
        ,  ["Körper und Kleidung", "Body and clothing"]
        ,  ["Natur und Tiere", "Nature and Animals"]
        ,  ["Essen und Trinken", "Food and drink"]
        ,  ["Reise und Orte", "Travel and Places"]
   ]
}
```
````
Rendering:

```{flashcard}
{
     "title":  "Vocabulary German/English"
   , "entries": [
           ["der Tag",    "day"]
        ,  ["heute", "today"]
        ,  ["die Woche", "Week"]
        ,  ["der Monat", "Month"]
        ,  ["der Wochentag", "weekday or day of week"]
        ,  ["der Diestang",  "Tuesday"]
        ,  ["der Mittwoch", "Wednesday"]
        ,  ["die Sicht", "View"]
        ,  ["mehr Bilder", "More pictures"]
        ,  ["das Unternehmen", "business, company, firm"]
        ,  ["die Wirklichkeit", "relity"]
        ,  ["die Hauptsache", "the main thing"]
        ,  ["die Ausgabe", "Issue/edition"]
        ,  ["die Verzauberte Ausgabe", "enchanted edition"]
        ,  ["die Gemütlich Ausgabe", "cozy (confortable) edition"]
        ,  ["die Letzte Ausgabe", "Latest Issue/Edition"]
        ,  ["die Richtige vorige Ausgabe", "Correct previous issue/edition"]
        ,  ["die Vorherige Ausgabe", "Previous Issue"]
        ,  ["seher gut", "very good or very well"]
        ,  ["Körper und Kleidung", "Body and clothing"]
        ,  ["Natur und Tiere", "Nature and Animals"]
        ,  ["Essen und Trinken", "Food and drink"]
        ,  ["Reise und Orte", "Travel and Places"]
   ]
}
```

It is possible to view all flashcards and their backside at once; go to next card; go to previous card; view the backside of the current flashcard; and jump to a next random card. Note that this feature is still under development. 

## Further Reading 

+ https://mystmd.org/guide/admonitions
+ https://mystmd.org/sandbox
   + => Allows testing MyST online without installation.
+ https://myst-parser.readthedocs.io/en/latest/syntax/math.html
+ https://markdown-it-py.readthedocs.io/en/latest/architecture.html
+ https://mystmd.org/guide/glossaries-and-terms 