# sub_agents/nutrition_meal_planning/agent.py

import os
import re
import requests
from requests_oauthlib import OAuth1

from google.adk.tools import LongRunningFunctionTool
from google.adk.agents import Agent


class FatSecretClient:
    def __init__(self):
        self.consumer_key    = os.getenv("FATSECRET_KEY")
        self.consumer_secret = os.getenv("FATSECRET_SECRET")
        if not (self.consumer_key and self.consumer_secret):
            raise ValueError("Set FATSECRET_KEY and FATSECRET_SECRET in your environment")

        
        self.auth = OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            signature_method="HMAC-SHA1",
            signature_type="QUERY"
        )

        self.base_url = "https://platform.fatsecret.com/rest/server.api"

    def search_foods(self, query: str, page_number: int = 0, max_results: int = 5):
        params = {
            "method":            "foods.search",
            "search_expression": query,
            "format":            "json",
            "page_number":       page_number,
            "max_results":       max_results,
        }
        resp = requests.get(self.base_url, params=params, auth=self.auth)
        resp.raise_for_status()
        return resp.json()

    def get_food(self, food_id: str):
        params = {
            "method":  "food.get",
            "food_id": food_id,
            "format":  "json"
        }
        resp = requests.get(self.base_url, params=params, auth=self.auth)
        resp.raise_for_status()
        return resp.json()


_fs = FatSecretClient()


def fatsecret_search_tool(query: str) -> str:
    """
    Search FatSecret for foods matching `query` and return a formatted summary
    of the top results, including:
      - Food name
      - Calories per serving
      - Macronutrient breakdown (protein / carbs / fats)
      - Portion size
    Always appends “Data provided by FatSecret” at the end.
    """
    data  = _fs.search_foods(query)
    foods = data.get("foods", {}).get("food") or []
    if not foods:
        return f"No foods found for “{query}”."

    output = []
    for idx, item in enumerate(foods[:3], start=1):
        name = item.get("food_name", "Unknown")
        desc = item.get("food_description", "")

        cal = prot = carb = fat = "N/A"
        portion_amount = portion_unit = ""

        m = re.match(
            r"Per\s*([\d\.]+)\s*(g|ml)\s*-\s*Calories:\s*([\d\.]+)kcal"
            r"\s*\|\s*Fat:\s*([\d\.]+)g"
            r"\s*\|\s*Carbs:\s*([\d\.]+)g"
            r"\s*\|\s*Protein:\s*([\d\.]+)g",
            desc
        )
        if m:
            portion_amount, portion_unit = m.group(1), m.group(2)
            cal, fat, carb, prot = m.group(3), m.group(4), m.group(5), m.group(6)
        else:
            
            fid     = item["food_id"]
            details = _fs.get_food(fid).get("food", {})

            portions = details.get("food_portions", {}).get("food_portion", [])
            if portions:
                portion = portions[0]
                portion_amount = portion.get("metric_serving_amount", "")
                portion_unit   = portion.get("metric_serving_unit", "")

            serving = details.get("serving_sizes", {}).get("serving_size", {})
            cal  = serving.get("calories",     "N/A")
            prot = serving.get("protein",      "N/A")
            carb = serving.get("carbohydrate", "N/A")
            fat  = serving.get("fat",          "N/A")

        output.append(
            f"{idx}. **{name}** — {cal} kcal | P: {prot}g • C: {carb}g • F: {fat}g\n"
            f"   • Portion: {portion_amount} {portion_unit}"
        )

    return "\n".join(output)


fatsecret_tool = LongRunningFunctionTool(fatsecret_search_tool)


nutrition_meal_planning = Agent(
    name="nutrition_meal_planning",
    model="gemini-2.0-flash-exp",
    description="Nutrition Meal Planning agent (FatSecret only — no links).",
    instruction="""
Whenever the user asks about nutrient amounts (calories, protein, carbs, fats)
or basic meal-nutrition for a single food, call the `fatsecret_search_tool`
with their food item as `query` and return exactly the tool’s output.
If the results are fetched via the FatSecret API, append “Data provided by FatSecret” to the end.
""",
    tools=[fatsecret_tool]
)
