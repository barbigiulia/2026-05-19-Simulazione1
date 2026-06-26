import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        res = []
        for g in self._model.getGeneri():
            res.append(ft.dropdown.Option(text=g[1],
                                          key= g[0] ))
        return res


    def handleCreaGrafo(self, e):
        genereID = self._view._ddGenre.value

        if genereID is None :
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere", color="red"))
            self._view.update_page()
            return
        try:
            genreID = int(genereID)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Genere non valido nel database", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(genreID)
        self._view._ddArtist.options = self.getArtist(genereID)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        tupla = self._model.getMaggioreInfluenza()
        self._view.txt_result.controls.append(ft.Text(f"Artista con maggiore influenza: {tupla[0].Name} con influenza: {tupla[1]}", color="purple"))
        for arco in self._model.archiPesati():
            self._view.txt_result.controls.append(
                ft.Text(f"{arco[0]} -> {arco[1]}    peso: {arco[2]}", color="purple"))

        self._view.update_page()

    def getArtist(self,genereID):
        res=[]
        for a in self._model.getArtisti(genereID):
            res.append(ft.dropdown.Option(text=a.Name, key= a.ArtistId))
        return res


    def handleCammino(self,e):
        self._view.txt_result.clean()
        artistaID = self._view._ddArtist.value
        if artistaID is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un artista", color="red"))
            self._view.update_page()
            return

        path = self._model.trovaCammino(int(artistaID))
        self._view.txt_result.controls.append(ft.Text(f"Cammino semplice di lunghezza massima", color="orange"))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(f"--> {n}", color="orange"))
        self._view.update_page()
