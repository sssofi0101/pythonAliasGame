from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class HelloScreen(Screen):
    pass


class CountTeamsScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HelloScreen(name='firstscreen'))
        sm.add_widget(CountTeamsScreen(name='secondscreen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
