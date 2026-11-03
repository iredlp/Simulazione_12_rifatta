import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # grafo semplice
        self._idMapA = {}

    def getAllVoti(self):
        self._voti = DAO.getAllRange()
        return self._voti

    def creaGrafo(self, voto1, voto2):
        self._grafo.clear()
        self._idMapA.clear()

        attori = DAO.getAllNodes(voto1, voto2)
        for a in  attori:
            self._idMapA[a.id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in   attori:
            a. list_film.clear()
           # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a. list_film = DAO. getFilmPerAttori(a.id, voto1, voto2)
           # a.popolarita = DAO.getPopolarita(a.ArtistId)
        print("3 - Informazioni recuperate")

        for i in range(len( attori)):
            a1 =  attori[i]
            for j in range(i + 1, len( attori)):
                a2 =  attori[j]
                filmComuni = (set(a1. list_film) & set(a2.list_film ))
                peso = 0
                #ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE
                for film in filmComuni:
                    incasso=DAO.getIncassiPerFilm(film)
                    peso+=incasso[0]
                if len( filmComuni) > 0:
                   # if p1 > p2:
                    self._grafo.add_edge(a1, a2, weight=peso)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getTop5Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(archi,
            key=lambda x: (-x[2]["weight"], x[0].name, x[1].name),
            reverse= False)[:5]

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        # PERCHè DEVE ESSERE DEBOLMENTE CONNESSA!!
       # components = list(nx.weakly_connected_components(self._grafo))
        if len(components) == 0:
            return [], 0, set()

        # Tengo solo le componenti con più di un nodo
        # components = [c for c in components if len(c) > 1]
        largest = max(components, key=len)
        #  pesi = {}
        # for nodo in largest:
        #  minPeso = None
        #  for vicino in self._grafo.neighbors(nodo):
        #   peso = self._grafo[nodo][vicino]["weight"]
        #   if minPeso is None or peso < minPeso:
        # []    minPeso = peso
        # pesi[nodo] = minPeso
        # ordered_nodes_pesi = sorted(largest, key=lambda n: pesi[n], reverse=True)
        # Ordino per numero di ATTORI
       # details = sorted(largest, key=lambda n: len(n.list_attori), reverse=True)
        # details = [(n, pesi[n]) for n in ordered_nodes_pesi]
        return components, len(components), largest #, details

    def getCammino(self):
        self._best_path = []
        self._best_score = float("-inf")

        for nodo in self._grafo.nodes:
            parziale = [nodo]
            self._ricorsione(parziale, 0)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale, score):
        ultimo = parziale[-1]

        # Controllo se il cammino attuale è migliore
        if len(parziale) > len(self._best_path):
            self._best_path = list(parziale)
            self._best_score = score

        # Esploro i vicini
        for vicino in self._grafo.neighbors(ultimo):

            # Non posso visitare due volte lo stesso nodo
            if vicino not in parziale:

                # L'età deve essere strettamente decrescente
                if (ultimo.date_of_birth is not None
                        and vicino.date_of_birth is not None
                        and vicino.date_of_birth > ultimo.date_of_birth):
                    # Aggiungo il vicino
                    parziale.append(vicino)

                    # Continuo la ricorsione
                    self._ricorsione(parziale, score + 1)

                    # Backtracking
                    parziale.pop()