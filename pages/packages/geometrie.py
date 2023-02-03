# -*- coding: utf-8 -*-

#from sympy import *
import sympy as sy
import numpy as np

class Geometrie():
    """
    Ebene ueber drei Punkte
    Ebene ueber Stuetzvektor und Normalenvektor
    Ebene ueber Normalenvektor und Parameter d
    Ebene ueber Stuetzvektor und zwei Spannvektoren

    Geraden ueber zwei Punkte
    Geraden ueber Stuetzvektor und Richtungsvektor

    """
    def description(self):
        print("Punkte, Geraden und Ebenen")

    def ebenePunkte(self, punkt1, punkt2, punkt3):
        spannvektor1 = np.asarray(punkt2)-np.asarray(punkt1)
        spannvektor2 = np.asarray(punkt3)-np.asarray(punkt1)

        normalenvektor = np.cross(spannvektor1, spannvektor2)
        normalenvektor = self.gcdArray(normalenvektor)
        parameterD = np.dot(punkt1, normalenvektor)
        return [normalenvektor, parameterD]

    def ebeneParameterform(self, stuetzvektor, spannvektor1, spannvektor2):
        normalenvektor = np.cross(spannvektor1,spannvektor2)
        parameterD = np.dot(stuetzvektor, normalenvektor)
        return [normalenvektor, parameterD]

    def ebeneKoordinatenform(self, normalenvektor, parameterD):
        return [normalenvektor, parameterD]

    def ebeneNormalenform(self, normalenvektor, stuetzvektor):
        parameterD = np.dot(stuetzvektor, normalenvektor)
        return [normalenvektor, parameterD]

    def geradeVektoren(self, stuetzvektor, richtungsvektor):
        return [stuetzvektor, richtungsvektor]

    def geradePunkte(self, punkt1, punkt2):
        richtungsvektor = np.asarray(punkt2)-np.asarray(punkt1)
        return [punkt1, richtungsvektor]
    


    """
    Umwandeln von Ebenen
    Koordinatengleichung in Normalengleichung
    Koordinatengleichung in Parameterform
    """

    def ebeneInNormalengleichung(self, ebene):
        spurpunkte = self.spurpunkteBerechnen(ebene)
        stuetzvektor = spurpunkte[0]
        return [ebene[0], stuetzvektor]
    
    def ebeneInParameterform(self, ebene):
        spurpunkte = self.spurpunkteBerechnen(ebene)
        achsen = np.array([1,0,0,0,1,0,0,0,1]).reshape(3,3)
        spannvektoren = np.array([])

        if len(spurpunkte) == 3:
            stuetzvektor = spurpunkte[0]
            spannvektor1 = spurpunkte[1] - spurpunkte[0]
            spannvektor2 = spurpunkte[2] - spurpunkte[0]
        elif len(spurpunkte) == 2:
            # löschen des else-teils
            stuetzvektor = spurpunkte[0]
            spannvektor1 = spurpunkte[1] - spurpunkte[0]
            for item in achsen:
                if np.dot(item, ebene[0]) == 0:
                    spannvektoren = np.append(spannvektoren, item)
            spannvektor2 = spannvektoren.astype(int)
        else: #ein Spurpunkt
            stuetzvektor = spurpunkte[0]
            for item in achsen:
                if np.dot(item, ebene[0]) == 0:
                    spannvektoren = np.append(spannvektoren, item)
            spannvektor1 = spannvektoren[0:3].astype(int)
            spannvektor2 = spannvektoren[3:6].astype(int)
        return [stuetzvektor, spannvektor1, spannvektor2]

    """
    Lagebeziehungen/Schnittpunkte
    Punkt - Gerade
    Punkte - Ebene
    Gerade - Gerade
    Gerade - Ebene
    Ebene - Ebene

    """
    def punktAufGerade(self, punkt, gerade):
        t = sy.Symbol('t')
        vektor = gerade[0] - punkt
        """system = Matrix(( (gerade[1][0], vektor[0]), (gerade[1][1], vektor[1]), (gerade[1][2], vektor[2]) ))
        x = solve_linear_system(system, t)"""
        x = sy.solve([gerade[1][0]*t - vektor[0], gerade[1][1]*t - vektor[1], gerade[1][2]*t - vektor[2]],t)
        """print(x)"""
        if len(x) > 0:
            return True
        else:
            return False

    def punktAufEbene(self, punkt, ebene):
        x = 0
        for i in range(len(punkt)):
            x += punkt[i]*ebene[0][i]
        if x == ebene[1]:
            return True
        else:
            return False

    def lageGeraden(self, gerade1, gerade2):
        t = sy.Symbol('t')
        u = sy.Symbol('u')

        if self.skalaresVielfaches(gerade1[1], gerade2[1]):
            if self.punktAufGerade(gerade1[0], gerade2):
                return [0, "Geraden sind identisch"]
            else:
                return [1, "Geraden sind parallel"]
        else:
            lsg = sy.solve([gerade1[0][0] + t * gerade1[1][0] - gerade2[0][0] - u * gerade2[1][0], 
                       gerade1[0][1] + t * gerade1[1][1] - gerade2[0][1] - u * gerade2[1][1], 
                       gerade1[0][2] + t * gerade1[1][2] - gerade2[0][2] - u * gerade2[1][2]], [t,u])
            if len(lsg) == 0:
                return [2, "Geraden sind windschief"]
            else:
                schnittpunkt = np.empty(0, int)
                for i in range(len(gerade1[0])):
                    temp = gerade1[0][i] + lsg[t] * gerade1[1][i]
                    schnittpunkt = np.append(schnittpunkt, temp)
                return [3, schnittpunkt]

    def lageGeradeEbene(self, gerade, ebene):
        if (np.dot(gerade[1], ebene[0]) == 0): 
            if self.punktAufEbene(gerade[0], ebene):
                return[0, "Gerade liegt in Ebene"]
            else:
                return[1, "Gerade und Ebene sind parallel"]
        else:
            t = sy.Symbol('t')
            lsg = sy.solve(ebene[0][0] * (gerade[0][0] + t * gerade[1][0]) + ebene[0][1] * (gerade[0][1] + t * gerade[1][1]) + ebene[0][2] * (gerade[0][2] + t * gerade[1][2]) - ebene[1], t)
            schnittpunkt = np.empty(0, int)
            for i in range(len(ebene[0])):
                temp = gerade[0][i] + lsg[0] * gerade[1][i]
                schnittpunkt = np.append(schnittpunkt, temp)
            return[2, schnittpunkt]

    def lageEbenen(self, ebene1, ebene2):
        x = sy.Symbol('x')
        y = sy.Symbol('y')
        z = sy.Symbol('z')
        
        #tempEbene1 = np.append(ebene1[0], ebene1[1])
        #tempEbene2 = np.append(ebene2[0], ebene2[1])

        gleichung = [ebene1[0][0]*x + ebene1[0][1]*y + ebene1[0][2]*z - ebene1[1], ebene2[0][0]*x + ebene2[0][1]*y + ebene2[0][2]*z - ebene2[1]]
        lsg = sy.linsolve(gleichung,(x,y,z))

        if self.skalaresVielfaches(ebene1[0], ebene2[0]):
            if len(lsg)==0:
                return [1, "Die Ebenen sind parallel"]
            else:
                return (0, "Die Ebenen sind identisch")
        else:
            (x0, y0, z0) = tuple(*lsg)
            xWert = x0.as_ordered_terms()
            yWert = y0.as_ordered_terms()
            zWert = z0.as_ordered_terms()
            
            stuetzvektor = np.empty(0, int)
            richtungsvektor = np.empty(0, int)

            for item in xWert:
                if item.is_number:
                    stuetzvektor = np.append(stuetzvektor, item)
                else:
                    richtungsvektor = np.append(richtungsvektor, item)
            if len(stuetzvektor) == 0:
                stuetzvektor = np.append(stuetzvektor, 0)
            if len(richtungsvektor) == 0:
                richtungsvektor = np.append(richtungsvektor, 0)
            
            for item in yWert:
                if item.is_number:
                    stuetzvektor = np.append(stuetzvektor, item)
                else:
                    richtungsvektor = np.append(richtungsvektor, item)
            if len(stuetzvektor) == 1:
                stuetzvektor = np.append(stuetzvektor, 0)
            if len(richtungsvektor) == 1:
                richtungsvektor = np.append(richtungsvektor, 0)

            for item in zWert:
                if item.is_number:
                    stuetzvektor = np.append(stuetzvektor, item)
                else:
                    richtungsvektor = np.append(richtungsvektor, item)
            if len(stuetzvektor) == 2:
                stuetzvektor = np.append(stuetzvektor, 0)
            if len(richtungsvektor) == 2:
                richtungsvektor = np.append(richtungsvektor, 0)
            
            nenner = np.empty(0, int)

            zahlErweitern = 1
            
            for item in richtungsvektor:
                nenner = sy.denom(item)
                zahlErweitern = sy.ilcm(zahlErweitern, nenner)
                
            richtungsvektor = richtungsvektor * zahlErweitern
            ausgabeRichtungsvektor = np.array([])

            for i in range(len(richtungsvektor)):
                ausgabeRichtungsvektor = np.append(ausgabeRichtungsvektor,richtungsvektor[i].subs({y: 1, x: 1, z: 1}))
                
            return [2, self.geradeVektoren(stuetzvektor, ausgabeRichtungsvektor)]
                
    """
    Abstaende
    Punkt - Punkt
    Punkt - Gerade
    Punkt - Ebene
    Gerade - Ebene
    Ebene - Ebene

    """

    def abstandPunktPunkt (self, punkt1, punkt2):
        abstand = 0
        for i in range(len(punkt1)):
            abstand += (punkt1[i] - punkt2[i])**2
        return np.sqrt(abstand)

    def abstandPunktGerade (self, punkt, gerade):
        if self.punktAufGerade(punkt, gerade):
            return 0
        else:
            hilfsebene = self.ebeneNormalenform(gerade[1], punkt)
            schnittpunkt = self.lageGeradeEbene(gerade, hilfsebene)
            return self.abstandPunktPunkt(punkt, schnittpunkt[1])

    def abstandPunktEbene (self, punkt, ebene):
        if self.punktAufEbene(punkt, ebene):
            return 0
        else:
            zaehler = np.dot(punkt, ebene[0]) - ebene[1]
            nenner = 0
            for item in ebene[0]:
                nenner += item**2
            
            return zaehler/np.sqrt(nenner)
    
    def abstandGeradeEbene(self, gerade, ebene):
        lagebeziehung = self.lageGeradeEbene(gerade, ebene)

        if lagebeziehung[0] == 0 or lagebeziehung[0] == 2:
            return 0
        else:
            return self.abstandPunktEbene(gerade[0], ebene)
    
    def abstandEbenen(self, ebene1, ebene2):
        if self.lageEbenen(ebene1, ebene2)[0] == 1:
            hilfsgerade = self.geradeVektoren(np.array([0,0,0]), ebene1[0])
            schnittpunkt1 = self.lageGeradeEbene(hilfsgerade, ebene1)
            schnittpunkt2 = self.lageGeradeEbene(hilfsgerade, ebene2)
            abstand = self.abstandPunktPunkt(schnittpunkt1[1],schnittpunkt2[1])
            return abstand
        else:
            return 0

    """
    Winkel
    Gerade - Gerade
    Gerade - Ebene
    Ebene - Ebene
    
    """

    def winkelVektoren(self, vektor1, vektor2):
        zaehler = np.dot(vektor1, vektor2)
        norm1 = 0
        norm2 = 0
        for i in range(len(vektor1)):
            norm1 += vektor1[i]**2
            norm2 += vektor2[i]**2
        argument = zaehler/(np.sqrt(norm1)*np.sqrt(norm2))
        return np.acos(argument)

    def winkelVektorenAbsolute(self, vektor1, vektor2):
        winkel = self.winkelVektoren(vektor1, vektor2)
        if winkel > np.pi/2:
            winkel = np.pi - winkel
        return winkel

    def winkelGeraden(self, gerade1, gerade2):
        winkel = self.winkelVektorenAbsolute(gerade1[1], gerade2[1])
        return winkel

    def winkelEbenen(self, ebene1, ebene2):
        winkel = self.winkelVektorenAbsolute(ebene1[0], ebene2[0])
        return winkel
		
    def winkelGeradeEbene(self, gerade, ebene):
        winkel = self.winkelVektorenAbsolute(gerade[1], ebene[0])
        return np.pi/2 - winkel
        
		
    def winkelRadGrad(self, winkel):
        return 180.0/np.pi * winkel

    """
    Hilfsmethoden
    Skalares Vielfaches
    Spurpunkte berechnen aus Koordinatengleichung
    ggT von zwei Zahlen
    ggT eines numpy-Arrays

    """

    def skalaresVielfaches(self, vek1, vek2):
        normalenvektor = np.cross(vek1, vek2)
        vielfaches = True

        for item in normalenvektor:
            if item != 0:
                return False
        
        return True
    
    def spurpunkteBerechnen(self, ebene):
        spurpunkte = np.array([])

        t = sy.Symbol('t')
        if ebene[0][0] != 0:
            koordinate = sy.solve(ebene[0][0]*t-ebene[1],t)
            spurpunkte = np.append(spurpunkte, [koordinate[0], 0, 0])
        if ebene[0][1] != 0:
            koordinate = sy.solve(ebene[0][1]*t-ebene[1],t)
            spurpunkte = np.append(spurpunkte, [0, koordinate[0], 0])
        if ebene[0][2] != 0:
            koordinate = sy.solve(ebene[0][2]*t-ebene[1],t)
            spurpunkte = np.append(spurpunkte, [0, 0, koordinate[0]])
        arrayZeilen = (int)(len(spurpunkte)/3)
        return spurpunkte.reshape(arrayZeilen,3)

    def gcd(self, a, b):
        while b > 0:
            a, b = b, a % b
        return a

    def gcdArray(self, a):
        if a.dtype == 'object':
            return a
        for item in a:
                if item != np.floor(item):
                    return a
        ggT = a[0]
        for i in a[1:]:
            ggT = self.gcd(ggT, np.fabs(i))
        
        vektorGekuerzt = np.array([])
        vektor2 = a.astype(int)
        
        for item in vektor2:
            value = item/ggT
            vektorGekuerzt = np.append(vektorGekuerzt,value).astype(int)
        
        return vektorGekuerzt