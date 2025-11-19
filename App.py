import os
import json
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import our agents
from agents import RecipeAgent, NutritionAgent, ShoppingAgent
from tools import InMemorySessionService

load_dotenv()
console = Console()

def display_recipe_menu(raw_data):
    """Helper to visualize recipes in a clean table."""
    try:
        data = json.loads(raw_data)
        if isinstance(data, list):
            table = Table(title="🍽️  Proposed Menu", show_header=True, header_style="bold magenta")
            table.add_column("Dish Name", style="cyan")
            table.add_column("Prep Time", style="green")
            table.add_column("Key Ingredients (Preview)", style="dim")

            for item in data:
                # Handle varying keys just in case
                name = item.get("title", item.get("name", "Unknown"))
                time = item.get("prep_time", "N/A")
                # Join first 3 ingredients for preview
                ing = ", ".join(item.get("ingredients", [])[:3]) + "..."
                table.add_row(name, time, ing)
            
            console.print(table)
            return True # Success
    except:
        return False # Parsing failed, just show raw text

def main():
    # Check Key
    if not os.getenv("GOOGLE_API_KEY"):
        console.print("[bold red]CRITICAL ERROR:[/bold red] GOOGLE_API_KEY not found.")
        return

    # Header
    console.print(Panel(
        "[bold white]🍽️  Smart Meal Prep Agent[/bold white]\n"
        "[dim]Interactive Mode | Human-in-the-Loop Enabled[/dim]", 
        style="bold green", expand=False
    ))
    
    # Init Agents
    try:
        with console.status("[bold green]Booting Agent Swarm...[/bold green]"):
            session_db = InMemorySessionService()
            recipe_finder = RecipeAgent()
            nutrition_analyzer = NutritionAgent()
            shopping_generator = ShoppingAgent()
        console.print("[green]✓ System Ready[/green]\n")
    except Exception as e:
        console.print(f"[bold red]Startup Failed:[/bold red] {e}")
        return

    while True:
        try:
            user_query = console.input("[bold cyan]What would you like to cook? > [/bold cyan]")
            
            if user_query.lower() in ['exit', 'quit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            if not user_query.strip():
                continue

            # ==========================================
            # PHASE 1: INTERACTIVE RECIPE LOOP
            # ==========================================
            
            # Initial Prompt
            current_prompt = f"Find 3-4 high quality recipes for: {user_query}"
            approved_recipes = None

            while True:
                console.print()
                with console.status("[bold blue]👩‍🍳 Recipe Agent is researching...[/bold blue]", spinner="dots"):
                    # The agent class maintains chat history (self.chat), 
                    # so subsequent calls in this loop function as a conversation.
                    raw_recipes = recipe_finder.send_message(current_prompt)

                # 1. Show the User the Options
                is_valid_json = display_recipe_menu(raw_recipes)
                
                if not is_valid_json:
                    # Fallback if JSON breaks
                    console.print(Panel(raw_recipes, title="Recipe Output (Raw)", border_style="cyan"))

                # 2. Critique Loop
                console.print("\n[bold yellow]Options:[/bold yellow] [bold green](Enter)[/bold green] to Approve, or type feedback to Refine.")
                feedback = console.input("[bold magenta]Critique > [/bold magenta]")

                if not feedback.strip():
                    # User hit Enter -> Approved
                    console.print("[green]✓ Menu Approved! Proceeding to analysis...[/green]")
                    approved_recipes = raw_recipes
                    break
                else:
                    # User gave feedback -> Loop context
                    console.print(f"[dim]Feedback received: '{feedback}'. Agent is updating...[/dim]")
                    current_prompt = (
                        f"The user has this feedback: '{feedback}'. "
                        "Please adjust the list and output a NEW JSON array with the changes. "
                        "Keep the same JSON format."
                    )

            # ==========================================
            # PHASE 2: EXECUTION (Nutrition & Shopping)
            # ==========================================
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                transient=False,
            ) as progress:
                
                # ANALYSIS
                task2 = progress.add_task("🥗 Nutrition Agent Analyzing...", total=None)
                nutrition_report = nutrition_analyzer.send_message(
                    f"Analyze the nutrition for this approved data: {approved_recipes}"
                )
                progress.update(task2, completed=True, description="[green]✓ Analysis Complete[/green]")
                
                console.print(Panel(Markdown(nutrition_report), title="Nutritional Intelligence", border_style="magenta"))

                # LOGISTICS
                task3 = progress.add_task("🛒 Shopping Agent Optimizing...", total=None)
                shopping_list = shopping_generator.send_message(
                    f"Create a consolidated shopping list for these recipes: {approved_recipes}"
                )
                progress.update(task3, completed=True, description="[green]✓ List Generated[/green]")
                
                # Final Output
                console.print(Panel(Markdown(shopping_list), title="FINAL OUTPUT: Shopping List", border_style="green"))

                # Save State
                session_db.save_meal_plan({"query": user_query, "result": shopping_list})
                console.print("[dim]✓ Plan persisted to session memory[/dim]\n")
                
                # Reset Recipe Agent history for the next major User Query
                # (Optional: In a real app you might want to clear history here, 
                # but instantiating new agents per query is safer if memory is cheap)
                recipe_finder = RecipeAgent() 
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()