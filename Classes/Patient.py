import os
from .Articulation import Articulation
from .Donnees import Donnees
import statistics

class Patient:

    def __init__(self, nom, donneesBrutes):
        self.nom = nom

        #Si côté droit patho, on échange les jambes pour que tout les côtés patho soient à gauche
        if self.nom[0:2] == "D_":
            self.nom+= " inverse"
            correspondancesArticulations = [
                {"line":0, "nom": "PelvisD"},
                {"line":3, "nom": "HancheD"},
                {"line":6, "nom": "GenouD"},
                {"line":9, "nom": "ChevilleD"},
                {"line":12, "nom": "PiedD"},
                {"line":16, "nom": "PelvisG"},
                {"line":19, "nom": "HancheG"},
                {"line":22, "nom": "GenouG"},
                {"line":25, "nom": "ChevilleG"},
                {"line":28, "nom": "PiedG"}]
        else :
            correspondancesArticulations = [
                {"line":0, "nom": "PelvisG"},
                {"line":3, "nom": "HancheG"},
                {"line":6, "nom": "GenouG"},
                {"line":9, "nom": "ChevilleG"},
                {"line":12, "nom": "PiedG"},
                {"line":16, "nom": "PelvisD"},
                {"line":19, "nom": "HancheD"},
                {"line":22, "nom": "GenouD"},
                {"line":25, "nom": "ChevilleD"},
                {"line":28, "nom": "PiedD"}]

        self.articulations = {}
        for i in range(0,len(correspondancesArticulations)) :
            coresp = correspondancesArticulations[i]
            self.articulations[coresp["nom"]]=Articulation(donneesBrutes[coresp["line"]],donneesBrutes[coresp["line"]+1],donneesBrutes[coresp["line"]+2],1)

        self.PressionD = Donnees(donneesBrutes[15],1)

        self.PressionG = Donnees(donneesBrutes[31],1)

        self.moyennePourcentageContactG = statistics.mean(donneesBrutes[32])
        self.variancePourcentageContactG = statistics.variance(donneesBrutes[32])
        self.moyennePourcentageContactD = statistics.mean(donneesBrutes[33])
        self.variancePourcentageContactD = statistics.variance(donneesBrutes[33])
        print("Patient " + self.nom + " OK")
    def depuisFichier(emplacement):

        donnees_traj=[]
        donnees_devices=[]
        donnees_events=[]
        donnees_model=[]
        listePlaceForceplateZ=[]
        debut_donnees_events = 0
        fin_donnees_events = 0
        debut_donnees_model = 0
        fin_donnees_model = 0
        debut_donnees_devices = 0
        debut_donnees_traj = 0
        Lcontact=[]
        Rcontact=[]
        Loff=[]
        Roff=[]
        LRatioContact=[]
        RRatioContact=[]
        DonneesFPZG=[]
        DonneesFPZD=[]

        progFPZG = [[]]
        progFPZD = [[]]
        progPelvGX = [[]]
        progPelvGY = [[]]
        progPelvGZ = [[]]
        progPelvDX = [[]]
        progPelvDY = [[]]
        progPelvDZ = [[]]
        progHancheGX = [[]]
        progHancheGY = [[]]
        progHancheGZ = [[]]
        puissHancheG = [[]]
        progHancheDX = [[]]
        progHancheDY = [[]]
        progHancheDZ = [[]]
        puissHancheD = [[]]
        progGenouGX = [[]]
        progGenouGY = [[]]
        progGenouGZ = [[]]
        puissGenouG = [[]]
        progGenouDX = [[]]
        progGenouDY= [[]]
        progGenouDZ = [[]]
        puissGenouD = [[]]
        progChevilleGX = [[]]
        progChevilleGY = [[]]
        progChevilleGZ = [[]]
        puissChevilleG = [[]]
        progChevilleDX = [[]]
        progChevilleDY = [[]]
        progChevilleDZ = [[]]
        puissChevilleD = [[]]
        progPiedDX =[[]]
        progPiedDY =[[]]
        progPiedDZ =[[]]
        progPiedGX =[[]]
        progPiedGY =[[]]
        progPiedGZ =[[]]

        donnees_brutes=open(emplacement).readlines()


        #Première boucle, détection des limites des blocs de données

        for j in range(0,len(donnees_brutes)):
            ligne_en_cours=donnees_brutes[j].split(",")
            if "Events\n" in ligne_en_cours :
                debut_donnees_events = j+4
            if "ï»¿Events\n"in ligne_en_cours :
                debut_donnees_events = j+2
            if "Model Outputs\n" in ligne_en_cours :
                fin_donnees_devices = j-2
                debut_donnees_model = j+5
            if "Devices\n" in ligne_en_cours :
                fin_donnees_events = j-2
                debut_donnees_devices = j+5
            if "Trajectories\n" in ligne_en_cours :
                if debut_donnees_model!=0:
                    fin_donnees_model = j-2
                else :
                    fin_donnees_devices = j - 2
                debut_donnees_traj = j+5

        #Deuxième boucle, récupération des données

        for j in range(0,len(donnees_brutes)):
            ligne_en_cours=donnees_brutes[j].split(",")

            if j == debut_donnees_traj:
                timeOffset=int(ligne_en_cours[0])
            if debut_donnees_model <= j <= fin_donnees_model:
                donnees_model.append(ligne_en_cours)
            if debut_donnees_events <= j <= fin_donnees_events:
                donnees_events.append(ligne_en_cours)
            if debut_donnees_devices <= j <= fin_donnees_devices:
                donnees_devices.append(ligne_en_cours)
            if j>=debut_donnees_traj:
                donnees_traj.append(ligne_en_cours)

        #On cherche quelles colonnes contiennent les données des marqueurs qui nous intéressent
        noms_devices = donnees_brutes[debut_donnees_devices-3].split(",")
        noms_model_output = donnees_brutes[debut_donnees_model-3].split(",")
        for j in range(0,len(noms_devices)):
            if "Force Plate - Force" in noms_devices[j]:
                listePlaceForceplateZ.append(j+2)
        for j in range(0,len(noms_model_output)):
            if "LFootProgressAngles" in noms_model_output[j]:
                LFoot=j
            if "RFootProgressAngles" in noms_model_output[j]:
                RFoot=j
            if "LAnkleAngles" in noms_model_output[j]:
                LAnkle=j
            if "RAnkleAngles" in noms_model_output[j]:
                RAnkle=j
            if "LAnklePower" in noms_model_output[j]:
                LAnkPow = j
            if "RAnklePower" in noms_model_output[j]:
                RAnkPow = j
            if "LKneeAngles" in noms_model_output[j]:
                LKnee=j
            if "RKneeAngles" in noms_model_output[j]:
                RKnee=j
            if "LKneePower" in noms_model_output[j]:
                LKneePow = j
            if "RKneePower" in noms_model_output[j]:
                RKneePow = j
            if "LHipAngles" in noms_model_output[j]:
                LHip=j
            if "RHipAngles" in noms_model_output[j]:
                RHip=j
            if "LHipPower" in noms_model_output[j]:
                LHipPow = j
            if "RHipPower" in noms_model_output[j]:
                RHipPow = j
            if "LPelvisAngles" in noms_model_output[j]:
                LPelv=j
            if "RPelvisAngles" in noms_model_output[j]:
                RPelv=j

        if len(listePlaceForceplateZ)>0:
            for j in range(0, len(donnees_devices)):
                for k in range(0,len(donnees_devices[j])):
                    if k==listePlaceForceplateZ[0]:
                        DonneesFPZG.append(float(donnees_devices[j][k]))
                    if k == listePlaceForceplateZ[1]:
                        DonneesFPZD.append(float(donnees_devices[j][k]))
        #TODO : Bout de code pour créer les events
        if fin_donnees_events==0:
            # Premier Contact
            Lcontact=createFootContactEvent(DonneesLHEE[1],timeOffset)
            Rcontact=createFootContactEvent(DonneesRHEE[1],timeOffset)
            #Dernier Contact
            Loff=createFootOffEvent(DonneesLTOE[1],timeOffset)
            Roff=createFootOffEvent(DonneesRTOE[1],timeOffset)
        else :
            for j in range(0,len(donnees_events)):
                if "Left" in donnees_events[j][1]:
                    if "Foot Strike" in donnees_events[j][2] and int(float(donnees_events[j][3])*100) > timeOffset :
                        Lcontact.append(int(float(donnees_events[j][3])*100)-timeOffset)
                    elif "Foot Off" in donnees_events[j][2] and int(float(donnees_events[j][3])*100) > timeOffset :
                        Loff.append(int(float(donnees_events[j][3])*100)-timeOffset)
                if "Right" in donnees_events[j][1]:
                    if "Foot Strike" in donnees_events[j][2] and int(float(donnees_events[j][3])*100) > timeOffset :
                        Rcontact.append(int(float(donnees_events[j][3]) * 100)-timeOffset)
                    elif "Foot Off" in donnees_events[j][2] and int(float(donnees_events[j][3])*100) > timeOffset :
                        Roff.append(int(float(donnees_events[j][3]) * 100)-timeOffset)

        #On s'assure que le premier event est un contact et le dernier un off
        if Loff[0]<Lcontact[0]:
            Loff.pop(0)
        if Roff[0]<Rcontact[0]:
            Roff.pop(0)
        if Loff[-1]<Lcontact[-1]:
            Lcontact.pop(-1)
        if Roff[-1]<Rcontact[-1]:
            Rcontact.pop(-1)

        #On récupère toutes les données à gauche
        for i in range(0,len(Lcontact)-1):
            LRatioContact.append(100*(Loff[i]-Lcontact[i])/(Lcontact[i+1]-Lcontact[i]))
            if i>0:
                progPiedGX.append([])
                progPiedGY.append([])
                progPiedGZ.append([])
                progChevilleGX.append([])
                progChevilleGY.append([])
                progChevilleGZ.append([])
                puissChevilleG.append([])
                progGenouGX.append([])
                progGenouGY.append([])
                progGenouGZ.append([])
                puissGenouG.append([])
                progHancheGX.append([])
                progHancheGY.append([])
                progHancheGZ.append([])
                puissHancheG.append([])
                progPelvGX.append([])
                progPelvGY.append([])
                progPelvGZ.append([])
                progFPZG.append([])
            for j in range(Lcontact[i],Lcontact[i+1]):
                for k in range(0,len(noms_model_output)):
                    if k==LFoot:
                        progPiedGX[i].append(float(donnees_model[j][k]))
                        progPiedGY[i].append(float(donnees_model[j][k + 1]))
                        progPiedGZ[i].append(float(donnees_model[j][k + 2]))
                    if k==LAnkle:
                        progChevilleGX[i].append(float(donnees_model[j][k]))
                        progChevilleGY[i].append(float(donnees_model[j][k + 1]))
                        progChevilleGZ[i].append(float(donnees_model[j][k + 2]))
                    if k==LAnkPow:
                        if donnees_model[j][k+2] !="":
                            puissChevilleG[i].append(float(donnees_model[j][k+2]))
                        else:
                            puissChevilleG[i].append(0)
                    if k==LKnee:
                        progGenouGX[i].append(float(donnees_model[j][k]))
                        progGenouGY[i].append(float(donnees_model[j][k + 1]))
                        progGenouGZ[i].append(float(donnees_model[j][k + 2]))
                    if k==LKneePow:
                        if donnees_model[j][k + 2] != "":
                            puissGenouG[i].append(float(donnees_model[j][k + 2]))
                        else:
                            puissGenouG[i].append(0)
                    if k == LHip:
                        progHancheGX[i].append(float(donnees_model[j][k]))
                        progHancheGY[i].append(float(donnees_model[j][k + 1]))
                        progHancheGZ[i].append(float(donnees_model[j][k + 2]))
                    if k==LHipPow:
                        if donnees_model[j][k + 2] != "":
                            puissHancheG[i].append(float(donnees_model[j][k+2]))
                        else:
                            puissHancheG[i].append(0)
                    if k == LPelv:
                        progPelvGX[i].append(float(donnees_model[j][k]))
                        progPelvGY[i].append(float(donnees_model[j][k + 1]))
                        progPelvGZ[i].append(float(donnees_model[j][k + 2]))
                if len(listePlaceForceplateZ) > 0:
                    for k in range(0,9):
                        if j<Loff[i]:
                            progFPZG[i].append(-DonneesFPZG[10*j+k])

        #On récupère toutes les données à droite
        for i in range(0, len(Rcontact)-1):
            RRatioContact.append(100*(Roff[i]-Rcontact[i])/(Rcontact[i+1]-Rcontact[i]))
            if i>0:
                progPiedDX.append([])
                progPiedDY.append([])
                progPiedDZ.append([])
                progChevilleDX.append([])
                progChevilleDY.append([])
                progChevilleDZ.append([])
                puissChevilleD.append([])
                progGenouDX.append([])
                progGenouDY.append([])
                progGenouDZ.append([])
                puissGenouD.append([])
                progHancheDX.append([])
                progHancheDY.append([])
                progHancheDZ.append([])
                puissHancheD.append([])
                progPelvDX.append([])
                progPelvDY.append([])
                progPelvDZ.append([])
                progFPZD.append([])

            for j in range(Rcontact[i], Rcontact[i+1]):
                for k in range(0,len(noms_model_output)):
                    if k==RFoot:
                        progPiedDX[i].append(float(donnees_model[j][k]))
                        progPiedDY[i].append(float(donnees_model[j][k + 1]))
                        progPiedDZ[i].append(float(donnees_model[j][k + 2]))
                    if k==RAnkle:
                        progChevilleDX[i].append(float(donnees_model[j][k]))
                        progChevilleDY[i].append(float(donnees_model[j][k + 1]))
                        progChevilleDZ[i].append(float(donnees_model[j][k + 2]))
                    if k == RAnkPow:
                        if donnees_model[j][k + 2] != "":
                            puissChevilleD[i].append(float(donnees_model[j][k + 2]))
                        else:
                            puissChevilleD[i].append(0)
                    if k==RKnee:
                        progGenouDX[i].append(float(donnees_model[j][k]))
                        progGenouDY[i].append(float(donnees_model[j][k + 1]))
                        progGenouDZ[i].append(float(donnees_model[j][k + 2]))
                    if k==RKneePow:
                        if donnees_model[j][k + 2] != "":
                            puissGenouD[i].append(float(donnees_model[j][k+2]))
                        else:
                            puissGenouD[i].append(0)
                    if k == RHip:
                        progHancheDX[i].append(float(donnees_model[j][k]))
                        progHancheDY[i].append(float(donnees_model[j][k + 1]))
                        progHancheDZ[i].append(float(donnees_model[j][k + 2]))
                    if k==RHipPow:
                        if donnees_model[j][k + 2] != "":
                            puissHancheD[i].append(float(donnees_model[j][k+2]))
                        else:
                            puissHancheD[i].append(0)
                    if k == RPelv:
                        progPelvDX[i].append(float(donnees_model[j][k]))
                        progPelvDY[i].append(float(donnees_model[j][k + 1]))
                        progPelvDZ[i].append(float(donnees_model[j][k + 2]))
                if len(listePlaceForceplateZ) > 0:
                    for k in range(0,9):
                        if j < Roff[i]:
                            progFPZD[i].append(-DonneesFPZD[10*j+k])


        donneesBrutes = [progPelvDX,progPelvDY,progPelvDZ, progHancheDX,progHancheDY,progHancheDZ, progGenouDX, progGenouDY, progGenouDZ,\
            progChevilleDX, progChevilleDY, progChevilleDZ, progPiedDX, progPiedDY, progPiedDZ, progFPZD, progPelvGX,\
            progPelvGY,progPelvGZ, progHancheGX,progHancheGY,progHancheGZ, progGenouGX, progGenouGY, progGenouGZ, progChevilleGX,\
            progChevilleGY, progChevilleGZ, progPiedGX, progPiedGY, progPiedGZ, progFPZG, LRatioContact, RRatioContact, \
            puissHancheD, puissGenouD, puissChevilleD, puissHancheG, puissGenouG, puissChevilleG]
        return Patient(emplacement.split("\\")[-1].replace(".csv",""), donneesBrutes)

Patient.depuisFichier = staticmethod(Patient.depuisFichier)