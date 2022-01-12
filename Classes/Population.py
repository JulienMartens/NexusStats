import os
import math
import numpy as np
import matplotlib.pyplot as plt
from .Patient import Patient 
from .ArticulationMoyenne import ArticulationMoyenne
from .DonneesMoyennes import DonneesMoyennes

class Population:
        
    def __init__(self):
    
        pass


    def depuisDossier(self, dossier):
        self.nom = dossier.split('/')[-1]
        self.patients = []
        self.moyennePourcentageContactG = []
        self.variancePourcentageContactG = 0
        self.moyennePourcentageContactD = []
        self.variancePourcentageContactD = 0
        self.listeArticulations = ["PelvisD", "HancheD", "GenouD", "ChevilleD", "PiedD", "PelvisG", "HancheG", "GenouG", "ChevilleG", "PiedG"]
        self.articulations = {}

        nombrePatients = len(os.listdir(dossier))
        for i in range(0,len(os.listdir(dossier))):
            self.patients.append(Patient.depuisFichier(dossier+"\\"+os.listdir(dossier)[i]))
            if i==0:
                for j in self.listeArticulations:
                    self.articulations[j] = ArticulationMoyenne([self.patients[i].articulations[j].moyenneX],[self.patients[i].articulations[j].moyenneY],[self.patients[i].articulations[j].moyenneZ], [self.patients[i].articulations[j].varianceX],[self.patients[i].articulations[j].varianceY],[self.patients[i].articulations[j].varianceZ])
                self.PressionD = DonneesMoyennes([self.patients[i].PressionD.moyenneX], [self.patients[i].PressionD.varianceX])
                self.PressionG = DonneesMoyennes([self.patients[i].PressionG.moyenneX],[self.patients[i].PressionG.varianceX])

                self.moyennePourcentageContactG.append(self.patients[i].moyennePourcentageContactG)
                self.variancePourcentageContactG+=self.patients[i].variancePourcentageContactG /len(self.patients)
                self.moyennePourcentageContactD.append(self.patients[i].moyennePourcentageContactD)
                self.variancePourcentageContactD+=self.patients[i].variancePourcentageContactD /len(self.patients)

            else :
                for j in self.listeArticulations:
                    self.articulations[j].update(self.patients[i].articulations[j].moyenneX,self.patients[i].articulations[j].moyenneY,self.patients[i].articulations[j].moyenneZ, self.patients[i].articulations[j].varianceX,self.patients[i].articulations[j].varianceY,self.patients[i].articulations[j].varianceZ)

                self.PressionD.update(self.patients[i].PressionD.moyenneX,self.patients[i].PressionD.varianceX)
                self.PressionG.update(self.patients[i].PressionG.moyenneX,self.patients[i].PressionG.varianceX)

                self.moyennePourcentageContactG.append(self.patients[i].moyennePourcentageContactG)
                self.variancePourcentageContactG+=self.patients[i].variancePourcentageContactG /len(self.patients)
                self.moyennePourcentageContactD.append(self.patients[i].moyennePourcentageContactD)
                self.variancePourcentageContactD+=self.patients[i].variancePourcentageContactD /len(self.patients)
            
        self.stdevPourcentageContactD= math.sqrt(self.variancePourcentageContactD)
        self.stdevPourcentageContactG= math.sqrt(self.variancePourcentageContactG)
        self.moyennePourcentageContactD = sum(self.moyennePourcentageContactD)/len(self.moyennePourcentageContactD)
        self.moyennePourcentageContactG = sum(self.moyennePourcentageContactG)/len(self.moyennePourcentageContactG)
        
        for i in self.articulations:
           self.articulations[i].updateStats()
        self.PressionD.updateStats()
        self.PressionG.updateStats()
        print("Population " + self.nom + " OK" )

    def depuisComparatifPopulation(self, population1,population2):

        self.nom = population2.nom +" - "+population1.nom    
        self.listeArticulations = ["PelvisD", "HancheD", "GenouD", "ChevilleD", "PiedD", "PelvisG", "HancheG", "GenouG", "ChevilleG", "PiedG"]
        self.articulations = {}

        self.moyennePourcentageContactG = (population1.moyennePourcentageContactG + population1.moyennePourcentageContactG)/2
        self.variancePourcentageContactG = (population1.variancePourcentageContactG + population1.variancePourcentageContactG)/2
        self.stdevPourcentageContactG = math.sqrt(self.variancePourcentageContactG)
        self.moyennePourcentageContactD = (population1.moyennePourcentageContactD + population1.moyennePourcentageContactD)/2
        self.variancePourcentageContactD = (population1.variancePourcentageContactD + population1.variancePourcentageContactD)/2
        self.stdevPourcentageContactD = math.sqrt(self.variancePourcentageContactD)

        for i in self.listeArticulations:
            self.articulations[i] = self.generateurArticulation(population1.articulations[i],population2.articulations[i])
        print("Population " + self.nom + " OK" )


    def generateurArticulation(self,articulation1,articulation2):
        moyenneOutX = []
        moyenneOutY = []
        moyenneOutZ = []
        varianceOutX = []
        varianceOutY = []
        varianceOutZ = []

        for i in range(0,len(articulation1.moyenneX)):
            moyenneOutX.append(articulation2.moyenneX[i] - articulation1.moyenneX[i])
            moyenneOutY.append(articulation2.moyenneY[i] - articulation1.moyenneY[i])
            moyenneOutZ.append(articulation2.moyenneZ[i] - articulation1.moyenneZ[i])
        for i in range(0,len(articulation2.varianceX)):
            varianceOutX.append(articulation2.varianceX[i])
            varianceOutY.append(articulation2.varianceY[i])
            varianceOutZ.append(articulation2.varianceZ[i])
        for i in range(0,len(articulation2.varianceX)):
            varianceOutX.append(articulation2.varianceX[i])
            varianceOutY.append(articulation2.varianceY[i])
            varianceOutZ.append(articulation2.varianceZ[i])
            
        articulationOutput = ArticulationMoyenne([moyenneOutX],[moyenneOutY],[moyenneOutZ], varianceOutX,varianceOutY,varianceOutZ)
        articulationOutput.updateStats()
        return articulationOutput