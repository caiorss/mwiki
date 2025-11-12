import mwiki.latex as latex 


def test_get_latex_macros_1():
    macros = r"""
        \newcommand{\R}{\mathbb{R}};
    """
    expected = { r"\R": r"\mathbb{R}" }
    out = latex.get_latex_macros(macros)
    assert out == expected 
    

def test_get_latex_macros_2():
    macros = r"""
        \newcommand{\R}{  \mathbb{R}  };
    """
    expected = { r"\R": r"\mathbb{R}" }
    out = latex.get_latex_macros(macros)
    assert out == expected 


def test_get_latex_macros_3():
    macros = r"""
        \newcommand{ \R }{  \mathbb{R}  };
    """
    expected = { r"\R": r"\mathbb{R}" }
    out = latex.get_latex_macros(macros)
    assert out == expected 

    
def test_get_latex_macros_4():
    macros = r"""
        \newcommand{\Z}{\mathbb{Z}};
        \newcommand{\R}{\mathbb{R}};
    """
    expected = { r"\R": r"\mathbb{R}", 
                 r"\Z": r"\mathbb{Z}"
               }
    ## breakpoint()
    out = latex.get_latex_macros(macros)
    assert out == expected 

def test_get_latex_macros_5():
    macros = r"""
        \DeclareMathOperator*{\argmax}{arg\,max}
    """
    expected = { r"\argmax": r"\operatorname*{arg\,max}" }
    # breakpoint()
    out = latex.get_latex_macros(macros)
    assert out == expected 

def test_get_latex_macros_6():
    macros = r"""
        \DeclareMathOperator*{  \argmax  }{  arg\,max  }
    """
    expected = { r"\argmax": r"\operatorname*{arg\,max}" }
    ## breakpoint()
    out = latex.get_latex_macros(macros)
    assert out == expected 


def test_get_latex_macros_7():
    macros = r"""
        % Some commentary here
        \DeclareMathOperator{\argmin}{arg\,min}; % Some left commentary
    """
    expected = { r"\argmin": r"\operatorname{arg\,min}" }
    out = latex.get_latex_macros(macros)
    assert out == expected 

def test_get_latex_macros_8():
    macros = r"""
       % Macro shortcut \Z for \mathbb{Z}
            \newcommand{\Z}{\mathbb{Z}};

        \DeclareMathOperator*{  \argmax  }{  arg\,max  };

        \DeclareMathOperator{\argmin}{arg\,min};
        
        % Macro shortcut for the set of real numbers  
        \newcommand{\R}{\mathbb{R}};

        % Macro oneover, example \oneover{4} yields \frac{1}{4}
        \def\oneover{\frac{1}}

        % --- end of macros definition -----%
    """
    expected = {   r"\R": r"\mathbb{R}" 
                 , r"\Z": r"\mathbb{Z}"
                 , r"\argmax": r"\operatorname*{arg\,max}"
                 , r"\argmin": r"\operatorname{arg\,min}"
                 , r"\oneover": r"\frac{1}"
                 }
    out = latex.get_latex_macros(macros)
    assert out == expected 



def test_get_latex_macros_9():
    macros = r"""
        \newcommand{\pd}[2]{ \frac{\partial #1}{\partial #2} }
        \newcommand{  \pd2  }[2]  { \frac{\partial #1}{\partial #2} }
    """
    expected = {
          r"\pd":       r"\frac{\partial #1}{\partial #2}"
        , r"\pd2":      r"\frac{\partial #1}{\partial #2}"
    }
    out = latex.get_latex_macros(macros)
    assert out == expected 


def test_get_latex_macros_10():
    macros = r"""
        \newcommand{\p}{\partial}
        \newcommand{\supnorm}[1]{  \norm[\infty]{#1}  }
        \newcommand{\pd}[2]{ \frac{\partial #1}{\partial #2} }
    """
    expected = {
          r"\p":       r"\partial"
        , r"\pd":      r"\frac{\partial #1}{\partial #2}"
        , r"\supnorm": r"\norm[\infty]{#1}"
    }
    out = latex.get_latex_macros(macros)
    assert out == expected 

def test_get_latex_macros_11():
    macros = r"""
        \newcommand{\laplace}[1]{ \mathcal{L}\{#1\}  }
    """
    expected =  {
        r"\laplace": r"\mathcal{L}\{#1\}"
    }
    out= latex.get_latex_macros(macros)
    assert out == expected 


def test_get_latex_macros_12():
    macros = r"""
        \newcommand{\BigO}[1]{ \mathcal{O}\!\left(#1\right) }
    """
    expected =  {
        r"\BigO": r"\mathcal{O}\!\left(#1\right)"
    }
    out= latex.get_latex_macros(macros)
    assert out == expected 
