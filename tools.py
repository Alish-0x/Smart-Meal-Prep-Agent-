import random

# --- Mock Database ---
class InMemorySessionService:
    def __init__(self):
        self.saved_plans = []

    def save_meal_plan(self, plan_data: dict):
        self.saved_plans.append(plan_data)
        return "Success"

# --- Specific Tools ---

def calculate_macros_tool(ingredients_text: str):
    """
    Estimates nutritional macros for a given set of ingredients.
    """
    # Hackathon Tip: Make mock data deterministic but varied so it looks real.
    # We use the length of the text to seed the randomness so the same input gives the same output.
    seed = len(ingredients_text)
    random.seed(seed)
    
    est_calories = random.randint(300, 800)
    protein = random.randint(10, 40)
    carbs = random.randint(20, 80)
    fats = random.randint(10, 30)

    return {
        "status": "success",
        "calories": est_calories,
        "macros": {
            "protein": f"{protein}g",
            "carbs": f"{carbs}g",
            "fats": f"{fats}g"
        },
        "note": "Estimated based on standard portion sizes."
    }

def get_pantry_staples():
    """Returns a list of common items users typically have."""
    return [
        "salt", "pepper", "olive oil", "vegetable oil", 
        "flour", "sugar", "water", "butter", "garlic powder"
    ]

# --- NEW TOOL ---
def save_to_file(content: str, filename: str = "shopping_list.md"):
    """
    Saves the provided text content to a file on the local disk.
    Useful for saving shopping lists, recipes, or reports.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully saved content to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

# Update registry
tools_registry = {
    "calculate_macros": calculate_macros_tool,
    "get_pantry_staples": get_pantry_staples,
    "save_to_file": save_to_file  # <--- Add this
}