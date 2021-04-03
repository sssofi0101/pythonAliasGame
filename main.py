from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Rontainer(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return Rontainer()


if __name__ == '__main__':
    MyApp().run()