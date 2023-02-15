import streamlit as st
import numpy as np
import sympy as sp

from pages.packages.geometrie import *
from pages.packages.latexout import *
from pages.packages.geogebra import *
from pages.packages.abstaende import *

rechner = Geometrie()
ggb = Geogebra()
abstand = Abstaende()

def eingabeAnzeigen(obj1, obj2):
    if isinstance(obj1, sp.geometry.Point3D):
        str_obj_1 = punkt('P_1', obj1)
    elif isinstance(obj1, sp.geometry.Line3D):    
        str_obj_1 = gerade_sp('g_1', obj1)
    elif isinstance(obj1, sp.geometry.Plane):
        str_obj_1 = "E_1:" + sp.latex(obj1.equation(x='x_1', y='x_2', z='x_3')) + "= 0"
    if isinstance(obj2, sp.geometry.Point3D):
        str_obj_2 = punkt('P_2', obj2)
    elif isinstance(obj2, sp.geometry.Line3D):    
        str_obj_2 = gerade_sp('g_2', obj2)
    elif isinstance(obj2, sp.geometry.Plane):
        str_obj_2 = "E_2:" + sp.latex(obj2.equation(x='x_1', y='x_2', z='x_3')) + "= 0"
    ausgabe = r"""
    Es wurden folgende Daten eingegeben
    $$
    \begin{align*}
    & %s \\
    & %s
    \end{align*}
    $$
    """ % (str_obj_1, str_obj_2)
    return ausgabe

st.header("Abstände")

st.markdown("""
Wähle aus, zwischen welcher Art von Objekten der Abstand berechnet werden soll und gib die dafür benötigten Werte ein. Dezimalzahlen werden mit einem "." eingegeben und die einzelnen Koordinaten mit einem "," getrennt. Es können auch Brüche (z.B. "1/2") eingegeben werden.
""")

col1, col2 = st.columns(2)

auswahl1, auswahl2 = 0,0
t,s = sp.symbols('t s')

with col1:
    ob1_auswahl = st.radio('Objekt 1', ['Punkt 1', 'Gerade 1', 'Ebene 1'])
    if ob1_auswahl == 'Punkt 1':
        auswahl1 = 1
        eingabe_p1 = st.text_input("Koordinaten von $P_1$")
        try:
            p_1 = sp.Point(eingabe_p1.split(','))
        except:
            st.write('korrekte Daten eingeben')
    elif ob1_auswahl == 'Gerade 1':
        auswahl1 = 2
        eingabe_g1_sv = st.text_input("Stützvektor 1")
        eingabe_g1_rv = st.text_input("Richtungsvektor 1")
        try:
            g1_rv_list = eingabe_g1_rv.split(',')
            g1_rv = tuple([sp.nsimplify(item) for item in g1_rv_list])
            g1_sv = sp.Point(eingabe_g1_sv.split(','))
            g1 = sp.Line3D(g1_sv, direction_ratio=g1_rv)
            g1z1 = g1_sv[0] + t * g1_rv[0]
            g1z2 = g1_sv[1] + t * g1_rv[1]
            g1z3 = g1_sv[2] + t * g1_rv[2]
        except:
            st.write('korrekte Daten eingeben')
    elif ob1_auswahl == 'Ebene 1':
        auswahl1 = 3
        eingabe_e1_n = st.text_input("Normalenvektor von $E_1$")
        eingabe_e1_p = st.text_input("Punkt auf $E_1$")
        try:
            e1_n_list = eingabe_e1_n.split(',')
            e1_n = tuple([sp.nsimplify(item) for item in e1_n_list])
            e1_p = sp.Point(eingabe_e1_p.split(','))
            e1_d = 0
            for i in range(len(e1_n)):
                e1_d+= e1_n[i]*e1_p[i]
            e1 = sp.geometry.Plane(e1_p, normal_vector=e1_n)
        except:
            st.write('korrekte Daten eingeben')

