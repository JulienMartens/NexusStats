import numpy as np
import scipy.stats as scp
import matplotlib.pyplot as plt
import os
import xlsxwriter
from .Population import Population

class ComparatifPopulations():
    def __init__(self,population1,population2=""):
        self.population1 = population1
        self.population2 = population2

        #Generation stats de la pop 1
        self.generateurDonneesGlobal(population1,os.getcwd() + "\\Donnees "+ self.population1.nom)
        if not os.path.exists(os.getcwd() + "\\Donnees "+ self.population1.nom + "\\Patients"):
            os.mkdir(os.getcwd() + "\\Donnees "+ self.population1.nom + "\\Patients") 
        for i in self.population1.patients:
            self.generateurDonneesGlobal(i, os.getcwd() + "\\Donnees "+ self.population1.nom + "\\Patients\\" + i.nom)
        #Si 2 pops, stats de la pop 2 + comparaison des pops
        if population2 != "":
            self.diffPopulation = Population()
            self.diffPopulation.depuisComparatifPopulation(population1,population2)
            self.generateurDonneesGlobal(population2,os.getcwd() + "\\Donnees "+ self.population2.nom)            
            if not os.path.exists(os.getcwd() + "\\Donnees "+ self.population2.nom + "\\Patients"):
                os.mkdir(os.getcwd() + "\\Donnees "+ self.population2.nom + "\\Patients") 
            for i in self.population2.patients:
                self.generateurDonneesGlobal(i, os.getcwd() + "\\Donnees "+ self.population2.nom + "\\Patients\\" + i.nom)

            self.generateurDonneesGlobal(self.diffPopulation,os.getcwd() + "\\Donnees "+ self.diffPopulation.nom)            
            self.testKSGlobal(self.population1, self.population2,os.getcwd()+ "\\Donnees "+ self.diffPopulation.nom)

    def testKSGlobal(self, population1, population2, path):
        workbook = xlsxwriter.Workbook(path + '\\Test Kolmogorov-Smirnov.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0, "Articulation")
        worksheet.write(1,0, "Axe")
        colonne = 1
        #Kolmogorov-Smirnov test, hypothèse nulle = p-value > 5% = les 2 pops sont les mêmes
        for articulation in population1.articulations:
            worksheet.write(0,colonne, articulation)
            worksheet.write(1,colonne, "X")
            worksheet.write(1,colonne+2, "Y")
            worksheet.write(1,colonne+4, "Z")
            for i in range(0,3):
                worksheet.write(2,colonne+2*i, "statistic")
                worksheet.write(2,colonne+2*i+1, "p-value")

            resultat = self.testKS(population1.articulations[articulation],population2.articulations[articulation])
            cellFormatRouge = workbook.add_format({ 'bg_color': '#F08080'})
            cellFormatVert = workbook.add_format({ 'bg_color': '#90EE90'})

            for i in range(0,3):
                if resultat[i][1]<0.05:
                    worksheet.write(3,colonne+2*i,resultat[i][0],cellFormatRouge)
                    worksheet.write(3,colonne+2*i+1,resultat[i][1],cellFormatRouge)
                else:
                    worksheet.write(3,colonne+2*i,resultat[i][0],cellFormatVert)
                    worksheet.write(3,colonne+2*i+1,resultat[i][1],cellFormatVert)

            colonne +=6
        workbook.close()
        print("Test Kolmogorov-Smirnov OK")
        return

    def testKS(self,articulation1, articulation2):
        resultat=[]
        resultat.append(scp.ks_2samp(articulation1.moyenneX, articulation2.moyenneX))
        resultat.append(scp.ks_2samp(articulation1.moyenneY, articulation2.moyenneY))
        resultat.append(scp.ks_2samp(articulation1.moyenneZ, articulation2.moyenneZ))

        return resultat

    def generateurDonneesGlobal(self,population,path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.generateurDonneesExcel(population, path)
        self.generateurGraphePopulation(population, path)
        print("Stats " + population.nom + " OK")

    def generateurDonneesExcel(self, population,path):
        workbook = xlsxwriter.Workbook(path + '\\' +population.nom + '.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Articulation")
        worksheet.write(1,0, "Axe")
        
        colonne = 1
        
        for articulation in population.articulations:
            worksheet.write(0, colonne, articulation)
            worksheet.write(1,colonne, "X")
            worksheet.write(1,colonne+1, "ecart-type X")
            worksheet.write(1,colonne+2, "Y")
            worksheet.write(1,colonne+3, "ecart-type Y")
            worksheet.write(1,colonne+4, "Z")
            worksheet.write(1,colonne+5, "ecart-type Z")

            for i in range(0,len(population.articulations[articulation].moyenneX)):
                    worksheet.write(i+2, colonne, population.articulations[articulation].moyenneX[i])
                    worksheet.write(i+2, colonne+1, population.articulations[articulation].stdevX[i])
                    worksheet.write(i+2, colonne+2, population.articulations[articulation].moyenneY[i])
                    worksheet.write(i+2, colonne+3, population.articulations[articulation].stdevY[i])
                    worksheet.write(i+2, colonne+4, population.articulations[articulation].moyenneZ[i])
                    worksheet.write(i+2, colonne+5, population.articulations[articulation].stdevZ[i])
            colonne += 6
        workbook.close()


    def generateurGraphePopulation(self, population,path):
        correspondancesGraphe = [
            {"cote":"G", "noms": ["Bascule bassin G","Obliquité bassin G","Rotation bassin G"], "donnees":population.articulations["PelvisG"]},
            {"cote":"G", "noms": ["Flexion hanche G","Abd-adduction hanche G","Rotation hanche G"], "donnees":population.articulations["HancheG"]},
            {"cote":"G", "noms": ["Flexion genou G","","Varus-Valgus genou G"], "donnees":population.articulations["GenouG"]},
            {"cote":"G", "noms": ["Flexion cheville G","Rotation cheville G",""], "donnees":population.articulations["ChevilleG"]},
            {"cote":"G", "noms": ["","","Progression pas G"], "donnees":population.articulations["PiedG"]},
            {"cote":"D", "noms": ["Bascule bassin D","Obliquité bassin D","Rotation bassin D"], "donnees":population.articulations["PelvisD"]},
            {"cote":"D", "noms": ["Flexion hanche D","Abd-adduction hanche D","Rotation hanche D"], "donnees":population.articulations["HancheD"]},
            {"cote":"D", "noms": ["Flexion genou D","","Varus-Valgus Denou D"], "donnees":population.articulations["GenouD"]},
            {"cote":"D", "noms": ["Flexion cheville D","Rotation cheville D",""], "donnees":population.articulations["ChevilleD"]},
            {"cote":"D", "noms": ["","","Progression pas D"], "donnees":population.articulations["PiedD"]}]

        for i in range(0,len(correspondancesGraphe)):
            corresp = correspondancesGraphe[i]

            for j in range(0,len(corresp["noms"])):
                if corresp["noms"][j]!="":
                    if j == 0:
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneX,corresp["donnees"].stdevX,population.moyennePourcentageContactG)
                        elif corresp["cote"]=="D":    
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneX,corresp["donnees"].stdevX,population.moyennePourcentageContactD)
                    elif j == 1:                    
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneY,corresp["donnees"].stdevY,population.moyennePourcentageContactG)
                        elif corresp["cote"]=="D":    
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneY,corresp["donnees"].stdevY,population.moyennePourcentageContactD)
                    elif j == 2:
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneZ,corresp["donnees"].stdevZ,population.moyennePourcentageContactG)
                        elif corresp["cote"]=="D":            
                            self.generateurGrapheSimple(corresp["noms"][j], path, corresp["donnees"].moyenneZ,corresp["donnees"].stdevZ,population.moyennePourcentageContactD)

    def generateurGrapheSimple(self,nom, path, donnees, donneesStdev,contact):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.grid(color='black', linestyle='-', linewidth=0.1)
        ax.set_title(nom)
        ax.set_xlabel('% cycle')
        if "Angle" in nom :
            ax.set_ylabel('Angle (°)')
        elif "Pression" in nom :
            ax.set_ylabel('Poids (N)')
        elif "Puissance" in nom :
            ax.set_ylabel('Puissance W/Kg')
        ax.set_xlim(0, 100)

        #Utilise les valeurs min et max possibles comme min et max de graphe.
        minGraph = min(donnees)-max(donneesStdev)
        maxGraph = max(donnees)+max(donneesStdev)
        ax.set_ylim(minGraph, maxGraph)

        #Génère les plots de données et les zone grisées de stDev
        donneesErrPos = []
        donneesErrNeg = []        
        for i in range(0,len(donnees)):
            donneesErrPos.append(donnees[i]+donneesStdev[i])
            donneesErrNeg.append(donnees[i]-donneesStdev[i])
        ax.plot(np.linspace(0, 100, num=len(donnees)),donnees, c='blue',linewidth=0.7)
        ax.fill_between(np.linspace(0, 100, num=len(donnees)), donneesErrPos, donneesErrNeg, alpha=0.2)
        ax.plot([contact, contact],[-360, 360], c='blue',linewidth=2, linestyle="--")
        fig.savefig(path+"\\"+nom, bbox_inche='tight')
        plt.close()
