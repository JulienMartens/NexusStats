import statistics

class Articulation:

    def __init__(self, x, y, z, stats=0):
        self.X = x
        self.Y = y
        self.Z = z
        if stats == 1:
            self.updateStats()
        
    def update(self,x,y,z, stats=0):
        self.X.append(x)
        self.Y.append(y)
        self.Z.append(z)
        if stats == 1:
            self.updateStats()

    def updateStats(self):
        self.moyenneX, self.varianceX, self.stdevX = self.stats(self.X)
        self.moyenneY, self.varianceY, self.stdevY = self.stats(self.Y)
        self.moyenneZ, self.varianceZ, self.stdevZ = self.stats(self.Z)

    def stats(self, donnees):
        precisionMoyenne = 50
        moyenne=[]
        variance = []
        stdev = []
        for i in range(0, precisionMoyenne):
            valeursEnCours=[]
            for j in range(0,len(donnees)):
                valeursEnCours.append(donnees[j][int(i/precisionMoyenne*len(donnees[j]))])
            moyenne.append(statistics.mean(valeursEnCours))
            variance.append(statistics.variance(valeursEnCours))
            stdev.append(statistics.stdev(valeursEnCours))
        return(moyenne,variance,stdev)

