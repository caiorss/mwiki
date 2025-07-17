---
title: Mathematics, Calculus and Linear Algebra Reference Card

label: math-calculus-refcard

description: Reference card for math and calculus. This quick reference covers trigonometric identities, derivatives, integrals, statistcs and matrix calculus.

subject: math

uuid: 7cdf985e-63f5-419f-bc2f-4da9c09ca2bc

equation_enumeration: subsection
---


#math #engineering #calculus #latex  #refcard #formula


Math and Calculus Cheat Sheet 

## Related 

+ [[Index]]
+ [[LaTeX Refcard]]
+ [[Matlab(Octave) Programming]]
+ [[Linear Algebra]]
+ [[Discrete Mathematics]]
+ [[Signals and Systems]] 
+ [[Jupyter Notebook]]
 
## Overview 

**Tooling**

  + Python SymPy Computer Algebra System
    + https://live.sympy.org/


  + **Mathics** - Lightweight Alternative to Mathematics built on-top of Pyhthon/SymPy
    + http://mathics.github.io
    + http://mathics.github.io/docs/mathics-1.0.pdf
    + https://github.com/mathics/Mathics/wiki/Installing
    + https://github.com/mathics/mathics

**Logic and Proof**

Terminology:

+ Algorithms
+ Axioms
+ Conjectures
+ Corollaries
+ Criteria
+ Definitions
+ Examples
+ Lemmas
+ Observations
+ Properties
+ Propositions
+ Proofs
+ Remarks
+ Theorems

## Physical Units 

**Metric Prefixes**

| prefix     | factor        |     | prefix     | factor         |
| ---------- | ------------- | --- | ---------- | -------------- |
| exa        | $10^{18}$ (E) |     | atto       | $10^{-18}$ (a) |
| peta       | $10^{15}$ (P) |     | femto      | $10^{-15}$ (f) |
| tera       | $10^{12}$ (P) |     | pico       | $10^{-12}$ (p) |
| giga       | $10^9$ (G)    |     | nano       | $10^{-9}$ (n)  |
| mega       | $10^6$ (M)    |     | micro      | $10^{-6}$ (u)  |
| kilo       | $10^3$ (k)    |     | milli      | $10^{-3}$ (m)  |
| hector     | $10^2$ (h)    |     | centi      | $10^{-2}$ (c)  |
| deca       | $10^1$ (m)    |     | centi      | $10^{-1}$ (d)  |
| N/A - None | $10^0$ (1)    |     | N/A - None | $10^0$ (1)     |

**Physical Units**

| System           | Unit name | Suffix | In meters |
| ---------------- | --------- | ------ | --------- |
|                  | Meter     | m      | 1.0       |
|                  |           |        |           |
| Imperial         | Foot      | ft     | 0.3048    |
| Imperial         | Inch      | in     | 0.0254    |
| Nautical Mile    |           |        |           |
| Terrestrial Mile |           |        |           |
|                  |           |        |           |

## Fundamental Polynomial Equations

### Line Function  

A general line equation has the following format, where $\alpha$ is the line slope or anglular coefficient and $\beta$ is the intercept of the line and the Y axis when x = 0.

$$
  y = f(x) = \alpha x + \beta
$$

Given two points of this line equations $(x_1, \, y_1)$ and $(x_2, \, y_2)$, the line equation can be found by using,

$$
   y - y_1 = \frac{y_2 - y_1}{x_2 - x_1}(x - x_1)
$$

so, the line slope coefficient $\alpha$ is given by,

$$
   \alpha = \frac{y_2 - y_1}{x_2 - x_1}
$$

and the coefficient $\beta$ can be determined as:

$$
  \beta = - \alpha x_1 + y_1
$$

The solution of the line equation $f(x) = 0$, is the point x where this curve intercepts the $X$ axis or $y = 0$. It is observable that this point is:

$$
  x = - \beta / \alpha
$$


### Quadratic Equation and Quadratic Curve

A quadratic cuve has the format $\eqref{EqQuadratic}$, where $a \in \mathbb{R}$, $b \in \mathbb{R}$ and $c \in \mathbb{R}$.

$$
  \label{EqQuadratic}
  f(x) = a x^2 + b x + c
$$


**Solution of Quadratic Equation**

The solution of the quadtratic equation $f(x) = 0$ can be found as:


$$
\begin{cases}
   x &= \underbrace{ \dfrac{-b \pm \sqrt{\Delta}}{2a} }_{\text{real roots}} \in \mathbb{R} 
     \quad &\text{if } \Delta \geq 0
   

  \\ x &= \underbrace{
         \dfrac{-b \pm \mathrm{j} \sqrt{-\Delta}}{2a} }_{\text{complex conjugate roots}} \in \mathbb{C}
     \quad &\text{if } \Delta < 0
\end{cases}
$$

Where $\Delta$ is given by:

$$
\Delta = b^2 - 4ac 
$$

**Determine Quadratic Equation from Points**

Given three distinct points $(x_1, \, y_1)$, $(x_2, \, y_2)$ and $(x_3, \, y_3)$ of a quadratic cuve $f(x) = ax^2 + bx + c$, the coefficients of the quatratic curve that intercepts those points can be determined by solving the following linear system for the column vector $[a \, b \, c]^T$. 

$$
\begin{bmatrix}
      x_1^2 & x_1 & 1 
   \\ x_2^2 & x_2 & 1
   \\ x_3^2 & x_3 & 1
\end{bmatrix}

\begin{bmatrix}
  a \\ b \\ c
\end{bmatrix}

= 

\begin{bmatrix}
  y_1 \\ y_2 \\ y_3
\end{bmatrix}
$$


{nl}


**Solve the equation in Python's Sympy**

Since this linear system is small, it is worth solving it in symbolic form in order to be able to implement it as software.

Import Sympy and enable pretty printing.

```python
import sympy as sp
sp.init_printing()
```

Create symbols and matrices.

```python
x1, x2, x3, y1, y2, y3, a, b, c = sp.symbols("x1 x2 x3 y1 y2 y3 a b c")

A = sp.Matrix([[x1**2, x1, 1], [x2**2, x2, 1], [x3**2, x3, 1]])

x = sp.Matrix([a, b, c])
y = sp.Matrix([y1, y2, y3])
```

