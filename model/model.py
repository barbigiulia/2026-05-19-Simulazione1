import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()


    def getGeneri(self):
        return DAO.getGeneri()

    def getArtisti(self, genereID):
        return DAO.getArtisti(genereID)


    def buildGraph(self,genereID):
        self._grafo.clear()
        artisti = []
        for a in DAO.getNodes(genereID):
            artisti.append(a)
        self._grafo.add_nodes_from(artisti)

        self.addEdges(genereID)

    def addEdges(self, genereID):

        acquisti = DAO.getAcquistiClienti(genereID)
        # CustomerId = set( ArtistId_1, ....)
        diz = {}
        for acq in acquisti:
            if acq[0] not in diz:
                diz[acq[0]] = set()
            diz[acq[0]].add(acq[1])


        pop = dict()
        popolarita = DAO.getPopolarita(genereID)
        for p in popolarita:
            if p[0] not in pop:
                pop[p[0]] = int(p[1])

        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i+1,len(nodi)):   # evito i duplicati con a1 < a2
                a1 = nodi[i]
                a2  = nodi[j]

                comune =False
                for c in diz.keys():
                    if a1.ArtistId in diz[c] and a2.ArtistId in diz[c]:
                        comune = True
                        break
                if comune:
                    # posso aggiungere l'arco tra gli artisti a1 e a2
                    popA1 = pop.get(a1.ArtistId, 0)
                    popA2 = pop.get(a2.ArtistId, 0)
                    peso = popA1+popA2

                    if popA1 > popA2:
                        self._grafo.add_edge(a1,a2,weight=peso)
                    elif popA2 > popA1:
                        self._grafo.add_edge(a2, a1, weight=peso)
                    else:
                        self._grafo.add_edge(a1, a2, weight=peso)
                        self._grafo.add_edge(a2, a1, weight=peso)


    def getNumNodi(self):
        return len(self._grafo.nodes)
    def getNumArchi(self):
        return len(self._grafo.edges)


    def getMaggioreInfluenza(self):
        res = []
        for a in self._grafo.nodes:
            pesoUscenti=0
            pesoEntranti=0
            for u,v,data in self._grafo.out_edges(a,data=True):
                pesoUscenti += data["weight"]
            for u,v,data in self._grafo.in_edges(a,data=True):
                pesoEntranti +=data['weight']
            res.append((a, pesoUscenti-pesoEntranti))
        res.sort(key=lambda x:x[1], reverse=True)
        return res[0]

    def archiPesati(self):
        res=[]
        for u,v, data in self._grafo.edges(data=True):
            res.append((u, v, data["weight"]))
        res.sort(key=lambda x:x[2], reverse=True)
        return res[:5]



    def trovaCammino(self, artistID):
        nodoStart = None
        for n in self._grafo.nodes:
            if n.ArtistId == artistID:
                nodoStart = n
                break
        self._bestPath = [] # il più lungo

        self._ricorsione(nodoStart, [nodoStart], 0 )
        return self._bestPath

    def _ricorsione(self, nodoStart, parziale, ultimoPeso):
        # cammino semplice = OGNI NODO è VISITATO UNA VOLTA SOLA

        if len(parziale) > len(self._bestPath):
            self._bestPath = list(parziale)

        for vicino in self._grafo.successors(nodoStart):
            if vicino not in parziale:
                peso = self._grafo[nodoStart][vicino]["weight"]
                if peso > ultimoPeso:
                    parziale.append(vicino)

                    self._ricorsione(vicino, parziale, peso)
                    parziale.pop()
