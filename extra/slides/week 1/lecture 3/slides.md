\[circle\] \[circle\]

# 

<div class="frame">

Outline

</div>

# Introduction to Python

<div class="frame">

Introduction to Python

<div class="center">

Why Python?

</div>

- A **high-level** language for
  **beginners**

- with a **clean syntax**, but...

- **Industrial strength** programming
  language used at thousands of companies (one of three official Google
  languages)

- Free, well documented, well supported

<div class="alert alert-block alert-info">

Recall We will use Python 3 (there are non-backwards compatible
differences with respect to Python 2). Further, Python 2 is now
unsupported.

</div>

</div>

<div class="frame">

A (Python) program is composed by a sequence of:

- **definitions** (also
  **expressions**) which are
  **evaluated**

- **statements** (also
  **commands**) which are
  **executed**

In plain terms...

- **expressions** yield some results (e.g.,
  `5 * 5`)

- **statements** instruct the interpreter to
  do something (e.g., print on screen, assign to variable)

Expressions and statements can either

- be directly written into a shell (<span style="color: red">interactive
  mode</span>)

- be written into a text file and then loaded into the shell
  (**script mode**).

</div>

<div class="frame">

<div class="center">

Interactive vs. Script Mode

</div>

Interactive Mode:  
perfectly fine for testing and learning.  
Type your commands/expressions into the shell and Python will
execute/evaluate those immediately:

|             |                    |
|:------------|:-------------------|
| `>>> 5 * 5` | $\leftarrow$input  |
| `25`        | $\leftarrow$output |

Script Mode:  
is what you normally do.  

- write the entire source code in a text file ending with the `.py`
  extension (say `myscript.py`)

- `myscript.py` will be executed in its entirety by the Python
  interpreter

</div>

# Programming in Python

<div class="frame">

Programming in Python

</div>

# Scalar Objects

<div class="frame">

Scalar Objects

- `int`: represents integers (e.g., `5`)

- `float`: represents real numbers (e.g., `3.14`)

- `bool`: represents Boolean values (`True` or `False`)

- `NoneType`: special with only one value (`None`)

<div class="alert alert-block alert-info">

Hint Use the `type()` function if you are not sure about the data type.

</div>

Examples:

|                 |                    |
|:----------------|:-------------------|
| `>>> type(109)` | $\leftarrow$input  |
| `<class 'int'>` | $\leftarrow$output |

|                   |                    |
|:------------------|:-------------------|
| `>>> type(10.9)`  | $\leftarrow$input  |
| `<class 'float'>` | $\leftarrow$output |

</div>

## Type `int()`

<div class="frame">

Values:  
$\ldots, -3, -2, -1, 0, 1, 2, 3, \ldots$  
Integer literals look like a sequence of numbers with no periods nor
commas.  
Operations:  

- +, -, \*, /

- \*\*

- unary -

- %

<div class="alert alert-block alert-info">

Note In Python 3, operations between integers may not yield an integer.

</div>

Examples:

<div class="flushleft">

|            |                                          |
|:-----------|:-----------------------------------------|
| `>>> 7/5`  | $\leftarrow$input                        |
| `1.4`      | $\leftarrow$output                       |
| `>>> 7//5` | $\leftarrow$ `//` is the floor division! |
| `1`        |                                          |

</div>

</div>

## Type `float()`

<div class="frame">

Values:  
some (approximated) range of $\mathbb{R}$  
Note that:  

- numbers with a "`.`" are decimals (e.g., `2.0`)

- numbers with no decimal separator are integers (e.g., `2`)

Operations:  

- +, -, \*, /

- \*\*

- unary -

- %

<div class="alert alert-block alert-info">

Note In Python 3, operations between floats or between a float and an
integer, always yield a float.

</div>

Indeed:

<div class="flushleft">

|               |                                          |
|:--------------|:-----------------------------------------|
| `>>> 7.0/5.0` | $\leftarrow$input                        |
| `1.4`         | $\leftarrow$output                       |
| `>>> 7.0//5`  | $\leftarrow$ `//` is the floor division! |
| `1.0`         |                                          |

</div>

</div>

<div class="frame">

Python stores floating point numbers as base 2 (binary) fractions:
$$\text{\{number\}} = \text{\{integer mantissa\}} \cdot 2^{-\text{\{exponent\}}}$$
For example:
$0.125 = 1 \cdot 2^{-3} = 1\cdot \frac{1}{2^3}=1\cdot \frac{1}{8}$.

<div class="alert alert-block alert-info">

Warning Not all numbers can be represented in base 2 fractions. Python
chooses the best approximation it can. The same also holds for some
numbers in base 10 fraction. What about 1/3?

</div>

Python may yield some <span style="color: red">approximation
errors</span>, that propagate as expressions go through.  
Example:

<div class="flushleft">

|                                       |                    |
|:--------------------------------------|:-------------------|
| `>>> 0.1+0.2`                         | $\leftarrow$input  |
| `0.30000000000000004`                 | $\leftarrow$output |
| `>>> 0.1+0.2+0.1+0.2`                 |                    |
| `0.6000000000000001`                  |                    |
| `>>> 0.1+0.2+0.1+0.2+0.1+0.2+0.1+0.2` |                    |
| `1.2000000000000002`                  |                    |

</div>

</div>

## Type `bool`

<div class="frame">

Values:  
`True` and `False` (capitalized!)  
Operations:  

- not `a` = $\begin{cases}
          \texttt{True} & \text{if} \texttt{ a } \text{is} \texttt{ False }\\
          \texttt{False} & \text{if} \texttt{ a } \text{is} \texttt{ True }
      \end{cases}$

