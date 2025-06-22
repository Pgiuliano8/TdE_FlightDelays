import copy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

        self.bestPath = []
        self.bestScore = 0

    def buildGraph(self, n):
        nodes = DAO.getNodes(n)
        for node in nodes:
            self._idMap[node.ID] = node
        self._graph.add_nodes_from(nodes)
        edges = DAO.getEdges(self._idMap)
        for a in edges:
            if self._graph.has_edge(a.a1, a.a2):
                self._graph[a.a1][a.a2]["weight"] += a.peso
            else:
                self._graph.add_edge(a.a1, a.a2, weight=a.peso)

    def getNodes(self):
        return list(self._graph.nodes())

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAreoportiConnessi(self, airport):
        res = []
        neighbors = self._graph.neighbors(airport)
        for n in neighbors:
            res.append((n, self._graph[n][airport]["weight"]))
        return sorted(res, key = lambda x: x[1], reverse = True)

    def cammino_ottimo(self, start, end, maxArchi):
        self.bestPath = []
        self.bestScore = 0

        self.ricorsione([start], end, maxArchi)

        return self.bestPath, self.bestScore

    def ricorsione(self, parziale, end, maxArchi):
        if parziale[-1] == end:
            score = self.calcola_score(parziale)
            if score > self.bestScore:
                self.bestScore = score
                self.bestPath = copy.deepcopy(parziale)

        if len(parziale) == maxArchi+1:
            return

        for vicino in self._graph.neighbors(parziale[-1]):
            if vicino not in parziale:  # evita cicli
                parziale.append(vicino)
                self.ricorsione(parziale, end, maxArchi)
                parziale.pop()

    def calcola_score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score




