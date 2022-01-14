## Utilisation :

Ce script genère des graphiques et données statistiques a partir de données PlugInGait de Vicon Nexus.

Pour fonctionner, il faut préparer 1 ou 2 populations de csv exportés de Nexus 2, chacune contenue dans un dossier distinct. Les CSV doivent contenir des modèles PlugInGait reconstruits, sans trous dans les données.

Le script génèrera ensuite pour chaque population un dossier de résultats dans le dossier où il se trouve.

**Exemple d'organisation des dossiers de population :**

![population](https://user-images.githubusercontent.com/47147929/149176687-a8df554e-64ac-4467-ba42-a360e6631287.PNG)


## Graphes et données :

Pour chaque population, ce script génère les graphiques normalisés par cycle de marche du mouvement et de son écart-type pour chaque articulation dans les 3 axes. 
Il génère ensuite les mêmes graphiques de la différence entre la 2ème population et la première ainsi que pour chaque patient de chaque population.

Les données brutes utilisées pour les graphiques sont stockées dans un CSV contenu dans le dossier où se trouve le graphe.

**Exemple de graphe généré :**
![Flexion cheville D](https://user-images.githubusercontent.com/47147929/149182881-69557d04-b3db-4926-a4ce-76a70c74ed2a.png)

## Test statistique :

**Test de Kolmogorov-Smirnov** : Permet de comparer la progression articulaire de 2 articulations : pour chaque test, une p-value < 0,05 indique une différence statistique entre les mouvements des 2 articulations testées. Un test de Kolmogorov-Smirnov est réalisé pour comparer chaque articulation de la population 1 avec celles de la population 2

Les résultats de ce test sont stockés dans  "Test Kolmogorov-Smirnov.xlsx", contenu dans le dossier de résultat contenant les courbes de différences entre les 2 populations; Ils sont aussi affichés dans le coin de chaque courbe, sur un fond rouge si l'articulation observée est différente entre les 2 populations, sur un fond vert sinon :

![boite rouge](https://user-images.githubusercontent.com/47147929/149499861-4437b92f-24e2-4004-9474-8bcd924ff683.PNG)

## Cas d'utilisation :

### 1 seule population :

Dans le cas où on veut seulement récupérer les données et graphes pour une population de patient, séléctionner le dossier qui la contient en premier et cliquer sur "Annuler" lors de la selection de la seconde population.

### Cas de population avec côté sain et pathologique :

Dans le cas où on a une population (par exemple de patients hémiplégiques) présentant un côté sain et un côté pathologique, identifier le côté pathologique du patient en commencant le csv par "G_" ou "D_" en fonction d'une pathologie du côté gauche ou droit. par exemple, patient1.csv devra être nommé G_patient1.csv si son côté gauche est pathologique.

Le script échangera ensuite les côté gauche et droit des patients présentant une pathologie à droite afin que tous les membres sains soient à droite et tous les membres pathologiques à gauche pour tous les patients. 

Un patient dont le côté gauche et droit ont été inversés portera la mention "inversé" dans son nom. Par exemple, le patient D_toto.csv s'appellera D_toto inversé.
