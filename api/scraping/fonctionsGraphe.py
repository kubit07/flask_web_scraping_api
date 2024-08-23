import networkx as nx
import json
import matplotlib.pyplot as plt

"""Sauvegarde du graphe dans un fichier json

Args:
  graphe: Le graphe à sauvegarder.
  name: Le nom du fichier json dans lequel on sauvegarde le graphe.
"""
def saveGraph(graphe, name):
    s1 = json.dumps(graphe, default=nx.node_link_data)
    with open(name, "w") as outfile:
        outfile.write(s1)

"""Charge le graphe à partir d'un fichier json

Args:
  name: Le nom du fichier json contenant le graphe.

Returns:
  Le graphe contenu dans le fichier json.
"""
def loadGraph(name):
    with open(name, "r") as json_file:
        data = json.load(json_file)
    return nx.node_link_graph(data)

"""
Affiche le graphe passé en paramètre, avec la valeur de l'attribut 'recompense' sur les liens.

Args:
  graphe (networkx.Graph): Le graphe à afficher
"""
def afficherGraphe(graphe):
  pos=nx.spring_layout(graphe,seed=42)
  nx.draw(graphe, pos=pos, with_labels=True,connectionstyle='arc3, rad = 0.1')
  lab = {(v,w):round(graphe.edges[v,w]['recompense'],3) for (v,w) in graphe.edges}
  nx.draw_networkx_edge_labels(graphe, pos=pos, edge_labels=lab, label_pos=0.3,font_size=7)
  plt.show()

"""
Parcours le graphe en largeur à partir du noeud de destination.

Args:
  graphe (networkx.Graph): Le graphe à parcourir
  destination: Le noeud de départ du parcours, il correspond à la destination pour laquelle on souhaite obtenir le chemin optimal grâce à l'algorithme par renforcement.

Returns: 
  La liste des noeuds parcourus
"""
def parcoursLargeurGraphe(graphe, destination):
  #edges = nx.bfs_edges(graphe, destination, reverse=True)
  edges = nx.edge_bfs(graphe, destination,orientation='reverse')
  parcours = [u for u, _, _ in edges]
  return parcours

"""Initialisation des attributs 'temps' et'recompense' pour chaque arête du graphe.

L'attribut 'temps' correspond à la durée estimée de parcours de l'arête et est calculé
à partir de la longueur de l'arête, de la vitesse de la voiture et de la densité de voitures sur l'arête.
L'attribut 'récompense' correspond à l'inverse de l'attribut 'temps'.

Args:
  graphe (networkx.Graph): Le graphe dont on veut initialiser les attributs 'temps' et'recompense'.
"""
def initTempsRecompense(graphe):
  for e in graphe.edges:
    longueur = graphe.edges[e]['longueur']
    vitesse = graphe.edges[e]['vitesse']
    densite = graphe.edges[e]['nb_voitures'] / longueur
    if densite > 200:
      densite = 200
    graphe.edges[e]['temps'] = longueur / (vitesse-0.80*vitesse*(densite/200))
    graphe.edges[e]['recompense'] = - graphe.edges[e]['temps']

"""
Retourne la valeur maximale de l'attribut 'recompense' des liens entre le noeud passé en paramètre et ses voisins.

Args:
  graphe (networkx.Graph): Le graphe associé au noeud passé en paramètre.
  noeud: Le noeud dont on veut trouver la valeur maximale de l'attribut 'recompense'.

Returns:
  Un tuple contenant la valeur maximale de l'attribut'recompense' des liens entre le noeud passé en paramètre et ses voisins,
  ainsi que le noeud voisin associé à cette valeur.
"""
def getMaxRecompense(graphe, noeud):
  voisins = nx.neighbors(graphe,noeud)
  reward = None
  for v in voisins:
    r = graphe.edges[noeud, v]['recompense']
    if reward == None:
      reward = (v,r)
    else:
      if reward[1] < r:
        reward = (v,r)
  return reward

"""
Propage une nouvelle récompense dans le graphe en suivant le parcours en largeur du graphe.
Met à jour les attributs 'future_recompense' et 'recompense' des liens du graphe.

Args:
  start: Le noeud pour lequel le lien a une nouvelle récompense
  graphe: Le graphe.
  parcours: Le parcours en largeur du graphe.
  dest: Le noeud de destination de l'algorithme par renforcement.
  y: Le paramètre lambda de l'apprentissage par renforcement, par défaut 0.9. Il doit être compris entre 0 et 1.
"""
def propagationNouvelleRecompense(start, graphe, parcours, dest, y=0.9):
  assert 0 <= y <= 1, "y doit être compris entre 0 et 1"
  #on initialise la recompense obtenue lors de l'arrivée à la destination
  list_temps = [graphe.edges[v1,v2]['temps'] for (v1,v2) in graphe.edges]
  recompense_destination = sum(list_temps) #somme des temps des liens du graphe
  #choix de la ville pour laquelle on va commencer la maj
  if start != dest: # si on ne fait la maj que d'une sous partie du graphe
    ind = parcours.index(start) + 1 #on regarde le prochain noeud après celui du lien qui a été modifié
  else:#si on fait la maj de tout le graphe
    ind = 0
  for n in range(ind, len(parcours)): #on visite les noeuds dans l'ordre du parcours en largeur pour changer leur récompenses
    noeud = parcours[n]
    voisins = nx.neighbors(graphe,noeud)
    for v in voisins:
      lien = graphe.edges[noeud,v]
      if v == dest:
        #si c'est un lien qui permet d'atteindre la destination il ne faut pas regarder la récompense futur
        #on attribue une récompense fixée pour avoir atteint la destination
        lien['futur_recompense'] = recompense_destination
      else: #sinon on regarde la récompense maximale qui pourra être obtenu après
        futurMaxReward = getMaxRecompense(graphe,v)
        lien['futur_recompense'] = futurMaxReward[1]
      lien['recompense'] = - lien['temps'] + y * lien['futur_recompense']


"""
Retourne le chemin optimal entre le départ et la destination.

Args:
  depart (str): Le noeud de départ.
  destination (str): La destination.
  graphe (networkx.Graph): Le graphe contenant le noeud de départ et la destination.

Returns:
  dict: Dictionnaire contenant le trajet optimal sous forme de liste, le temps de parcours en minutes et 
  le total des récompenses obtenues.
"""
def getCheminOptimal(depart, destination, graphe):
  trajet = [depart]
  total_recompense = 0
  temps = 0
  courant = trajet[-1]
  while courant != destination:
    prochain = getMaxRecompense(graphe,courant)
    trajet.append(prochain[0])
    total_recompense += prochain[1]
    temps += graphe.edges[courant,prochain[0]]["temps"]
    courant = prochain[0]
  return {"trajet":trajet, "temps":temps,"recompense":total_recompense}