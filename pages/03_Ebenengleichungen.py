import streamlit as st
import numpy as np
import sympy as sp
from pages.packages.geometrie import *
from pages.packages.latexout import *

st.header("Ebenengleichung aufstellen")

st.markdown("""
Gib in die beiden Textfelder die Koordinaten von drei Punkten ein, die auf der Ebene liegen. Die Koordinaten werden durch ein Komma getrennt, für Dezimalzahlen wird der Punkt verwendet.
""")

col1, col2, col3 = st.columns(3)

with col1:
    eingabe_a = st.text_input("Punkt 1")
with col2:
    eingabe_b = st.text_input("Punkt 2")
with col3:
    eingabe_c = st.text_input("Punkt 3")

rechner = Geometrie()

try:
    a = sp.Matrix([eingabe_a.split(",")])
    b = sp.Matrix([eingabe_b.split(",")])
    c = sp.Matrix([eingabe_c.split(",")])
    u = b-a
    v = c-a
    n = u.cross(v)
    d = n.dot(a)
    nullvektor = True
    x_1, x_2, x_3 = sp.symbols('x_1 x_2 x_3')

    for komp in n:
        if komp != 0:
            nullvektor = False
    if nullvektor:
        st.write("Zu den gegebenen Punkten lässt sich keine Ebene aufstellen.")
    else:
        st.markdown(r"""
        Wähle den Ortsvektor des Punktes 1 als Stützvektor
        $$
        \begin{align*}
            \vec{p} = %s
        \end{align*}
        $$
        und als Spannvektoren die Verbindungsvektoren von Punkt 1 zu den anderen beiden Punkten
        $$
        \begin{align*}
            \vec{u} &= %s - %s = %s\\
            \vec{v} &= %s - %s = %s
        \end{align*}
        $$
        Die Ebenengleichung in **Parameterform** lautet
        $$
        \begin{align*}
            E: \vec{x} = %s + s \cdot %s + t \cdot %s
        \end{align*}
        $$
        Für die Normalengleichung braucht man einen Stützvektor und den Normalenvektor, der über das Vektorprodukt der beiden Spannvektoren berechnet wird
        $$
        \begin{align*}
            \vec{n} = %s \times %s = %s
        \end{align*}
        $$
        Damit erhält man die **Normalengleichung**
        $$
        \begin{align*}
            E: \left(\vec{x} - %s \right) \cdot %s = 0
        \end{align*}
        $$
        Für die Koordinatengleichung muss der Parameter d mithilfe des Skalarprodukts des Stützvektors und des Normalenvektors berechnet werden
        $$
        \begin{align*}
            d = %s \cdot %s = %s
        \end{align*}
        $$
        Mihilfe des Normalenvektors und dem Wert von d erhält man die **Koordinatengleichung**
        $$
        \begin{align*}
            E: %s = %s
        \end{align*}
        $$
        """ % (pmatrix(a), pmatrix(b), pmatrix(a), pmatrix(u), pmatrix(c), pmatrix(a), pmatrix(v), pmatrix(a), pmatrix(u), pmatrix(v),
        pmatrix(u), pmatrix(v), pmatrix(n),
        pmatrix(a), pmatrix(n),
        pmatrix(a), pmatrix(n), sp.latex(d),
        sp.latex(n[0]*x_1+n[1]*x_2+n[2]*x_3), sp.latex(d)))
except:
    st.write("Bitte korrekte Werte eingeben.")