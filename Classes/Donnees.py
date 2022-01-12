import statistics

class Donnees:
    def __init__(self, x, stats=0):
        self.X = x
        if stats == 1:
            self.updateStats()
        
    def update(self,x, stats=0):
        self.X.append(x)
        if stats == 1:
            self.updateStats()

    def updateStats(self):
        self.moyenneX, self.varianceX = self.stats(self.X)
    
    def stats(self, donnees):
        precisionMoyenne = 50
        moyenne=[]
        variance = []
        for i in range(0, precisionMoyenne):
            valeursEnCours=[]
            for j in range(0,len(donnees)):
                valeursEnCours.append(donnees[j][int(i/precisionMoyenne*len(donnees[j]))])
            moyenne.append(statistics.mean(valeursEnCours))
            variance.append(statistics.variance(valeursEnCours))
        return(moyenne,variance)

