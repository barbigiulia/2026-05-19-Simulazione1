import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillCountry(self):
        res = []
        for c in self._model.getCountries():
            res.append(ft.dropdown.Option(c))
        return res

    def handleCreaGrafo(self, e):
        country = self._view._ddCountry.value
        if country is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un paese", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(country)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        # aggiorna il dropdown dei clienti ora che il grafo esiste
        self._view._ddClienti.options = self.fillClienti()
        self._view.update_page()




    def stampaInfo(self,e):
        piuInfluente, top5 = self._model.getPiuInfluente()
        country = self._view._ddCountry.value
        if country is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un paese", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Il cliente più influente è {piuInfluente[0]}:"
                                                      f" influenza pari a {piuInfluente[1]}", color="pink"))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore", color="purple"))
        for u,v,peso in top5:
            self._view.txt_result.controls.append(ft.Text(f"{u} - {v}  : peso {peso}"))
        self._view.update_page()

    def fillClienti(self):
        res =[]
        for n in self._model.fillClienti():
            res.append(ft.dropdown.Option(text=str(n), key=str(n.CustomerId)))
        return res
    def trovaSeq(self,e):
        idCliente = self._view._ddClienti.value
        if idCliente is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un cliente", color="red"))
            self._view.update_page()
            return

        nodoStart = self._model.getClienteById(idCliente)

        path = self._model.bestPath(nodoStart)
        self._view.txt_result.controls.append(ft.Text("Cammino semplice di lunghezza massima"))
        tot = 0
        for n in path:
            tot += n.fatturatoTotale
            self._view.txt_result.controls.append(ft.Text(f"--> {n}   | fatturato Totale: {n.fatturatoTotale}"))

        self._view.txt_result.controls.append(ft.Text(f"Numero archi del cammino: {len(path)}", color="blue"))
        self._view.txt_result.controls.append(ft.Text(f"Fatturato complessivo: {tot}", color="blue"))

        self._view.update_page()