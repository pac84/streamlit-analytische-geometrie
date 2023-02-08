import streamlit as st
import numpy as np
import sympy as sp

from pages.packages.geometrie import *
from pages.packages.latexout import *
from pages.packages.geogebra import *

rechner = Geometrie()
ggb = Geogebra()

st.header("Lagebeziehung von zwei Ebenen")

st.markdown("""
Gib in die beiden Textfelder die Werte des Normalenvektors und des Parameters d durch ein Komma getrennt ein.
""")

col1, col2 = st.columns(2)

with col1:
    st.write("Ebene 1")
    eingabe_e1_n = st.text_input("Normalenvektor von $E_1$")
    eingabe_e1_p = st.text_input("Punkt auf $E_1$")
with col2:
    st.write("Ebene 2")
    eingabe_e2_n = st.text_input("Normalenvektor von $E_2$")
    eingabe_e2_p = st.text_input("Punkt auf $E_2$")
try:
    e1_n_list = eingabe_e1_n.split(',')
    e2_n_list = eingabe_e2_n.split(',')
    
    e1_n = tuple([sp.nsimplify(item) for item in e1_n_list])
    e2_n = tuple([sp.nsimplify(item) for item in e2_n_list])

    e1_p = sp.Point(eingabe_e1_p.split(','))
    e2_p = sp.Point(eingabe_e2_p.split(','))

    e1_d,e2_d = 0, 0
    for i in range(len(e1_n)):
        e1_d+= e1_n[i]*e1_p[i]
        e2_d+= e2_n[i]*e2_p[i]

    e1 = sp.geometry.Plane(e1_p, normal_vector=e1_n)
    e2 = sp.geometry.Plane(e2_p, normal_vector=e2_n)
    
    st.markdown(r"""
    Die eingegebenen Ebenengleichungen sind
    $$
    \begin{align*}
        & \color{red} %s\\
        & \color{blue} %s
    \end{align*}
    $$
    """ % (planeKoordinatengleichung('E_1', e1_n, e1_d), planeKoordinatengleichung('E_2', e2_n, e2_d)))

    erg = rechner.lageEbenen([e1_n, e1_d], [e2_n, e2_d])

    if erg[0] == 2:
        t = sp.symbols('t')
        
        schnitt_gerade = sp.geometry.Line3D(erg[1][0], direction_ratio=erg[1][1])
        z1 = sp.sympify(schnitt_gerade.p1[0] + t * schnitt_gerade.direction_ratio[0], evaluate=False)
        z2 = sp.sympify(schnitt_gerade.p1[1] + t * schnitt_gerade.direction_ratio[1], evaluate=False)
        z3 = sp.sympify(schnitt_gerade.p1[2] + t * schnitt_gerade.direction_ratio[2], evaluate=False)

        st.markdown(r"""
        Die beiden Normalenvektoren sind keine Vielfachen voneinander, d.h. die Ebenen schneiden sich in einer Schnittgeraden. Zur Berechnung der Geradengleichung wird in einer Ebenengleichung $x_1$, $x_2$ oder $x_3$ durch einen Parameter $t$ ersetzt (meist $x_3=t$) und die Gleichung nach einer der beiden verbleibenden Variablen umgestellt. Anschließend setzt man beides in die andere Ebene ein und bestimmt die verbleibende Koordinate in Abhängigkeit von $t$. 
        
        In diesem Fall erhält man
        $$
        \begin{align*}
            x_1 &= %s\\
            x_2 &= %s\\
            x_3 &= %s
        \end{align*}
        $$
        Daraus ergibt sich die Gleichung der Schnittgerade zu
        $$
        \begin{align*}
            %s
        \end{align*}
        $$
        """ % (sp.latex(z1), sp.latex(z2), sp.latex(z3), gerade_sp('g', schnitt_gerade)))
        
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_1',schnitt_gerade), ggb.ebene3d('E_1', e1_n, e1_d), ggb.ebene3d('E_2', e2_n, e2_d), ggb.farbe('E_1', 'red'), ggb.farbe('E_2', 'blue')]), height=600, width=800)
    else:
        identisch = e1.equals(e2)
        x_1, x_2, x_3, d = sp.symbols('x_1 x_2 x_3 d')
        gleichung = e1_n[0] * x_1 + e1_n[1] * x_2 + e1_n[2] * x_3
        gleichung2 = gleichung.subs([(x_1, sp.UnevaluatedExpr(e2_p.x)), (x_2, sp.UnevaluatedExpr(e2_p.y)), (x_3, sp.UnevaluatedExpr(e2_p.z))], order='none')
        gleichung3 = gleichung.subs([(x_1, e2_p.x), (x_2, e2_p.y), (x_3, e2_p.z)])
        if identisch:
            auswertung = "Die Aussage in der letzten Zeile ist wahr. Der Punkt liegt in der Ebene, d.h. die Ebenen sind identisch."
        else:
            auswertung = "Die Aussage in der letzten Zeile ist nicht wahr. Der Punkt liegt nicht in der Ebene, d.h. die Ebenen sind parallel."
        st.markdown(r"""
        Die Normalenvektoren der beiden Ebenen sind Vielfache voneinander, d.h. die beiden Ebenen sind parallel zueinander oder sie sind identisch. Zur Überprüfung führt man eine Punktprobe eines Punktes der einen Ebene mit der anderen Ebene durch. Wenn ein Punkt der einen Ebene in der anderen Ebene liegt, dann sind die Ebenen identisch und ansonsten parallel.
        $$
        \begin{align*}
            %s &= %s\\
            %s &= %s\\
            %s &= %s
        \end{align*}
        $$
        %s
        """ % (sp.latex(gleichung), sp.latex(e1_d),
               sp.latex(gleichung2), sp.latex(e1_d),
               sp.latex(gleichung3), sp.latex(e1_d), auswertung))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3d('E_1', e1_n, e1_d), ggb.ebene3d('E_2', e2_n, e2_d), ggb.farbe('E_1', 'red'), ggb.farbe('E_2', 'blue')]), height=600, width=800)
except:
    st.write("Bitte korrekte Daten eingeben.")