Create the equation object. Solve `A * x = y` indirectly by converting this equation to sympy standard format `eqrhs: A * x - y`, that solves `eqrhs == 0` or `A * x - y == 0` for x, vector of variables a, b and c.

```python
eq = A * x - y
 
>>> eq
⎡    2                ⎤
⎢a⋅x₁  + b⋅x₁ + c - y₁⎥
⎢                     ⎥
⎢    2                ⎥
⎢a⋅x₂  + b⋅x₂ + c - y₂⎥
⎢                     ⎥
⎢    2                ⎥
⎣a⋅x₃  + b⋅x₃ + c - y₃⎦

```


Solve the equation system for a, b and c.

```python
sols = sp.solve([eq[0], eq[1], eq[2]], (a, b, c))

>>> sols[a]
  -x₁⋅y₂ + x₁⋅y₃ + x₂⋅y₁ - x₂⋅y₃ - x₃⋅y₁ + x₃⋅y₂   
───────────────────────────────────────────────────
  2        2           2        2     2           2
x₁ ⋅x₂ - x₁ ⋅x₃ - x₁⋅x₂  + x₁⋅x₃  + x₂ ⋅x₃ - x₂⋅x₃ 

>>> sols[b]
  2        2        2        2        2        2   
x₁ ⋅y₂ - x₁ ⋅y₃ - x₂ ⋅y₁ + x₂ ⋅y₃ + x₃ ⋅y₁ - x₃ ⋅y₂
───────────────────────────────────────────────────
  2        2           2        2     2           2
x₁ ⋅x₂ - x₁ ⋅x₃ - x₁⋅x₂  + x₁⋅x₃  + x₂ ⋅x₃ - x₂⋅x₃ 
 
>>> sols[c]
  2           2              2           2        2              2   
x₁ ⋅x₂⋅y₃ - x₁ ⋅x₃⋅y₂ - x₁⋅x₂ ⋅y₃ + x₁⋅x₃ ⋅y₂ + x₂ ⋅x₃⋅y₁ - x₂⋅x₃ ⋅y₁
─────────────────────────────────────────────────────────────────────
           2        2           2        2     2           2         
         x₁ ⋅x₂ - x₁ ⋅x₃ - x₁⋅x₂  + x₁⋅x₃  + x₂ ⋅x₃ - x₂⋅x₃  
```

Generate the LaTeX expression for the values of a, b and c.

```python
>>> print(sp.latex(sols[a]))
\frac{- x_{1} y_{2} + x_{1} y_{3} + x_{2} y_{1} - x_{2} y_{3} - x_{3} y_{1} + x_{3} y_{2}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}

>>> print(sp.latex(sols[b]))
\frac{x_{1}^{2} y_{2} - x_{1}^{2} y_{3} - x_{2}^{2} y_{1} + x_{2}^{2} y_{3} + x_{3}^{2} y_{1} - x_{3}^{2} y_{2}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}


>>> print(sp.latex(sols[c]))
\frac{x_{1}^{2} x_{2} y_{3} - x_{1}^{2} x_{3} y_{2} - x_{1} x_{2}^{2} y_{3} + x_{1} x_{3}^{2} y_{2} + x_{2}^{2} x_{3} y_{1} - x_{2} x_{3}^{2} y_{1}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}
```

{nl}

Solution:

$$
\begin{split}
   a &=  \frac{- x_{1} y_{2} + x_{1} y_{3} + x_{2} y_{1} - x_{2} y_{3} - x_{3} y_{1} + x_{3} y_{2}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}
 
 \\ b &= \frac{x_{1}^{2} y_{2} - x_{1}^{2} y_{3} - x_{2}^{2} y_{1} + x_{2}^{2} y_{3} + x_{3}^{2} y_{1} - x_{3}^{2} y_{2}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}

 \\ c &= \frac{x_{1}^{2} x_{2} y_{3} - x_{1}^{2} x_{3} y_{2} - x_{1} x_{2}^{2} y_{3} + x_{1} x_{3}^{2} y_{2} + x_{2}^{2} x_{3} y_{1} - x_{2} x_{3}^{2} y_{1}}{x_{1}^{2} x_{2} - x_{1}^{2} x_{3} - x_{1} x_{2}^{2} + x_{1} x_{3}^{2} + x_{2}^{2} x_{3} - x_{2} x_{3}^{2}}
\end{split}
$$


Code Generation using CSE - Common Subexpression Elimination:

```python
>>> result = sp.Matrix([sols[a], sols[b], sols[c]])

>>> u = sp.numbered_symbols("u")
>>> r = sp.cse(result, symbols = u)

# --- Intermediate Variables -------#
for var, expr in r[0]: print(f" {var} := {expr}")

 u0 := x3**2
 u1 := u0*x1
 u2 := x1**2
 u3 := u2*x2
 u4 := x2**2
 u5 := u4*x3
 u6 := u4*x1
 u7 := u2*x3
 u8 := u0*x2
 u9 := 1/(u1 + u3 + u5 - u6 - u7 - u8)
   
eqq = r[1][0]

# --------- Final Variables -------#
>> print(f" a := {eqq[0]}")
 a := u9*(-x1*y2 + x1*y3 + x2*y1 - x2*y3 - x3*y1 + x3*y2)

>> print(f" b := {eqq[1]}")
 b := u9*(u0*y1 - u0*y2 + u2*y2 - u2*y3 - u4*y1 + u4*y3)

>>> print(f" c := {eqq[2]}")
 c := u9*(u1*y2 + u3*y3 + u5*y1 - u6*y3 - u7*y2 - u8*y1)
```




## Trigonometric Functions 

**Basic Trigonometric Identities**

$$
\cos^2 \alpha + \sin^2 \alpha = 1
$$

**Euler's Identity**

$$
   e^{j \theta} = \cos\theta + j \sin \theta
$$

Note: $j = \sqrt{-1}$ imaginary unit and $\theta$ is the angle in radians.

**Half Angle Trigonometric Identities** 

$$
\begin{split}
      \sin \frac{\alpha}{2} &= \pm \sqrt{ \frac{1 - \cos \alpha}{2}  }
   \\ \cos \frac{\alpha}{2} &= \pm \sqrt{ \frac{1 + \cos \alpha}{2}}
   \\ \tan \frac{\alpha}{2} &= \frac{1 - \cos \alpha}{\sin \alpha} 
                            = \frac{\sin \alpha}{ 1 + \cos \alpha}
