import pandas as pd
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from matplotlib import pyplot as plt
import os
import seaborn as sns
from kivy.uix.image import Image


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
        self.diabetes_button.bind(on_press=lambda _: self.show_questions("Family"))

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

        categories = {
            "General": [
                "What is your gender?",
                "What is your age?",
                "What is your height (in meters)?",
                "What is your weight (kg)?",
                "Do you have diabetes?"
            ],
            "Heart": [
                "What is your pulse rate?",
                "What is your systolic blood pressure?",
                "What is your diastolic blood pressure?",
                "What is your glucose level?",
                "Enter your BMI"
            ],
            "Family": [
                "Do you have diabetes?",
                "Do you have a family history of diabetes?",
                "Are you hypertensive?",
                "Do you have a family history of hypertension?",
                "Do you have a family history of cardiovascular diseases?"
            ]
        }

        self.selected_category = category  # Store the selected category
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
        category = self.selected_category  # Retrieve the stored category
        advice = self.generate_medical_advice(answers, category)
        self.show_results(advice)

    def generate_medical_advice(self, answers, category):
        advice = f"Based on your answers:\n"

        if category == "General":

            try:
                height = float(answers[2])
                weight = float(answers[3])
                bmi = weight / (height ** 2)
            except (ValueError, IndexError) as e:
                return "There was an error processing the BMI. Please make sure to enter valid numerical values for height and weight."

            advice += f"Your BMI is {bmi}/n"
            if bmi < 18.5:
                advice = "You are underweight. You may need to increase your calorie intake. Focus on a balanced diet. "
                if answers[4].lower() == "yes":
                    advice += "Make sure to manage your blood sugar while increasing caloric intake. "
            elif 18.5 <= bmi < 24.9:
                advice = "You are in a healthy weight range. Maintain a balanced diet and stay active! "
                if answers[4].lower() == "yes":
                    advice += " Keep up the good work with blood sugar control. "
            elif 25 <= bmi < 29.9:
                advice = "You are overweight. Consider regular exercise and a healthy eating plan to lose weight. "
                if answers[4].lower() == "yes":
                    advice += "Since you have diabetes, weight loss is crucial for better blood sugar management. "
                else:
                    advice += "You may want to consider losing weight to prevent potential health issues like diabetes. "
            elif bmi >= 30:
                advice = "You have obesity. It's important to consult with a healthcare professional to develop a weight-loss plan. "
                if answers[4].lower() == "yes":
                    advice += "Weight loss is critical in managing diabetes. A healthcare provider can assist you in developing a suitable plan. "
                else:
                    advice += "It’s important to start working on weight loss to reduce the risk of developing diabetes and other health complications. "
                # An additional diabetes-specific advice if the person has diabetes
            if answers[4].lower() == "yes":
                advice += "Make sure to monitor your blood sugar regularly and work with your healthcare provider to tailor your diet and exercise. "

        if category == "Heart":
            # Pulse Rate Advice
            if float(answers[0]) < 60:
                advice += "Your pulse rate is below the normal range. If you feel lightheaded or fatigued, consult a healthcare provider. "
            elif float(answers[0]) > 100:
                advice += "Your pulse rate is high. This could indicate stress, dehydration, or a heart condition. Consider getting a check-up. "
            else:
                advice += "Your pulse rate is within a healthy range. Keep up the good work! "

            # Blood Pressure Advice
            if float(answers[1]) < 90 or float(answers[2]) < 60:
                advice += "Your blood pressure is lower than normal. Ensure you're eating enough salt and staying hydrated, but consult a doctor if symptoms like dizziness occur. "
            elif float(answers[1]) >= 130 or float(answers[2]) >= 80:
                advice += "Your blood pressure is on the higher side. Try managing stress, exercising, and reducing salt intake. Consult a healthcare provider if it remains high. "
            else:
                advice += "Your blood pressure is in a healthy range. Maintain a balanced diet and regular physical activity to keep it in check. "

            # Glucose Level Advice
            if float(answers[3]) < 70:
                advice += "Your glucose level is low. You may need to eat something with carbohydrates to prevent hypoglycemia. "
            elif 70 <= float(answers[3]) <= 99:
                advice += "Your glucose level is in the normal range. Keep eating a balanced diet and stay active to maintain it. "
            elif 100 <= float(answers[3]) <= 125:
                advice += "Your glucose level is elevated, which may indicate pre-diabetes. Consider adopting a healthier diet and increasing physical activity. "
            else:
                advice += "Your glucose level is high, which could indicate diabetes. It is essential to consult a healthcare provider for further evaluation. "

            # BMI Advice
            if float(answers[4]) < 18.5:
                advice += "You are underweight. It may be helpful to focus on nutrient-rich, calorie-dense foods to gain weight in a healthy manner. "
            elif 18.5 <= float(answers[4]) <= 24.9:
                advice += "You are in a healthy weight range. Continue with a balanced diet and regular physical activity. "
            elif 25 <= float(answers[4]) <= 29.9:
                advice += "You are overweight. Consider adopting a balanced diet and regular exercise routine to lose weight in a healthy way. "
            else:
                advice += "You are in the obesity range. It is important to consult a healthcare provider to work on a weight loss plan, especially for better overall health. "

        if category == "Family":
            # Diabetes Advice
            if answers[0].lower() == "yes":
                advice += "You are diabetic, it's important to regularly monitor your blood glucose levels, follow your prescribed treatment, and maintain a balanced diet. Regular exercise is also essential. "
            elif answers[1].lower() == "yes":
                advice += "Since you have a family history of diabetes, consider getting your blood glucose levels checked regularly and focus on maintaining a healthy weight and diet to prevent it. "

            # Hypertension Advice
            if answers[2].lower() == "yes":
                advice += "You are hypertensive. It is crucial to follow a low-salt diet, manage stress, and stay active. Make sure to monitor your blood pressure regularly and consult your healthcare provider for medication if necessary. "
            elif answers[3].lower() == "yes":
                advice += "Given that you have a family history of hypertension, consider regular blood pressure check-ups and lifestyle changes such as a balanced diet, regular exercise, and reduced salt intake. "

            # Cardiovascular Disease Advice
            if answers[4].lower() == "yes":
                advice += "Having a cardiovascular disease requires you to follow your doctor's recommendations closely. A heart-healthy diet, regular exercise, and controlling other risk factors like cholesterol and blood pressure are essential. "

        return advice

    def generate_graph(self, answers, category):
        fig, ax = plt.subplots(figsize=(4, 3))
        # Load data
        data = pd.read_csv("Diabetes_Final_Data_V2.csv")

        # Convert to DataFrame
        df = pd.DataFrame(data)

        if category == "General":
            inputAge = inputAge = int(answers[1].text)  # Use .text to get the input string
            inputGender = answers[0].text.strip().capitalize()
            inputWeight = float(answers[3].text)
            inputHeight = float(answers[2].text)
            inputDiabetic = answers[4].text.strip().capitalize()

            # Calculate user's BMI
            user_bmi = inputWeight / (inputHeight ** 2)

            # BMI categories and thresholds
            categories = ["Underweight", "Normal weight", "Overweight", "Obesity"]
            category_ranges = [18.5, 24.9, 29.9, 40]  # Upper thresholds
            colors = ["blue", "green", "orange", "red"]

            # Divide the data into diabetic and non-diabetic groups
            diabetic_group = data[data['diabetic'] == "Yes"]
            non_diabetic_group = data[data['diabetic'] == "No"]

            # Calculate average BMI for each category in both diabetic and non-diabetic groups
            bmi_values_diabetic = []
            bmi_values_non_diabetic = []

            # For each category, calculate the mean BMI
            for low, high in zip([0] + category_ranges[:-1], category_ranges):
                # Diabetic group
                diabetic_bmi = diabetic_group[(diabetic_group['bmi'] > low) & (diabetic_group['bmi'] <= high)]
                bmi_values_diabetic.append(diabetic_bmi['bmi'].mean() if not diabetic_bmi.empty else 0)

                # Non-diabetic group
                non_diabetic_bmi = non_diabetic_group[
                    (non_diabetic_group['bmi'] > low) & (non_diabetic_group['bmi'] <= high)]
                bmi_values_non_diabetic.append(non_diabetic_bmi['bmi'].mean() if not non_diabetic_bmi.empty else 0)

            # Plotting
            fig, ax = plt.subplots()

            # Plot both groups' average BMI bars
            bars_diabetic = ax.bar(categories, bmi_values_diabetic, color=colors, alpha=0.6,
                                   label="Diabetic Group Averages")
            bars_non_diabetic = ax.bar(categories, bmi_values_non_diabetic, color=colors, alpha=0.3,
                                       label="Non-Diabetic Group Averages")

            # Highlight user's BMI
            user_index = (
                0 if user_bmi < 18.5 else
                1 if 18.5 <= user_bmi < 24.9 else
                2 if 25 <= user_bmi < 29.9 else
                3
            )
            ax.bar(categories[user_index], bmi_values_diabetic[user_index], color="purple", label="Your BMI")

            # Add annotations for BMI values
            for i, bar in enumerate(bars_diabetic):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{height:.1f}", ha="center", fontsize=10)

            # Highlight user's BMI value
            ax.axhline(y=user_bmi, color="purple", linestyle="--", linewidth=2, label=f"Your BMI: {user_bmi:.2f}")

            # Graph labels and legend
            ax.set_title(f"BMI Comparison - Diabetic vs Non-Diabetic (Your Age: {inputAge}, Gender: {inputGender})",
                         fontsize=14)
            ax.set_ylabel("Average BMI Value", fontsize=12)
            ax.set_xlabel("BMI Categories", fontsize=12)
            ax.legend(loc="upper left", fontsize=10)

            plt.tight_layout()

            # Save the figure as a PNG image
            image_path = "bmi_graph.png"
            fig.savefig(image_path)
            plt.close(fig)  # Close the figure after saving

            return image_path  # Return the image file path for later use


        elif category == "Heart":
            user_data = {
                'pulse_rate': float(answers[0].text),
                'systolic_bp': float(answers[1].text),
                'diastolic_bp': float(answers[2].text),
                'glucose': float(answers[3].text),
                'bmi': float(answers[4].text),
            }

            # Create Box Plots
            plt.figure(figsize=(16, 8))
            parameters = ['pulse_rate', 'systolic_bp', 'diastolic_bp', 'glucose', 'bmi']

            for i, param in enumerate(parameters):
                plt.subplot(1, 5, i + 1)
                sns.boxplot(df[param], color='lightblue', width=0.5)
                plt.scatter(0, user_data[param], color='red', label='User Value', zorder=5)
                plt.title(param.replace('_', ' ').title())
                plt.xlabel('')
                plt.ylabel('Value')
                plt.legend()

            plt.tight_layout()

            # Save the figure as a PNG image
            image_path = "heart_graph.png"
            fig.savefig(image_path)
            plt.close(fig)  # Close the figure after saving

            return image_path

        elif category == "Family":
            # User Input
            user_data = {
                'diabetic': answers[0].text.strip().lower(),
                'family_diabetes': 1 if answers[1].text.strip().lower() == 'yes' else 0,
                'hypertensive': 1 if answers[2].text.strip().lower() == 'yes' else 0,
                'family_hypertension': 1 if answers[3].text.strip().lower() == 'yes' else 0,
                'cardiovascular_disease': 1 if answers[4].text.strip().lower() == 'yes' else 0
            }

            # Create Bar Plots for Categorical Data
            plt.figure(figsize=(16, 6))
            parameters = ['family_diabetes', 'hypertensive', 'family_hypertension', 'cardiovascular_disease']

            for i, param in enumerate(parameters):
                plt.subplot(1, 4, i + 1)
                sns.countplot(x=df[param], palette='pastel')
                # Highlight the user's input with a red frame
                user_bar_position = user_data[param]
                bar_height = df[param].value_counts().get(user_bar_position, 0)
                plt.gca().patches[user_bar_position].set_edgecolor('red')
                plt.gca().patches[user_bar_position].set_linewidth(3)
                plt.title(param.replace('_', ' ').title())
                plt.xlabel('')
                plt.ylabel('Count')

            plt.tight_layout()

            # Save the figure as a PNG image
            image_path = "family_graph.png"
            fig.savefig(image_path)
            plt.close(fig)

            return image_path

