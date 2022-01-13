from turtle import position
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
            self.resultatsKSTest = self.testKSGlobal(self.population1, self.population2,os.getcwd()+ "\\Donnees "+ self.diffPopulation.nom)
            self.generateurDonneesGlobal(self.diffPopulation,os.getcwd() + "\\Donnees "+ self.diffPopulation.nom, self.resultatsKSTest)            

    def testKSGlobal(self, population1, population2, path):
        if not os.path.exists(path):
            os.mkdir(path)
        workbook = xlsxwriter.Workbook(path + '\\Test Kolmogorov-Smirnov.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0, "Articulation")
        worksheet.write(1,0, "Axe")
        colonne = 1
        #Kolmogorov-Smirnov test, hypothèse nulle = p-value > 5% = les 2 pops sont les mêmes
        resultatTests = {}
        for articulation in population1.articulations:
            worksheet.write(0,colonne, articulation)
            worksheet.write(1,colonne, "X")
            worksheet.write(1,colonne+2, "Y")
            worksheet.write(1,colonne+4, "Z")
            for i in range(0,3):
                worksheet.write(2,colonne+2*i, "statistic")
                worksheet.write(2,colonne+2*i+1, "p-value")

            resultatTests[articulation] = self.testKS(population1.articulations[articulation],population2.articulations[articulation])
            cellFormatRouge = workbook.add_format({ 'bg_color': '#F08080'})
            cellFormatVert = workbook.add_format({ 'bg_color': '#90EE90'})

            for i in range(0,3):
                if resultatTests[articulation][i][1]<0.05:
                    worksheet.write(3,colonne+2*i,resultatTests[articulation][i][0],cellFormatRouge)
                    worksheet.write(3,colonne+2*i+1,resultatTests[articulation][i][1],cellFormatRouge)
                else:
                    worksheet.write(3,colonne+2*i,resultatTests[articulation][i][0],cellFormatVert)
                    worksheet.write(3,colonne+2*i+1,resultatTests[articulation][i][1],cellFormatVert)

            colonne +=6
        workbook.close()
        print("Test Kolmogorov-Smirnov OK")
        return resultatTests

    def testKS(self,articulation1, articulation2):
        resultat=[]
        resultat.append(scp.ks_2samp(articulation1.moyenneX, articulation2.moyenneX))
        resultat.append(scp.ks_2samp(articulation1.moyenneY, articulation2.moyenneY))
        resultat.append(scp.ks_2samp(articulation1.moyenneZ, articulation2.moyenneZ))

        return resultat

    def generateurDonneesGlobal(self,population,path, KStest=""):
        if not os.path.exists(path):
            os.mkdir(path)
        self.generateurDonneesExcel(population, path)
        self.generateurGraphePopulation(population, path, KStest)
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


    def generateurGraphePopulation(self, population,path, KStest):
        correspondancesGraphe = [
            {"cote":"G", "noms": ["Bascule bassin G","Obliquité bassin G","Rotation bassin G"], "articulation": "PelvisG"},
            {"cote":"G", "noms": ["Flexion hanche G","Abd-adduction hanche G","Rotation hanche G"], "articulation": "HancheG"},
            {"cote":"G", "noms": ["Flexion genou G","","Varus-Valgus genou G"], "articulation": "GenouG"},
            {"cote":"G", "noms": ["Flexion cheville G","Rotation cheville G",""], "articulation": "ChevilleG"},
            {"cote":"G", "noms": ["","","Progression pas G"], "articulation": "PiedG"},
            {"cote":"D", "noms": ["Bascule bassin D","Obliquité bassin D","Rotation bassin D"], "articulation": "PelvisD"},
            {"cote":"D", "noms": ["Flexion hanche D","Abd-adduction hanche D","Rotation hanche D"], "articulation": "HancheD"},
            {"cote":"D", "noms": ["Flexion genou D","","Varus-Valgus Denou D"], "articulation": "GenouD"},
            {"cote":"D", "noms": ["Flexion cheville D","Rotation cheville D",""], "articulation": "ChevilleD"},
            {"cote":"D", "noms": ["","","Progression pas D"], "articulation": "PiedD"}]

        for i in range(0,len(correspondancesGraphe)):
            corresp = correspondancesGraphe[i]
            donnees = population.articulations[corresp['articulation']]

            for j in range(0,len(corresp["noms"])):
                if corresp["noms"][j]!="":
                    if KStest!='':
                        KStestEnCours = KStest[corresp["articulation"]][j][1]
                    else:
                        KStestEnCours = ""
                    if j == 0:
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneX,donnees.stdevX,population.moyennePourcentageContactG,KStestEnCours)
                        elif corresp["cote"]=="D":    
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneX,donnees.stdevX,population.moyennePourcentageContactD, KStestEnCours)
                    elif j == 1:                    
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneY,donnees.stdevY,population.moyennePourcentageContactG, KStestEnCours)
                        elif corresp["cote"]=="D":    
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneY,donnees.stdevY,population.moyennePourcentageContactD, KStestEnCours)
                    elif j == 2:
                        if corresp["cote"]=="G":
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneZ,donnees.stdevZ,population.moyennePourcentageContactG, KStestEnCours)
                        elif corresp["cote"]=="D":            
                            self.generateurGrapheSimple(corresp["noms"][j], path, donnees.moyenneZ,donnees.stdevZ,population.moyennePourcentageContactD, KStestEnCours)

    def generateurGrapheSimple(self,nom, path, donnees, donneesStdev,contact, KStest):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.grid(color='black', linestyle='-', linewidth=0.1)
        ax.set_title(nom)
        ax.set_xlabel('% cycle')
        ax.set_ylabel('Angle (°)')
        ax.set_xlim(0, 100)

        #Utilise les valeurs min et max possibles comme min et max de graphe.
        minGraph = min(donnees)-max(donneesStdev)*1.1
        maxGraph = max(donnees)+max(donneesStdev)*1.1
        ax.set_ylim(minGraph, maxGraph)
        if KStest != '':
            if KStest < 0.05:
                color = "#F08080"
            else :
                color = "#90EE90"
            positionTexte = maxGraph-(abs(maxGraph)+abs(minGraph))*0.04
            ax.text(1, positionTexte,"P-value KS: " + str(KStest), bbox=dict(boxstyle="square,pad=0.3",fc=color))
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
