#A simple class to define oxide components of a rock
class Component:
    
    def __init__(self):
        self.formula = None
        self.weight = 0
        self.ox2cat = 0 #ratio of O to cation
        self.catNum = 0
        self.cation = None
        
    def __init__(self, name, M, ox, cNum, cat):
        
        self.formula = name
        self.weight = M
        self.ox2cat = ox #ratio of O to cation
        self.catNum = cNum
        self.cation = cat
        
        