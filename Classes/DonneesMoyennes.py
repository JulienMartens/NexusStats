import statistics
import math

class DonneesMoyennes:
    def __init__(self, x,varX, stats=0):
        self.X = x
        self.varianceX = varX
        if stats == 1:
            self.updateStats()
        
    def update(self,x,varX, stats=0):
        self.X.append(x)
        self.varianceX.append(varX)
        if stats == 1:
            self.updateStats()

    def updateStats(self):
        self.moyenneX, self.stdevX = self.stats(self.X,self.varianceX)
    
    def stats(self, donnees,variance):
        precisionMoyenne = 50
        moyenne=[]
        stdev=[0]*precisionMoyenne
        for i in range(0, precisionMoyenne):
            valeursEnCours=[]
            for j in range(0,len(donnees)):
                valeursEnCours.append(donnees[j][int(i/precisionMoyenne*len(donnees[j]))])
                stdev[i]+=variance[j][i]
            moyenne.append(statistics.mean(valeursEnCours))
        for i in range(0,len(stdev)):
            stdev[i] = math.sqrt(stdev[i])
        return(moyenne,stdev)

