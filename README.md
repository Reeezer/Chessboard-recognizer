# Chess.com Board recognizer

## Participants

*Léon Muller*

*Lenny Boegli*

## Introduction

Pour ce projet de traitement d'images, nous avons décidé de réaliser un algorithme permettant de détecter un plateau d'échec trouvé sur chess.com et en reconnaitre l'état. Un utilisateur pourra alors fournir un screenshot du plateau (avec les formes et couleurs des pièces adéquates à notre programme) afin d'en obtenir l'état.

Ainsi, grâce à la reconnaissance du plateau de jeu d'après un screenshot, un utilisateur pourrait avoir un BOT et le faire jouer à sa place par exemple.

## Installation et prise en main

Dans le dossier fourni, vous pourrez retrouver des dossiers contenant les images nécessaires à notre projet, des scripts python permettant de générer d'autres images, ainsi que des notebooks contenant l'entrainement et l'utilisation des modèles de deep learning.

Si vous souhaitez lancer les différents scripts, il vous faudra commencer par installer tous les packages python utilisés sur votre machine ou dans un environnement de développement. Pour ce faire, il vous suffit d'exécuter la commande suivante à la racine du projet : `pip install -r requirements.txt`

## Marche suivie & fonctionnalités

### Extraction des cases

La première étape du projet est l'extraction du plateau de jeu dans une image, et le découper case par case en format row major. Pour ce faire, il suffit de lancer le script `board_finder.py`.

En entrée, l'utilisateur fournit un screenshot de son écran de taille 1920x1080p contenant le plateau de jeu sur chess.com.

> Notre script ne permet que de détecter un plateau sur un screenshot d'un écran d'une résolution de 1920x1080p. La taille de la fenêtre du navigateur importe peu, car le site chess.com conserve la taille du plateau peu importe la taille de la fenêtre. Cependant, il ne faut surtout pas zoomer ou dézoomer dans le navigateur.

