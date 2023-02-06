import streamlit as st
import numpy as np
import sympy as sp

from pages.packages.geometrie import *
from pages.packages.latexout import *
from pages.packages.geogebra import *

rechner = Geometrie()
ggb = Geogebra()

st.header("Geradengleichung aufstellen")

st.markdown("""
Gib in die beiden Textfelder die Koordinaten von zwei Punkten ein, die auf einer Geraden liegen. Die Koordinaten werden durch ein Komma getrennt, für Dezimalzahlen wird der Punkt verwendet.
""")

col1, col2 = st.columns(2)

with col1:
    st.write("Gerade 1")
    eingabe_g1_sv = st.text_input("Stützvektor 1")
    eingabe_g1_rv = st.text_input("Richtungsvektor 1")
with col2:
    st.write("Gerade 2")
    eingabe_g2_sv = st.text_input("Stützvektor 2")
    eingabe_g2_rv = st.text_input("Richtungsvektor 2")

try:
    g1_rv_list = eingabe_g1_rv.split(',')
    g2_rv_list = eingabe_g2_rv.split(',')

    g1_rv = tuple([sp.nsimplify(item) for item in g1_rv_list])
    g2_rv = tuple([sp.nsimplify(item) for item in g2_rv_list])
    g1_sv = sp.Point(eingabe_g1_sv.split(','))
    g2_sv = sp.Point(eingabe_g2_sv.split(','))
    g1 = sp.Line3D(g1_sv, direction_ratio=g1_rv)
    g2 = sp.Line3D(g2_sv, direction_ratio=g2_rv)

    parallel = sp.Line3D.is_parallel(g1,g2)
    
    t,s = sp.symbols('t s')
    g1z1 = g1_sv[0] + t * g1_rv[0]
    g1z2 = g1_sv[1] + t * g1_rv[1]
    g1z3 = g1_sv[2] + t * g1_rv[2]
    
    g2z1 = g2_sv[0] + s * g2_rv[0]
    g2z2 = g2_sv[1] + s * g2_rv[1]
    g2z3 = g2_sv[2] + s * g2_rv[2]

    if parallel:
        
        g1z1_lsg = sp.solve(g1z1-g2_sv[0],t)
        g1z2_lsg = sp.solve(g1z2-g2_sv[1],t)
        g1z3_lsg = sp.solve(g1z3-g2_sv[2],t)

        if g1 in g2:
            auswertung = "Die drei Gleichungen werden alle für denselben Wert von t gelöst, d.h. die Geraden sind **identisch**."
        else:
            auswertung = "Die drei Gleichungen werden nicht alle für denselben Wert von t gelöst, d.h. die Geraden sind **parallel**."
        berechnung = r"""
    Die Richtungsvektoren sind Vielfache voneinander, d.h. die beiden Geraden sind parallel oder identisch. Wenn ein Punkt (z.B. Stützpunkt von Gerade 2) auch auf Gerade 1 liegt, dann sind sie identisch, sonst parallel. Einsetzen des Stützvektors von Gerade 2 in Gerade 1
    $$
    \begin{align*}
        \color{red}%s + t \cdot %s \color{black}= \color{blue}%s
    \end{align*}
    $$
    liefert die folgenden drei Gleichungen, die nur von t abhängen
    $$
    \begin{align*}
        %s = %s \quad &\Rightarrow \quad t = %s\\
        %s = %s \quad &\Rightarrow \quad t = %s\\
        %s = %s \quad &\Rightarrow \quad t = %s
    \end{align*}
    $$
    %s
        """ % (pmatrix(g1_sv), pmatrix(g1_rv), pmatrix(g2_sv), sp.latex(g1z1), sp.latex(g2_sv[0]), sp.latex(g1z1_lsg[0]), sp.latex(g1z2), sp.latex(g2_sv[1]), sp.latex(g1z2_lsg[0]), sp.latex(g1z3), sp.latex(g2_sv[2]), sp.latex(g1z3_lsg[0]), auswertung)
    else: 
        lsg = sp.solve([g1z1-g2z1, g1z2-g2z2, g1z3-g2z3], s,t)
        schnittpunkt = sp.Line3D.intersection(g1,g2)

        if len(lsg) > 0:
            s1 = lsg[s]
            t1 = lsg[t]
            auswertung = r"""
    Das LGS ist lösbar für $t = %s$ und $s= %s$. Der Schnittpunkt wird berechnet, indem man den Wert von $t$ in $g_1$ oder den Wert von $s$ in $g_2$ einsetzt.
    $$
    \begin{align*}
        \vec{x} = %s + \left(%s\right) \cdot %s = \begin{pmatrix} %s \\ %s \\ %s \end{pmatrix}
    \end{align*}
    $$
    Die beiden Geraden schneiden sich im Punkt $P(%s|%s|%s)$.
        """ % (sp.latex(t1), sp.latex(s1),
               pmatrix(g1_sv), sp.latex(t1), pmatrix(g1_rv),
               sp.latex(schnittpunkt[0].x), sp.latex(schnittpunkt[0].y), sp.latex(schnittpunkt[0].z),
               sp.latex(schnittpunkt[0].x), sp.latex(schnittpunkt[0].y), sp.latex(schnittpunkt[0].z))
        else:    
            auswertung = "Das LGS ist nicht lösbar, d.h. die beiden Geraden sind **windschief** zueinander."
        berechnung = r"""
    Die Richtungsvektoren sind keine Vielfachen voneinander, d.h. die Geraden schneiden sich in einem Punkt oder sind windschief. Die beiden Geradengleichungen müssen gleichgesetzt werden und die Lösung des LGS bestimmt werden. Falls es keine Lösung gibt, sind die Geraden windschief. Gleichsetzen der beiden Geraden liefert
    $$
    \begin{align*}
        \color{red}%s + t \cdot %s \color{black}= \color{blue}%s + s \cdot %s
    \end{align*}
    $$    
    und damit die drei Gleichungen
    $$
    \begin{align*}
        %s = %s \\
        %s = %s \\
        %s = %s 
    \end{align*}
    $$
    %s
        """ % (pmatrix(g1_sv), pmatrix(g1_rv), pmatrix(g2_sv), pmatrix(g2_rv),
               sp.latex(g1z1),sp.latex(g2z1),sp.latex(g1z2),sp.latex(g2z2),sp.latex(g1z3),sp.latex(g2z3), auswertung)
        

    st.markdown(r"""
    Bei Geraden im Raum gibt es vier mögliche Lagebeziehungen, die sich abhängig von den Richtungsvektoren in zwei Fälle gruppieren lassen:
    - Wenn die Richtungsvektoren Vielfache voneinander sind
        - und sie einen gemeinsamen Punkt haben (Punktprobe), dann sind sie **identisch**.
        - sie keinen gemeinsamen Punkt haben (Punktprobe), dann sind sie **parallel**.
    - Wenn die Richtungsvektoren keine Vielfachen sind und
        - das LGS beim Gleichsetzen der beiden Geradengleichungen eine Lösung liefert, dann **schneiden sie sich**.
        - das LGS keine Lösung liefert, dann sind sie **windschief**.

    Folgende Geradengleichungen wurden eingegeben
    $$
    \begin{align*}
        \color{red}  g_1: \vec{x} &\color{red}  =%s + t \cdot %s\\
        \color{blue} g_2: \vec{x} &\color{blue} = %s + s \cdot %s
    \end{align*}
    $$
    %s
    """ % (pmatrix(g1_sv), pmatrix(g1_rv), pmatrix(g2_sv), pmatrix(g2_rv), berechnung))
    if len(lsg)>0:
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_1',g1), ggb.gerade3dsp('g_2', g2), ggb.farbe('g_1', 'red'), ggb.farbe('g_2', 'blue'),  ggb.punkt3dsp('P',
                                                                                                                                                                                      schnittpunkt[0])]), height=600, width=800)
    else: 
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_1',g1), ggb.gerade3dsp('g_2', g2), ggb.farbe('g_1', 'red'), ggb.farbe('g_2', 'blue')]), height=600, width=800)
except:
    st.write("Bitte korrekte Werte eingeben.")