import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        voti = self._model.getAllVoti()

        for g in voti:
            g_str = str(g)
            # self._view._ddGenre.options.append( g_str)
            self._view._ddrating1.options.append(ft.dropdown.Option(key=g_str, text=g_str))
            self._view._ddrating2.options.append(ft.dropdown.Option(key=g_str, text=g_str))

        self._view.update_page()

    def handleCreaGrafo(self, e):
        voto1 = self._view._ddrating1.value
        voto2 = self._view._ddrating2.value

        if not voto1 or not voto2:
            self._view.create_alert("Selezionare entrambe i VOTI prima di creare il grafo.", color="red")
            return
        # try:
        # v1 = float(self._view._txtRatingMin.value.replace(",", "."))
        # v2 = float(self._view._txtRatingMax.value.replace(",", "."))
        # except (ValueError, AttributeError):
        # self._view.create_alert("Inserisci due valori numerici validi per la valutazione.")
        # return
        # v1 = self._view._txtRatingMin.value
        # v2 = self._view._txtRatingMax.value

        try:
            self._model.creaGrafo(voto1, voto2)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
        # self.fillDDRegisti(data1, data2)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return

        top5 = self._model.getTop5Archi()
        self._view._txt_result.controls.append(ft.Text(f"Archi di peso maggiore", color="green"))

        for i, arco in enumerate(top5, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append(ft.Text(
                f"{i})  {a1.name}  ({a1.id}) -- {a2.name}  ({a2.id} )"
                f"(peso: {dati['weight']})")
            )

        components, numero, largest = self._model.getConnessaInfo()

        self._view._txt_result.controls.append(
            ft.Text(f"Numero componenti debolmente connesse: {numero}"))

        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione componente maggiore: {len(largest)}"))

        self._view._txt_result.controls.append(
            ft.Text("Nodi della componente maggiore:"))

        for nodo in largest:
            self._view._txt_result.controls.append(
                ft.Text(f"Attore: {nodo.name} "))

        self._view.update_page()

    def handleCammino(self, e):
        self._view._txt_result.controls.clear()
        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return
        percorso, lunghezza = self._model.getCammino()

        self._view._txt_result.controls.append(
            ft.Text(f"Lunghezza cammino: {lunghezza}")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero nodi: {len(percorso)}")
        )

        self._view._txt_result.controls.append(
            ft.Text("Percorso trovato:")
        )

        for nodo in percorso:
            self._view._txt_result.controls.append(
                ft.Text(f"{nodo.name} - Data di nascita: {nodo.date_of_birth}")
            )

        self._view.update_page()