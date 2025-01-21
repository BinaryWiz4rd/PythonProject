from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

class MainWindow(MDScreen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        #https://www.tutorialspoint.com/kivy/kivy-text-markup.htm#:~:text=Although%20Kivy%27s%20Label%20object%20has%20properties%20such%20as,the%20markup%20property%20of%20the%20label%20to%20True.
        self.title_label = MDLabel(
            text="[b]Pick a genre of questions[/b]", markup=True,
            halign="center",
            size_hint_y=None,
            height=100,
            font_style="H5"
        )
        self.layout.add_widget(self.title_label)
        #https://kivymd.readthedocs.io/en/latest/components/button/index.html
        #https://m3.material.io/components/icon-buttons/overview
        #https://rgbcolorpicker.com/0-1
        button_layout = MDBoxLayout(orientation='horizontal', padding=20, spacing=20)

        self.general_button = MDIconButton(
            icon="account",
            size_hint=(self.width/3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.698, 0.329)
        )

        self.heart_button = MDIconButton(
            icon="heart",
            size_hint=(self.width/3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.639, 0.114, 0.114) #rbga in a format 0-1
        )

        self.diabetes_button = MDIconButton(
            icon="medical-bag",
            size_hint=(self.width/3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.804, 1)
        )

        self.general_button.bind(on_press=lambda x: self.show_questions("General"))
        self.heart_button.bind(on_press=lambda x: self.show_questions("Heart"))
        self.diabetes_button.bind(on_press=lambda x: self.show_questions("Diabetes"))

        button_layout.add_widget(self.general_button)
        button_layout.add_widget(self.heart_button)
        button_layout.add_widget(self.diabetes_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def show_questions(self, category):
        self.manager.current = 'questions'
        self.manager.get_screen('questions').set_category(category)

class QuestionsWindow(MDScreen):
    def __init__(self, **kwargs):
        super(QuestionsWindow, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)

        self.question_label = MDLabel(halign="center")
        self.layout.add_widget(self.question_label)

        self.answer_input = MDTextField(hint_text="Enter your answer", multiline=False)
        self.layout.add_widget(self.answer_input)

        self.submit_button = MDRectangleFlatButton(text="Submit", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5})
        self.submit_button.bind(on_press=self.submit_answer)
        self.layout.add_widget(self.submit_button)

        self.questions = []
        self.current_question_index = 0

    def set_category(self, category):
        if category == "General":
            self.questions = [
                "What is your gender?",
                "What is your age?",
                "What is your height (in meters)?",
                "What is your weight (kg)?",
                "What is your glucose level?"
            ]
        elif category == "Heart":
            self.questions = [
                "What is your pulse rate?",
                "What is your systolic blood pressure?",
                "What is your diastolic blood pressure?"
            ]
        elif category == "Diabetes":
            self.questions = [
                "Do you have a family history of diabetes?",
                "Are you hypertensive?",
                "Do you have a family history of hypertension?",
                "Do you have a family history of cardiovascular diseases?"
            ]

        self.current_question_index = 0
        self.display_question()

    def display_question(self):
        if self.current_question_index < len(self.questions):
            self.question_label.text = self.questions[self.current_question_index]
            self.answer_input.text = ""
        else:
            self.show_results()

    def submit_answer(self, instance):
        self.current_question_index += 1
        self.display_question()

    def show_results(self):
        self.manager.current = 'results'

class ResultsWindow(MDScreen):
    def __init__(self, **kwargs):
        super(ResultsWindow, self).__init__(**kwargs)
        self.add_widget(MDLabel (text="Thank you for your submission! Here are your results:", halign="center"))
        #i tu poniżej się da graph

class WindowManager(MDScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.add_widget(MainWindow(name='main'))
        self.add_widget(QuestionsWindow(name='questions'))
        self.add_widget(ResultsWindow(name='results'))

class MyApp(MDApp):
    def build(self):
        return WindowManager()

if __name__ == "__main__":
    MyApp().run()