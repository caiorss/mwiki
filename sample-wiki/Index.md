
This is the index page. The first page shown by MWiki.

## Bookmarks

+ [Triple product](https://en.wikipedia.org/wiki/Triple_product)
+ [Cross Product][crossprod]

[crossprod]:  <https://en.wikipedia.org/wiki/Cross_product>
      "In mathematics, the cross product or vector product (occasionally directed area product, to emphasize its geometric significance) is a binary operation on two vectors in a three-dimensional oriented Euclidean vector space."  
      
## Special Hyperlinks Examples

Links to Mastodon Open Source communities:

+ @kde@floss.social 
+ @GTK@floss.social 
+ @postmarketOS@fosstodon.org


Paper with DOI Hyperlink:

+ *Time Aware Least Recent Used (TLRU) cache management policy in ICN*
  + <r-doi:10.1109/ICACT.2014.6779016> 

See this arxiv paper:  
+ <arxiv:1609.06088> - *Time Derivative of Rotation Matrices: a tutorial*, shiyu zhao, (2016)  

See this Arxiv paper:
+ *Time Derivative of Rotation Matrices: a Tutorial*, shiyu zhao, (2016)  
  - <r-arxiv:1609.06088> 

Semantic Scholar Article: 
+ *Secure Distribution of Protected Content in Information-Centric Networking* - <S2CID:198967720>   
 
Semantic Scholar Article: 
+ *Secure Distribution of Protected Content in Information-Centric Networking* 
  - <r-S2CID:198967720>   
 

RFC Standards:

+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

RFC Standards:
+ *Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content*
  + <r-rfc:7231>

Python PEP (1):
+ Python WSGI - Webserver Gateway Interface  <pep:333> 

Python PEP (2):
+ *Python WSGI - Webserver Gateway Interface*
  + <r-pep:333> 
  + Abstract: *This document specifies a proposed standard interface between web servers and Python web applications or frameworks, to promote web application portability across a variety of web servers.*

Hyperlink to CVE (Common Vulnerability Exposures):
+ See: `<cve:CVE-2024-53104>`:  <cve:CVE-2024-53104> 
+ See: `<r-cve:CVE-2024-53104>`: <r-cve:CVE-2024-53104> 
+ Brief: *media: uvcvideo: Skip parsing frames of type UVC_VS_UNDEFINED in uvc_parse_format*

     
## Internal Pages 

Hyperlinks to internal pages that still does not exist will be shown in red, while hyperlinks to existing internal pages will be shown as green. 

+ [[MWiki Syntax]]
+ [[Unix System programming]] 
+ [[Open Source Licenses]]  

## Images 

Picture of Java Duke Mascot (External Image):

```markdown
![Java's Duke Mascot](/static/example_java_duke_mascot.svg)
```

![Java's Duke Mascot](/static/example_java_duke_mascot.svg)
   
Internal Image:

+ [[logo-java-coffee-cup.png]]

```
![[logo-java-coffee-cup.png]]
```

![[logo-java-coffee-cup.png]]  
 
 
Copying and pasting images.

+ If the website is served using https (http + {abbr}`TLS (Transport Layer Security)`), it is possible to paste images from other web pages (web sites) or documents. First click at the image to copied to the clipboard with the right mouse  right button and select copy. Then hit Ctrl+v or right click to the open context meny and click at paste on the Wiki page editor. Pasted images are always saved in the folder `<path-to-wiki-folder>/pasted`

![[pasted-image-1743470376610.png]] 

For instance, this Python logo image whose MWiki markdown is 
```
![[pasted-image-1743470376610.png]]
```

corresponds to the file

+ `./sample-wiki/pasted/pasted-image-1743470376610.png`
 
## Math 
### Definition 

:::{def} Inverse Matrix 
:label: inverse-matrix

The inverse matrix $A^{-1}$ of a matrix $A: n \times n$ is defined as a matrix that when multiplied by the square matrix A yields the identity matrix. Note that not always an inverse matrix of a square matrix Q exists. 

$$
  \notag
   A^{-1} A \triangleq A^{-1} \triangleq \mathbf{I}
$$

:::

### Theorem 

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

### Solved Exercise 

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
 
## Pseudocode of Algorithms in LaTeX
Code in LaTeX:

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