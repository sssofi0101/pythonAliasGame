from kivy.app import App
# Позволяет работать с окнами как с экранами, которые легко переключать.
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config  # нужно для использования клавиатуры
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
import random
Config.set('kivy', 'keyboard_mode', 'systemanddock')


# Класс, инициализирующий первое окно(экран) программы.
class HelloScreen(Screen):
    pass


teams_count = 0  # количество команд, которое указал пользователь
scores = []  # список, содержащий очки, набранные командами
tasks_game = False


# Класс, инициализирующий второе окно(экран) программы и определяющий взаимодействия с ним.
class CountTeamsScreen(Screen):
    def get_teams_count(self):
        """
        Функция для получения информации из второго окна программы, о том, сколько команд будет участвовать в игре.
        Получает количество команд, задает размер списка scores для очков, набранных командами, 
        и устанавливает их равными нулю для начала, затем переключает приложение на третий экран.
        """
        screen = self.manager.get_screen('secondscreen')
        try:
            global teams_count
            # Получаем количество команд, указанное пользователем.
            teams_count = int(screen.input2.text)
            s = 0
            while s < teams_count:
                # Добавляем в список с очками столько нулевых элементов, сколько команд.
                scores.append(0)
                s = s+1
            if screen.tasks_mode.state == 'down':
                global tasks_game
                tasks_game = True
            self.manager.current = 'thirdscreen'  # переходим на следующий экран
        except ValueError:
            screen.label.text = 'Ошибка!!! \nВведите количество команд'


names = []  # список, содержащий названия команд
current_team = 1  # текущий номер команды


# Класс, инициализирующий третье окно(экран) программы и определяющий взаимодействия с ним.
class TeamsNamesScreen(Screen):
    def get_names(self):
        """
        Функция для получения информации из третьего окна программы о названиях команд.
        Получает имена команд и добавляет их в список names, затем переключает приложение на четвертый экран.
        """
        global current_team
        if self.input_text.text == '':
            # Если пользователь не ввел название, программа укажет об ошибке.
            self.number_of_team.text = 'Ошибка!!! \nВведите название команды'
        else:
            names.append(self.input_text.text)  # добавляет названия команд в список
            if current_team < teams_count:
                current_team = current_team+1
                # Меняет команду, для которой пользователь должен указать название.
                self.number_of_team.text = str(current_team)
                self.input_text.text = ''
            else:
                self.manager.current = 'fourthscreen'  # переходим на следующий экран


seconds_on_tour = 0  # количество секунд на раунд для игрока, которое указал пользователь
tours_count = 0  # количество туров игры, которое указал пользователь
counter = 0  # счетчик для секунд во время раунда


# Класс, инициализирующий четвертое окно(экран) программы и определяющий взаимодействия с ним.
class GameSettingsScreen(Screen):
    def get_settings(self):
        """
         Функция для получения информации о количестве секунд на игрока в игре и о количестве туров
         из четвертого экрана программы.
         Получает количество секунд на игрока и количество туров и присваивает эти значения переменным
         seconds_on_tour и tours_count,
         затем переключает приложение на пятый экран.
        """
        global seconds_on_tour
        global tours_count
        # Если пользователь не ввел количество времени на игрока, программа укажет об ошибке.
        if self.input_time.text == '':
            self.label1.text = 'Ошибка!!! \nВведите количество времени на игрока'
        else:
            try:
                seconds_on_tour = int(self.input_time.text)  # получает количество секунд для игрока
                global counter
                counter = seconds_on_tour
                self.label1.text = 'Введите количество времени на игрока'
            except ValueError:
                self.label1.text = 'Ошибка!!! Введите целое число\nВведите количество времени на игрока'
            if self.input_tours.text == '':  # если пользователь не ввел количество туров, программа укажет об ошибке
                self.label2.text = 'Ошибка!!! \nВведите количество туров\n(1 тур - игра всех игроков в командах)'
            else:
                try:
                    tours_count = int(self.input_tours.text)  # получает количество туров для игры
                    self.label2.text = 'Введите количество туров\n(1 тур - игра всех игроков в командах)'
                except ValueError:
                    self.label2.text = \
                        'Ошибка!!! Введите целое число\nВведите количество туров\n' \
                        '(1 тур - игра всех игроков в командах)'
        if not(seconds_on_tour == 0) and (not(tours_count == 0)):
            self.manager.current = 'fifthscreen'  # переходим на следующий экран


i = 0  # счетчик для команд
j = 1  # счетчик для туров
prev_i = 0  # номер предыдущей игравшей команды
f = open('words.txt', encoding='utf8')  # открываем файл с набором слов для игры
lines = f.readlines()
dictionary = lines[0].split('\u2028')
f.close()
f2 = open('tasks.txt', encoding='utf8')  # открываем файл с набором заданий для игры
lines2 = f2.readlines()
tasks = lines2[0].split('\u2029')
f2.close()


