import streamlit as st
import numpy as np
import sympy as sp

from pages.packages.geometrie import *
from pages.packages.latexout import *

st.header("Geradengleichung aufstellen")

st.markdown("""
Gib in die beiden Textfelder die Koordinaten von zwei Punkten ein, die auf einer Geraden liegen. Die Koordinaten werden durch ein Komma getrennt, für Dezimalzahlen wird der Punkt verwendet.
""")

col1, col2 = st.columns(2)

with col1:
    eingabe_a = st.text_input("Punkt 1")
with col2:
    eingabe_b = st.text_input("Punkt 2")

rechner = Geometrie()

try:
    a = sp.Matrix([eingabe_a.split(",")])
    b = sp.Matrix([eingabe_b.split(",")])
    v = b-a

    st.markdown(r"""
    Wähle den Ortsvektor des Punktes 1 als Stützvektor
    $$
    \begin{align*}
        \vec{p} = %s
    \end{align*}
    $$
    und den Verbindungsvektor der beiden Punkte als Richtungsvektor
    $$
    \begin{align*}
        \vec{v} = %s - %s = %s
    \end{align*}
    $$
    Die Geradengleichung lautet
    $$
    \begin{align*}
        g: \vec{x} = %s + t \cdot %s
    \end{align*}
    $$
    """ % (pmatrix(a), pmatrix(b), pmatrix(a), pmatrix(v), pmatrix(a), pmatrix(v)))
    
except:
    st.write("Bitte korrekte Werte eingeben.")