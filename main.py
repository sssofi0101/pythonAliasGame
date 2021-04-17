from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
Config.set('kivy','keyboard_mode','systemanddock')


class HelloScreen(Screen):
    pass

teams_count=0
class CountTeamsScreen(Screen):
    def get_teams_count(self):
        try:
            screen=self.manager.get_screen('secondscreen')
            global teams_count
            teams_count=int(screen.input2.text)
        except:
            teams_count= 0


names=[]
current_team=1
class TeamsNamesScreen(Screen):
    def get_names(self):
        global current_team
        if (self.input_text.text == ''):
            self.number_of_team.text = 'Ошибка!!! \n' + self.number_of_team.text
        else:
            names.append(self.input_text.text)
            if (current_team <teams_count):
                current_team=current_team+1
                self.number_of_team.text = str(current_team)
                self.input_text.text = ''
            else:self.manager.current='fourthscreen'


class GameSettingsScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HelloScreen(name='firstscreen'))
        sm.add_widget(CountTeamsScreen(name='secondscreen'))
        sm.add_widget(TeamsNamesScreen(name='thirdscreen'))
        sm.add_widget(GameSettingsScreen(name='fourthscreen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
