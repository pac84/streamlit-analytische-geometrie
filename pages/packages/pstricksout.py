# -*- coding: utf-8 -*-

from numpy.core.records import array
import sympy as sy
import numpy as np
import math
from geometrie import Geometrie

rechner = Geometrie()

def Punkt(punkt, hilfslinien):
    if hilfslinien == True:
        ausgabe = r'\pstThreeDDot[drawCoor=true, dotstyle=*, dotsize=5pt]('
    else:
        ausgabe = r'\pstThreeDDot[drawCoor=false, dotstyle=*, dotsize=5pt]('    
    for i in punkt:
        ausgabe += str(sy.N(i,3)) + ','
    ausgabe = ausgabe[:-1] + ')'
    return ausgabe

def Vektor(anfang, ende):
    ausgabe = r'\def\farbe{blue}' + '\n'
    ausgabe += r'\pstThreeDLine[linecolor=\farbe, linewidth=0.8pt, arrowscale=2]{->}('

    for i in anfang:
        ausgabe += str(sy.N(i,3)) + ','
    ausgabe = ausgabe[:-1] + ')'
        
    ausgabe += '('

    for i in ende:
        ausgabe += str(sy.N(i,3)) + ','
    ausgabe = ausgabe[:-1] + ')'

    return ausgabe

def Gerade(gerade, hilfslinien, verlaengerung1, verlaengerung2):
    punkt1 = np.asarray(gerade[0])-verlaengerung1*np.asarray(gerade[1])
    punkt2 = np.asarray(gerade[0])+verlaengerung2*np.asarray(gerade[1])

    ausgabe = r'\def\farbe{blue}' + '\n'
    ausgabe += r'\pstThreeDLine[linecolor=\farbe, linewidth=0.8pt]('

    for i in punkt1:
        ausgabe += str(sy.N(i,3)) + ','
    ausgabe = ausgabe[:-1] + ')'
        
    ausgabe += '('

    for i in punkt2:
        ausgabe += str(sy.N(i,3)) + ','
    ausgabe = ausgabe[:-1] + ')'

    if hilfslinien == True:
        hilfspunkt = np.asarray(gerade[0]) + np.asarray(gerade[1])
        ausgabe += '\n' + Punkt(gerade[0], True) + '\n'
        ausgabe += Punkt(hilfspunkt, True)

    return ausgabe

