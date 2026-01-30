improt numpy as np 

def make_counter():
    count = -1
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

class Goo:
    counter = make_counter()

    def __init__(self, pos, mass=1.0):
        self._pos = np.array(pos, dtype=float)
        self._vit = np.zeros(2, dtype=float)
        self._mass = mass
        self._voisin = []
        #self.ppvoisin() in dev
        #self.ppplateforme() in dev
        self._nm = counter()

    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
    
    @setter
    def pos(self, new_pos):
        self._pos = np.array(new_pos, dtype=float)

    @setter
    def vit(self, new_vit):
        self._vit = np.array(new_vit, dtype=float)

    @property
    def pos(self):
        return self._pos
    
    @property
    def vit(self):
        return self._vit

class StaticGoo(Goo):
    def __init__(self, pos, mass=1.0):
        super().__init__(pos,mass)
    
    @Goo.vit.setter
    def vit(self, new_vit):
        pass

    @Goo.pos.setter
    def pos(self, new_pos):
        pass
