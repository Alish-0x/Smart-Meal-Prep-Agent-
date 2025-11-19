# 🍽️ Smart Meal Prep Agent

An intelligent multi-agent system powered by Google's Gemini API that helps you plan meals, analyze nutrition, and generate optimized shopping lists with human-in-the-loop refinement.

## ✨ Features

- **Interactive Recipe Discovery**: AI-powered search for high-quality recipes matching your preferences
- **Human-in-the-Loop Approval**: Iterative feedback system to refine recipe suggestions until perfect
- **Nutritional Analysis**: Automatic macro calculations and health comparisons across recipes
- **Smart Shopping Lists**: Consolidated, categorized lists that exclude pantry staples
- **Auto-Save Functionality**: Shopping lists saved to `shopping_list.md` automatically
- **Session Memory**: Meal plans persisted for future reference
- **Beautiful CLI**: Rich terminal interface with progress indicators and formatted output

## 🏗️ Architecture

The system uses three specialized agents that work together:

```
┌─────────────────┐
│  RecipeAgent    │ ──> Google Search Tool
│  (Research)     │ <── User Feedback Loop
└────────┬────────┘
         │ Approved Recipes
         ▼
┌─────────────────┐
│ NutritionAgent  │ ──> Internal Knowledge
│  (Analysis)     │ 
└────────┬────────┘
         │ Health Report
         ▼
┌─────────────────┐
│ ShoppingAgent   │ ──> Pantry Staples Tool
│  (Logistics)    │ ──> File Save Tool
└─────────────────┘
```

### Agent Responsibilities

1. **RecipeAgent**: 
   - Searches the web for recipes using Google Search integration
   - Returns structured JSON with recipe details
   - Iteratively refines based on user feedback

2. **NutritionAgent**: 
   - Analyzes nutritional profiles of approved recipes
   - Compares macro distributions
   - Highlights the healthiest option

3. **ShoppingAgent**: 
   - Consolidates ingredients across recipes
   - Removes common pantry staples
   - Groups items by category
   - Saves final list to disk

## 📋 Prerequisites

- Python 3.8+
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/app/apikey))

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Alish-0x/Smart-Meal-Prep-Agent-.git
cd Smart-Meal-Prep-Agent-
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your-actual-api-key-here
MODEL_NAME=gemini-2.0-flash
```

⚠️ **Important**: Replace `your-actual-api-key-here` with your real Google API key.

## 🎮 Usage

### Basic Flow

1. **Start the application**
```bash
python App.py
```

2. **Enter your meal request**
```
What would you like to cook? > healthy vegetarian dinners
```

3. **Review & Refine**
   - The system displays 3-4 recipe options in a formatted table
   - Press **Enter** to approve, OR
   - Type feedback like: `"make them spicier"`, `"add more protein"`, `"swap dish 2 for something vegan"`

4. **Automatic Processing**
   - Once approved, nutrition analysis runs automatically
   - Shopping list generates and saves to `shopping_list.md`

### Example Session

```
🍽️  Smart Meal Prep Agent
Interactive Mode | Human-in-the-Loop Enabled

✓ System Ready

What would you like to cook? > quick Asian-inspired meals

👩‍🍳 Recipe Agent is researching...

┌─────────────── 🍽️  Proposed Menu ────────────────────┐
│ Dish Name              │ Prep Time │ Key Ingredients │
├────────────────────────┼───────────┼─────────────────┤
│ Teriyaki Chicken Bowl  │ 25 min    │ chicken, soy... │
│ Pad Thai               │ 30 min    │ rice noodles... │
│ Miso Glazed Salmon     │ 20 min    │ salmon, miso... │
└────────────────────────┴───────────┴─────────────────┘

Options: (Enter) to Approve, or type feedback to Refine.
Critique > make one vegetarian

Feedback received: 'make one vegetarian'. Agent is updating...

[Updated recipes displayed...]

Critique > [Enter]

✓ Menu Approved! Proceeding to analysis...
🥗 Nutrition Agent Analyzing...
✓ Analysis Complete

[Nutrition Report]

🛒 Shopping Agent Optimizing...
✓ List Generated

[Shopping List]

✓ Plan persisted to session memory
```

## 📁 Project Structure

```
smart-meal-prep-agent/
├── App.py                 # Main application & UI logic
├── agents.py              # Agent class definitions
├── tools.py               # Custom tools & mock services
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (API keys)
├── shopping_list.md       # Generated output (auto-created)
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | (required) | Your Google AI Studio API key |
| `MODEL_NAME` | `gemini-2.0-flash` | Gemini model to use |

### Agent Customization

You can modify agent behavior by editing their system instructions in `agents.py`:

- **Temperature**: Adjust `temperature` in `BaseAgent.__init__` (default: 0.7)
- **Retry Logic**: Modify `retries` parameter in `send_message()` method
- **Recipe Count**: Change the prompt in `App.py` from `"Find 3-4..."` to any number

## 🛠️ Available Tools

| Tool | Purpose | Used By |
|------|---------|---------|
| `google_search` | Web search for recipes | RecipeAgent |
| `get_pantry_staples` | Returns common ingredients list | ShoppingAgent |
| `save_to_file` | Writes content to disk | ShoppingAgent |
| `calculate_macros` | Mock nutritional calculation | (Available but unused) |

## 📝 Output Files

- **`shopping_list.md`**: Markdown-formatted shopping list with checkboxes
- Format example:
```markdown
## Shopping List

### Proteins
- [ ] 2 lbs chicken breast
- [ ] 1 lb salmon

### Produce
- [ ] 2 bell peppers
- [ ] 1 bunch cilantro
```

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify the key is on the line `GOOGLE_API_KEY=your-key-here` (no spaces)
- Check that `python-dotenv` is installed

### Agent returns errors instead of recipes
- Check API key validity at [Google AI Studio](https://aistudio.google.com/)
- Verify internet connection (required for Google Search)
- Check rate limits on your API key

### JSON parsing errors
- The RecipeAgent has robust cleanup logic
- If issues persist, check the `raw_recipes` output in debug mode
- Ensure model name is correct in `.env`

## 🔮 Future Enhancements

- [ ] Add web scraping for full recipe instructions
- [ ] Integrate with grocery delivery APIs
- [ ] Export to Google Calendar for meal scheduling
- [ ] Multi-language support
- [ ] Dietary restriction filters (allergies, kosher, etc.)
- [ ] Cost estimation per meal
- [ ] Batch cooking optimization

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

## 💬 Support

For issues or questions:
- Open an issue on GitHub


---

**Built with ❤️ **