\end{split}
$$

**Double Angle Formulas Trigonometric Identities**

$$
\begin{split}
     \sin 2 \alpha &= 2 \sin \alpha \cos \alpha
  \\ \cos 2 \alpha &= \cos^2 \alpha - \sin^2 \alpha
  \\ \cos 2 \alpha &= 1 - 2 \sin^2 \alpha
  \\ \tan 2 \alpha &= \frac{ 2 \tan \alpha }{ 1 - \tan^2 \alpha }
\end{split}
$$
 

**Properties**

| Properties                                  |                                                   |
| ------------------------------------------- | ------------------------------------------------- |
|                                             |                                                   |
| **Symmetry Properties**                     |                                                   |
| Cosine is an even function (pt: função par) | $\cos (-x) = \cos (x)$                            |
| Sine is a odd function (pt: função impar)   | $\sin (-x) = - \sin(x)$                           |
|                                             | $\sin (\pi/2 - x) = \sin(90 - x) = \cos x$        |
|                                             | $\cos (\pi/2 - x) = \cos(90 - x) = \sin x$        |
|                                             | $\cos (\pi/2 - x) = \cos(90 - x) = \sin x$        |
| **Arc Operations**                          |                                                   |
| Sin of the sum of angles                    | $\sin(x + y) = \sin x . \cos y + \cos x . \sin y$ |
| Cos of the sum of angles                    | $\cos(x + y) = \cos x . \cos y - \sin x . \sin y$ |
|                                             |                                                   |
| **Identities**                              |                                                   |
| Pythagorean identity                        | $(\sin x)^2 + (\cos x)^2 = 1$                     |

**Notable angles** 

| Degrees | Randians    | Sin          | Cos          | Tan          |
| ------- | ----------- | ------------ | ------------ | ------------ |
| 0       | 0           | 0            | 1            | 0            |
| 30      | $\pi/6$     | 1/2          | $\sqrt{3}/2$ | $\sqrt{3}/3$ |
| 45      | $\pi/4$     | $\sqrt{2}/2$ | $\sqrt{2}/2$ | 1            |
| 60      | $\pi/3$     | $\sqrt{3}/2$ | 1/2          | $\sqrt{3}$   |
| 90      | $\pi/2$     | 1            | 0            | $\infty$     |
| 180     | $\pi$       | 0            | -1           | 0            |
| 270     | $(3/2) \pi$ | -1           | 0            | $-\infty$    |
| 360     | $2\pi$      | 0            | 1            | 0            |

 
## Derivatives  
            
### Derivative Rules

| Function                                             | Derivative                                                                        | Description                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------- |
| f(x)                                                 | $\dot{f}(x) = \dfrac{df}{dx}$                                                     | Derivative of generic function                    |
| $r(x) = c$                                           | 0                                                                                 | Derivative of constant                            |
| $c f(x)$                                             | $c \dfrac{df}{dx}$                                                                | Function multiplied by constant                   |
| $c + f(x)$                                           | $\dfrac{df}{dx}$                                                                  | Function added to constant                        |
| $f(x) + g(x)$                                        | $\dfrac{df}{dx} + \dfrac{dg}{dx}$                                                 | Sum of functions                                  |
| $f(x) g(x)$                                          | $f \dfrac{f}{dx} + g \dfrac{df}{dx}$                                              | Product of functions                              |
| $f(u(x))$                                            | $\left[\dfrac{d}{du} f(u) \right] \dfrac{du}{dx} = \dfrac{df}{du} \dfrac{du}{dx}$ | Chain Rule                                        |
| $\dfrac{1}{f(x)}$                                    | $-\dfrac{1}{f^2} \dfrac{df}{dx}$                                                  | Dertivative of function                           |
| $\dfrac{g}{f}$                                       | $\dfrac{f \dot{g} - g \dot{f}}{f^2}$                                              | Derivative of ratio                               |
| $f^{-1}(x)$                                          | $\left. \left[ \dfrac{d}{dy} f(y) \right]^{-1}    \right\vert_{y = f^{-1}(x)}$    | Derivative of inverse function                    |
| $\left. \dfrac{d}{dx} f^{-1}(x) \right\vert_{x = a}$ | $\left. \left[ \dfrac{d}{dy} f(y) \right]^{-1}    \right\vert_{y = f^{-1}(a)}$    | Derivative of inverse function evaluated at x = a |

### Basic Derivatives


| Function f(x)  | Derivative                   |                                                   |
| -------------- | ---------------------------- | ------------------------------------------------- |
| $x$            | 1                            |                                                   |
| $x^2$          | $2x$                         |                                                   |
| $x^3$          | $3 x^2$                      |                                                   |
| $x^p$          | $p x^{p - 1}$                | $p \in \mathbb{R}$                                |
| $1/x$          | $-1/x^2$                     |                                                   |
| $\sqrt{x}$     | $\dfrac{1}{2 \sqrt{x}}$      |                                                   |
| $e^x$          | $e^x$                        |                                                   |
| $e^{a x}$      | $a e^{a x}$                  |                                                   |
| $a^x$          | $a^x \ln a$                  |                                                   |
| $e^{f(x)}$     | $e^{f(x)} f(x) \dot{f}(x)$   |                                                   |
| $\ln x$        | $1/x$                        | Derivative of natural logarithm base $\mathrm{e}$ |
| $\log_a x$     | $\dfrac{1}{x \ln a}$         | Derivative of logarithm of base a                 |
| $\sin x$       | $\cos x$                     |                                                   |
| $\cos x$       | $- \sin x$                   |                                                   |
| $\tan x$       | $\sec^2 x$                   |                                                   |
| $\sec x$       | $\sec x \tan x$              |                                                   |
| $\sin^{-1}(x)$ | $\dfrac{1}{\sqrt{1 - x^2}}$  | arc sine                                          |
| $\cos^{-1}(x)$ | $-\dfrac{1}{\sqrt{1 - x^2}}$ | arc cosine                                        |
| $\tan^{-1}(x)$ | $\dfrac{1}{1 + x^2}$         | arc tangent or arctan                             |


### Derivative of Inverse Function 

Derivative of inverse function $f^{-1}(x)$ of $f(x)$ at $x = a$.

