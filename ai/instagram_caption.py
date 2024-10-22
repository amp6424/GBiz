# importing needed modules
import os
import google.generativeai as genai

# creating instagram bot class
class InstagramBot:

    def __init__(self):
        # Set your API key directly in the notebook
        os.environ["API_KEY"] = "" # your instagram api key
        # Configure the API key
        genai.configure(api_key=os.environ["API_KEY"])
        # Specify the model
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def create_caption(self, industry, context, tone="fun"):
        # Generate a general prompt based on user input
        prompt = (
            f"Write an engaging Instagram post for a business in the {industry} industry. "
            f"The post should focus on {context}. "
            f"Use a {tone} tone and include emojis to make it lively and appealing."
        )
        
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            # Print the generated post
            print(response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
bot = InstagramBot()
# bot.create_caption("food", "a new menu item launch", "exciting")
bot.create_caption("travel", "growing the business intra-city", "exciting, professional")
