import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()

    def getCountries(self):
        return DAO.getCountries()

    def getClienteById(self, customerId):
        for c in self._grafo.nodes:
            if str(c.CustomerId) == str(customerId):
                return c
        return None
    def fillClienti(self):
        return list(self._grafo.nodes)

    def buildGraph(self,country):
        self._grafo.clear()
        nodi = []
        for c in DAO.getNodes(country):
            nodi.append(c)
        self._grafo.add_nodes_from(nodi)
        fatturato = DAO.getFatturato(country)  # conviene avere già il dizionario
        for c in nodi:
            c.fatturatoTotale = fatturato.get(c.CustomerId,0.0)

        self.addEdges_con_query(country)
        # se nel DAO avessi restituito le tuple (CustomerId, fatturato)
        #fatturatoList = DAO.getFatturato(country)  # lista di tuple
        #fatturatoMap = {}
        #for tupla in fatturatoList:
         #   fatturatoMap[tupla[0]] = tupla[1]

        #for c in nodi:
         #   c.fatturatoTotale = fatturatoMap.get(c.CustomerId, 0.0)


    def addEdges_con_query(self,country):
        coppie = DAO.getCoppie(country)
        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i+1, len(nodi)):
                cliente1 = nodi[i]
                cliente2 = nodi[j]
                for  c1, c2 in coppie:
                    if (cliente1.CustomerId == c1 and cliente2.CustomerId == c2) or (cliente2.CustomerId == c1 and cliente1.CustomerId == c2):
                        fatturato1 = cliente1.fatturatoTotale
                        fatturato2 = cliente2.fatturatoTotale
                        if fatturato1 > fatturato2:
                            self._grafo.add_edge(cliente1, cliente2, weight=fatturato2+fatturato1)
                        elif fatturato1 < fatturato2:
                            self._grafo.add_edge(cliente2, cliente1, weight=fatturato1 + fatturato2)
                        else:
                            self._grafo.add_edge(cliente1, cliente2, weight=fatturato1 + fatturato2)
                            self._grafo.add_edge(cliente2, cliente1, weight=fatturato1 + fatturato2)

    # ========= LOGICA IN PYTHON PER AGGIUNGERE ARCHI CON PESI ===============
    def addEdges_con_pyhton(self, country):
        righe = DAO.getArtistiPerCliente(country)

        # costruisco mappa CustomerId -> set di ArtistId
        mappaArtisti = {}
        for customerId, artistId in righe:
            if customerId not in mappaArtisti:
                mappaArtisti[customerId] = set()
            mappaArtisti[customerId].add(artistId)

        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):
                cliente1 = nodi[i]
                cliente2 = nodi[j]

                artisti1 = mappaArtisti.get(cliente1.CustomerId, set())
                artisti2 = mappaArtisti.get(cliente2.CustomerId, set())

                if len(artisti1 & artisti2) > 0:  # intersezione non vuota
                    fatturato1 = cliente1.fatturatoTotale
                    fatturato2 = cliente2.fatturatoTotale

                    if fatturato1 > fatturato2:
                        self._grafo.add_edge(cliente1, cliente2, weight=fatturato1 + fatturato2)
                    elif fatturato1 < fatturato2:
                        self._grafo.add_edge(cliente2, cliente1, weight=fatturato1 + fatturato2)
                    else:
                        self._grafo.add_edge(cliente1, cliente2, weight=fatturato1 + fatturato2)
                        self._grafo.add_edge(cliente2, cliente1, weight=fatturato1 + fatturato2)

# ===========================================================

    def getPiuInfluente(self):
        res=[]
        for c in self._grafo.nodes:
            pesoUscenti= 0
            pesoEntranti=0
            for u,v ,data in self._grafo.out_edges(c,data=True):
                pesoUscenti += data["weight"]
            for u,v ,data in self._grafo.in_edges(c,data=True):
                pesoEntranti += data["weight"]
            res.append((c, pesoUscenti-pesoEntranti))
        res.sort(key=lambda x: x[1], reverse=True)

        lista=[]
        for u,v,data in self._grafo.edges(data=True):
            lista.append((u,v,data["weight"]))
        lista.sort(key=lambda x: x[2], reverse=True)
        return res[0], lista[:5]

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getNumNodi(self):
        return len(self._grafo.nodes)


    # =============== RICORSIONE =========================
    # Cammino semplice di lunghezza massima a partire da un nodo iniziale
    # fatturato decrescente
    # un nodo può essere visitato solo una volta !! (cammino semplice)
    def bestPath(self,nodoStart):
        self._bestPath = []
        self._ricorsione(nodoStart, [nodoStart], nodoStart.fatturatoTotale)

        return self._bestPath
    def _ricorsione(self,nodoCorrente, parziale, ultimoFatturato ):
        if len(parziale) >len(self._bestPath):
            self._bestPath = list(parziale)

        for c in self._grafo.successors(nodoCorrente):
            if c not in parziale:
                if c.fatturatoTotale <= ultimoFatturato:
                    parziale.append(c)
                    self._ricorsione(c, parziale, c.fatturatoTotale)
                    parziale.pop()

