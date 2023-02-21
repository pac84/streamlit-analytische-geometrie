import sympy as sp
import numpy as np
from pages.packages.latexout import *

class Winkel():
    def schnittwinkel(self, obj1, obj2):
        winkel = sp.N(obj1.angle_between(obj2))
        winkelDeg = 180*winkel/np.pi

        if np.abs(np.floor(winkelDeg)-winkelDeg) > 0:
            ausgabe = '= %.2f ...' % winkelDeg
        else:
            ausgabe = r"= %s" % sp.latex(int(winkelDeg))

        return ausgabe

        
    def gerade_gerade(self, gerade1, gerade2):
        if sp.geometry.Line3D.are_concurrent(gerade1, gerade2):
            schnittpunkt = gerade1.intersection(gerade2)
            skalarprodukt = np.dot(gerade1.direction_ratio, gerade2.direction_ratio)

            rechenweg =  r"""
Da sich die Geraden im Punkt $%s$ schneiden, kann der Schnittwinkel $\alpha$ mithilfe der Richtungsvektoren und durch Einsetzen in die folgende Formel berechnet werden
$$
\begin{align*}
    \cos(\alpha) &= \frac{|\vec{u} \cdot \vec{v}|}{|\vec{u}| \cdot |\vec{v}|}\\
    &= \frac{\left|%s \cdot %s\right|}{\sqrt{(%s)^2+(%s)^2+(%s)^2} \cdot \sqrt{(%s)^2+(%s)^2+(%s)^2}}\\
    &= \frac{\left|%s\right|}{\sqrt{%s} \cdot \sqrt{%s}}\\
    &= %s\\
    \Rightarrow \alpha & %s\degree
\end{align*}
$$
            """ % (punkt('S',schnittpunkt[0]), pmatrix(gerade1.direction_ratio), pmatrix(gerade2.direction_ratio), gerade1.direction_ratio[0], gerade1.direction_ratio[1], gerade1.direction_ratio[2], gerade2.direction_ratio[0], gerade2.direction_ratio[1], gerade2.direction_ratio[2],
                   sp.latex(skalarprodukt), sp.latex(gerade1.direction_ratio[0]**2+gerade1.direction_ratio[1]**2+gerade1.direction_ratio[2]**2), sp.latex(gerade2.direction_ratio[0]**2+gerade2.direction_ratio[1]**2+gerade2.direction_ratio[2]**2),
                   #sp.latex(np.abs(skalarprodukt)), sp.latex(sp.sqrt(gerade1.direction_ratio[0]**2+gerade1.direction_ratio[1]**2+gerade1.direction_ratio[2]**2)*sp.sqrt(gerade2.direction_ratio[0]**2+gerade2.direction_ratio[1]**2+gerade2.direction_ratio[2]**2)),
                   sp.latex(np.abs(skalarprodukt)/(sp.sqrt(gerade1.direction_ratio[0]**2+gerade1.direction_ratio[1]**2+gerade1.direction_ratio[2]**2)*sp.sqrt(gerade2.direction_ratio[0]**2+gerade2.direction_ratio[1]**2+gerade2.direction_ratio[2]**2))),
                   sp.latex(self.schnittwinkel(gerade1, gerade2)))
            return rechenweg
        elif gerade1.is_similar(gerade2):
            return r"Die beiden Geraden sind identisch, d.h. der Schnittwinkel ist $\alpha=0\degree$."
        else:
            return "Die Geraden sind parallel, d.h. es gibt keinen Schnittwinkel."
    
    def ebene_ebene(self, ebene1, ebene2):
        if sp.geometry.Plane.are_concurrent(ebene1, ebene2):
            skalarprodukt = np.dot(ebene1.normal_vector, ebene2.normal_vector)
            rechenweg =  r"""
Da sich die Ebenen schneiden, kann der Schnittwinkel $\alpha$ mithilfe der Normalenvektoren und durch Einsetzen in die folgende Formel berechnet werden
$$
\begin{align*}
    \cos(\alpha) &= \frac{|\vec{n_1} \cdot \vec{n_2}|}{|\vec{n_1}| \cdot |\vec{n_2}|}\\
    &= \frac{\left|%s \cdot %s\right|}{\sqrt{(%s)^2+(%s)^2+(%s)^2} \cdot \sqrt{(%s)^2+(%s)^2+(%s)^2}}\\
    &= \frac{\left|%s\right|}{\sqrt{%s} \cdot \sqrt{%s}}\\
    &= %s\\
    \Rightarrow \alpha & %s\degree
\end{align*}
$$
            """ % (pmatrix(ebene1.normal_vector), pmatrix(ebene2.normal_vector), ebene1.normal_vector[0], ebene1.normal_vector[1], ebene1.normal_vector[2], ebene2.normal_vector[0], ebene2.normal_vector[1], ebene2.normal_vector[2],
                   sp.latex(skalarprodukt), sp.latex(ebene1.normal_vector[0]**2+ebene1.normal_vector[1]**2+ebene1.normal_vector[2]**2), sp.latex(ebene2.normal_vector[0]**2+ebene2.normal_vector[1]**2+ebene2.normal_vector[2]**2),
                   sp.latex(np.abs(skalarprodukt)/(sp.sqrt(ebene1.normal_vector[0]**2+ebene1.normal_vector[1]**2+ebene1.normal_vector[2]**2)*sp.sqrt(ebene2.normal_vector[0]**2+ebene2.normal_vector[1]**2+ebene2.normal_vector[2]**2))),
                   sp.latex(self.schnittwinkel(ebene1, ebene2)))
            return rechenweg
        elif ebene1.is_similar(ebene2):
            return r"Die beiden Ebenen sind identisch, d.h. der Schnittwinkel ist $\alpha=0\degree$."
        else:
            return "Die Ebenen sind parallel, d.h. es gibt keinen Schnittwinkel."
    

    def gerade_ebene(self, gerade1, ebene2):
        if ebene2.is_parallel(gerade1) and ebene2.distance(gerade1) == 0:
            return r"Die Gerade liegt in der Ebene, d.h. der Schnittwinkel ist $\alpha = 0\degree$."
        elif ebene2.is_parallel(gerade1) and ebene2.distance(gerade1) != 0:
            return "Die beiden Gerade und die Ebene sind parallel, d.h. es existiert kein Schnittwinkel."
        else:
            skalarprodukt = np.dot(gerade1.direction_ratio, ebene2.normal_vector)
            rechenweg =  r"""
Da die Gerade die Ebene schneidet, kann der Schnittwinkel $\alpha$ mithilfe des Richtungsvektors der Geraden und des Normalenvektors der Ebene durch Einsetzen in die folgende Formel berechnet werden
$$
\begin{align*}
    \sin(\alpha) &= \frac{|\vec{u} \cdot \vec{n}|}{|\vec{u}| \cdot |\vec{n}|}\\
    &= \frac{\left|%s \cdot %s\right|}{\sqrt{(%s)^2+(%s)^2+(%s)^2} \cdot \sqrt{(%s)^2+(%s)^2+(%s)^2}}\\
    &= \frac{\left|%s\right|}{\sqrt{%s} \cdot \sqrt{%s}}\\
    &= %s\\
    \Rightarrow \alpha & %s\degree
\end{align*}
$$
            """ % (pmatrix(gerade1.direction_ratio), pmatrix(ebene2.normal_vector), gerade1.direction_ratio[0], gerade1.direction_ratio[1], gerade1.direction_ratio[2], ebene2.normal_vector[0], ebene2.normal_vector[1], ebene2.normal_vector[2],
                   sp.latex(skalarprodukt), sp.latex(gerade1.direction_ratio[0]**2+gerade1.direction_ratio[1]**2+gerade1.direction_ratio[2]**2), sp.latex(ebene2.normal_vector[0]**2+ebene2.normal_vector[1]**2+ebene2.normal_vector[2]**2),
                   sp.latex(np.abs(skalarprodukt)/(sp.sqrt(gerade1.direction_ratio[0]**2+gerade1.direction_ratio[1]**2+gerade1.direction_ratio[2]**2)*sp.sqrt(ebene2.normal_vector[0]**2+ebene2.normal_vector[1]**2+ebene2.normal_vector[2]**2))),
                   sp.latex(self.schnittwinkel(ebene2, gerade1)))
            return rechenweg
