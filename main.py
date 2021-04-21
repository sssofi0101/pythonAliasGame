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
            self.manager.current = 'thirdscreen'
        except:
            screen.label.text = 'Ошибка!!! \nВведите количество команд'


names=[]
current_team=1
class TeamsNamesScreen(Screen):
    def get_names(self):
        global current_team
        if (self.input_text.text == ''):
            self.number_of_team.text = 'Ошибка!!! \nВведите название команды'
        else:
            names.append(self.input_text.text)
            if (current_team <teams_count):
                current_team=current_team+1
                self.number_of_team.text = str(current_team)
                self.input_text.text = ''
            else:self.manager.current='fourthscreen'

seconds_on_tour=0
tours_count=0
class GameSettingsScreen(Screen):
    def get_settings(self):
        global seconds_on_tour
        global tours_count
        if (self.input_time.text == ''):
            self.label1.text = 'Ошибка!!! \nВведите количество времени на игрока'
        else:
            try:
                seconds_on_tour=int(self.input_time.text)
                self.label1.text='Введите количество времени на игрока'
            except:self.label1.text = 'Ошибка!!! Введите целое число\nВведите количество времени на игрока'
            if self.input_tours.text == '':
                self.label2.text = 'Ошибка!!! \nВведите количество туров\n(1 тур - игра всех игроков в командах)'
            else:
                try:
                    tours_count= int(self.input_tours.text)
                    self.label2.text = 'Введите количество туров\n(1 тур - игра всех игроков в командах)'
                except:
                    self.label2.text = 'Ошибка!!! Введите целое число\nВведите количество туров\n(1 тур - игра всех игроков в командах)'
        if not(seconds_on_tour==0)and(not(tours_count==0)):
            self.manager.current = 'fifthscreen'



class GameScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HelloScreen(name='firstscreen'))
        sm.add_widget(CountTeamsScreen(name='secondscreen'))
        sm.add_widget(TeamsNamesScreen(name='thirdscreen'))
        sm.add_widget(GameSettingsScreen(name='fourthscreen'))
        sm.add_widget(GameScreen(name='fifthscreen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
