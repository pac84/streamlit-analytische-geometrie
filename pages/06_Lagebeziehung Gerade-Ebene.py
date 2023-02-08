import streamlit as st
import numpy as np
import sympy as sp

from pages.packages.geometrie import *
from pages.packages.latexout import *
from pages.packages.geogebra import *

rechner = Geometrie()
ggb = Geogebra()

st.header("Lagebeziehung von Gerade und Ebene")

st.markdown("""
Gib in die links die Daten einer Geraden und rechts einer Ebene ein. Die Werte werden durch ein Komma getrennt, Dezimalzahlen mit einem Punkt (z.B. 0.5) oder als Bruch (z.B. 1/2).
""")

col1, col2 = st.columns(2)

with col1:
    st.write("Gerade")
    eingabe_g_sv = st.text_input("Stützvektor von $g$")
    eingabe_g_rv = st.text_input("Richtungsvektor von $g$")
with col2:
    st.write("Ebene")
    eingabe_e_n = st.text_input("Normalenvektor von $E$")
    eingabe_e_p = st.text_input("Punkt auf $E$")
try:
    # Auswertung für E
    e_n_list = eingabe_e_n.split(',')
    e_n = tuple([sp.nsimplify(item) for item in e_n_list])
    e_p = sp.Point(eingabe_e_p.split(','))
    e_d = 0
    for i in range(len(e_n)):
        e_d+= e_n[i]*e_p[i]
    e = sp.geometry.Plane(e_p, normal_vector=e_n)

    # Auswertung für g
    g_rv_list = eingabe_g_rv.split(',')
    g_rv = tuple([sp.nsimplify(item) for item in g_rv_list])
    g_sv = sp.Point(eingabe_g_sv.split(','))
    g = sp.Line3D(g_sv, direction_ratio=g_rv)
    t = sp.symbols('t')
    gz1 = g_sv[0] + t * g_rv[0]
    gz2 = g_sv[1] + t * g_rv[1]
    gz3 = g_sv[2] + t * g_rv[2]
    
    schnittpunkt = e.intersection(g)
    
    x_1, x_2, x_3, d = sp.symbols('x_1 x_2 x_3 d')
    gleichung = e_n[0] * x_1 + e_n[1] * x_2 + e_n[2] * x_3
    gleichung2 = gleichung.subs([(x_1, sp.UnevaluatedExpr(gz1)), (x_2, sp.UnevaluatedExpr(gz2)), (x_3, sp.UnevaluatedExpr(gz3))], order='none')
    gleichung3 = gleichung.subs([(x_1, gz1), (x_2, gz2), (x_3, gz3)])

    gleichung22 = gleichung.subs([(x_1, sp.UnevaluatedExpr(g_sv.x)), (x_2, sp.UnevaluatedExpr(g_sv.y)), (x_3, sp.UnevaluatedExpr(g_sv.z))], order='none')
    gleichung32 = gleichung.subs([(x_1, g_sv.x), (x_2, g_sv.y), (x_3, g_sv.z)])

    lsg_t = sp.solve(gleichung3-e_d, t)

    if gleichung32 == e_d:
        auswertung = "Die Aussage in der letzten Zeile ist wahr, d.h. der Punkt von $g$ liegt in der Ebene $E$ und damit liegt die Gerade in der Ebene."
    else:
        auswertung = "Die Aussage in der letzten Zeile ist nicht wahr, d.h. der Punkt von $g$ liegt nicht in der Ebene $E$ und damit ist die Gerade parallel zur Ebene."
    if np.dot(e_n, g_rv) == 0:
        auswertung = r"""
    Da der Richtungsvektor orthogonal zum Normalenvektor ist, ist $g$ parallel zu $E$ oder $g$ liegt in $E$. Zur Überprüfung führt man eine Punktprobe mit dem Stützpunkt der Gerade $g$ durch.
    $$
    \begin{align*}
        %s &= %s \\
        %s &= %s \\
        %s &= %s
    \end{align*}
    $$
    %s
    """ % (sp.latex(gleichung), sp.latex(e_d),
           sp.latex(gleichung22), sp.latex(e_d),
           sp.latex(gleichung32), sp.latex(e_d), auswertung)
    else:
        auswertung = r"""
    Richtungsvektor und Normalenvektor sind nicht orthogonal zueinander, d.h. es gibt einen Schnittpunkt. Zur Berechnung des Schnittpunkts wird die Gerade zeilenweise in die Ebene eingesetzt und die Gleichung nach $t$ aufgelöst
    $$
    \begin{align*}
        %s &= %s \\
        %s &= %s \\
        %s &= %s \\
        t &= %s
    \end{align*}
    $$
    Durch Einsetzen des Wertes von $t$ in die Geradengleichung erhält man den Schnittpunkt
    $$
    \begin{align*}
        \vec{x} = %s + \left(%s\right) \cdot %s = \begin{pmatrix} %s \\ %s \\ %s \end{pmatrix}
    \end{align*}
    $$
    Die Gerade schneidet die Ebene im Punkt $P\left(%s|%s|%s\right)$.
    """ % (sp.latex(gleichung), sp.latex(e_d),
           sp.latex(gleichung2), sp.latex(e_d),
           sp.latex(gleichung3), sp.latex(e_d), sp.latex(lsg_t[0]),
           pmatrix(g_sv), sp.latex(lsg_t[0]), pmatrix(g_rv),
               sp.latex(schnittpunkt[0].x), sp.latex(schnittpunkt[0].y), sp.latex(schnittpunkt[0].z),
               sp.latex(schnittpunkt[0].x), sp.latex(schnittpunkt[0].y), sp.latex(schnittpunkt[0].z))

    st.markdown(r"""
    Es wurden folgende Gerade und Ebene eingegeben
    $$
    \begin{align*}
        %s \quad \text{und} \quad %s
    \end{align*}
    $$
    Wenn der Normalenvektor der Ebene und der Richtungsvektor der Gerade orthogonal sind, dann liegt die Gerade parallel zur Ebene oder die Gerade liegt in der Ebene. Andernfalls schneidet die Gerade die Ebene in einem Punkt.

    Berechnen des Skalarprodukts des Richtungsvektors der Geraden und des Normalenvektors der Ebene
    $$
    \begin{align*}
        %s \cdot %s = \left(%s\right)\cdot\left(%s\right) + \left(%s\right)\cdot\left(%s\right) + \left(%s\right)\cdot\left(%s\right) = %s
    \end{align*}
    $$
    %s
    """ % (gerade_sp('g', g), planeKoordinatengleichung('E', e_n, e_d),
           pmatrix(g_rv), pmatrix(e_n),
           sp.latex(g_rv[0]), sp.latex(e_n[0]), sp.latex(g_rv[1]), sp.latex(e_n[1]), sp.latex(g_rv[2]), sp.latex(e_n[2]) , sp.latex(np.dot(g_rv, e_n)), auswertung))

    if np.dot(e_n, g_rv) == 0:
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3d('E', e_n, e_d), ggb.gerade3dsp('g', g)]), height=600, width=800)
    else:
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3d('E', e_n, e_d), ggb.gerade3dsp('g', g), ggb.punkt3dsp('P', schnittpunkt[0])]), height=600, width=800)
except:
    st.write("Bitte korrekte Daten eingeben.")