![](https://i.imgur.com/IMjzDgY.png)
> Figure 1: Screenshot du navigateur sur le site chess.com lors d'une partie d'échecs

Sur ce screenshot, il faut premièrement trouver le plateau de jeu. Pour ce faire, un treshold sur l'image en HSV est effectué. Cette opération enlève la plus grande partie des données de l'image:

![](https://i.imgur.com/iLJwbXy.png)
> Figure 2: Image après le seuillage appliqué

Puis, en appliquant une détection de contour Canny dessus on peut détecter le contour du plateau d'après la taille recherchée.

![](https://i.imgur.com/TJ2SDse.png)
> Figure 3: Le damier trouvé sur l'image

Ensuite, connaissant la position et la taille du damier, on peut l'extraire de l'image. Une fois cette étape réalisée, il faut recommencer les étapes précédentes sur le damier extrait pour en extraire les cases une à une.

Treshold:

![](https://i.imgur.com/hC5M3ez.png)
> Figure 4: Seuille appliqué sur le damier

Contours:

![](https://i.imgur.com/HRK0wOS.png)
> Figure 5: Contours de cases

On peut constater que seulement les carrés verts qui ne se trouvent pas au bord sont trouvés.
Ce n'est pas un problème, car on va tout de même pouvoir trouver à partir de ces carrés la taille moyenne d'un carré. Puis, il suffira d'extraire chaque carré en commençant en partant du haut.

![](https://i.imgur.com/MIKKYXm.png)
> Figure 6: Une des pièces du damier extraites

Une fois toutes les pièces trouvées et extraites, nous les retournons dans une liste pour qu'elles soient envoyées aux scripts suivants.

Pour tester, il y a une variable globale qui est appelée `debugLevel`, la mettre à 1 va afficher les images trouvées.

#### Essais avec Hough

En utilisant des seuils et canny, si la personne zoom, change la résolution, change les couleurs ou autre, la reconnaissance des carrés ne fonctionnera plus. Pour rendre le tout plus général, nous avons tenté de passer par l'utilisation de Hough que vous pourrez retrouver dans le script `HoughTest.py`.

D'abord, nous avons trié toutes les lignes de tailles similaires. Puis, nous cherchons une taille qui nous donne environ 8 lignes sur l'image. Le problème est que l'image contient beaucoup de bruit: il manquait souvent une ligne, une des lignes n'était pas au bon endroit, etc. En théorie, Hough devrait être un meilleur moyen d'extraire les différentes cases. Cependant, faute de temps, nous n'étions pas capables de l'implémenter de façon correcte et utilisable.

![](https://i.imgur.com/ytoQvGV.png)
> Figure 7: Screenshot qui fonctionne

![](https://i.imgur.com/Z4xgzY8.png)
> Figure 8: Screenshot qui ne marche pas du tout 

Pour essayer d’autres screenshots, lancez:
`HoughTest.py [PathToImage]`

### Reconnaissance de pièces

Une fois que l'on a trouvé et extrait les différentes cases du plateau, il nous faut reconnaitre la pièce présente sur la case en question.

Nous avons stocké et recensé toutes les différentes pièces possibles dans le dossier `pieces_screens/pieces/`, ainsi que tous les fonds possibles dans le dossier `pieces_screens/backgrounds/`.

![](https://i.imgur.com/36f0UWe.png)
> Figure 9: Les différents fonds possibles

![](https://i.imgur.com/DEM5yya.png)
> Figure 10: Les différentes pièces possibles

Enfin, pour reconnaitre une pièce sur une case donnée nous avons commencé par utiliser le template matching, cependant celui-ci n'était pas assez précis, et nous sommes donc passés par l'utilisation d'un modèle de Deep learning.

#### Template matching

La première approche a été de réaliser du template matching entre les cases fournies du plateau et l'intégralité des combinaisons possibles de pièces et de fonds.

##### Génération des combinaisons

Afin de générer toutes ces combinaisons, il suffit de lancer le script `generate_pieces.py`. Celui-ci va donc pour chaque pièce créer et sauvegarder la combinaison de celle-ci avec tous les fonds disponibles. Ayant 4 fonds possibles, ainsi que 12 pièces (6 pièces noires, et 6 blanches), nous avons alors généré 48 combinaisons possibles que l'on peut ensuite retrouver dans le dossier `all_pieces/`.

![](https://i.imgur.com/6fDBrM7.png)
> Figure 11: Toutes les combinaisons de pièces/fonds possibles

##### Tests de reconnaissance

Une fois toutes ces pièces générées, il suffira de tester la ressemblance pour une case donnée avec chacune des pièces en lançant le script `piece_recognizer.py`. De plus, pour chaque vérification de ressemblance, nous testons plusieurs tailles possibles, car les cases reçues ne sont pas toujours de la même taille d'un screenshot à l'autre. 

Nous avons pour le template matching utilisé la méthode `TM_CCOEFF_NORMED`, c'est celle qui s'est avérée la plus efficace d'après nos tests. Ainsi, chaque test renvoie une évaluation de ressemblance, et l'on en récupère le meilleur de tous. Nous avons ensuite déterminé que si ce résultat (pour le meilleur match) était inférieur à 0.38, cela voulait dire qu'aucune pièce n'a réellement été reconnue sur la case donnée, et donc que la case est vide. Dans le cas contraire, nous avons bien trouvé la pièce présente sur la case donnée.

De plus, à la fin de l'exécution de ce script, le plateau de jeu est reconstitué de deux manières : affichage simple, et Forsyth Edward Notation (FEN). Ces deux méthodes seront expliquées par la suite.

La méthode du 'template matching' se révèle efficace, mais manque trop souvent de précision. En effet, en moyenne nous avions plus de 75% de bonnes réponses, or cela n'est pas assez haut lorsque l'on veut retranscrire une partie d'échecs. C'est pourquoi nous avons décidé de remplacer le 'template matching' par un modèle de deep learning.

#### Deep learning

Le template matching n'étant pas assez précis, nous sommes partis sur l'utilisation de deep learning. Premièrement, il nous a fallu récolter des données grâce au template matching.

##### Génération des premières données

Pour pouvoir récupérer les données nécessaires pour entrainer notre modèle, nous avons utilisé l'algorithme de template matching sur des plateaux pris en screenshot grâce au script `screenshoter.py` qui fait des screenshots de l'écran entier en pressant sur la touche espace du clavier. 

Pour récolter des données, nous avons alors utilisé ce script tout en regardant en tant que spectateurs une partie sur chess.com. Il suffisait donc d'appuyer sur la barre espace lorsque le plateau de jeu avait beaucoup changé. Les différents plateaux pris en screenshot sont alors rangés dans le dossier `unlabeled_boards/`.

![](https://i.imgur.com/UfwMWG4.png)
> Figure 12: Screenshots des plateaux de jeu

Nous avons alors ensuite utilisé le template matching afin de reconnaitre les pièces trouvées et de les rangées dans leurs dossiers respectifs dans le dossier `labeledConstSize/`. Le script `board_labeler.py` réalisait cette tâche, mais a été très vite modifié pour utiliser le deep learning pour reconnaitre les pièces.

![](https://i.imgur.com/BFAgu1r.png)
> Figure 13: Les différents dossiers pour chaque pièce dans `labeledConstSize/`

![](https://i.imgur.com/xPv6hUD.png)
> Figure 14: Les pièces extraites dans le dossier `labeledConstSize/`

Étant donné que le template matching effectuait beaucoup de fautes, il nous a fallu contrôler toutes les images en faisant de la reconnaissance d'images par traitement humain. C'est-à-dire de supprimer les images mal rangées, car celles-ci auraient trompé le modèle de deep learning.

##### Le modèle choisi

Nous avons choisi d'utiliser une méthode appelée 'transfert learning'. Elle consiste en l'utilisation d'un modèle déjà préentrainé, resnet50 pour ce projet, et en l'affinage de l'entrainement de ce modèle pour qu'il soit plus performant sur nos données. 

L'inconvénient est que ce modèle est donc très volumineux, il prend donc du temps pour s'entrainer et beaucoup de place sur le disque.

##### Entrainement

Pour réaliser l'entrainement du modèle, nous lui avons fourni les données ainsi récoltées dans le dossier `labeledConstSize/`. Après ce premier entrainement, le modèle possédait déjà une précision de 96% environ. Un score plutôt excellent ! Cependant, sur un plateau de 64 cases, le modèle faisait en moyenne 3 fautes, ce qui n'est pas assez bon.

##### Génération de nouvelles données

Nous avons alors choisi de remplacer le template matching par le modèle déjà entrainé dans le script `board_labeler.py`. Ce modèle a une précision beaucoup plus élevée que le template matching. Nous avons alors effectué à nouveau les étapes de récoltes de données et d'entrainement grâce à ce modèle.

##### Data augmentation

Enfin, pour éviter l'overfitting et tendre vers une généralisation de notre modèle, nous avons ajouté de la data augmentation inplace. C'est-à-dire que lorsque nous entrainons notre modèle de deep learning, les données en entrée sont modifiées de façon aléatoire de 3 différentes manières :
- Random Translation: translation aléatoire des images
- Random Contrast: modification aléatoire des contrastes
- Random Zoom: zoom aléatoire dans une zone de l'image

Étant donné que nous n'avons que des données provenant de screenshots, ces données sont toutes trop similaires. En soi, ce n'est pas un réel problème, car nous souhaitons aussi reconnaitre l'état de jeu d'un plateau à partir d'un screenshot. Cependant, le modèle ne permettait pas de généraliser les prédictions qu'il faisait et donc était très mauvais lorsque la qualité des cases fournies n'était pas exactement la même que celles sur lesquelles il s'était entrainé. C'est pourquoi nous avons réalisé de la data augmentation, afin de modifier les données d'entrées justes assez pour que celles-ci ne soient pas simplement identiques. Cette data augmentation applique tout de même des modifications plausibles, on ne souhaiterait pas par exemple tourner les images sur elles-mêmes.

##### Évaluation

Après évaluation du modèle sur 10% de nos données, nous obtenons une précision de plus de 99%. Ce modèle nous permet alors de reconnaitre presque parfaitement les cases d'un plateau d'échec, et donc nous permet de retrouver le plateau de 64 cases d'un jeu d'échecs.

Une fois les cases retrouvées, nous les affichons de différentes manières à un utilisateur ou un programme potentiel.

Voici donc le résultat de la reconnaissance d'un plateau:
![](https://i.imgur.com/PJa7MPk.png)
> Figure 15: Screenshot d'un plateau et recréation de celui-ci à partir des cases reconnues

### Affichage du plateau reconnu

Une fois que le plateau de jeu a été reconnu par notre algorithme, il va nous falloir l'afficher à l'utilisateur pour qu'il puisse le comprendre et l'analyser ou alors l'utiliser avec un de ses scripts. C'est pourquoi nous avons choisi de proposer 3 affichages différents pour représenter un plateau.

#### Affichage simple

L'affichage simple est la retranscription du plateau sous forme de grille de lettres dans la console. Les lettres sont les premières lettres des noms des pièces:
- Rook -> r
- Pawn -> p
- Bishop -> b
- King -> k
- Queen -> q
- Knight -> n (seule exception)
- Empty -> -

Ensuite, la couleur est représentée grâce à la casse:
- white -> upper
- black -> lower

![](https://i.imgur.com/l3k0FIn.png)
> Figure 16: Exemple de cet affichage

#### Forsyth Edward Notation (FEN)

L'affichage d'après la notation Forsyth Edward reprend les mêmes règles que l'affichage simple, cependant le tout se fait sur une seule ligne. De plus: les cases vides sont comptées et représentées par le nombre de cases vide qu'il y a à la suite.

> Cet affichage prend normalement d'autres paramètres comme le joueur actuel et le dernier mouvement, mais nous ne sommes pas en mesure de le fournir.

![](https://i.imgur.com/RkYFMcl.png)
> Figure 17: Exemple de cet affichage

#### Recréation d'une image du plateau

Enfin, la recréation d'une image du plateau est la reconstitution du plateau grâce aux images de pièces et de fonds que l'on met les une à côté des autres.

Le seul souci est que nous n'avons aucun moyen de connaitre la couleur de la première case, nous sommes donc partis du principe que celle-ci sera toujours blanche. Or en fonction de la couleur des pions du joueur, celle-ci peut changer. Ce n'est pas un défaut majeur, car ces couleurs n'apportent aucune aide ou obligation dans un jeu d'échecs.

![](https://i.imgur.com/ghMvc5f.png)
> Figure 18: Exemple de cet affichage

## Améliorations

 * Rendre l'extraction des carrés plus générale
     * Photo au lieu de screenshot
     * Résolution différente
     * Plus de bruit sur l'image (flou, rotation, etc.)
 * Reconnaitre le prochain joueur
     * Pour trouver le meilleur tour, il faut savoir qui doit jouer
 * Faire un modèle DeepLearning plus léger

## Conclusion

Ce projet permet à partir d'un screenshot d'un plateau de jeu présent sur chess.com d'en reconnaître l'état avec précision. Nous sommes alors passés par plusieurs méthodes afin d'augmenter à chaque fois la précision de cette reconnaissance et ainsi permettre à un utilisateur de retrouver quasiment parfaitement le plateau de jeu. Les différentes façons de retourner l'état du plateau permettent à un utilisateur de réutiliser ce code pour fournir à un BOT par exemple l'état actuel du plateau de jeu.
