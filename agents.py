import os
import time
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import tools_registry

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-exp")

class BaseAgent:
    def __init__(self, name, instruction, tools=None, json_mode=False):
        self.name = name
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.tools = tools
        self.config = types.GenerateContentConfig(
            system_instruction=instruction,
            tools=tools,
            temperature=0.7,
        )
        if json_mode:
            self.config.response_mime_type = "application/json"

        self.chat = self.client.chats.create(model=MODEL_NAME, config=self.config)

    def send_message(self, message, retries=5):
        for attempt in range(retries):
            try:
                response = self.chat.send_message(message)
                text = response.text or ""
                # Robust cleanup for JSON code blocks
                if "```" in text:
                    text = re.sub(r"```json\s*|\s*```", "", text).strip()
                return text
            except Exception as e:
                # ... (Retry logic same as previous) ...
                error_str = str(e)
                if "503" in error_str or "429" in error_str:
                    if attempt < retries - 1:
                        time.sleep((2 ** attempt) + 1)
                        continue
                return f"Error in {self.name}: {error_str}"
        return f"Error: {self.name} unavailable."

# --- 1. Recipe Finder Agent (UPDATED INSTRUCTION) ---
recipe_agent_instruction = """
You are the Recipe Finder Agent. 
Your goal is to find distinct, high-quality recipes that strictly match the user's request.

INSTRUCTIONS:
1. Use the 'google_search' tool to find real recipes.
2. **CRITICAL:** You MUST return a valid JSON array of objects in EVERY response, even if you are just updating a list based on feedback.
3. Do NOT output conversational text (like "Here is the updated list"). JUST output the JSON array.
4. Each object must have these exact keys: 
   - "title": The name of the recipe.
   - "ingredients": A simple list of strings.
   - "prep_time": Estimated time.
   - "source_url": The URL of the recipe found.
"""

class RecipeAgent(BaseAgent):
    def __init__(self):
        google_search_tool = types.Tool(google_search=types.GoogleSearch())
        # We keep json_mode=False to allow Tool use, but instructions enforce JSON output
        super().__init__("Recipe Finder", recipe_agent_instruction, tools=[google_search_tool])

# --- 2. Nutrition Analyzer Agent ---
nutrition_agent_instruction = """
You are the Nutrition Analyzer Agent.
Your goal is to calculate the nutritional profile for a provided list of recipes.
INSTRUCTIONS:
1. Receive a JSON list of recipes.
2. Use INTERNAL KNOWLEDGE to estimate calories, protein, carbs, and fats.
3. Output a readable summary (Markdown) comparing the recipes.
4. Highlight the "Healthiest Choice".
"""

class NutritionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nutrition Analyzer", nutrition_agent_instruction)

# --- 3. Shopping List Generator Agent (UPDATED) ---
shopping_agent_instruction = """
You are the Shopping List Generator Agent.
Your goal is to create a consolidated shopping list and SAVE it to a file.

INSTRUCTIONS:
1. Input: A list of recipes.
2. Use 'get_pantry_staples' to remove common items.
3. Consolidate duplicates and group by category.
4. Create a clean Markdown checklist.
5. **CRITICAL:** Use the 'save_to_file' tool to save the final list to 'shopping_list.md'.
6. Output the final list in the chat as well.
"""

class ShoppingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "Shopping List Generator", 
            shopping_agent_instruction, 
            # Add the new tool here so the model knows it exists
            tools=[
                tools_registry['get_pantry_staples'],
                tools_registry['save_to_file']
            ]
        )