with col2:
    ob2_auswahl = st.radio('Objekt 2', ['Punkt 2', 'Gerade 2', 'Ebene 2'])
    if ob2_auswahl == 'Punkt 2':
        auswahl2 = 1
        eingabe_p2 = st.text_input("Koordinaten von $P_2$")
        try:
            p_2 = sp.Point(eingabe_p2.split(','))
        except:
            st.write('korrekte Daten eingeben')
    elif ob2_auswahl == 'Gerade 2':
        auswahl2 = 2
        eingabe_g2_sv = st.text_input("Stützvektor 2")
        eingabe_g2_rv = st.text_input("Richtungsvektor 2")
        try:
            g2_rv_list = eingabe_g2_rv.split(',')
            g2_rv = tuple([sp.nsimplify(item) for item in g2_rv_list])
            g2_sv = sp.Point(eingabe_g2_sv.split(','))
            g2 = sp.Line3D(g2_sv, direction_ratio=g2_rv)
            g2z1 = g2_sv[0] + s * g2_rv[0]
            g2z2 = g2_sv[1] + s * g2_rv[1]
            g2z3 = g2_sv[2] + s * g2_rv[2]
        except:
            st.write('korrekte Daten eingeben')
    elif ob2_auswahl == 'Ebene 2':
        auswahl2 = 3
        eingabe_e2_n = st.text_input("Normalenvektor von $E_2$")
        eingabe_e2_p = st.text_input("Punkt auf $E_2$")
        try:
            e2_n_list = eingabe_e2_n.split(',')
            e2_n = tuple([sp.nsimplify(item) for item in e2_n_list])
            e2_p = sp.Point(eingabe_e2_p.split(','))
            e2_d = 0
            for i in range(len(e2_n)):
                e2_d+= e2_n[i]*e2_p[i]
            e2 = sp.geometry.Plane(e2_p, normal_vector=e2_n)
        except:
            st.write('korrekte Daten eingeben')

if auswahl1 == 1 and auswahl2 == 1:
    try:
        st.markdown(eingabeAnzeigen(p_1, p_2))
        st.markdown(r"""
        Einsetzen der Koordinaten der Punkte in die Formel für den Abstand
        %s
        """ % (abstand.punkt_punkt(p_1, p_2)))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.punkt3dsp('P_1', p_1),ggb.punkt3dsp('P_2', p_2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 2 and auswahl2 == 2:
    try:
        st.markdown(eingabeAnzeigen(g1, g2))
        st.markdown(abstand.gerade_gerade(g1, g2))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_1', g1), ggb.gerade3dsp('g_2', g2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 3 and auswahl2 == 3:
    try:
        st.markdown(eingabeAnzeigen(e1, e2))
        st.markdown(abstand.ebene_ebene(e1,e2))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3dsp('E_1',e1),ggb.ebene3dsp('E_2',e2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 1 and auswahl2 == 2:
    try:
        st.markdown(eingabeAnzeigen(p_1, g2))
        st.markdown(abstand.punkt_gerade(p_1,g2))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_2', g2), ggb.punkt3dsp('P_1', p_1)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 2 and auswahl2 == 1:
    try:
        st.markdown(eingabeAnzeigen(g1, p_2))
        st.markdown(abstand.punkt_gerade(p_2, g1))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.gerade3dsp('g_1', g1), ggb.punkt3dsp('P_2', p_2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 1 and auswahl2 == 3:
    try:
        st.markdown(eingabeAnzeigen(p_1, e2))
        st.markdown(abstand.punkt_ebene(p_1, e2))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3dsp('E_2', e2), ggb.punkt3dsp('P_1', p_1)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 3 and auswahl2 == 1:
    try:
        st.markdown(eingabeAnzeigen(e1, p_2))
        st.markdown(abstand.punkt_ebene(p_2, e1))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3dsp('E_1', e1), ggb.punkt3dsp('P_2', p_2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 2 and auswahl2 == 3:
    try:
        st.markdown(eingabeAnzeigen(g1, e2))
        st.markdown(abstand.gerade_ebene(g1, e2))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3dsp('E_2', e2), ggb.gerade3dsp('g_1', g1)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')
elif auswahl1 == 3 and auswahl2 == 2:
    try:
        st.markdown(eingabeAnzeigen(e1, g2))
        st.markdown(abstand.gerade_ebene(g2, e1))
        st.components.v1.html(ggb.ausgabeJavascript3d(600,800,[ggb.ebene3dsp('E_1', e1), ggb.gerade3dsp('g_2', g2)]), height=600, width=800)
    except:
        st.write('korrekte Daten eingeben')