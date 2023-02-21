import sympy as sp
from pages.packages.latexout import *

class Abstaende():
    def punkt_punkt(self, punkt1, punkt2):
        p_1, p_2, p_3, q_1, q_2, q_3 = sp.symbols('p_1 p_2 p_3 q_1 q_2 q_3')
        
        if punkt1.equals(punkt2):
            rechenweg = r"""
        $$
        \begin{align*}
            d &= 0 \\
        \end{align*}
        $$    
        """
            return rechenweg

        d = sp.sqrt((p_1-q_1)**2 + (p_2-q_2)**2 + (p_3-q_3)**2)
        d1 = d.subs([(p_1-q_1, sp.UnevaluatedExpr(punkt1.x-punkt2.x)),(p_2-q_2, sp.UnevaluatedExpr(punkt1.y-punkt2.y)),(p_3-q_3, sp.UnevaluatedExpr(punkt1.z-punkt2.z))])
        d2 = d.subs([(p_1,punkt1.x),(p_2,punkt1.y),(p_3,punkt1.z),(q_1,punkt2.x),(q_2,punkt2.y),(q_3,punkt2.z)])
        rechenweg = r"""
$$
\begin{align*}
    d &= %s \\
    &= %s \\
    &= %s
\end{align*}
$$
        """ % (sp.latex(d),(sp.latex(d1)), sp.latex(d2))
        return rechenweg

    def punkt_gerade(self, punkt1, gerade):
        if gerade.contains(punkt1):
            rechenweg = "Der Punkt liegt auf der Geraden, d.h. der Abstand ist $d=0$."
            return rechenweg
        h = sp.geometry.Plane(punkt1,normal_vector = gerade.direction_ratio)
        punkt2 = sp.geometry.intersection(h,gerade)
        rechenweg = r"""
Aufstellen einer Hilfsebene $E$, die den Punkt $%s$ enthält und orthogonal zur Gerade $g$ ist, d.h. der Normalenvektor der Ebene ist der Richtungsvektor der Geraden
$$
\begin{align*}
    E: %s &= 0
\end{align*}
$$
Berechnen des Schnittpunkts von $E$ mit $g$ zu $%s$. Der Abstand des Punktes zur Gerade ist derselbe wie der Abstand der beiden Punkte. Für den Abstand gilt
    %s
    """ % (punkt('P',punkt1), sp.latex(h.equation()), punkt('S', punkt2[0]), self.punkt_punkt(punkt1, punkt2[0]))
        return rechenweg
    
    def punkt_ebene(self, punkt1, ebene1):
        x_1, x_2, x_3 = sp.symbols('x_1 x_2 x_3')
        if len(ebene1.intersection(punkt1)) != 0:
            rechenweg = "Der Punkt liegt in der Ebene, d.h. der Abstand ist $d=0$."
            return rechenweg
        hilfsgerade = sp.geometry.Line3D(punkt1, direction_ratio=ebene1.normal_vector)
        schnittpunkt = sp.geometry.intersection(ebene1, hilfsgerade)
        normvec = ebene1.normal_vector
        paramd = np.dot(normvec, ebene1.p1)
        zaehler = normvec[0]*x_1 + normvec[1]*x_2 + normvec[2]*x_3 - paramd
        rechenweg = r"""
Aufstellen der Hilfsgeraden $h$, die den Punkt P enthält und orthogonal zur Ebene $E$ ist, d.h. als Richtungsvektor den Stützvektor der Ebene übernimmt.
$$
\begin{align*}
    %s
\end{align*}
$$
Berechnung des Schnittpunkts $S$ der Geraden $h$ mit der Ebene $E$, es gilt $%s$. Der Abstand des Punktes zur Ebene ist derselbe wie der Abstand der beiden Punkte. Für den Abstand gilt
%s
Alternativ kann der Abstand auch mit der Hesse'schen Normalform berechnet werden, indem man die Koordinaten des Punktes einsetzt.
$$  
\begin{align*}
    d &= \frac{|%s|}{\sqrt{(%s)^2+(%s)^2+(%s)^2}}\\
    &= \frac{|%s|}{\sqrt{%s}}\\
    &= \frac{|%s|}{\sqrt{%s}}\\
    &= %s
\end{align*}
$$
        """ % (gerade_sp('h', hilfsgerade), punkt('S', schnittpunkt[0]), self.punkt_punkt(punkt1, schnittpunkt[0]),
               sp.latex(ebene1.equation(x='x_1',y='x_2',z='x_3')), sp.latex(normvec[0]),sp.latex(normvec[1]),sp.latex(normvec[2]),
               sp.latex(zaehler.subs([(x_1,sp.UnevaluatedExpr(punkt1.x)),(x_2,sp.UnevaluatedExpr(punkt1.y)),(x_3,sp.UnevaluatedExpr(punkt1.z))])), sp.latex(normvec[0]**2+normvec[1]**2+normvec[2]**2),
               sp.latex(ebene1.equation(x=punkt1.x,y=punkt1.y,z=punkt1.z)), sp.latex(normvec[0]**2+normvec[1]**2+normvec[2]**2),
               sp.latex(ebene1.distance(punkt1)))
        return rechenweg
        
    def gerade_ebene(self, gerade1, ebene1):
        schnittpunkt = sp.geometry.intersection(gerade1, ebene1)
        abstand = ebene1.distance(gerade1)
        parallel = ebene1.is_parallel(gerade1)
        normalvektor = ebene1.normal_vector
        richtungsvektor = gerade1.direction_ratio
        skalar = np.dot(normalvektor, richtungsvektor)
        rechenweg = r"""
        Der Abstand von Gerade und Ebene ist nur dann nicht Null, wenn die Gerade parallel zur Ebene ist und die Gerade nicht in der Ebene liegt. Parallelität liegt dann vor, wenn der Richtungsvektor der Geraden und der Normalenvektor der Ebene orthogonal sind
        $$
        \begin{align*}
            %s \cdot %s = %s
        \end{align*}
        $$
        """ % (pmatrix(gerade1.direction_ratio), pmatrix(ebene1.normal_vector), sp.latex(skalar))
        if parallel:
            if abstand == 0:
                rechenweg += "Gerade und Ebene sind parallel, allerdings liegt die Gerade in der Ebene, d.h. der Abstand ist $d=0$."
                return rechenweg
            else:
                rechenweg += "Gerade und Ebene sind parallel und die Gerade liegt nicht in der Ebene. Der Abstand der Gerade zur Ebene entspricht dem Abstand eines beliebigen Punktes auf der Geraden zur Ebene."
                rechenweg += self.punkt_ebene(gerade1.p1, ebene1)
                return rechenweg
        else:
            rechenweg += r"Das Skalarprodukt ist nicht Null. Die Gerade und die Ebene schneiden sich im Punkt $%s$, d.h. der Abstand ist $d=0$." % (punkt('S', schnittpunkt[0]))
            return rechenweg
        
    def gerade_gerade(self, gerade1, gerade2):
        if sp.geometry.Line3D.are_concurrent(gerade1, gerade2):
            schnittpunkt = gerade1.intersection(gerade2)
            return "Die Geraden schneiden sich im Punkt $%s$, d.h. der Abstand ist $d=0$." % punkt('S',schnittpunkt[0])
        if gerade1.is_similar(gerade2):
            return "Die beiden Geraden sind identisch, d.h. der Abstand ist $d=0$."
        if sp.geometry.Line3D.is_parallel(gerade1, gerade2):
            rechenweg = r"Die Geraden sind parallel, d.h. man kann den Abstand eine bliebigen Punktes der einen Geraden zur anderen Geraden berechnen."
            rechenweg += self.punkt_gerade(gerade2.p1, gerade1)
            return rechenweg
        normvec = np.cross(gerade1.direction_ratio, gerade2.direction_ratio)
        vecp1 = gerade1.p1
        vecp2 = gerade2.p1
        vecp3 = vecp1-vecp2

        rechenweg = r"""
        Berechne aus den Richtungsvektoren mithilfe des Kreuzprodukts den Vektor $\vec{n}$ zu
        $$
        \begin{align*}
            %s \times %s = %s
        \end{align*}
        $$
        Berechnung des Abstands über die Stützvektoren der beiden Geraden und den gerade berechneten Normalenvektor mit der Formel
        $$
        \begin{align*}
            d &= \frac{\left|\left(\vec{p}-\vec{q}\right) \cdot \vec{n}\right|}{|\vec{n}|}\\
            &= \frac{\left|\left(%s-%s\right) \cdot %s\right|}{\sqrt{(%s)^2+(%s)^2+(%s)^2}}\\
            &= \frac{\left|%s \cdot %s\right|}{\sqrt{%s}}\\
            &= \frac{\left|%s\right|}{%s}\\
            &= %s
        \end{align*}
        $$
        """ % (pmatrix(gerade1.direction_ratio), pmatrix(gerade2.direction_ratio), pmatrix(normvec),
               pmatrix(vecp1), pmatrix(vecp2), pmatrix(normvec),sp.latex(normvec[0]),sp.latex(normvec[1]),sp.latex(normvec[2]),
               pmatrix(vecp3), pmatrix(normvec), sp.latex(normvec[0]**2+normvec[1]**2+normvec[2]**2),
               sp.latex(np.dot(vecp3, normvec)),sp.latex(sp.sqrt(normvec[0]**2+normvec[1]**2+normvec[2]**2)),
               sp.latex(np.abs(np.dot(vecp3, normvec))/(sp.sqrt(normvec[0]**2+normvec[1]**2+normvec[2]**2))))
        return rechenweg
    
    def ebene_ebene(self, ebene1, ebene2):
        if ebene1.equals(ebene2):
            return "Die Ebenen sind identisch, d.h. ihr Abstand ist $d=0$."
        if sp.geometry.Plane.are_concurrent(ebene1, ebene2):
            return "Da die Normalenvektoren der beiden Ebenen keine Vielfachen voneinander sind, schneiden sich die Ebenen in einer Geraden. Der Abstand ist somit $d=0$."
        rechenweg = r"""
        Die Ebenen sind parallel zueinander und damit kann der Abstand eines beliebigen Punktes $P$ der einen Ebene zur anderen Ebene berechnet werden.
        %s
        """ % self.punkt_ebene(ebene2.p1, ebene1)
        
        return rechenweg