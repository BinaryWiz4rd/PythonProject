from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog

#trza wykminic czemu po odpaleniu apki nazywa sie ona "My"

class MainWindow(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        self.title_label = MDLabel(
            text="[b]Pick a genre of questions[/b]",
            markup=True,
            halign="center",
            size_hint_y=None,
            height=100,
            font_style="H5",
        )
        self.layout.add_widget(self.title_label)

        button_layout = MDBoxLayout(orientation="horizontal", padding=20, spacing=20)

        self.general_button = MDIconButton(
            icon="account",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.698, 0.329)
        )

        self.heart_button = MDIconButton(
            icon="heart",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.639, 0.114, 0.114)
        )

        self.diabetes_button = MDIconButton(
            icon="medical-bag",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.804, 1)
        )

        self.general_button.bind(on_press=lambda _: self.show_questions("General"))
        self.heart_button.bind(on_press=lambda _: self.show_questions("Heart"))
        self.diabetes_button.bind(on_press=lambda _: self.show_questions("Diabetes"))

        button_layout.add_widget(self.general_button)
        button_layout.add_widget(self.heart_button)
        button_layout.add_widget(self.diabetes_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def create_icon_button(self, icon, color):
        return MDIconButton(
            icon=icon,
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=color,
        )

    def show_questions(self, category):
        self.manager.current = "questions"
        self.manager.get_screen("questions").set_category(category)


class QuestionsWindow(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        self.add_widget(self.layout)

        self.title_label = MDLabel(
            text="Answer the following questions:", halign="center", font_style="H5"
        )
        self.layout.add_widget(self.title_label)

        self.submit_button = self.create_action_button("Submit Answers", self.submit_answers)
        self.return_button = self.create_action_button("Return", self.return_to_main)

    def create_action_button(self, text, callback):
        button = MDRectangleFlatButton(
            text=text, size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5}
        )
        button.bind(on_press=callback)
        return button

    def set_category(self, category):
        self.layout.clear_widgets()
        self.layout.add_widget(self.title_label)

#tu spoko byloby przeorganizowac te pytania, bo ostatnie w sumie malo diabetyczne jest a raczej genetyczne
        categories = {
            "General": [
                "What is your gender?",
                "What is your age?",
                "What is your height (in meters)?",
                "What is your weight (kg)?",
                "What is your glucose level?",
            ],
            "Heart": [
                "What is your pulse rate?",
                "What is your systolic blood pressure?",
                "What is your diastolic blood pressure?",
            ],
            "Diabetes": [
                "Do you have a family history of diabetes?",
                "Are you hypertensive?",
                "Do you have a family history of hypertension?",
                "Do you have a family history of cardiovascular diseases?",
            ],
        }

        self.questions = categories.get(category, [])
        self.answer_inputs = []

#z tymi pytaniami mam dylemat bo jest opcja =helpertext i ona normalnie daje nam pod pytaniem prompt ze ej wpisz liczbe a nie
#a w obecnej formie z lambda sie nie da tak to osiagnac, wiec idk trzeba by osobno kazde pytanie zapisac i dunno
#i wtedy warunki jak w pytaniu (Yes/No) user wpisuje cos innego niz answer.lower = "no" to nakrzycz na niego
        for question in self.questions:
            self.layout.add_widget(MDLabel(text=question, halign="left"))
            input_field = MDTextField(hint_text="Enter your answer", multiline=False)
            self.layout.add_widget(input_field)
            self.answer_inputs.append(input_field)

        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.return_button)

    def submit_answers(self, _):
        answers = [input_field.text for input_field in self.answer_inputs]
        advice = self.generate_medical_advice(answers)
        self.show_results(advice)

    def generate_medical_advice(self, answers):
        advice = "Based on your answers:\n"

#tu trzeba zrobic o wiele wiecej przypadkow i tez je poprawic bo sa srednie
        if len(answers) > 1 and answers[1].isdigit() and int(answers[1]) > 50:
            advice += "- You are over 50 years old. Regular health check-ups are recommended.\n"

        if len(answers) > 3 and answers[3].replace(".", "", 1).isdigit():
            weight = float(answers[3])
            if weight > 100:
                advice += "- Your weight is above average. Consider lifestyle changes.\n"

        return advice

#tu mam problem by wsadzic cokolwiek ponad Medical Advice, bo jest ustawione jako title, ale w tym miejscu bedzie graph
    def show_results(self, advice):
        dialog = MDDialog(
            title="Medical Advice",
            text=advice,
            buttons=[MDRectangleFlatButton(text="Close", on_release=lambda _: dialog.dismiss())],
        )
        dialog.open()

#ten button return mozna zrobic zeby byl na gorze po lewej stronie w formie strzalki
    def return_to_main(self, _):
        self.manager.current = "main"


class WindowManager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainWindow(name="main"))
        self.add_widget(QuestionsWindow(name="questions"))


class MyApp(MDApp):
    def build(self):
        return WindowManager()

if __name__ == "__main__":
    MyApp().run()
