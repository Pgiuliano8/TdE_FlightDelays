import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_nComoagnie = None
        self.btn_analizza = None
        self.dd_partenza = None
        self.btn_connessi = None
        self.dd_destinazione = None
        self.txt_nTratte = None
        self.btn_cerca = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Flights Delays", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        self.txt_nComoagnie = ft.TextField(
            label="# minimo comagnie",
            width=200,
            hint_text="Insert minimum number of companies"
        )

        self.btn_analizza = ft.ElevatedButton(text="Analizza areoporti", on_click=self._controller.handle_analizza)
        row1 = ft.Row([self.txt_nComoagnie, self.btn_analizza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self.dd_partenza = ft.Dropdown(label="Areoporto di partenza")
        self.btn_connessi = ft.ElevatedButton(text="Analizza areoporti", on_click=self._controller.handle_connessi)
        row2 = ft.Row([self.dd_partenza, self.btn_connessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.dd_destinazione = ft.Dropdown(label="Areoporto di destinazione")
        self.txt_nTratte = ft.TextField(label="# massimo tratte", width=200)
        self.btn_cerca = ft.ElevatedButton(text="Cerca percorso", on_click=self._controller.handle_cerca)
        row3 = ft.Row([self.dd_destinazione, self.txt_nTratte, self.btn_cerca],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