- `a` and `b` = $\begin{cases}
          \texttt{True} & \text{if both} \texttt{ b } \text{and} \texttt{ a } \text{are} \texttt{ True}\\
          \texttt{False} & \text{otherwise}
      \end{cases}$

- `a` or `b` = $\begin{cases}
          \texttt{True} & \text{if} \texttt{ a } \text{is} \texttt{ True } \text{or} \texttt{ b } \text{is} \texttt{ True }\\
          \texttt{False} & \text{otherwise}
      \end{cases}$

Booleans are the output of comparisons between items (e.g., `int` or
`float`):

Order:  
`i<j`, `i>j`, `i<=j`, `i>=j`

(In)equality:  
`i!=j`, `i==j`

</div>

<div class="frame">

|   `a`   |   `b`   | not `a` | not `b` | `a` and `b` | `a` or `b` |
|:-------:|:-------:|:-------:|:-------:|:-----------:|:----------:|
| `True`  | `True`  | `False` | `False` |   `True`    |   `True`   |
| `False` | `False` | `True`  | `True`  |   `False`   |  `False`   |
| `True`  | `False` | `False` | `True`  |   `False`   |   `True`   |
| `False` | `True`  | `True`  | `False` |   `False`   |   `True`   |

Truth Table between two Boolean variables `a` and `b`

</div>

## Type Conversions

<div class="frame">

Switching between `float` and `int` can be performed via
**casting**
(**explicit** conversion):

- `float(2)` converts value `2` (integer) to `2.0` (floating point)

- `int(2.9)` converts value `2.9` (floating point) to `2` (integer)

<div class="alert alert-block alert-info">

Warning `int()` does not round to the nearest integer: rather, it
truncates the decimal part. To round to the nearest integer, use
`round()` instead.

</div>

Python supports **widening** automatically
(**implicit** conversion):
$$\underbrace{\texttt{bool} \rightarrow \texttt{int} \rightarrow \texttt{float}}_\text{narrow to wide}$$

Widening:  
Python does it automatically, if needed  
Example: `1/0.5=2.0` because Python casts `1` to `float`

Narrowing:  
Python never does it automatically  
Because narrowing leads to information loss!

</div>

# Expressions

<div class="frame">

Expressions

- **Expressions** are combinations of
  **objects** and
  **operators**

- an expression yields a **value**, which
  has its own **type**

- the simplest expression has the form:

  <div class="center">

  `<object, operator, object>`

  </div>

</div>

## Arithmetic Operations on `int` and `float`: a Recap

<div class="frame">

<div class="tabular">

@ccc@ **Syntax** & **Operator** & **Output Type**  
`i+j` & Sum &  
`i-j` & Difference &  
`i*j` & Product &  
`i/j` & Division & result is float (always)  
`i%j` & Remainder (Modulo) &  
`i**j` & Power of &  
`i//j` & Floor division &  

</div>

</div>

## Comparison Between `int`s and `float`s: a Recap

<div class="frame">

<div class="alert alert-block alert-info">

Note Comparisons below evaluate to a `bool`.

</div>

|        |               |                                                       |
|:-------|:--------------|:------------------------------------------------------|
| `i<j`  | $\rightarrow$ | returns `True` if `i` is smaller than `j`             |
| `i<=j` | $\rightarrow$ | returns `True` if `i` is smaller than or equal to `j` |
| `i>j`  | $\rightarrow$ | returns `True` if `i` is greater than `j`             |
| `i>=j` | $\rightarrow$ | returns `True` if `i` is greater than or equal to `j` |
| `i==j` | $\rightarrow$ | returns `True` if `i` is equal to `j`                 |
| `i!=j` | $\rightarrow$ | returns `True` if `i` is not equal to `j`             |

Comparisons can be chained arbitrarily and comparisons have the same
priority:  

<div class="center">

`i<j<k` is the same as `i<j and j<k`

</div>

Since comparisons do not act in a pairwise fashion, ‘weird' comparisons
like

<div class="center">

`i<j>k`

</div>

are perfectly valid.

</div>

## Operator Precedence

<div class="frame">

Precedence between operators can be ‘forced' via parenthesis.  
In principle, operators follow the
**PEMDAS** order:

1.  **P**arenthesis

2.  **E**xponential

3.  **M**ultiplication and
    **D**ivision

4.  **A**ddition and
    **S**ubtraction

</div>

<div class="frame">

<div class="center">

The Big Picture

</div>

1.  Parenthesis: `(...)`

2.  Exponentiation: `**`

3.  Unary operators: `+` and `-`

4.  Binary arithmetic: `*`, `/`, `//` and `%`

5.  Binary arithmetic: `+` and `-`

6.  Comparisons: `>`, `<`, `>=`, `<=`, `==`, `!=`

7.  Logical not

8.  Logical and

9.  Logical or

<div class="alert alert-block alert-info">

Note Same line means same precedence. Read ties left to right.

</div>

<div class="alert alert-block alert-info">

Hint In case of emergency, use parenthesis!

</div>

</div>

# References

<div class="frame">

References

- Guttag, J. V. (2013). *Introduction to Computation and Programming
  using Python (Revised and Expanded Edition)*. MIT Press. \[Section
  2.1\]

- Downey, A. (2015). *Think Python*. Green Tea Press ed. 2nd. \[Sections
  1.2–1.5, 2.5, 5.1–5.3\]

- <https://docs.python.org/3/tutorial/floatingpoint.html>

- <https://www.geeksforgeeks.org/chaining-comparison-operators-python/>

</div>
