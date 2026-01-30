import numpy as np
from scipy.spatial import ConvexHull


class Platform:
    """Crée une plateforme convexe à partir d'un ensemble de points 2D (N>=3)."""

    def __init__(self, sommets):
        points = np.asarray(sommets, dtype=float)

        if points.ndim != 2 or points.shape[1] != 2:
            raise ValueError("sommets doit être un tableau/list de forme (N,2)")
        if points.shape[0] < 3:
            raise ValueError("Il faut au moins 3 points")

        convexe = ConvexHull(points)
        self.sommets = points[convexe.vertices]  # sommets du polygone convexe

# Modèles de plateformes — échelle 100

S = 100  # facteur d’échelle

# Carré (côté 100)
carre = Platform([
    [0, 0],
    [S, 0],
    [S, S],
    [0, S]
])

# Triangle rectangle (angle droit en (0,0))
triangle_rectangle = Platform([
    [0, 0],
    [2*S, 0],
    [0, S]
])

# Hexagone régulier (rayon ~100)
hexagone = Platform([
    [1.0*S, 0.0*S],
    [0.5*S, 0.87*S],
    [-0.5*S, 0.87*S],
    [-1.0*S, 0.0*S],
    [-0.5*S, -0.87*S],
    [0.5*S, -0.87*S]
])

# Triangle quelconque (non rectangle, non isocèle)
triangle_quelconque = Platform([
    [0.2*S, 0.1*S],
    [1.4*S, 0.3*S],
    [0.6*S, 1.1*S]
])

# Rectangle (largeur 200, hauteur 100)

rectangle = Platform([
    [0, 0],
    [2*S, 0],
    [2*S, S],
    [0, S]
])

pentagone = Platform([
    [0, 80],
    [70, 40],
    [40, -60],
    [-40, -60],
    [-80, 30]
])



