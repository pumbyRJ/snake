# import
from fltk import *
from time import sleep
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
	"""
	Fonction recevant les coordonnées d'une case du plateau sous la
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul
	prend en compte la taille de chaque case, donnée par la variable
	globale taille_case.
	"""
	i, j = case
	return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
	'''
	fonction qui dessine les pommes sur le terrain quand la fonction 
	est appellée a un endroit. 
	'''
	for pomme in pommes:
		x, y = case_vers_pixel(pomme)
		cercle(x, y, taille_case/2,
			   couleur = 'darkred', remplissage = 'red')
		rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
				  couleur = 'darkgreen', remplissage = 'darkgreen')
                  
def affiche_bombes(bombes):
	'''
	fonction qui dessine les bombes sur le terrain quand la fonction 
	est appellée a un endroit. 
	'''
	for bombe in bombes:
		x, y = case_vers_pixel(bombe)
		cercle(x, y, taille_case/2,
			   couleur = 'black', remplissage = 'black')
		rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
				  couleur = 'yellow', remplissage = 'yellow')

def affiche_serpent(serpent):
	"""
	Fonction qui recoit les coordonnées des cercles faisant partie du
	corps du serpent et qui pour tous les cercles faisant partie de la
	liste: serpent(donc de son corp) les dessine en cercle remplis de
	vert avec les contours vert foncé.
	"""
	for segment in range(len(serpent)):# boucle pour chaque rond faisant partie du serpent
		x, y = case_vers_pixel(serpent[segment])  # à modifier !!!
		cercle(x, y, taille_case/2 + 1,
		couleur = 'darkgreen', remplissage = 'green')

def change_direction(direction, touche):
	"""
	fonction 'lit' qui les touches pressées et retourne pour chaque touche
	une direction avec comme condition que la direction actuelle ne soit pas
	celle opposée à la direction que nous voulons.
	
	change_direction(direction,'up')
	>>>(0, 1)
	change_direction(direction, 'left')
	>>>(-1, 0)
	"""
	# à compléter !!!
	if touche == 'Up' and direction != (0, 1):
	# flèche haut pressée
		return (0, -1)
	# retourne la direction vers le haut si la direction actuelle n'est pas vers le bas
	elif touche == 'Down' and direction != (0, -1):
		return (0, 1)
	# retourne la direction vers le bas si la direction actuelle n'est pas vers le haut
	elif touche == 'Right' and direction != (-1, 0):
		return (1, 0)
	# retourne la direction vers la droite si la direction actuelle n'est pas vers la gauche
	elif touche == 'Left' and direction != (1, 0):
		return (-1, 0)
	# retourne la direction vers la gauche si la direction actuelle n'est pas vers la droite
	else:
		# pas de changement !
		return direction

def deplacement_serpent(serpent, direction):
	"""
	fonction qui prend les coordonnées de la tete du serpent ainsi que
	la direction dans la quelle il va pour savoir si il sort du plateau
	,si il se mange la queue ou si il mange une pomme ou si il ne fait
	rien de cela.
	
	deplacement_serpent()
	>>>False
	deplacement_serpent()
	>>>(24, 20)
	>>>True
	"""
	dx, dy = serpent[-1]
	if 0 > dy+direction[1] or dy+direction[1] > 29 or dx+direction[0] < 0 or dx+direction[0] > 39 :
		return False# arrete le jeu si le serpent sort de la fenetre
	elif (dx+direction[0], dy+direction[1]) in serpent and len(serpent) >1 :
		return False# arrete le jeu si le serpent se mange lui meme
	elif (dx+direction[0], dy+direction[1]) in pommes:
		pomme_aleatoire()# rajoute une nouvelle pomme apres que celle d avant est ete mangé
		pommes.remove((dx+direction[0], dy+direction[1]))# supprime la pomme que le serpent a mangé
	elif (dx+direction[0], dy+direction[1]) in bombes:
		return False
	else :# si il ne se passe rien
		serpent.pop(0)# supprime la queue du serpent
	serpent.append((dx+direction[0], dy+direction[1]))# ajoute la nouvelle tete a l'emplacement suivant
	return True
	
def pomme_aleatoire():
	"""
	fonction qui fait apparaitre des pommes aleatoirement sur le plateau
	en faisant attention qu'elle ne spawn pas sur le serpent ou une pomme
	deja presente.
	
	pomme_aleatoire()
	>>>False
	pomme_aleatoire()
	>>>(30, 24)
	"""
	pomme = (randint(0, 39), randint(0, 29))
	if pomme not in serpent and pomme not in pommes and pomme not in bombes:
		pommes.append(pomme)
		# si le spawn est sur le serpent,une pomme ou une bombe,elle ne spawn pas ajoute une pomme si l emplacement est vide
def bombe_aleatoire():
	'''
	fonction qui fait apparaitre des bombes aleatoirement sans qu'elle
	spawn sur le serpent ou une pomme ou encore sur une autre bombe.
	
	bombe_aleatoire()
	>>>False
	bombe_aleatoire()
	>>>(5, 12)
	'''
	bombe = (randint(0, 39), randint(0, 29))
	if bombe in serpent or bombe in bombes or bombe in pommes:
		return False
	else:
		bombes.append(bombe)

# programme principal
if __name__ == "__main__":
	# initialisation du jeu
	framerate = 10# taux de rafraîchissement du jeu en images/s
	direction = (0, 0)# direction initiale du serpent
	pommes = [(19, 10)]# liste des coordonnées des cases contenant des pommes et ajout de la toute premiere pomme
	serpent = [(19, 14)] # liste des coordonnées de cases adjacentes décrivant le serpent
	cree_fenetre(taille_case * largeur_plateau,
				 taille_case * hauteur_plateau)
	rectangle(0, 0, 600, 450, couleur = 'black', remplissage = 'pink')#arriere plan
	bombes = []
	for bombe in range(10):
		bombe_aleatoire()
	# boucle principale
	jouer = True
	texte(110, 125, 'appuyer sur une touche pour commencer', taille = 15,)
	mise_a_jour()
	attend_ev()
	nb =0
	while jouer:
	# affichage des objets
		efface_tout()
		rectangle(0, 0, 600, 450, couleur = 'black', remplissage = 'pink')# arriere plan
		affiche_pommes(pommes)
		affiche_serpent(serpent)# à modifier !
		affiche_bombes(bombes)
		texte(500, 0, 'SCORE :', couleur = 'black', ancrage = 'nw', taille = 10)
		texte(560, 0, [len(serpent)-1], couleur = 'black', ancrage = 'nw', taille = 10 )# compteur pour le score
		mise_a_jour()
	# gestion des événements
		ev = donne_ev()
		ty = type_ev(ev)
		if ty == 'Quitte':
			jouer = False
		elif ty == 'Touche':
			print(touche(ev))
			direction = change_direction(direction, touche(ev))
		if deplacement_serpent(serpent, direction) == False:
			jouer = False# si deplacement_serpent = False le jeu s'arrete
			texte(300, 225, 'PERDU', couleur = 'black', ancrage = 'center', taille = 20)# affiche 'perdu' si le joueur perd la partie
		if nb == 100:
			pomme_aleatoire()
			nb=0
		nb +=1
	# attente avant rafraîchissement
		sleep(1/framerate)
	# fermeture et sortie
	attend_ev()
	ferme_fenetre()
