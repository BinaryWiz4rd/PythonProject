import kivy #Zosia wlacz samo to i zobacz czy w tych [] nie ma ERROR
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#MOZEMY ZOSTAWIC JAK JEST ze pierwsze co sie pokazuje to wlasnie to i user moze wpisac parametry i
#dopiero jak wpisze to updatuje sie ten graph i on bedzie nowym oknem, zeby sobie nie utrudniac

#App oznacza ze biore wszystkie mozliwosci Kivy i wsadzam je do mojej klasy
#nie potrzebujemy __init__ bo ten App nam sam by default tworzy constructor
class MyGrid(GridLayout):
    #kwards is keywards
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs) #konstruktor grida
        self.cols = 1
        #self.cols = 2 #ile kolumn robimy w gridzie, polecam wpisac rozne i zoabczyc jak to dziala, bo dziala inaczej niz
        #wszedzie indziej

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Name"))
        self.name = TextInput(multiline=False) #tu user moze pisac
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Last Name"))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Weight"))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        print("Pressed") #pokaze nam w terminalu informacje ze pressed

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()