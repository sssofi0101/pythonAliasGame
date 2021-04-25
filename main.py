from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.clock import Clock
from functools import partial
import random
Config.set('kivy','keyboard_mode','systemanddock')


class HelloScreen(Screen):
    pass

teams_count=0
scores=[]
class CountTeamsScreen(Screen):
    def get_teams_count(self):
        screen = self.manager.get_screen('secondscreen')
        try:
            global teams_count
            teams_count=int(screen.input2.text)
            s=0
            while s<teams_count:
                scores.append(0)
                s=s+1
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
counter=0
class GameSettingsScreen(Screen):
    def get_settings(self):
        global seconds_on_tour
        global tours_count
        if (self.input_time.text == ''):
            self.label1.text = 'Ошибка!!! \nВведите количество времени на игрока'
        else:
            try:
                seconds_on_tour=int(self.input_time.text)
                global counter
                counter = seconds_on_tour
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


i=0
j=1
prev_i=0
f = open('words.txt',encoding='utf8')
lines=f.readlines()
dictionary=lines[0].split('\u2028')
f.close()
class GameScreen(Screen):
    def my_callback(screen,dt):
        global counter
        global seconds_on_tour
        if counter>0:
            counter = counter - 1
            screen.ids.timer.text = str(counter)
        else:
            screen.ids.skip_button.disabled=True
            screen.ids.right_button.disabled = True
            screen.ids.next_button.disabled = False

    def go_next(self):
        global i
        global counter
        global j
        global prev_i
        global tours_count
        global teams_count
        if j>tours_count:
            self.manager.current = 'sixthscreen'
            return
        self.team_name.text = names[i]
        prev_i=i
        if (i==0)and (j==1):
            Clock.schedule_interval(partial(GameScreen.my_callback,self), 1)
        if (i+1==teams_count):
            if (j<=tours_count):
                j=j+1
                i=0
        else:
            i = i + 1
        self.next_button.disabled = True
        self.right_button.disabled = False
        self.skip_button.disabled = False
        global seconds_on_tour
        counter=seconds_on_tour
        self.timer.text = str(counter)
        global dictionary
        word=random.choice(dictionary)
        self.word.text=word
        dictionary.remove(word)

    def right_answer(self):
        global scores
        scores[prev_i]=scores[prev_i]+1
        global dictionary
        word = random.choice(dictionary)
        self.word.text = word
        dictionary.remove(word)

    def skip(self):
        global dictionary
        word = random.choice(dictionary)
        self.word.text = word
        dictionary.remove(word)


class ScoreScreen(Screen):
    def raiting(self):
        d={}
        global names
        global scores
        for c in range(len(names)):
            d[names[c]]=scores[c]
        sorted_scores=sorted(d.values(), reverse=True)
        sorted_dict={}
        for j in sorted_scores:
            for k in d.keys():
                if (d[k]==j):
                    sorted_dict[k]=d[k]
        for t in sorted_dict.keys():
            self.teams.text=self.teams.text+'\n\n'+str(t)
        for s in sorted_dict.values():
           self.scores.text=self.scores.text+'\n\n'+str(s)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HelloScreen(name='firstscreen'))
        sm.add_widget(CountTeamsScreen(name='secondscreen'))
        sm.add_widget(TeamsNamesScreen(name='thirdscreen'))
        sm.add_widget(GameSettingsScreen(name='fourthscreen'))
        sm.add_widget(GameScreen(name='fifthscreen'))
        sm.add_widget(ScoreScreen(name='sixthscreen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
