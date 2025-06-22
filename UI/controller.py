import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceDDpartenza = None
        self._choiceDDarrivo = None

    def handle_analizza(self, e):
        self._view.txt_result.clean()
        n = self._view.txt_nComoagnie.value
        if n is None:
            self._view.create_alert("Inserire un numero")
            return
        try:
            n = int(n)
        except ValueError:
            self._view.create_alert("Inserire un numero")
            return

        self._model.buildGraph(n)
        self.fillDDpartenza()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.update_page()

    def handle_connessi(self, e):
        self._view.txt_result.clean()
        start = self._choiceDDpartenza
        if start is None:
            self._view.create_alert("Scegliere un areoporto")
            return
        connessi = self._model.getAreoportiConnessi(start)
        for c in connessi:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]}, {c[1]}"))
        self._view.update_page()

    def handle_cerca(self, e):
        self._view.txt_result.clean()
        start = self._choiceDDpartenza
        if start is None:
            self._view.create_alert("Scegliere un areoporto di partenza")
            return
        end = self._choiceDDarrivo
        if end is None:
            self._view.create_alert("Scegliere un areoporto di arrivo")
            return
        nTratte = self._view.txt_nTratte.value
        if nTratte is None:
            self._view.create_alert("Inserire un numero")
            return
        try:
            nTratte = int(nTratte)
        except ValueError:
            self._view.create_alert("Inserire un numero")
            return
        bestPath, bestScore = self._model.cammino_ottimo(start, end, nTratte)
        self._view.txt_result.controls.append(ft.Text(f"Il numero totale di voli disponibili sul percorso è {bestScore}"
                                                      f"\nGli areoporti visitati sono:"))
        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{a.IATA_CODE} {a.AIRPORT}\n"))
        self._view.update_page()

    def fillDDpartenza(self):
        nodi = self._model.getNodes()
        for a in nodi:
            self._view.dd_partenza.options.append(ft.dropdown.Option(text=a.IATA_CODE, data=a,
                                                                     on_click=self.readDDpartenza))
    def readDDpartenza(self, e):
        if e.control.data is None:
            print("error in reading dd")
            self._choiceDDpartenza = None
        self._choiceDDpartenza = e.control.data
        self.fillDDarrivo()

    def fillDDarrivo(self):
        nodi = self._model.getNodes()
        for a in nodi:
            if a != self._choiceDDpartenza:
                self._view.dd_destinazione.options.append(ft.dropdown.Option(text=a.IATA_CODE, data=a,
                                                                     on_click=self.readDDarrivo))
        self._view.update_page()

    def readDDarrivo(self, e):
        if e.control.data is None:
            print("error in reading dd")
            self._choiceDDarrivo = None
        self._choiceDDarrivo = e.control.data

