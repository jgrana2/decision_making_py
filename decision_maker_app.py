import os
from dotenv import load_dotenv
from openai import OpenAI

class DecisionMakerApp:
    def __init__(self):
        self.load_environment_variables()
        self.client = OpenAI()
        self.criteria = ["esfuerzo", "tiempo", "recursos", "comodidad", "eficiencia"]
        self.context = "which frontend framework to use when designing the Decision Making with AI Assistance App"
        self.options = ["PySide", "SwiftUI", "React native"]

    def set_context(self, context):
        self.context = context
        
    def set_criteria(self, criteria):
        self.criteria = criteria

    def set_options(self, options):
        self.options = options
    
    def load_environment_variables(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = openai_api_key

    def generate_template(self):
        return f"""Task: Assign percentage values to the provided criteria to reflect their relevance and importance in a decision-making process.

Criteria to assess: {self.criteria}

Context of the decision: {self.context}

Available options: {self.options}

Instructions:
1. For each criterion, assign percentage values to indicate their relative importance, where 100% is the highest importance, and 0% is the lowest.
2. Using the assigned criterion values, calculate the best option by determining reasonable values for each option based on the criteria. Use an exponential curve to map each criteria to options.
3. You MUST CALCULATE which option accumulates the highest total score.
4. You MUST list the resulting options scores in descending order, from the highest total score to the lowest.

Your Response: Let's proceed step by step.
"""

    def get_response_from_openai(self, template):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": template}
            ],
            temperature=0,
            stream=True
        )
        # Stream the response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:  # Check for NoneType instead of "None"
                    yield chunk.choices[0].delta.content
        
    def run(self):
        template = self.generate_template()
        for response_content in self.get_response_from_openai(template):
            yield response_content
        # response_content = self.get_response_from_openai(template)
        # if response_content:
        #     return response_content
        # else:
        #     return "No response received."

# Main execution
if __name__ == "__main__":
    app = DecisionMakerApp()
    app.run()
