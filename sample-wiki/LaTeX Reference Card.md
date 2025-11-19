---
title:       LaTeX Reference Card
description: Comprehensive overview of LaTeX and examples.

equation_enumeration_enabled: off
equation_enumeration_style:   subsection
---


## Typesetting                  

### Font Types


| LaTex              | Typesetting                  | Typical Use                               |
| ------------------ | ---------------------------- | ----------------------------------------- |
| ℜ                  | `\Re`                        | Real part of a complex number             |
| ℑ                  | `\Im`                        | Imaginary part of a complex number        |
| $\mathbb{R}$       | `\mathbb{R}`                 | Sets                                      |
| $\mathbb{F}$       | `\mathbb{F}`                 | Vectors                                   |
| $\mathfrak{J}$     | `\mathfrak{J}`               |                                           |
| $\mathscr{I}$      | `\mathscr{I}`                |                                           |
| $\mathcal{S}$      | `\mathcal{S}`                |                                           |
| $\mathcal{G}$      | `\mathcal{G}`                | Note: Used for describing lie algebra     |
| $\bar{Q}$          | `\bar{Q}`                    | Bar over symbol                           |
| $\hat{v}$          | `\hat{v}`                    | Unit vector                               |
| $\vec{u}$          | `\vec{u}`                    | handwritten vector notation               |
| $\mathbf{r}$       | `\mathbf{r}`                 | vector notation used in most university-level books |
| $\hat{\mathbf{n}}$ | `\hat\mathbf{n}`             | Unit vector using bold face               |
| $\tilde{n}$        | `\tilde{n}`                  | Tilde over symbol                         |
|                    |                              |                                           |

### Font Sizes 

```markdown 
+ $\Huge Hello!$
+ $\huge Hello!$
+ $\LARGE Hello!$
+ $\Large Hello!$
+ $\large Hello!$
+ $\normalsize Hello!$
+ $\small Hello!$
+ $\scriptsize Hello!$
+ $\tiny Hello!$
```
Rendering

+ $\Huge Hello!$
+ $\huge Hello!$
+ $\LARGE Hello!$
+ $\Large Hello!$
+ $\large Hello!$
+ $\normalsize Hello!$
+ $\small Hello!$
+ $\scriptsize Hello!$
+ $\tiny Hello!$

### Table

```latex
\notag 

\begin{array} {|l|l|}
      \hline symbol & description               & value & unit 
   \\ \hline m      & \text{rod mass}           & 0.15  & kg 
   \\ \hline m      & \text{cart mass}          & 0.4   & kg 
   \\ \hline l      & \text{rod length}         & 0.05  & m 
   \\ \hline j      & \text{rod intertia}       & 0.005 & kg.m^2 
   \\ \hline b      & \text{friction constant}  & 0.8 & n.m.s 
   \\ \hline  
\end{array}
```

Rendering:^{Note that MWiki markdown and MyST markdown already support tables.}

$$
\notag 

\begin{array} {|l|l|}
      \hline symbol & description               & value & unit 
   \\ \hline m      & \text{rod mass}           & 0.15  & kg 
   \\ \hline m      & \text{cart mass}          & 0.4   & kg 
   \\ \hline l      & \text{rod length}         & 0.05  & m 
   \\ \hline j      & \text{rod intertia}       & 0.005 & kg.m^2 
   \\ \hline b      & \text{friction constant}  & 0.8 & n.m.s 
   \\ \hline  
\end{array}
$$


## Symbols

### Greek Letters and Math Symbol

|  Rendering    | Code         |
| ------------- | ------------ |
| $\alpha$      |  `\alpha`    |
| $\beta$       |  `\beta`     |
| $\gamma$      |  `\gamma`    |
| $\Gamma$      |  `\Gamma`    |
| $\delta$      |  `\delta`    |
| $\Delta$      |  `\Delta`    |
| $\theta$      |  `\theta`    |
| $\Theta$      |  `\Theta`    |
| $\vartheta$   |  `\vartheta` |
| $\varTheta$   |  `\varTheta` |
| $\phi$        |  `\phi`      |
| $\Phi$        |  `\Phi`      |
| $\psi$        |  `\psi`      |
| $\Psi$        |  `\Psi`      |
| $\zeta$       |  `\zeta`     |
| $\eta$        |  `\eta`        |
| $\iota$       |  `\iota`       |
| $\kappa$      |  `\kappa`      | 
| $\nu$         |  `\nu`         |
| $\mu$         |  `\mu`       |
| $\xi$         |  `\xi`       |
| $\Xi$         |  `\Xi`       |
| $\tau$        |  `\tau`      |
| $\rho$        |  `\rho`      |
| $\pi$         |  `\pi`       |
| $\Pi$         |  `\Pi`       |
| $\sigma$      |  `\sigma`    |
| $\Sigma$      |  `\Sigma`    |
| $\epsilon$    |  `\epsilon`  |
| $\varepsilon$ |  `\varepsilon` |
| $\nabla$      |  `\nabla`^{Not a greek letter, but it is a widely used symbol in calculus and fluid mechanics.}
| $\partial$    | `\partial`^{Not a greek letter. This symbol is used for partial derivatives.} |