def Ebene(ebene):
    if ebene[1] == 0:
        return 'Ebene kann nicht eingezeichnet werden, liegt auf Koordinatenachse'
    spurpunkte = rechner.spurpunkteBerechnen(ebene)
    # Nur einen Achsenschnittpunkt
    if len(spurpunkte) == 1:
        indexPosition = indexNotNull(spurpunkte[0])
        ausgabe = r'\def\farbe{red}' + '\n'
        ausgabe += r'\def\sp{'+ str(sy.N(spurpunkte[0][indexPosition],3)) +'}' + '\n'
        ausgabe += r'\def\breite{5}' + '\n'
        ausgabe += r'\pgfmathsetmacro{\start}{\breite/2}' + '\n'
        if indexPosition == 0:
            ausgabe += r'\pstThreeDSquare[drawCoor=false, linestyle=none, linecolor=\farbe, linewidth=0.8pt, fillstyle=solid, fillcolor=\farbe, opacity=0.2](\sp,-\start,-\start)(0,\breite,0)(0,0,\breite)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](\sp,0,-\start)(\sp,0,\start)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](\sp,-\start,0)(\sp,\start,0)' + '\n'
        elif indexPosition == 1:
            ausgabe += r'\pstThreeDSquare[drawCoor=false, linestyle=none, linecolor=\farbe, linewidth=0.8pt, fillstyle=solid, fillcolor=\farbe, opacity=0.2](-\start,\sp,-\start)(\breite,0,0)(0,0,\breite)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](0,\sp,-\start)(0,\sp,\start)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](-\start,\sp,0)(\start,\sp,0)' + '\n'
        else:
            ausgabe += r'\pstThreeDSquare[drawCoor=false, linestyle=none, linecolor=\farbe, linewidth=0.8pt, fillstyle=solid, fillcolor=\farbe, opacity=0.2](-\start,-\start,\sp)(0,\breite,0)(\breite,0,0)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](0,-\start,\sp)(0,\start,\sp)' + '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe](-\start,0,\sp)(\start,0,\sp)' + '\n'
        return ausgabe

    # Zwei Achsenschnittpunkte
    elif len(spurpunkte) == 2:
        indexPosition1 = indexNotNull(spurpunkte[0])
        indexPosition2 = indexNotNull(spurpunkte[1])
        achseFrei = achseNichtGeschnitten(indexPosition1, indexPosition2)

        verbindung = spurpunkte[1] - spurpunkte[0]

        ausgabe = r'\def\farbe{red}' + '\n'
        ausgabe += r'\def\breite{8}' + '\n'
        ausgabe += r'\pstThreeDSquare[drawCoor=false, linecolor=\farbe, linestyle=none, linewidth=0pt, fillstyle=solid, fillcolor=\farbe, opacity=0.2]'
        ausgabe += '('

        for i in spurpunkte[0]:
            ausgabe += str(sy.N(i,3)) + ','
        ausgabe = ausgabe[:-1] + ')'
        
        ausgabe += '('

        for i in verbindung:
            ausgabe += str(sy.N(i,3)) + ','
        ausgabe = ausgabe[:-1] + ')'
        if achseFrei == 1:    
            ausgabe += r'(\breite,0,0)'
        if achseFrei == 2:    
            ausgabe += r'(0,\breite,0)'
        if achseFrei == 3:    
            ausgabe += r'(0,0,\breite)'

        ausgabe += '\n'
        ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe]'

        for item in spurpunkte:
            ausgabe += '('
            for i in item:
                ausgabe += str(sy.N(i,3)) + ','
            ausgabe = ausgabe[:-1] + ')'

        for spurpunkt in spurpunkte:
            ausgabe += '\n'
            ausgabe += r'\pstThreeDLine[linewidth=0.8pt, linecolor=\farbe]('

            for i in spurpunkt:
                ausgabe += str(sy.N(i,3)) + ','
            ausgabe = ausgabe[:-1] + ')'

            if achseFrei == 1:
                ausgabe += r'(\breite,' + str(sy.N(spurpunkt[1],3)) + r',' + str(sy.N(spurpunkt[2],3)) + ')'
            if achseFrei == 2:
                ausgabe += r'(' + str(sy.N(spurpunkt[0],3)) + r',\breite,' + str(sy.N(spurpunkt[2],3)) + ')'
            if achseFrei == 3:
                ausgabe += r'(' + str(sy.N(spurpunkt[0],3)) + r',' + str(sy.N(spurpunkt[1],3)) + r',\breite)'
        return ausgabe

    # Drei Achsenschnittpunkte
    elif len(spurpunkte) == 3:
        ausgabe = r'\def\farbe{red}' + '\n'
        ausgabe += r'\pstThreeDTriangle[drawCoor=false, linecolor=\farbe, linewidth=0.8pt, fillstyle=solid, fillcolor=\farbe, opacity=0.2]'
        for item in spurpunkte:
            ausgabe += '('
            for i in item:
                ausgabe += str(sy.N(i,3)) + ','
            ausgabe = ausgabe[:-1] + ')'
        return ausgabe
    
    else:
        return 'Keine Ebene definiert'


def indexNotNull(vektor):
    return max([index for index, el in enumerate(vektor) if el])

def achseNichtGeschnitten(index1, index2):
    value = index1 + index2

    if value == 1:
        return 3
    elif value == 2:
        return 2
    else:
        return 1

def Quader(eckpunkt, vekA, vekB, vekC):
    ausgabe = '\pstThreeDBox[hiddenLine, linewidth=1pt, drawCoor=false]('
    ausgabe += arrayToString(eckpunkt)
    ausgabe += ')(' + arrayToString(vekA) + ')(' + arrayToString(vekB) + ')(' + arrayToString(vekC) + ')'
    return ausgabe

def Kreis(mittelpunkt, richtungsvektor1, richtungsvektor2, farbe):
    ausgabe = '\pstThreeDCircle[linewidth=1pt, linecolor = black, fillstyle=solid, fillcolor=' + farbe + ', opacity=0.2]('
    ausgabe += arrayToString(mittelpunkt) + ')(' + arrayToString(richtungsvektor1) + ')(' + arrayToString(richtungsvektor2) + ')'
    return ausgabe

def arrayToString(eingabeArray):
    output = ''
    for item in eingabeArray:
        output += str(item) + ','
    return output[:-1]