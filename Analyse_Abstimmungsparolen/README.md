# Wie wird der Score berechnet?

Die Abstimmungsparolen der Parteien für die einzelnen Abstimmungen sind wie folgt encodiert: 1 = Ja, -1 = Nein, 0 = Stimmfreigabe. 

Pro Partei ergibt sich so für alle n Abstimmungen je ein Vektor ![](http://latex.codecogs.com/svg.latex?%5Cinline%20%5Clarge%20%5Cvec%7Bv_i%7D%20%5Cin%20%5C%7B-1,%200,%201%5C%7D%5En). Der Score von zwei Parteien ist die Länge des Vektor, der aus der Orthogonalprojektion der beiden Vektoren resultiert, transformiert ins Intervall $[0,1]$. Die Formel dafür lautet:

![](http://latex.codecogs.com/svg.latex?\large&space;\text{score}_{\vec{v_i}}(\vec{v_j})&space;=&space;\dfrac{1}{2}\left(\dfrac{\langle\vec{v_i},\vec{v_j}\rangle}{\langle\vec{v_i},\vec{v_i}\rangle}&plus;1\right))
