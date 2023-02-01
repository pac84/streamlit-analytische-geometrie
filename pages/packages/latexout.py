# -*- coding: utf-8 -*-

import sympy as sy
import numpy as np
import math
from pages.packages.geometrie import Geometrie

rechner = Geometrie()

def pmatrix(a):
    ausgabe = r"\begin{pmatrix}"
    for item in a:
        ausgabe+= " " + sy.latex(sy.nsimplify(item)) + r" \\"
    ausgabe = ausgabe[:-2]
    ausgabe += r"\end{pmatrix}"
    return ausgabe#.replace("frac", "nicefrac")

#
# Punkt
#

def punkt(name, koordinaten):
    rv = name + r'\left( '
    for item in koordinaten:
        rv += str(sy.latex(item)) + r' \middle| '
    rv = rv[:-10]
    rv += r'\right)'
    return rv

#
# Geradengleichung
#

def line(name, parameter, stuetzvektor, richtungsvektor):
    rv = name + r': \vec{x} = '
    rv += pmatrix(stuetzvektor)
    rv += " + "
    rv += parameter + " \cdot "
    rv += pmatrix(richtungsvektor)
    return rv

def gerade(name, gerade):
    ausgabe = line(name, 't', gerade[0], gerade[1])
    return ausgabe

#
# Ebenengleichungen
#

def planeParameter(name, parameter1, parameter2, stuetzvektor, spannvektor1, spannvektor2):
    rv = name + r': \vec{x} = '
    rv += pmatrix(stuetzvektor)
    rv += " + "
    rv += parameter1 + " \cdot "
    rv += pmatrix(spannvektor1)
    rv += " + "
    rv += parameter2 + " \cdot "
    rv += pmatrix(spannvektor2)
    return rv

def planeKoordinatengleichung(name, normalenvektor, parameterD):
    ersterEintrag = True
    rv = name + ': '
    for i in range(len(normalenvektor)):
        if normalenvektor[i] != 0:
            
            if normalenvektor[i] > 0:
                if ersterEintrag:
                    rechenzeichen = " "
                else:
                    rechenzeichen = "+"
            else:
                rechenzeichen = " "
            
            if normalenvektor[i] == 1:
                faktor = ""
            elif normalenvektor[i] == -1:
                faktor = "-"
            else:
                #faktor = str(sy.latex(normalenvektor[i]))
                faktor = str(normalenvektor[i])
            rv += rechenzeichen + faktor + r"x_{" + str(i+1) + r"} "
            ersterEintrag = False
    rv = rv[:-1]
    rv += " = " + str(parameterD)
    return rv

def planeNormalengleichung(name, normalenvektor, stuetzvektor):
    rv = name + r": \left(\vec{x} - "
    rv += pmatrix(stuetzvektor) + r"\right) \cdot "
    rv += pmatrix(normalenvektor) + r" = 0"
    return rv

def ebeneKoordinatengleichung(name, ebene):
    ausgabe = planeKoordinatengleichung(name, ebene[0], ebene[1])
    return ausgabe

def ebeneNormalengleichung(name, ebene):
    ebeneNormal = rechner.ebeneInNormalengleichung(ebene)
    ausgabe = planeNormalengleichung(name, ebeneNormal[0], ebeneNormal[1])
    return ausgabe

def ebeneParameterform(name, ebene):
    ebeneParameter = rechner.ebeneInParameterform(ebene)
    ausgabe = planeParameter(name, 's', 't', ebeneParameter[0], ebeneParameter[1], ebeneParameter[2])
    return ausgabe