import os
import pandas as pd
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from matplotlib import pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


class GraphWidget(MDBoxLayout):
    """
    This widget is used to display a graph (in the form of an image) in the ResultsWindow.
    It loads and shows the graph stored in 'bmi_graph.png' (or another image path).

    Attributes:
    image: Image widget to display the graph.
    """
    def __init__(self, **kwargs):
        """
        Initializes the GraphWidget and adds the Image widget to the layout.

        Arguments:
        **kwargs: Arbitrary keyword arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)
        # Initialize an Image widget to display the graph
        self.image = Image(source='bmi_graph.png')
        self.add_widget(self.image)


class ResultsWindow(MDScreen):
    """
    Results window where medical advice and generated graphs (BMI, heart-related, etc.)
    are displayed after user answers questions.

    Attributes:
        layout: The layout that holds the widgets in the Results window.
        title_label: Label showing the title "Your Results".
        advice_label: Label to display the health-related advice.
        graph_widget: Widget to display the graph.
        return_button: Button to return to the main menu.
        save_pdf_button: Button to save the results as a PDF.
        graph_path: Path to the generated graph.
        current_advice: The health advice text to save in the PDF.

    Methods:
        display_results(): displays the generated data
        return to main(): goes back to the main menu.
        save_to_pdf(): saves the generated data as PDF.
    """

    def __init__(self, **kwargs):
        """
        Initializes the ResultsWindow and sets up the layout and widgets.

        Args:
        **kwargs: Arbitrary keyword arguments passed to the parent constructor.
        """

        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        self.add_widget(self.layout)

        # Title label for the results page
        self.title_label = MDLabel(
            text="Your Results",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height=dp(40),
        )
        self.layout.add_widget(self.title_label)

        # Advice label to show health-related advice
        self.advice_label = MDLabel(
            text="",
            halign="center",
            size_hint=(1, None),
            height=dp(80),
        )
        self.layout.add_widget(self.advice_label)

        # Placeholder for the graph widget
        self.graph_widget = None

        # Return button to go back to the main menu
        self.return_button = MDRectangleFlatButton(
            text="Return to Main Menu",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
        )
        self.return_button.bind(on_press=self.return_to_main)
        self.layout.add_widget(self.return_button)

        # Button to save the results (advice + graph) to a PDF
        self.save_pdf_button = MDRectangleFlatButton(
            text="Save as PDF",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
        )
        self.save_pdf_button.bind(on_press=self.save_to_pdf)  # Fix: Correct binding
        self.layout.add_widget(self.save_pdf_button)

    def display_results(self, advice, graph_path):
        """
        Displays the advice text and the generated graph in the Results window.

        Arguments:
        advice (str): A string containing the medical advice for the user.
        graph_path (str): Path to the generated graph image.
        """
        self.advice_label.text = advice

        if self.graph_widget:
            self.layout.remove_widget(self.graph_widget)

        self.graph_widget = GraphWidget()
        self.graph_widget.image.source = graph_path
        self.layout.add_widget(self.graph_widget, index=2)

        self.graph_path = graph_path  # Store for saving to PDF
        self.current_advice = advice  # Store advice for saving

    def return_to_main(self, _):
        """
        Switches back to the main window screen.

        Arguments:
            _: Event argument (unused).
        """
        self.manager.current = "main"

    def save_to_pdf(self, _):
        """
        Saves the health advice and the generated graph to a PDF file named 'health_report.pdf'.
        This will include text advice and a graph image.

        Arguments:
            _: Event argument (unused).
        """
        pdf_filename = "health_report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        # Title of the PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Health Report")

        # Writing advice to the PDF
        c.setFont("Helvetica", 12)
        max_width = 400  # Max text width before wrapping
        y_position = height - 100  # Starting position

        # Split the advice text into lines that fit within the maximum width
        text_lines = simpleSplit(self.current_advice, "Helvetica", 12, max_width)

        for line in text_lines:
            c.drawString(100, y_position, line)
            y_position -= 20  # Move down for the next line
            if y_position < 100:  # Prevent text from going off the page
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50  # Reset y_position for new page

        # Add Image if it exists
        if self.graph_path:
            try:
                c.drawImage(self.graph_path, 100, y_position - 300, width=400, height=300)
            except Exception as e:
                print(f"Error adding image: {e}")

        c.save()
        print(f"PDF saved as {pdf_filename}")


class QuestionsWindow(MDScreen):
    """
    Window to ask the user a series of health-related questions.
    Based on their answers, medical advice and a graph will be generated.

    Methods:
        create_action_button(): Helper function to create action buttons.
        set_category(): Sets the category of questions based on the selected genre (General, Heart, Family).
        submit_answers(): Submits the user's answers and displays results with graphs.
        return_to_main(): Returns to the main menu screen.
        generate_graph(): Generates the graph and displays it.
        generate_heart_graph(): Generates the heart graph and displays it.
        generate_family_graph(): Generates the family graph and displays it.
        generate_advice(): Generates the advice and displays it.
    """
    def __init__(self, **kwargs):
        """
        Initializes the QuestionsWindow and sets up the layout and widgets.

        Arguments:
            **kwargs: Arbitrary keyword arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        self.add_widget(self.layout)

        # Title label to prompt the user for questions
        self.title_label = MDLabel(
            text="Answer the following questions:", halign="center", font_style="H5"
        )
        self.layout.add_widget(self.title_label)

        # Buttons for submitting answers and returning to the main menu
        self.submit_button = self.create_action_button("Submit Answers", self.submit_answers)
        self.return_button = self.create_action_button("Return", self.return_to_main)

    def create_action_button(self, text, callback):
        """
        Helper function to create action buttons.

        Arguments:
            text (str): The text to display on the button.
            callback (function): The function to call when the button is pressed.

        Returns:
            MDRectangleFlatButton: The created button widget.
        """

        button = MDRectangleFlatButton(
            text=text, size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5}
        )
        button.bind(on_press=callback)
        return button

    def set_category(self, category):
        """
        Sets the category of questions based on the selected genre (General, Heart, Family).

        Arguments:
            category (str): The category to set (General, Heart, or Family).
        """

        self.layout.clear_widgets()
        self.layout.add_widget(self.title_label)

        categories = {
            "General": [
                "What is your gender?",
                "What is your age?",
                "What is your height (in meters)?",
                "What is your weight (kg)?",
                "Do you have diabetes?",
            ],
            "Heart": [
                "What is your pulse rate?",
                "What is your systolic blood pressure?",
                "What is your diastolic blood pressure?",
                "What is your glucose level?",
                "Enter your BMI",
            ],
            "Family": [
                "Do you have diabetes?",
                "Do you have a family history of diabetes?",
                "Are you hypertensive?",
                "Do you have a family history of hypertension?",
                "Do you have a family history of cardiovascular diseases?",
            ],
        }

        self.selected_category = category
        self.questions = categories.get(category, [])
        self.answer_inputs = []

        # Add input fields for each question
        for question in self.questions:
            self.layout.add_widget(MDLabel(text=question, halign="left"))
            input_field = MDTextField(hint_text="Enter your answer", multiline=False)
            self.layout.add_widget(input_field)
            self.answer_inputs.append(input_field)

        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.return_button)

    def submit_answers(self, _):
        """
        Submits the user's answers, generates medical advice, and displays results with graphs.

        Arguments:
            _: Event argument (unused).

        """
        answers = [input_field.text for input_field in self.answer_inputs]
        category = self.selected_category

        # Generate medical advice based on the answers and category
        advice = self.generate_medical_advice(answers, category)

        graph_path = None
        if category == "General":
            graph_path = self.generate_graph(answers, category)
        elif category == "Heart":
            graph_path = self.generate_heart_graph(answers)
        elif category == "Family":
            graph_path = self.generate_family_graph(answers)

        # Display the results (advice + graph) in the ResultsWindow
        results_window = self.manager.get_screen("results")
        results_window.display_results(advice, graph_path)
        self.manager.current = "results"

    def return_to_main(self, _):
        """
        Returns to the main menu screen.

        Arguments:
            _: Event argument (unused).

        """
        self.manager.current = "main"

    def generate_family_graph(self, answers):
        """
        Generates a family health-related graph showing conditions such as diabetes, hypertension, etc.

        Arguments:
        answers(list): List of answers from the user

        Returns:
             str: Path to the generated graph image
        """
        user_data = {
            'diabetic': answers[0].strip().lower(),
            'family_diabetes': 1 if answers[1].strip().lower() == 'yes' else 0,
            'hypertensive': 1 if answers[2].strip().lower() == 'yes' else 0,
            'family_hypertension': 1 if answers[3].strip().lower() == 'yes' else 0,
            'cardiovascular_disease': 1 if answers[4].strip().lower() == 'yes' else 0
        }

        data = pd.read_csv("Diabetes_Final_Data_V2.csv")
        df = pd.DataFrame(data)

        # Plotting the graph
        plt.figure(figsize=(16, 6))
        parameters = ['family_diabetes', 'hypertensive', 'family_hypertension', 'cardiovascular_disease']

        for i, param in enumerate(parameters):
            plt.subplot(1, 4, i + 1)
            sns.countplot(x=df[param], palette='pastel')
            user_bar_position = user_data[param]
            bar_height = df[param].value_counts().get(user_bar_position, 0)
            plt.gca().patches[user_bar_position].set_edgecolor('red')
            plt.gca().patches[user_bar_position].set_linewidth(3)
            plt.title(param.replace('_', ' ').title())
            plt.xlabel('')
            plt.ylabel('Count')

        plt.tight_layout()

        image_path = "family_graph.png"
        plt.savefig(image_path)
        plt.close()

        return image_path

    def generate_heart_graph(self, answers):
        """
        Generates a graph displaying heart-related data.

        Arguments:
        answers(list): List of heart-related answers

        Returns:
            str: Path to the generated graph image
        """

        user_data = {
            'pulse_rate': float(answers[0]),
            'systolic_bp': float(answers[1]),
            'diastolic_bp': float(answers[2]),
            'glucose': float(answers[3]),
            'bmi': float(answers[4])
        }

        data = pd.read_csv("Diabetes_Final_Data_V2.csv")
        df = pd.DataFrame(data)

        plt.figure(figsize=(16, 8))
        parameters = ['pulse_rate', 'systolic_bp', 'diastolic_bp', 'glucose', 'bmi']

        for i, param in enumerate(parameters):
            plt.subplot(1, 5, i + 1)
            sns.boxplot(df[param], color='lightblue', width=0.5)
            plt.scatter(0, user_data[param], color='red', label='User  Value', zorder=5)
            plt.title(param.replace('_', ' ').title())
            plt.xlabel('')
            plt.ylabel('Value')
            plt.legend()

        plt.tight_layout()

        image_path = "heart_graph.png"
        plt.savefig(image_path)
        plt.close()

        return image_path

    def generate_graph(self, answers, category):
        """
        Generates a BMI graph using the answers.

        Arguments:
        answers(list): List of answers
        category(list): Category string ("General", "Heart", or "Family")

        Returns:
            str: Path to the generated graph image
        """

        if category == "General":
            height = float(answers[2])
            weight = float(answers[3])
            bmi = weight / (height ** 2)

            data = pd.read_csv("Diabetes_Final_Data_V2.csv")
            df = pd.DataFrame(data)

            categories = ["Underweight", "Normal weight", "Overweight", "Obesity"]
            category_ranges = [18.5, 24.9, 29.9, 40]
            colors = ["blue", "green", "orange", "red"]

            diabetic_group = data[data['diabetic'] == "Yes"]
            non_diabetic_group = data[data['diabetic'] == "No"]

            bmi_values_diabetic = []
            bmi_values_non_diabetic = []

            for low, high in zip([0] + category_ranges[:-1], category_ranges):
                diabetic_bmi = diabetic_group[(diabetic_group['bmi'] > low) & (diabetic_group['bmi'] <= high)]
                bmi_values_diabetic.append(diabetic_bmi['bmi'].mean() if not diabetic_bmi.empty else 0)

                non_diabetic_bmi = non_diabetic_group[
                    (non_diabetic_group['bmi'] > low) & (non_diabetic_group['bmi'] <= high)]
                bmi_values_non_diabetic.append(non_diabetic_bmi['bmi'].mean() if not non_diabetic_bmi.empty else 0)

            fig, ax = plt.subplots()

            bars_diabetic = ax.bar(categories, bmi_values_diabetic, color=colors, alpha=0.6,
                                   label="Diabetic Group Averages")
            bars_non_diabetic = ax.bar(categories, bmi_values_non_diabetic, color=colors, alpha=0.3,
                                       label="Non-Diabetic Group Averages")

            user_index = (
                0 if bmi < 18.5 else
                1 if 18.5 <= bmi < 24.9 else
                2 if 25 <= bmi < 29.9 else
                3
            )
            ax.bar(categories[user_index], bmi_values_diabetic[user_index], color="purple", label="Your BMI")

            for i, bar in enumerate(bars_diabetic):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{height:.1f}", ha="center", fontsize=10)

            ax.axhline(y=bmi, color="purple", linestyle="--", linewidth=2, label=f"Your BMI: {bmi:.2f}")

            ax.set_title(f"BMI Comparison - Diabetic vs Non-Diabetic", fontsize=14)
            ax.set_ylabel("Average BMI Value", fontsize=12)
            ax.set_xlabel("BMI Categories", fontsize=12)
            ax.legend(loc="upper left", fontsize=10)

            plt.tight_layout()

            plt.savefig("bmi_graph.png")
            plt.close(fig)

            return "bmi_graph.png"

    def generate_medical_advice(self, answers, category):
        """
        Generates health advice based on the user's answers.

        Arguments:
        answers(list): List of answers provided by the user
        category(list): The category of questions answered

        Returns:
            str: Path to the generated graph image
        """
        advice = f"Based on your answers:\n"

        if category == "General":
            try:
                height = float(answers[2])
                weight = float(answers[3])
                bmi = weight / (height ** 2)
            except (ValueError, IndexError) as e:
                return "There was an error processing the BMI. Please make sure to enter valid numerical values for height and weight."

            advice += f"Your BMI is {bmi:.2f}\n"
            if bmi < 18.5:
                advice += "You are underweight. You may need to increase your calorie intake. Focus on a balanced diet. "
            elif 18.5 <= bmi < 24.9:
                advice += "You are in a healthy weight range. Maintain a balanced diet and stay active! "
            elif 25 <= bmi < 29.9:
                advice += "You are overweight. Consider regular exercise and a healthy eating plan to lose weight. "
            else:
                advice += "You have obesity. It's important to consult with a healthcare professional to develop a weight-loss plan. "

        if category == "Heart":
            if float(answers[0]) < 60:
                advice += "Your pulse rate is below the normal range. If you feel lightheaded or fatigued, consult a healthcare provider. "
            elif float(answers[0]) > 100:
                advice += "Your pulse rate is high. This could indicate stress, dehydration, or a heart condition. Consider getting a check-up. "
            else:
                advice += "Your pulse rate is within a healthy range. Keep up the good work! "

            if float(answers[1]) < 90 or float(answers[2]) < 60:
                advice += "Your blood pressure is lower than normal. Ensure you're eating enough salt and staying hydrated, but consult a doctor if symptoms like dizziness occur. "
            elif float(answers[1]) >= 130 or float(answers[2]) >= 80:
                advice += "Your blood pressure is on the higher side. Try managing stress, exercising, and reducing salt intake. Consult a healthcare provider if it remains high. "
            else:
                advice += "Your blood pressure is in a healthy range. Maintain a balanced diet and regular physical activity to keep it in check. "

            if float(answers[3]) < 70:
                advice += "Your glucose level is low. You may need to eat something with carbohydrates to prevent hypoglycemia. "
            elif 70 <= float(answers[3]) <= 99:
                advice += "Your glucose level is in the normal range. Keep eating a balanced diet and stay active to maintain it. "
            elif 100 <= float(answers[3]) <= 125:
                advice += "Your glucose level is elevated, which may indicate pre-diabetes. Consider adopting a healthier diet and increasing physical activity. "
            else:
                advice += "Your glucose level is high, which could indicate diabetes. It is essential to consult a healthcare provider for further evaluation. "

            if float(answers[4]) < 18.5:
                advice += "You are underweight. It may be helpful to focus on nutrient-rich, calorie-dense foods to gain weight in a healthy manner. "
            elif 18.5 <= float(answers[4]) <= 24.9:
                advice += "You are in a healthy weight range. Continue with a balanced diet and regular physical activity. "
            elif 25 <= float(answers[4]) <= 29.9:
                advice += "You are overweight. Consider adopting a balanced diet and regular exercise routine to lose weight in a healthy way. "
            else:
                advice += "You are in the obesity range. It is important to consult a healthcare provider to work on a weight loss plan, especially for better overall health. "

        if category == "Family":
            if answers[0].lower() == "yes":
                advice += "You are diabetic, it's important to regularly monitor your blood glucose levels, follow your prescribed treatment, and maintain a balanced diet. Regular exercise is also essential. "
            elif answers[1].lower() == "yes":
                advice += "Since you have a family history of diabetes, consider getting your blood glucose levels checked regularly and focus on maintaining a healthy weight and diet to prevent it. "

            if answers[2].lower() == "yes":
                advice += "You are hypertensive. It is crucial to follow a low-salt diet, manage stress, and stay active. Make sure to monitor your blood pressure regularly and consult your healthcare provider for medication if necessary. "
            elif answers[3].lower() == "yes":
                advice += "Given that you have a family history of hypertension, consider regular blood pressure check-ups and lifestyle changes such as a balanced diet, regular exercise, and reduced salt intake. "

            if answers[4].lower() == "yes":
                advice += "Having a cardiovascular disease requires you to follow your doctor's recommendations closely. A heart-healthy diet, regular exercise, and controlling other risk factors like cholesterol and blood pressure are essential. "

        return advice