### Equality and comparison

| Name                      | LaTeX     | Symbol      |     |
| ------------------------- | --------- | ----------- | --- |
| Less or equal than        | `\leq`    | $\leq$      |     |
| Greater or equal than     | `\geq`    | $\geq$      |     |
| Much greater than<br>     | `\gg`     | $\gg$       |     |
| Much less than            | `\ll`     | $\ll$       |     |
| Not equal to              | `\neq`    | $\neq$      |     |
| Is equivalent to          | `\equiv`  | $\equiv$    |     |
| Is approximately equal to | `\approx` | $\approx$   |     |
| Is proportional to        | `\propto` | $\propto$   |     |
|                           |           |             |     |


### Sets Symbols and Logical Operators

| Name                 | LaTeX         | Symbol        |     |
| -------------------- | ------------- | ------------- | --- |
| Empty set            | `\emptyset`   |               |     |
| Natural Numbers      | `\mathbb{N}`  | $\mathbb{N}$  |     |
| Real Numbers         | `\mathbb{R}`  | $\mathbb{R}$  |     |
| Complex Numbers      | `\mathbb{Q}`  | $\mathbb{Q}$  |     |
| Quaternions          | `\mathbb{H}`  | $\mathbb{H}$  |     |
|                      |               |               |     |
| Element in set       | `\in`         | $\in$         |     |
| Element not in set   | `\notin`      | $\notin$      |     |
| Exists               | `\exists`     | $\exists$     |     |
| For all              | `\forall`     | $\forall$     |     |
| Union of sets        | `\cup`        | $\cup$        |     |
| Intersection of sets | `\cap`        | $\cap$        |     |
| Right arrow          | `\Rightarrow` | $\Rightarrow$ |     |
|                      |               |               |     |

## Common Cases

### Fractions


| Expression                      | Example                     | Description                                                                                                          |
| ------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `\frac{num}{den}`               | $\frac{a}{b}$               |                                                                                                                      |
| `\displaystyle \frac{num}{den}` | $\displaystyle \frac{b}{a}$ |                                                                                                                      |
| `\dfrac{num}{den}`              | $\dfrac{a}{b}$              | typesets the numerator and denominator in display style, it is equivalent to add `\displaystyle` to a latex commadn. |
| `\left(\dfrac{a}{b}\right)`     | $\left(\dfrac{a}{b}\right)$ |                                                                                                                      |
| `\tfrac{num}{den}`              |                             | uses text style (inline math)                                                                                        |
| `\cfrac{num}{den}`              |                             | continous fraction                                                                                                   |
| `a \over b`                     | $a \over b$                 |                                                                                                                      |
| `a \atop b`                     | $a \atop b$                 |                                                                                                                      |
| `n \choose k`                   | $n \choose k$               |                                                                                                                      |
 

### Complex Numbers 

| Name                             | Symbol                     | LaTeX                        |
| -------------------------------- | -------------------------- | ---------------------------- | 
| Real Numbers                     | $\mathbb{R}$               | `\mathbb{R}`                 |
| Complex Numbers                  | $\mathbb{Q}$               | `\mathbb{Q}`                 | 
| Imaginary Unit 'i' (Europe)      | $\mathrm{i}$               | `\mathrm{i}`                 |
| Imaginary Unit 'j' (Europe)      | $\mathrm{j}$               | `\mathrm{j}`                 |
| Imaginary Unit 'i' (Italic)      | $\textit{i}$               | `\textit{i}`                 |
| Imaginary Unit 'j' (Italic)      | $\textit{j}$               | `\textit{j}`                 |
| Imaginary Unit (i - imath)       | $\imath$                   | `\imath{i}`                  |
| Imaginary Unit (j - jmath)       | $\jmath$                   | `\jmath{j}`                  |
| Real part of z                   | $\Re\{z\}$                 | `\Re\{z\}`                   |
| Imaginary part of z              | $\Im\{z\}$                 | `\Im\{z\}`                   |
| Argument or phase angle of z     | $\arg z$                   | `\arg z`                     |
| Argument or phase angle of z     | $\angle z$                 | `\angle z`                   |
| Argument or phase angle of z     | $\angle\{z\}$              | `\angle\{z\}`                |
| Magnitude of complex number of z | $\rho = \| z\|$            | `\rho = \| z \|`             |
| Complex number     (Europe)      | $z = x +  \mathrm{i} y$    | `z = x + \mathrm{i} y`       |
| Complex number     (Europe)      | $z = x + \mathrm{j} y$     | `z = x + \mathrm{j} y`       |     |
| Complex number     (Italic)      | $z = x  + \textit{i} y$    | `z = x + \textit{i} y`       |     |
| Complex number     (Italic)      | $z = x + \textit{j} y$     | `z = x + \textit{j} y`       |
| Complex number in polar form     | $z = \rho e^{j \phi}$      | `z = \rho e^{j \phi}`        |
| Complex number in polar form     | $z = \rho \angle \phi$     | `z = \rho \angle \phi`       |     |
| Complex number in polar form     | $z = \rho\ \angle\{\phi\}$ | `z = \rho \angle \{ \phi \}` | 


