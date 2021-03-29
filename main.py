from kivy.app import App
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        b = Button(text='hello')
        return b

MyApp().run()