class MainWindow(MDScreen):
    """
    Main window for the app where users can select a category of questions (General, Heart, or Family).
    Based on the selected category, the user will be redirected to the relevant question screen.

    Methods:
        __init__(**kwargs):
            Initializes the MainWindow layout and buttons for selecting question categories.

        show_questions(category):
            Switches to the questions screen and sets the category for the questions.
    """

    def __init__(self, **kwargs):
        """
        Initializes the MainWindow layout and buttons for selecting question categories.

        Arguments:
        **kwargs: Additional keyword arguments to be passed to the superclass.
        """
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

        # General button for general health questions
        self.general_button = MDIconButton(
            icon="account",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.698, 0.329),
        )

        # Heart button for heart-related questions
        self.heart_button = MDIconButton(
            icon="heart",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.639, 0.114, 0.114),
        )

        # Diabetes button for family health-related questions
        self.diabetes_button = MDIconButton(
            icon="medical-bag",
            size_hint=(self.width / 3, 0.2),
            size=(100, 100),
            pos_hint={"center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.467, 0.804, 1),
        )

        # Bind buttons to show respective questions when clicked
        self.general_button.bind(on_press=lambda _: self.show_questions("General"))
        self.heart_button.bind(on_press=lambda _: self.show_questions("Heart"))
        self.diabetes_button.bind(on_press=lambda _: self.show_questions("Family"))

        # Add buttons to the layout
        button_layout.add_widget(self.general_button)
        button_layout.add_widget(self.heart_button)
        button_layout.add_widget(self.diabetes_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def show_questions(self, category):
        """
        Switches to the questions screen and sets the category for the questions.

        Arguments:
        category (str): The category of questions to display (e.g., 'General', 'Heart', 'Family').
        """

        self.manager.current = "questions"
        self.manager.get_screen("questions").set_category(category)


class MyApp(MDApp):
    """
    Main app class responsible for managing screen transitions and initializing the app.

    Methods:
        build(self):
            Builds the screen manager.
    """
    def build(self):
        """
        Builds the screen manager and adds the main, questions, and results screens.

        Returns:
        MDScreenManager: The screen manager that handles screen transitions.
        """
        sm = MDScreenManager()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(QuestionsWindow(name="questions"))
        sm.add_widget(ResultsWindow(name="results"))
        return sm


if __name__ == "__main__":
    """
    Starts the MyApp application and runs the Kivy app. Additionally, it cleans up any
    generated graph images after the application finishes.
    """
    MyApp().run()

    # Clean up generated graph images after execution
    for file in ["bmi_graph.png", "heart_graph.png", "diabetes_graph.png", "family_graph.png"]:
        if os.path.exists(file):
            os.remove(file)