$$
 \notag
 
  \left. \dfrac{d}{dx} f^{-1}(x) 
      \right\vert_{\displaystyle x = a} 
 
  = \left. \left[ 
       \dfrac{df}{dy} \right]^{-1} 
         \right\vert_{\displaystyle y = f^{-1}(a)}
$$

**Procedure for Determining the derivative of the inverse**

STEP 1: Given a, solve the following equation for y, in order to find $y_a$, the solution of this equation.

$$
\notag
   a = f(y)
$$

STEP 2: Compute the derivative of $f(y)$ with respect to y at $y = y_a$.

$$
 \notag 
  w = \left. \dfrac{d}{dy} f(y) \right\vert_{\displaystyle y = y_a} 
$$

STEP 3: Compute the value of the derivative of the inverse function of f(x) by taking the inverse of the previous result w.

$$
  \left. \dfrac{d}{dx} f^{-1}(x) 
           \right\vert_{\displaystyle x = a} 
   = \frac{1}{w}
$$


**Examples**

:::{example} Derivative of Inverse Function
 
Suppose $f(x)=x^5+2x^3+7x+1$, find $[{f}]^{-1}(1)$, the derivative of the inverse function of f(x) at x = 1.  [(sfu.ca)](<https://www.sfu.ca/math-coursenotes/Math%20157%20Course%20Notes/sec_DerivativesofInverse.html>)
 

```{solution}

Recall tha the derivative of $f^{-1}(x)$ can be determined as,

$$
 \notag
 
  \left. \dfrac{d}{dx} f^{-1}(x) \right\vert_{x = a} 
 
  = \left. \left[ 
       \dfrac{df}{dy} \right]^{-1} 
         \right\vert_{y = f^{-1}(a)}
$$

The first step is to determine $y = f^{-1}(1)$. Isolate y in this equation in order to find y corresponding to $a = 1$. that yields, 

$$
 \notag
     f(y) = 1
$$


Solve the equation $f(y) = 1$.

$$
 \notag 
 f(y) = y^5 + 2y^3 + 7y + 1 = 1
$$


It is observable that the solution of the previous equation is $y = 0$.

Compute the derivative of f(y) at y = 0.

$$
 \notag
  \begin{split}
 
 \left. \dfrac{d}{dy} f(y) \right\vert_{y = 0}
     &= \dfrac{d}{dy}
    \left .\left[ y^5 + 2y^3 + 7y + 1  \right] 
        \right\vert_{y = 0} 
     
     \\ &=  \left. [5 y^4 + 6 y^2 + 7 ] 
             \right\vert_{\displaystyle y = 0}
     \\ &=  7
\end{split}
$$

Finally, the derivative of $\dfrac{d}{dx} f^{-1}(x)$ can be evaluted at x = 1 by replacing the result of the previous computation in the formula for determining the derivative of the inverse function.

$$
 \notag
 
  \begin{split}
       \left. \dfrac{d}{dx} f^{-1}(x) \right\vert_{x = 0} 
       &=
         \left. \left[ \dfrac{df}{dy} \right]^{-1} 
                   \right\vert_{y = f^{-1}(0)}
 \\    &= (7)^{-1} = \frac{1}{7}

  \end{split}
$$

Solution: $[f^{-1}]'(1) = \dfrac{1}{7}$
```
:::
% --- End of Example - deriv. of inv. function ---%%

      
### Chain Rule

**Chain rule for function of one variable**

This notation explicitly states that the in the right-hand side of the equation f is expressed as function of u and not as function of x.  

$$
 \dfrac{d}{dx} f(u(x)) 
   = \left[ \dfrac{d}{du} f(u) \right] \dfrac{du}{dx}
$$

Concise notation for chain rule for functions of a single variable

$$
\dfrac{d}{dx} f(u(x)) = \dfrac{df}{du} \dfrac{du}{dx}
$$

**Chain rule for function of multi-variable functions**


$$
 \dfrac{d}{dt} f(x(t), y(t)) = \dfrac{\partial f}{\partial x} \dfrac{dx}{dt} + \dfrac{\partial f}{\partial y} \dfrac{dy}{dt}
$$


**Chain rule for coordinate changing**

Let f be function of $x$ and $y$. A new coordinate is introduced with
coordinates $v$ and $w$ in a way that $x = x(v, w)$ and $y = y(v, w)$. The partial derivative of f with respect to the new coordinate $v$, $w$ can be determined as:

$$
\begin{split}
  x &= x(v, w) \quad y = y(v, w) \\

  \frac{\partial f}{\partial v} &=
      \frac{\partial f}{\partial x}  \frac{\partial x}{\partial v} 
    + \frac{\partial f}{\partial y}  \frac{\partial y}{\partial v} \\


  \frac{\partial f}{\partial w} &=
      \frac{\partial f}{\partial x}  \frac{\partial x}{\partial w} 
    + \frac{\partial f}{\partial y}  \frac{\partial y}{\partial w} \\\end{split}
$$
 

**Examples**
 
:::{example} Chain Rule for Derivative Multi-Variate Functions

Let the function f be $f(x, y) = x^2/A^2 + y^2/B^2 - C$.  Find the derivative of f with respect to t. And x and y are functions of t, $x = x(t) = A \cos t$ and $y = y(t) = B \sin t$. 


```{solution}   

Method 1:  Find the derivative directly, by expressing x and y as function of t and replacing their values in the function f.

$$
 \notag 
\begin{split}

  \frac{df}{dt} &=& \frac{d}{dt} \left[ (A \cos t)^2 / A^2  + (B \sin t)^2 / B^2 - C\right] = 0 \\
\end{split}
$$

Method 2: Find the derivative using the chain rule 

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
% End of Example - multi-variate derivative  %
    
### Tangent Line Equation 

The derivative can be used for obtaining the tangent line equation $\eqref{eqtanget_diff}$ to a curve represented by a function f(x) at a particular point, where $\alpha \in \mathbb{R}$ and $\beta \in \mathbb{R}$ are the coefficients of the line equation. 

$$
  y = \alpha x + \beta 
  \label{eqtanget_diff}
$$

The coefficient $\alpha$, the line slope, can be computed as:

$$
\alpha = f'(x_a) = 
    \left. \frac{df}{dx} \right\vert_{\displaystyle x = x_a}
$$

Then, the coefficient $\beta$ can be found by replacing the pair $x_a, \: $y_a = f(x_a)$ in $\eqref{eqtanget_diff}$ and solving it for $\beta$. 

$$
  \beta = y_a - \alpha x_a
$$

so,

$$
  \beta = f(x_a) - f'(x_a) x_a
$$

The, the coefficients of the line equation tangent to the point $(x_a, y_a)$ are given by:

$$
 \begin{cases}
        \alpha = f'(x_a)
    \\  \beta  = f(x_a) - f'(x_a) x_a
 \end{cases}
$$
 
## Integrals 

References: 


  + [FOURIER SERIES - Graham S McDonald](<http://www.cse.salford.ac.uk/physics/gsmcdonald/H-Tutorials/Fourier-series-tutorial.pdf>)


 **General Rules** 

Linear combination of integrals: 


$$
  \int [a \cdot f(x) + b \cdot g(x)] dx  =  a \int f(x) dx + b \int g(x) dx 
$$

Power of a function: 


$$
  \int  [g(x)]^n g'(x) dx = \frac{1}{n + 1} [g(x)]^{n + 1} \quad n \neq -1
$$

Ratio between function's derivate and itself: 


$$
  \int \frac{g'(x)}{g(x)} dx = \ln || g(x) ||
$$


 **Common Integrals** 

Constant: 


$$
  \int C \cdot dx  = C \cdot x
$$

Power: 


$$
  \int x^n \cdot dx  = \frac{x^{n + 1}}{n + 1} \quad \neq -1
$$

Power: 


$$
  \int a^x \cdot dx  = \frac{a^x}{\ln a} \quad a > 0
$$

Exponential: 


$$
  \int e^x \cdot dx  = e^x 
$$



Logarithm: 


$$
  \int \frac{1}{x} \cdot dx  = \ln || x ||
$$

Sine:


$$
  \int \sin x = - \cos x
$$

Cosine: 


$$
  \int \cos x \cdot dx = \sin x
$$

Square sine: 


$$
  \int \sin^2 x \cdot dx = \frac{x}{2} - \frac{1}{4} \sin 2x
$$

Square cosine: 


$$
  \int \cos^2 x \cdot dx = \frac{x}{2} + \frac{1}{4} \sin 2x
$$

Sinh - hyperbolic sine: 


$$
  \int \text{sinh} x \cdot dx = \text{cosh} x
$$

Cosh - hyperbolic consine: 


$$
  \int \text{cosh} x \cdot dx = \text{sinh} x
$$


## Sums 


 - Reference: Dan Stefanica, *A Primer for Mathematics of Financial
   Engineering*, 1st ed. New York: FE PRess, 2008. Page 4.


$$
  \sum_{k = 1}^{n} k = \frac{n(n+1)}{2}
$$


$$
 \sum_{k = 1}^{n} k^2 =  \frac{n(n+1)(2n + 1)}{6}
$$


$$
 \sum_{k = 1}^{n} k^3 = (\frac{n(n+1)}{2})^2
$$

  
## Taylor Series       
### Taylor series expansion 

The Taylor series is a expansion of a real function f(x) about a point x  a. When a is equal to 0, the expansion is also known as Maclaurin series. 


$$
 \begin{split}
  f(x) &= \sum_{n = 0}^{\infty} \frac{f^{(n)}(a)}{n!}(x - a)^n 
    \\  &= f(a) + f^{(1)}(a)(x - a) 
              + \frac{f^{(2)}(a)}{2!}(x - a)^2 
              + \frac{f^{(3)}(a)}{3!}(x - a)^3 
              \cdots 
              
  \end{split}
$$ 

The Taylor series expansion is sometimes written as:


$$
  \begin{split}
  f(x + a)  &= \sum_{n = 0}^{\infty} \frac{f^{(n)}(a)}{n!}x^n 
         \\  &= f(a) + f^{(1)}(a)x 
              + \frac{f^{(2)}(a)}{2!} x^2 
              + \frac{f^{(3)}(a)}{3!} x^3 
              \cdots                        
  \end{split}
$$

where: 
 - $f^{(n)}(x) = \dfrac{d^nf}{dx^n}$ is the derivative of order n of a function f(x)
 - $f^{(0)}(x) = f(x)$ - "derivative" of order zero, it is the same as f(x).
 - $f^{(1)}(x) = \dfrac{df}{dx}$  - first order derivative 
 - $f^{(2)}(x) = \dfrac{d^2f}{dx^2}$ - second order derivative 

     
### Some Taylor series expansion 

Exponential 


$$
  e^{x} = \sum_{n = 0}^{\infty} \frac{x^n}{n!} 
        = 1 + x + \frac{1}{2!} x^2 + \frac{1}{3!} 3^2 + \frac{1}{4!} 4^2 + \cdots 
$$

Consine 


$$
  \cos x = \sum_{n = 0}^{\infty} \frac{(-1)^n}{(2n)!} x^{2n}
         = 1 - \frac{1}{2!}x^2 + \frac{1}{4!} x^4 - \frac{1}{6!} x^6 + \cdots 
$$

Sine 


$$
  \sin x = \sum_{n = 0}^{\infty} \frac{(-1)^n}{(2n + 1)!} x^{2n + 1} 
         = x -  \frac{1}{3!}x^3 + \frac{1}{5!}x^5 - \frac{1}{7!}x^7 + \cdots 
$$

Inverse tan or arctan


$$
  \arctan x =  \sum_{n = 0}^{\infty} \frac{(-1)^n}{2n + 1} x^{2n + 1}
            = x - \frac{1}{3} x^3 + \frac{1}{5} x^5 - \frac{1}{7!} x^7 + \cdots
$$

Natural Logarithm 


$$
  \ln(1 + x)  = \sum_{n = 1}^{\infty} \frac{x^n}{n}  (-1)^{n+1}
            =  x - \frac{1}{2} x^2 + \frac{1}{3}x^3 - \frac{1}{4} x^4 + \cdots 
$$

Geometric Power Series 


$$
 \frac{1}{1 + x} = 1 + x + x^2 + x^3 + \cdots 
$$

  
### Approximations for small values of x 

Misc Approximation 


$$
\begin{split}

  e^x             & \approx  1 + x  \\
  \ln (1 + x)     & \approx  x      \\ 
  \ln (1 - x)     & \approx  1 - x  \\
  \frac{1}{1 + x} & \approx  1 - x \\ 
  \frac{1}{1 - x} & \approx  1 + x \\ 
  (1 - x)^n       & \approx  1 - n x + n(n-1) x^2 / 2
\end{split}
$$


Approximations for small angles 


$$
\begin{split}
  \theta^2 &\approx 0
  \\ \sin \theta  & \approx   \theta                    
  \\ \cos \theta  & \approx   1 - \frac{\theta^2}{2} \approx 0    
  \\ \tan \theta  & \approx   \theta                    
  \\ \csc \theta  & \approx   1 / \theta + \theta / 6      
  \\ \sec \theta  & \approx    1 + \theta^2 / 2 \approx 0         
  \\ \cot \theta  & \approx    1 / \theta - \theta* 3   
\end{split}
$$


 - Where $\theta$ is the angle in radians. 

 
### References 

References: 

 + *Wolfram MathWorld* 
	 + <http://mathworld.wolfram.com/TaylorSeries.html>
 + *Wikipedia - Taylor Series* 
	 + <https://en.wikipedia.org/wiki/Taylor_series>
 + Wikipedia - *Small Angle Approximations* 
	 + <https://en.wikipedia.org/wiki/Small-angle_approximation>
 + *Expansions for Small Quantities* 
	 + <http://www.astro.umd.edu/~hamilton/ASTR498/expansions.pdf>
 

## Trigonometric Identities and Expansions 


 **Sine and Cosine Relation** 


$$
  (\sin \theta)^2 + (\cos \theta)^2 = 1
$$


 **Euler's Equation and Complex Numbers** 

Let $\mathrm{j} = \sqrt{-1}$ be the imaginary unit. 


Complex Exponential

$$
  e^{\mathrm{j} \theta} = \cos \theta + \mathrm{j} \sin \theta 
$$


and,

$$
e^{-\mathrm{j \theta}} = \cos \theta - \mathrm{j} \sin \theta
$$

Cosine of angle in radians expressed as linear combination of complex exponential 

$$
  \cos \theta 
    = \frac{1}{2} (e^{\mathrm{j} \theta} + e^{ - \mathrm{j} \theta}  )
$$


Sine of angle in radians expressed as linear combination of complex exponential 


$$
  \cos \theta = 
     \frac{1}{2 \mathrm{j}} 
       (e^{\mathrm{j}  \theta} + e^{ - \mathrm{j}  \theta}  )
$$

Derivative of complex exponential with respect to angle in radians.


$$
  \frac{d}{d \theta} e^{j \theta} = j \cdot e^{j \theta}
$$


 **Functions Symmetry** 


$$
  \cos(-x) = \cos(x)
$$


$$
  \sin(-x) = -\sin(x)
$$


 **Trigonometric expansions** 


$$
  \cos (a + b) = \cos a \cdot \cos b - \sin a  \sin b
$$


$$
  \sin (a + b) = \sin a \cdot \cos b - \sin a  \cos b
$$


$$
  \tan(b - a) = \dfrac{ \tan y - \tan x }{\tan x  \tan y + 1 }
$$

   
## Statistical Formulas 

Source: 
  + [(Doedel - Page 182)](<http://users.encs.concordia.ca/~doedel/courses/comp-233/slides.pdf>)
  + https://www3.nd.edu/~rwilliam/stats1/x12.pdf

Notation: 


  + $\pmb{X}$ bold capital letters mean probability distribution.
  + Var(X) => Variance of the distribution X
  + Cov(X, Y) => Covariance of the proabilities distributions X and Y
  + $\sigma_x$ => Standard deviation of variable X
  + $\mu$ => Average or menan of random variable X 


 **Expected Value Identities** 

Expected value of constant 'a': 

$$
   E(a) = a
$$

Expected value of a linear combination of random variables, 'a' and 'b' are constants.




$$
   E( a \cdot \pmb{X} + b \cdot \pmb{Y} ) = a \cdot \pmb{X} + b \cdot \pmb{Y}
$$


 **Covariance, Variance, Standard Deviation Identities** 

$$
  \text{Var}( \pmb{X} )  E[(X - \mu)^2]  E(X^2) - \mu^2 = \sigma_x^2
$$

$$
  \text{Var}(c \cdot \pmb{X} + d) = c^2 \cdot \text{Var}( \pmb{X} )
$$

$$
  \text{Cov}( \pmb{X}, \pmb{Y} ) = \text{Cov}( \pmb{Y}, \pmb{X} )
$$

$$
  \text{Cov}(c \cdot \pmb{X}, \pmb{Y} ) 
         = \text{Cov}( \pmb{X}, c \cdot \pmb{Y} ) 
         = c \cdot \text{Cov}( \pmb{X}, \pmb{Y} )
$$

$$
   \text{Cov}( \pmb{X} + \pmb{Y}, \pmb{Z} ) 
        =  \text{Cov}( \pmb{X}, \pmb{Y} ) +  \text{Cov}( \pmb{X}, \pmb{Z} )
$$

$$
   \text{Var}( \pmb{X} + \pmb{Y}) =  \text{Var}( \pmb{X} ) + \text{Var}( \pmb{Y} ) + 2 \text{Cov}( \pmb{X},\pmb{Y})
$$


## Linear algebra                        
### Notation 

General: 

  + $I = I_n$ (n x n)
    + identity matrix with all diagonal elements set to 1.
  + $1_{n, m}$ (n x m)
    + Matrix with n rows and m columsn with all elements set to 1.
  + $A_{(n x m )}$ or A (n x m)
    + A is a matirx with n rows and m columns
  + $A^T$ (m x n) - Transpose matrix of A
  + $A^{-1}$ inverse matrix of A for which:
    + $A  A^{-1} =  A^{-1} = A  I$

Column vector: 
  + Vcol (n x 1) matrix of a single column containing n elements.


$$
  \text{Vcol}_{(n x 1)} = 
    \begin{bmatrix} v_1 \\ v_2 \\ \cdots \\ v_n \end{bmatrix}
$$


Row vector: 
  + (1 x n) matrix of a single row. 


$$
  \text{Vrow}_{(1 x n)} = 
    \begin{bmatrix} v_1 & v_2 & \cdots & v_n \end{bmatrix}
$$

  
### Special matrices 

Zero matrix: 


$$
  0_{3 x 4} =  \begin{bmatrix}
                  0 & 0 & 0 & 0 \\
                  0 & 0 & 0 & 0 \\
                  0 & 0 & 0 & 0 \\
                  0 & 0 & 0 & 0 \\
                \end{bmatrix}
$$


```julia


  julia> zeros(3, 3)
  3×3 Array{Float64,2}:
   0.000  0.000  0.000
   0.000  0.000  0.000
   0.000  0.000  0.000


  julia> zeros(3, 1)
  3×1 Array{Float64,2}:
   0.000
   0.000
   0.000
```

Identity Matrix: 
 + All diagonal elements are 1. 


$$
  I_{2} =  \begin{bmatrix}
                  1 & 0 \\
                  0 & 1 \\
                \end{bmatrix}
$$




$$
  I_{3} =  \begin{bmatrix}
                  1 & 0 & 0 \\
                  0 & 1 & 0 \\
                  0 & 0 & 1 \\
                \end{bmatrix}
$$




```julia


  using LinearAlgebra 


  julia> eye(n) = zeros(n, n) + I


  julia> eye(3)
  3×3 Array{Float64,2}:
   1.000  0.000  0.000
   0.000  1.000  0.000
   0.000  0.000  1.000


  julia> eye(4)
  4×4 Array{Float64,2}:
   1.000  0.000  0.000  0.000
   0.000  1.000  0.000  0.000
   0.000  0.000  1.000  0.000
   0.000  0.000  0.000  1.000
```



Ones-based matrices:

$1_{n, n} = 1 \quad \text{for every i, j}$


```julia


  julia> ones(2, 2)
  2×2 Array{Float64,2}:
   1.00000E+00  1.00000E+00
   1.00000E+00  1.00000E+00


  julia> ones(3, 2)
  3×2 Array{Float64,2}:
   1.00000E+00  1.00000E+00
   1.00000E+00  1.00000E+00
   1.00000E+00  1.00000E+00


  julia> ones(3, 1)
  3×1 Array{Float64,2}:
   1.00000E+00
   1.00000E+00
   1.00000E+00


```


## Types of matrices 


 **Symmetric Matrix** 

Any matrix which equals to its transpose: 

Aij = Aji 


```julia


  # -------- Symmetric matrix  ---------


  julia> A = [1 7 3; 7 4 -5; 3 -5 6]
  3×3 Array{Int64,2}:
   1   7   3
   7   4  -5
   3  -5   6


  julia> A'
  3×3 LinearAlgebra.Adjoint{Int64,Array{Int64,2}}:
   1   7   3
   7   4  -5
   3  -5   6


  julia> A'  A
  true
```

Non Symmetric Matrix: 


```julia


  julia> B = [3 8 7; 9 5 6; 1 2 3]
  3×3 Array{Int64,2}:
   3  8  7
   9  5  6
   1  2  3


  julia> B'
  3×3 LinearAlgebra.Adjoint{Int64,Array{Int64,2}}:
   3  9  1
   8  5  2
   7  6  3


  julia> B  B'
  false
```
### Matrix Operations Rules 


 **Matrix multiplication is not symmetric**


$$
  A  B \neq B  A
$$


```julia


  julia> A = [ 4 5; 6 7]
  2×2 Array{Int64,2}:
   4  5
   6  7


  julia> B = [ 8 2; 1 5]
  2×2 Array{Int64,2}:
   8  2
   1  5


  julia> A * B
  2×2 Array{Int64,2}:
   37  33
   55  47


  julia> B * A
  2×2 Array{Int64,2}:
   44  54
   34  40


  julia> A * B  B * A
  false
```


 **Associativity** 


$$
  A . B . C  (A . B) C  A (B . C)
$$


 **Transpose matrix** 

Tranpose of product: 


$$
  (A  B)^T = B^T  A^T
$$


$$
  (A  B  C)^T  C^T (A  B)^T  (B  C)^T  A =  C^T  B^T  A^T
$$

Transpose of sum:


$$
  (A + B)^T = A^T + B^T
$$

  
### Column vector properties 

Let **a* and *b** be two (n x 1) column vectors: 


$$
  a_{(n x 1)} = 
    \begin{bmatrix} a_1 \\ a_2 \\ \cdots \\ a_n \end{bmatrix}
$$


$$
  b_{(n x 1)} = 
    \begin{bmatrix} b_1 \\ b_2 \\ \cdots \\ b_n \end{bmatrix}
$$

The scalar product (dot product) between **a* and *b** is: 


$$
  \mathbf{a} \cdot \mathbf{b} =  \sum_{i = 1}^n a_i  b_i 
            =  \mathbf{a}^T \mathbf{b}
            =  \mathbf{b}^T \mathbf{a}
$$

The L-2 norm or euclidian norm of a vector is given by: 


$$
  \text{norm}(\mathbf{a}) 
    = \| \mathbf{a} \| 
    = \sqrt{ \sum_{i = 1}^n a_i^2 } 
    = \sqrt{ \mathbf{a}^T \cdot \mathbf{a}} 
$$

## Matrix Calculus
  
### Definitions 



Let **x** be a (n x 1) column vector and y be a (m x 1) column vector.


$$
  x_{(n x 1)} = 
    \begin{bmatrix} x_1 \\ x_2 \\ \cdots \\ x_n \end{bmatrix}
$$


$$
  y_{(m x 1)} = 
    \begin{bmatrix} y_1 \\ y_2 \\ \cdots \\ y_n \end{bmatrix}
$$
### Derivate of a scalar with respect to a vector

If $F(X): R^N \rightarrow R$ - F(X) = F(x1, x2, ... xn) is a multivariate function, the derivate of the scalar function F(X) with respect to the vector X is: 


  + Note: $\nabla F$ means gradient vector of F(X)


$$
  \frac{\partial F}{\partial x}  
     = \nabla F
     =   \begin{bmatrix} 
            \frac{\partial F}{\partial x_1} \\             
            \frac{\partial F}{\partial x_2} \\
            \cdots \\ 
            \frac{\partial F}{\partial x_n} \\
         \end{bmatrix}


$$


 **See:** 


 + http://www.ams.sunysb.edu/~zhu/ams571/matrixvector.pdf
   + Page 38, page 39 
### Derivate of a vector with respect to a scalar 

If the vector Y is a function (Y = Y(t)) of the scalar t, the derivate of Y with respect to t is: 


$$
   \frac{\partial Y(t)}{\partial t} = 
     \begin{bmatrix} 
         \frac{\partial y_1(t)}{\partial t}  \\
         \frac{\partial y_2(t)}{\partial t}  \\
         \frac{\partial y_3(t)}{\partial t}  \\ 
         \cdots                              \\
         \frac{\partial y_m(t)}{\partial t}  \\
     \end{bmatrix}
$$
### Derivate of a vector with respect to a vector 

If the vector Y (m x 1) is a function of the vector X (n x 1), then the derivate of Y with respect to Y is: 
  + where J[Y(X)] is the <u>Jacobian</u> matrix of Y(X)


$$
   \frac{\partial Y(X)}{\partial X} 
       =  J[Y(X)] 
       =
       \begin{bmatrix} 
           \frac{\partial y_1}{\partial x_1} 
         & \frac{\partial y_2}{\partial x_1} 
         & \cdots 
         & \frac{\partial y_m}{\partial x_1}  \\


           \frac{\partial y_1}{\partial x_2} 
         & \frac{\partial y_2}{\partial x_2} 
         & \cdots 
         & \frac{\partial y_m}{\partial x_2}  \\


           \cdots & \cdots  & \cdots & \cdots \\ 


           \frac{\partial y_1}{\partial x_2} 
         & \frac{\partial y_2}{\partial x_2} 
         & \cdots 
         & \frac{\partial y_m}{\partial x_2}  \\
       \end{bmatrix}
$$
### Derivate rules for matrices and vectors 

References: 
  + http://www.ams.sunysb.edu/~zhu/ams571/matrixvector.pdf
  + https://atmos.washington.edu/~dennis/MatrixCalculus.pdf
  + https://www.comp.nus.edu.sg/~cs5240/lecture/matrix-differentiation.pdf
  + http://www.ee.ic.ac.uk/hp/staff/dmb/matrix/calculus.html
  + https://en.wikipedia.org/wiki/Matrix_calculus



Let X be n x 1 vector where $x \in R^n$

$$
  x_{(n x 1)} = 
    \begin{bmatrix} x_1 \\ x_2 \\ \cdots \\ x_n \end{bmatrix}
$$

Let C be matrix of (n x n) constant elements where $C \in R^{n x n}$


$$
  C = \begin{bmatrix}
        c_{11} & c_{12} & c_{13} \cdots c_{1n} \\ 
        c_{21} & c_{22} & c_{23} \cdots c_{2n} \\ 
        c_{31} & c_{32} & c_{33} \cdots c_{3n} \\ 
       \cdots  & \cdots & \cdots & \cdots      \\
        c_{n1} & c_{n2} & c_{n3} \cdots c_{nn} \\ 
      \end{bmatrix}
$$

The following identities are valid: 


 + Derivate of product between constant matrix and column vector.


$$
   \frac{\partial }{\partial X} (C . X)  
        = \frac{\partial (C . x)}{\partial X} 
        = C^T 
$$


 + Derivate of product between column vector and constant matrix. 


$$
   \frac{\partial }{\partial X} (X^T . C)  
        = \frac{\partial (X^T C)}{\partial X} 
        = C 
$$


 + Derivate of scalar product between vector and itself.
   + Note: this result is a vector. 


$$
   \frac{\partial }{\partial X} (X^T . X)  
        = \frac{\partial (X^T . X)}{\partial X} 
        = 2 X
$$


 + Derivate of a scalar product between vectors.
   + Let Y be a (n x 1) vector. 


$$
   \frac{\partial }{\partial X} (y^T x)  
    = \frac{\partial }{\partial X} (x^T y)  
    = y^T
$$






 + Derivative of quadratic form. 


$$
   \frac{\partial }{\partial X} (X^T . C . X)  
        = \frac{\partial (X^T . C. X)}{\partial X} 
        = (C + C^T) . x 
        = x^T (C + C^T) 
$$


 + Derivative of scalar defined by $\alpha = y^T . A . x$
   + A is a (m x n) matrix independent of both X and Y.
   + Y is (m x 1) vector independent of X.
   + X is a (n x 1) vector. 


$$
    \frac{\partial \alpha}{\partial X}
     = \frac{\partial}{\partial X} \left( y^T . A . x \right)
     = y^T . A
$$


  + Chain rule of the derivate of scalar product.
    + Note: $\alpha$ is a scalar.
    + Note: v is a vector and dependent on vector x.


$$
  \frac{\partial \alpha(x)}{\partial x} 
       = \frac{\partial}{\partial x} (v^t . v)
       = 2 v^T \frac{\partial v}{\partial x}
$$
### Useful  gradients 

Reference: [Imperial College of London](<https://www.doc.ic.ac.uk/~dfg/ProbabilisticInference/InferenceAndMachineLearningNotes.pdf>) and (Petersen and Pederson, 2012) 

List of useful and pervasive identities for computing gradient in machine learning. 


$$
\displaystyle 

\begin{cases}

     \dfrac{\partial f(X)^T}{\partial X} 
        &=& \left[ 
              \dfrac{\partial f(X)}{\partial X} 
             \right]^T
        
  \\ \dfrac{\partial}{\partial x} tr(f(X)) 
       &=& tr 
         \left( \dfrac{\partial f(X)}{\partial X} \right)

  \\    \dfrac{\partial}{\partial X} \det f(X) 
       &=& det X  \; tr \left(X^{-1} 
           \dfrac{\partial f(X)}{\partial X} \right)

  \\  \dfrac{\partial}{\partial x} (x^t \cdot a) 
        &=& a^t


  \\  \dfrac{\partial}{\partial x} (a^t \cdot X \cdot b) 
        &=& a \cdot b^t

  \\ \dfrac{\partial}{\partial x} (x^t \cdot B \cdot x) 
        &=& x^t (B + B^t)
\end{cases}
$$
 
 
Where,
  + $\det A$ is the determinant (scalar) of a square matrix A.
  + $\mathrm{tr}(A)$ is the trace of matrix A, sum of diagonal elements.             