#apka ogolnie dzialal i wykresy sie zapisuja, jedyne co to sie nie pokazuja w oknie hihi
    def show_results(self, advice):
        # Generate the appropriate graph and get the saved image path
        graph_image_path = self.generate_graph(self.answer_inputs, self.selected_category)

        # Create the layout for the dialog
        content = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        # Add the image widget first (Graph)
        graph_image = Image(source=graph_image_path)  # Use Kivy's Image widget here
        content.add_widget(graph_image)

        # Then, add the Medical Advice text
        content.add_widget(MDLabel(text="Medical Advice", halign="center", font_style="H6"))
        content.add_widget(MDLabel(text=advice, halign="left"))

        # Create the dialog
        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            buttons=[
                MDRectangleFlatButton(text="Close", on_release=lambda _: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    #tu mam problem by wsadzic cokolwiek ponad Medical Advice, bo jest ustawione jako title, ale w tym miejscu bedzie graph
    # def show_results(self, advice):
    #         dialog = MDDialog(
    #             title="Medical Advice",
    #             text=advice,
    #             buttons=[MDRectangleFlatButton(text="Close", on_release=lambda _: dialog.dismiss())],
    #         )
    #         dialog.open()
    #
    # #ten button return mozna zrobic zeby byl na gorze po lewej stronie w formie strzalki
    #     def return_to_main(self, _):
    #         self.manager.current = "main"

#ten button return mozna zrobic zeby byl na gorze po lewej stronie w formie strzalki
    def return_to_main(self, _):
        self.manager.current = "main"


class WindowManager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainWindow(name="main"))
        self.add_widget(QuestionsWindow(name="questions"))


class HealthAdviceApp(MDApp):
    def build(self):
        return WindowManager()

if __name__ == "__main__":
    HealthAdviceApp().run()
