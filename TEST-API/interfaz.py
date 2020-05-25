import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.config import Config
Config.set('graphics', 'width', '680')
Config.set('graphics', 'height', '960')

class Contenedor(BoxLayout):
    None

class Menu(GridLayout):
    None

class PanelMaquina(BoxLayout):
    None
class PanelApi(BoxLayout):
    None

class Interfaz(App):
    def build(self):
        return Contenedor()
        return Menu()



if __name__=='__main__':
    Interfaz().run()
