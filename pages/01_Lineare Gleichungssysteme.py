import streamlit as st
import numpy as np
import sympy as sp
from fractions import Fraction
from latexifier import latexify

st.header("Lineare Gleichungssysteme")

st.markdown("""
Für das Lösen linearer Gleichungssysteme bietet sich ab drei Gleichungen mit drei Unbekannten das Gauß-Verfahren an. Dazu wird das Gleichungssystem durch die folgenden drei Umformungen in die obere Dreiecksgestalt gebracht:
- Multiplikation einer Gleichung mit einem Faktor
- Umformung einer Gleichung durch Addition/Subtraktion mit einer anderen Gleichung
- Tauschen von zwei Gleichungen
Gib für jede der drei Zeilen jeweils die Koeffizienten durch ein Komma getrennt in die drei Textfelder ein. Dezimalzahlen erhalten einen "." als Trennzeichen. Achte bei der Eingabe auf die Reihenfolge, erst $x_1$, $x_2$, $x_3$ und zum Schluss der Wert auf der rechten Seite des Gleichheitszeichens.
""")
z1 = st.text_input("Zeile 1")
z2 = st.text_input("Zeile 2")
z3 = st.text_input("Zeile 3")

z1a = z1.split(",")
z2a = z2.split(",")
z3a = z3.split(",")

x_1, x_2, x_3, t = sp.symbols("x_1, x_2, x_3, t")

try:
    matrix = sp.Matrix([z1a, z2a, z3a])
    # Testmatrizen für eine, keine und unendlich viele Lösungen
    #matrix = sp.Matrix([[1,2,1,9],[-2,-1,5,5],[1,-1,3,4]])
    #matrix = sp.Matrix([[2,-3,-1,4],[1,2,3,1],[3,-8,-5,5]])
    #matrix = sp.Matrix([[1,2,-3,6],[2,-1,4,2],[4,3,-2,14]])
    matrix2 = matrix.echelon_form()
    matrix3, mat_piv = matrix.rref()

    smatrix = sp.Matrix([z1a[:-1], z2a[:-1], z3a[:-1]])
    svektor = sp.Matrix([z1a[-1], z2a[-1], z3a[-1]])
    
    st.markdown(r"""
    Es wurde das folgende LGS eingegeben:
    $$
    \begin{align*}
        %s
    \end{align*}
    $$
    Durch Umformen erhält man folgende Matrix in Stufenform
    $$
    \begin{align*}
        %s
    \end{align*}
    $$
    """ % (sp.latex(matrix,mat_str = "array",mat_delim="("), sp.latex(matrix2,mat_str = "array",mat_delim="(")))
    if len(mat_piv) == 3 and mat_piv[2] == 3:
        st.markdown(r"""
        Das LGS hat keine Lösung, da die Gleichung
        $$
        \begin{align*}
            0 \cdot x_1 + 0 \cdot x_2 + 0 \cdot x_3 = %s
        \end{align*}
        $$  
        in der letzten Zeile keine Lösung besitzt.""" % (sp.latex(matrix2[2,3])))
    else:
        if len(mat_piv) == 3:
            gl3 = matrix2[2,2] * x_3 - matrix2[2,3]
            lsg3 = sp.solve(gl3, x_3)
            zeile1 = r"""%s &= %s \\
            x_3 &= %s
            """ % (sp.latex(matrix2[2,2] * x_3), sp.latex(matrix2[2,3]), sp.latex(lsg3[0]))
        else:
            lsg3 = [t]
            zeile1 = r"x_3 &= t"
        gl2 = matrix2[1,1] * x_2 + matrix2[1,2] * lsg3[0] - matrix2[1,3]
        lsg2 = sp.solve(gl2, x_2)
        gl1 = matrix2[0,0] * x_1 + matrix2[0,1] * lsg2[0] + matrix2[0,2] * lsg3[0] - matrix2[0,3]
        lsg1 = sp.solve(gl1, x_1)

        st.markdown(r"""
        Das LGS hat eine Lösung, Berechnung von $x_3$ mithilfe der letzten Gleichung
        $$
        \begin{align*}
            %s
        \end{align*}
        $$
        Lösung für $x_3$ in die 2. Zeile einsetzen und $x_2$ berechnen
        $$
        \begin{align*}
            %s &= %s \\
            x_2 &= %s
        \end{align*}
        $$
        Lösung für $x_3$ und $x_2$ in die 1. Zeile einsetzen und $x_1$ berechnen
        $$
        \begin{align*}
            %s &= %s \\
            x_1 &= %s
        \end{align*}
        $$
        Die Lösung des LGS ist
        $$
        \begin{align*}
            x_1 &= %s \\
            x_2 &= %s \\
            x_3 &= %s
        \end{align*}
        $$
        """ % (zeile1,
        sp.latex(matrix2[1,1] * x_2 + matrix2[1,2] * lsg3[0]), sp.latex(matrix2[1,3]), sp.latex(lsg2[0]),
        sp.latex(matrix[0,1] * x_1 + matrix2[1,1] * lsg2[0] + matrix2[1,2] * lsg3[0]), sp.latex(matrix2[0,3]), sp.latex(lsg1[0]),
        sp.latex(lsg1[0]), sp.latex(lsg2[0]), sp.latex(lsg3[0])))
except:
    st.write("Bitte korrekte Daten eingeben.")