# Класс, инициализирующий пятое окно(экран) программы и определяющий взаимодействия с ним.
class GameScreen(Screen):
    def my_callback(screen, dt):
        """
        Функция в пятом экране программы для определения поведения таймера.
        """
        global counter
        global seconds_on_tour
        if counter > 0:
            counter = counter - 1  # обратный отсчет таймера
            screen.ids.timer.text = str(counter)
        else:
            screen.ids.skip_button.disabled = True
            screen.ids.right_button.disabled = True
            screen.ids.next_button.disabled = False

    def my_popup(self):
        """
        Функция для определения поведения и внешнего вида всплывающих окон.
        """
        global tasks
        word = random.choice(tasks)
        popup = Popup(title='Задание',
                      content=Label(text=word, text_size=(200, None), shorten_from='right'),
                      size_hint=(0.8, 0.7),
                      separator_color=[0.96, 0.56, 0, 1],
                      title_color=[0.36, 0.54, 0.66, 1])

        def my_callback2(instance):
            """
            Функция  для определения поведения всплывающего окна при его закрытии.
            """
            view = ModalView()
            view.dismiss(force=True)
            self.logic()
            return False

        popup.bind(on_dismiss=my_callback2)
        popup.open()

    def logic(self):
        """
        Функция для продолжения игры в пятом экране программы.
        Осуществляет переход к следующему игроку, следующему туру или перехода на следующий, шестой, экран
        в зависимости от хода игры, также запускает таймер и выводит слова для игры на экран.
        """
        global i
        global counter
        global j
        global prev_i
        global tours_count
        global teams_count
        self.team_name.text = names[i]
        prev_i = i
        if (i == 0) and (j == 1):
            Clock.schedule_interval(partial(GameScreen.my_callback, self), 1)
        # Если номер команды последний, а тур не последний, то переходим снова к первой команде и следующему туру.
        if i+1 == teams_count:
            if j <= tours_count:
                j = j+1
                i = 0
        else:
            i = i + 1
        self.next_button.disabled = True
        self.right_button.disabled = False
        self.skip_button.disabled = False
        global seconds_on_tour
        counter = seconds_on_tour
        self.timer.text = str(counter)
        global dictionary
        word = random.choice(dictionary)
        self.word.text = word  # вывод случайного слова из набора для игры на экран программы для пользователя
        dictionary.remove(word)  # удаляем уже использованное слово из набора

    def go_next(self):
        """
         Функция для продолжения игры в пятом экране программы.
         Запускает игру с заданиями или без них в зависимости от выбранного пользователем режима.
        """
        global i
        global counter
        global j
        global prev_i
        global tours_count
        global teams_count
        if j > tours_count:  # если номер текущего тура больше общего количества туров
            self.manager.current = 'sixthscreen'  # переходим на следующий экран
            return
        global tasks_game
        if tasks_game is True:
            self.my_popup()
        else:
            self.logic()

    def right_answer(self):
        """
        Функция для обозначения правильного ответа пользователем в пятом окне программы.
        Добавляет одно очко команде, меняет выведенное на экран слово для игры.
        """
        global scores
        scores[prev_i] = scores[prev_i]+1  # добавляет одно очко команде
        global dictionary
        word = random.choice(dictionary)
        self.word.text = word  # вывод случайного слова из набора для игры на экран программы для пользователя
        dictionary.remove(word)  # удаляем уже использованное слово из набора

    def skip(self):
        """
        Функция для пропуска слова в пятом экране программы. Меняет выведенное на экран слово для игры.
        """
        global dictionary
        word = random.choice(dictionary)
        self.word.text = word  # вывод случайного слова из набора для игры на экран программы для пользователя
        dictionary.remove(word)  # удаляем уже использованное слово из набора


# Класс, инициализирующий шестое окно(экран) программы и определяющий взаимодействия с ним.
class ScoreScreen(Screen):
    def rating(self):
        """
        Функция для вывода рейтинга в шестом окне.
        """
        d = {}
        global names
        global scores
        for c in range(len(names)):
            d[names[c]] = scores[c]
        sorted_scores = sorted(d.values(), reverse=True)
        sorted_dict = {}
        for o in sorted_scores:
            for k in d.keys():
                if d[k] == o:
                    sorted_dict[k] = d[k]  # сортирует команды по набранным очкам
        for t in sorted_dict.keys():
            self.teams.text = self.teams.text+'\n\n'+str(t)  # выводит отсортированный по убыванию очков порядок команд
        for s in sorted_dict.values():
            # Выводит отсортированный по убыванию очки для команд в соседней колонке.
            self.scores.text = self.scores.text+'\n\n'+str(s)


class MyApp(App):  # класс, инициализирующий приложение.
    def build(self):
        """
        Функция, собирающая приложение и добавляющая к нему экраны.
        """
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
