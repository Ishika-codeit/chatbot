# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random

class ActionCareerRecommendation(Action):
    def name(self):
        return "action_career_recommendation"

    def run(self, dispatcher, tracker, domain):
        # Extract user message
        user_input = tracker.latest_message.get('text')

        # Simple AI-based career recommendations (can be replaced with ML)
        tech_careers = ["Software Engineer", "Data Scientist", "AI Researcher", "Cybersecurity Expert"]
        medical_careers = ["Doctor", "Nurse", "Pharmacist", "Biomedical Engineer"]
        business_careers = ["Marketing Manager", "Entrepreneur", "Financial Analyst", "HR Specialist"]

        if "technology" in user_input or "AI" in user_input:
            recommendation = random.choice(tech_careers)
        elif "medical" in user_input or "doctor" in user_input:
            recommendation = random.choice(medical_careers)
        elif "business" in user_input or "finance" in user_input:
            recommendation = random.choice(business_careers)
        else:
            recommendation = "It depends on your interests! Do you like technology, medicine, or business?"

        dispatcher.utter_message(text=f"Based on your interest, I recommend exploring a career as a {recommendation}. Would you like to know more?")
        return []
        import openai
from rasa_sdk import Action

# Replace with your OpenAI API Key
OPENAI_API_KEY = "your-api-key"

class ActionCareerAdviceGPT(Action):
    def name(self):
        return "action_career_advice_gpt"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message.get('text')

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a career advisor AI."},
                      {"role": "user", "content": user_input}],
            max_tokens=100
        )

        career_advice = response['choices'][0]['message']['content']
        dispatcher.utter_message(text=career_advice)
        return []
        import json
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionFetchNotesPYQ(Action):
    def name(self):
        return "action_fetch_notes_pyq"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()
        
        # Load notes & PYQs from JSON file
        with open("data/notes_pyq.json", "r") as file:
            subject_data = json.load(file)

        # Identify subject based on user input
        subject = None
        for key in subject_data.keys():
            if key in user_message:
                subject = key
                break

        if subject:
            notes = subject_data[subject]["notes"]
            pyqs = "\n".join(subject_data[subject]["pyq"])
            response = f"📖 **{subject.capitalize()} Notes:** {notes}\n\n❓ **Previous Year Questions:**\n{pyqs}"
        else:
            response = "Sorry, I don't have notes for that subject. Try asking for Math, Physics, or Chemistry."

        dispatcher.utter_message(text=response)
        return []
import json
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionStartQuiz(Action):
    def name(self):
        return "action_start_quiz"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()

        # Load quiz data
        with open("data/quiz.json", "r") as file:
            quiz_data = json.load(file)

        # Identify subject
        subject = None
        for key in quiz_data.keys():
            if key in user_message:
                subject = key
                break

        if subject:
            question_data = random.choice(quiz_data[subject])
            question = question_data["question"]
            options = question_data["options"]
            answer = question_data["answer"]

            response = f"📝 {question}\nA) {options[0]}\nB) {options[1]}\nC) {options[2]}\nD) {options[3]}"

            dispatcher.utter_message(text=response)
            return [SlotSet("current_question", question), SlotSet("correct_answer", answer)]
        else:
            dispatcher.utter_message(text="❌ Sorry, I don't have a quiz for that subject. Try Math or Science.")
            return []
class ActionCheckAnswer(Action):
    def name(self):
        return "action_check_answer"

    def run(self, dispatcher, tracker, domain):
        user_answer = tracker.latest_message.get("text").strip().lower()
        correct_answer = tracker.get_slot("correct_answer")

        # Normalize answer input (A/B/C/D) to values
        options_map = {"a": 0, "b": 1, "c": 2, "d": 3}
        
        with open("data/quiz.json", "r") as file:
            quiz_data = json.load(file)

        # Find the correct answer based on the previous question asked
        question_text = tracker.get_slot("current_question")
        correct_value = None
        for subject, questions in quiz_data.items():
            for question in questions:
                if question["question"] == question_text:
                    correct_value = question["answer"]
                    break

        if correct_value is None:
            dispatcher.utter_message(text="❌ Oops! Something went wrong. Please try again.")
            return []

        # Match user answer to correct answer
        user_answer_value = None
        for key, value in options_map.items():
            if key in user_answer:
                user_answer_value = value
                break

        if user_answer_value is not None and correct_value == quiz_data[subject][0]["options"][user_answer_value]:
            dispatcher.utter_message(text="✅ Correct! Well done. Want another question?")
        else:
            dispatcher.utter_message(text=f"❌ Incorrect. The right answer was {correct_value}. Want to try again?")
        
        return []
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import re

class ActionCalculateMath(Action):
    def name(self):
        return "action_calculate_math"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        
        try:
            # Extract numbers and operators
            result = eval(re.sub(r'[^0-9+\-*/(). ]', '', user_message))
            response = f"The answer is {result}."
        except Exception:
            response = "Sorry, I couldn't understand that math expression."

        dispatcher.utter_message(text=response)
        return []
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionCareerAdviceGPT(Action):
    def name(self):
        return "action_career_advice_gpt"

    def run(self, dispatcher, tracker, domain):
        advice = "Based on your interests, I suggest looking into AI and data science careers!"
        dispatcher.utter_message(text=advice)
        return []
