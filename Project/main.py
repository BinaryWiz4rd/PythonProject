import kivy #Zosia wlacz samo to i zobacz czy w tych [] nie ma ERROR
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib.pyplot as plt
#MOZEMY ZOSTAWIC JAK JEST ze pierwsze co sie pokazuje to wlasnie to i user moze wpisac parametry i
#dopiero jak wpisze to updatuje sie ten graph i on bedzie nowym oknem, zeby sobie nie utrudniac

#App oznacza ze biore wszystkie mozliwosci Kivy i wsadzam je do mojej klasy
#nie potrzebujemy __init__ bo ten App nam sam by default tworzy constructor

class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.grid = MyGrid()
        self.add_widget(self.grid)

class MyGrid(GridLayout):
    # konstruktor grida
    def __init__(self, **kwargs): #kwards is keywards
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        #self.cols = 2 #ile kolumn robimy w gridzie, polecam wpisac rozne i zoabczyc jak to dziala, bo dziala inaczej niz
        #wszedzie indziej

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Name"))
        self.name_input = TextInput(multiline=False) #tu user moze cos wpisac
        self.inside.add_widget(self.name_input)

        self.inside.add_widget(Label(text="Last Name"))
        self.last_name_input = TextInput(multiline=False)
        self.inside.add_widget(self.last_name_input)

        self.inside.add_widget(Label(text="Weight"))
        self.weight_input = TextInput(multiline=False)
        self.inside.add_widget(self.weight_input)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        try:
            weight = float(self.weight_input.text)  #daj output wagi
            screen_manager = self.parent.parent
            screen_manager.current = 'second'  #idz do drugiego okna
            screen_manager.get_screen('second').display_graph(weight)  #daj info o wadze do drugiego okieneczka
        except ValueError:
            print("enter valid weight pls man")

class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)

    def display_graph(self, weight):
        plt.figure(figsize=(5, 5))
        plt.title("Weight Input")
        plt.bar(["Weight"], [weight], color='blue')
        plt.ylabel("Weight (kg)")
        plt.ylim(0, max(weight + 10, 10))  #ustawiam limit y-axis
        plt.show()

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.add_widget(MainWindow(name='main'))
        self.add_widget(SecondWindow(name='second'))

class MyApp(App):
    def build(self):
        return WindowManager()

if __name__ == "__main__":
    MyApp().run()