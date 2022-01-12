## Usage :

Ce script genère des graphiques et données statistiques a partir de données PlugInGait de Vicon Nexus.

Pour fonctionner, il faut préparer 1 ou 2 populations de csv exportés de Nexus 2, chacune contenue dans un dossier distinct. Les CSV doivent contenir des modèles PlugInGait reconstruits, sans trous dans les données.

## Graphes et données :

Pour chaque population, ce script génère les graphiques normalisés par cycle de marche du mouvement et de son écart-type pour chaque articulation dans les 3 axes. 
Il génère ensuite les mêmes graphiques de la différence entre la 2ème population et la première ainsi que pour chaque patient de chaque population.
Les données brutes utilisées pour les graphiques sont stockées dans un CSV contenu dans le dossier correspondant.

## Test statistique :

**Test de Kolmogorov-Smirnov** : Permet de comparer la progression articulaire de 2 articulations : pour chaque test, une p-value < 0,05 indique une différence statistique entre les mouvements des 2 articulations testées. Un test de Kolmogorov-Smirnov est réalisé pour comparer chaque articulation de la population 1 avec celles de la population 2

Les résultats de ce test sont stockés dans  "Test Kolmogorov-Smirnov.xlsx", contenu dans le dossier de résultat contenant les courbes de différences entre les 2 populations.

## 1 seule population :

Dans le cas où on veut seulement récupérer les données et graphes pour une population de patient, séléctionner le dossier qui la contient en premier et cliquer sur "Annuler" lors de la selection de la seconde population.

## Cas de population avec côté sain et pathologique :

Dans le cas où on a une population (par exemple de patients hémiplégiques) présentant un côté sain et un côté pathologique, identifier le côté pathologique du patient en commencant le csv par "G_" ou "D_" en fonction d'une pathologie du côté gauche ou droit. par exemple, patient1.csv devra être nommé G_patient1.csv si son côté gauche est pathologique.

Le script échangera ensuite les côté gauche et droit des patients présentant une pathologie à droite afin que tous les membres sains soient à droite et tous les membres pathologiques à gauche pour tous les patients. 

Un patient dont le côté gauche et droit ont été inversés portera la mention "inversé" dans son nom. Par exemple, le patient D_toto.csv s'appellera D_toto inversé.
