from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout


class Container(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run()