import statistics
import math

class ArticulationMoyenne:

    def __init__(self, x, y, z,varx,vary,varz, stats=0):
        self.X = x
        self.Y = y
        self.Z = z
        self.varianceX = varx
        self.varianceY = vary
        self.varianceZ = varz
        if stats == 1:
            self.updateStats()
        
    def update(self,x,y,z,varx,vary,varz, stats=0):
        self.X.append(x)
        self.Y.append(y)
        self.Z.append(z)
        self.varianceX.append(varx)
        self.varianceY.append(vary)
        self.varianceZ.append(varz)
        if stats == 1:
            self.updateStats()

    def updateStats(self):
        self.moyenneX, self.stdevX, self.moyenneVarianceX = self.stats(self.X, self.varianceX)
        self.moyenneY, self.stdevY, self.moyenneVarianceY = self.stats(self.Y, self.varianceY)
        self.moyenneZ, self.stdevZ, self.moyenneVarianceZ = self.stats(self.Z, self.varianceZ)
    
    def stats(self, donnees,variance):
        precisionMoyenne = 50
        moyenne=[]
        stdev = []
        moyenneVariance=[0]*precisionMoyenne
        for i in range(0, precisionMoyenne):
            valeursEnCours=[]
            for j in range(0,len(donnees)):
                valeursEnCours.append(donnees[j][int(i/precisionMoyenne*len(donnees[j]))])
                moyenneVariance[i]+=variance[j][i]/len(donnees)
            moyenne.append(statistics.mean(valeursEnCours))
        for i in range(0,len(moyenneVariance)):
            stdev.append(math.sqrt(moyenneVariance[i]))
        return(moyenne,stdev,moyenneVariance)