Note:
 + The imaginary unit 'j' is preferred in electrical engineering-related fields, instead of 'i' because the symbol 'i' is used in those fields for denoting electrical current.
 + In Europe, it considered as good typography the imaginary unit as an upright 'i' or 'j' written in LaTeX as  $\mathrm{i}$ (\mathrm{i}) or j $\mathrm{j}$ (\mathrm{j}). The letter 'i' in written in italic  $\textit{i}$ (\textit{i}) style when used as an index or summation index. 
 + Shortcut for writing imaginary unit \renewcommand{\i}{{\mathrm{i}}, then the imaginary unit can be written in LaTeX as just 'z + \i y'.
 + ([Usenet comp.text.tex](https://groups.google.com/g/comp.text.tex/c/1xisGZPVB6s), 2001)
  

## Matrix


**Basic Matrix (bmatrix)**

```latex
\begin{bmatrix}
     a_{11} & a_{12}
  \\ a_{21} & a_{22}
\end{bmatrix}
```
$$
\begin{bmatrix}
     a_{11} & a_{12}
  \\ a_{21} & a_{22}
\end{bmatrix}
$$


**Basic matrix (PMatrix)**


```latex
\begin{pmatrix}
A & B & C \cr
d & e & f \cr
1 & 2 & 3 \cr
\end{pmatrix}
```

$$
\begin{pmatrix}
A & B & C \cr
d & e & f \cr
1 & 2 & 3 \cr
\end{pmatrix}
$$


**Basic matrix (BMatrix)**


```latex
\begin{Bmatrix} 
 x & y \\ 
 z & v 
\end{Bmatrix}
```

$$
\begin{Bmatrix} 
 x & y \\ 
 z & v 
\end{Bmatrix}
$$

 **Matrix with N elements and dots**

```latex
 \begin{bmatrix} 
      d_1     & c_1      & 0         & \cdots   & 0        \\ 
      a_1     & d_2      & c_2       & \cdots   & 0        \\
      0       & a_2      & d_3       & \cdots   & 0        \\
      \vdots  & \vdots   & \ddots    & \ddots   & c_{n-1}  \\
      0       &  0       & \cdots    & a_{n-1}  & d_{n}
    \end{bmatrix} 
```

$$
 \begin{bmatrix} 
      d_1     & c_1      & 0         & \cdots   & 0        \\ 
      a_1     & d_2      & c_2       & \cdots   & 0        \\
      0       & a_2      & d_3       & \cdots   & 0        \\
      \vdots  & \vdots   & \ddots    & \ddots   & c_{n-1}  \\
      0       &  0       & \cdots    & a_{n-1}  & d_{n}
    \end{bmatrix} 
$$

**Matrix written in indices notation**

```latex
R =  \begin{bmatrix}
            R_{11} & R_{12} & R_{13}
        \\  R_{21} & R_{22} & R_{23}
        \\  R_{31} & R_{32} & R_{33}
      \end{bmatrix}
```

$$
R =  \begin{bmatrix}
            R_{11} & R_{12} & R_{13}
        \\  R_{21} & R_{22} & R_{23}
        \\  R_{31} & R_{32} & R_{33}
      \end{bmatrix}
$$


**Matrix that consists of column vectors** (Rotation Matrix in this case)

A rotation 3 by matrix $R$ consists of 3 column vectors $\mathbf{u}$, $\mathbf{v}$ and $\mathbf{w}$, which are basis vectors of the rotated reference frame expressed in the fixed frame. The unit vector$\mathbf{u}$ is the x axis of the rotated frame, $\mathbf{v}$ is the y axis of the rotated frame and $\mathbf{w}$ is its z axis.


```latex
R = \begin{bmatrix}
             |      &     |      &    |       
      \\ \mathbf{u} & \mathbf{v} & \mathbf{w}
      \\     |      &     |      &    |       
    \end{bmatrix}

    \in \mathbb{R}^{3 \times 3}
```

$$
R = \begin{bmatrix}
             |      &     |      &    |       
      \\ \mathbf{u} & \mathbf{v} & \mathbf{w}
      \\     |      &     |      &    |       
    \end{bmatrix}
    
    \in \mathbb{R}^{3 \times 3}
$$


 **Jacobian Matrix**


```latex
\begin{align}
 J(\mathbf{x}) &= 
	 \frac{\partial \mathbf{f}}{\partial \mathbf{x}} =
    \begin{bmatrix}
            \dfrac{\partial f_1}{\partial x_1}
          & \dfrac{\partial f_1}{\partial x_2}
          & \cdots
          & \dfrac{\partial f_n}{\partial x_n}    \\

            \dfrac{\partial f_2}{\partial x_1}
          & \dfrac{\partial f_2}{\partial x_2}
          & \cdots
          & \dfrac{\partial f_n}{\partial x_n}     \\

         \vdots  & \vdots   & \ddots    & \ddots  \\

          \dfrac{\partial f_n}{\partial x_1}
        & \dfrac{\partial f_n}{\partial x_2}
        & \cdots
        & \dfrac{\partial f_n}{\partial x_n}
       \end{bmatrix}
     \\ \text{where}
     \\
     \mathbf{x} &= \begin{bmatrix} 
				     x_1 & \cdots & x_n 
				  \end{bmatrix}^T
	 \\ \mathbf{f}(\mathbf{x}) &= 
	    \begin{bmatrix} 
		    f_1(\mathbf{x}) & \cdots & f_m(\mathbf{x})
		\end{bmatrix}^T
\end{align}
``` 

$$
\begin{align}
 J(\mathbf{x}) &= 
	 \frac{\partial \mathbf{f}}{\partial \mathbf{x}} =
    \begin{bmatrix}
            \dfrac{\partial f_1}{\partial x_1}
          & \dfrac{\partial f_1}{\partial x_2}
          & \cdots
          & \dfrac{\partial f_n}{\partial x_n}    \\

            \dfrac{\partial f_2}{\partial x_1}
          & \dfrac{\partial f_2}{\partial x_2}
          & \cdots
          & \dfrac{\partial f_n}{\partial x_n}     \\

         \vdots  & \vdots   & \ddots    & \ddots  \\

          \dfrac{\partial f_n}{\partial x_1}
        & \dfrac{\partial f_n}{\partial x_2}
        & \cdots
        & \dfrac{\partial f_n}{\partial x_n}
       \end{bmatrix}
     \\ \text{where}
     \\
     \mathbf{x} &= \begin{bmatrix} 
				     x_1 & \cdots & x_n 
				  \end{bmatrix}^T
	 \\ \mathbf{f}(\mathbf{x}) &= 
	    \begin{bmatrix} 
		    f_1(\mathbf{x}) & \cdots & f_m(\mathbf{x})
		\end{bmatrix}^T
\end{align}
$$



**Matrix with Row Labels (Labeled Matrix)**

```latex
\begin{array}{cc} 
&
\begin{array}{ccccc} 1 & 2 & 3 & 4 & 5\\
\end{array}
\\
A =
&
\left[
\begin{array}{ccccc}
h & e & l & l & o \\
m & s & e & * & * \\
m & e & t & a & *
\end{array}
\right]
\end{array}
```  

$$
\begin{array}{cc} 
&
\begin{array}{ccccc} 1 & 2 & 3 & 4 & 5\\
\end{array}
\\
A =
&
\left[
\begin{array}{ccccc}
h & e & l & l & o \\
m & s & e & * & * \\
m & e & t & a & *
\end{array}
\right]
\end{array}
$$



**Matrix with Rows and Columns Labels**

```latex
\begin{array}{c c} 
& \begin{array}{c c c} a & b &c \\ \end{array} \\
\begin{array}{c c c}p\\q\\r \end{array} &
\left[
\begin{array}{c c c}
.1 & .1 & 0 \\
.4 & 1 & 0 \\
.8 & 0 & .4
\end{array}
\right]
\end{array}
```   

$$
\begin{array}{c c} 
& \begin{array}{c c c} a & b &c \\ \end{array} \\
\begin{array}{c c c}p\\q\\r \end{array} &
\left[
\begin{array}{c c c}
.1 & .1 & 0 \\
.4 & 1 & 0 \\
.8 & 0 & .4
\end{array}
\right]
\end{array}
$$
