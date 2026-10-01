#!/usr/bin/env python3
"""
verify_nutrition.py
Deterministic nutritional verification engine for Weekly Table meal catalogue.
Sources:
  - FSANZ (Food Standards Australia New Zealand) AFCD (Release 2)
  - Australian Supermarket Mandatory NIP (Nutrition Information Panel) from Coles & Woolworths
"""

from verify_system import FOOD_DATABASE, RECIPE_SPECS, calc_nutrition

if __name__ == "__main__":
    print("=" * 80)
    print("PROFILE 1: STANDARD ATHLETIC TARGET (Athletic Target: 44g+ Protein | ~500 kcal)")
    print("=" * 80 + "\n")
    for r_id, spec in RECIPE_SPECS.items():
        res = calc_nutrition(spec["standard_servings"], spec["standard_ingredients_raw"])
        ps = res["per_serving"]
        print(f"{r_id}: {spec['title']} ({spec['standard_servings']} servings)")
        print(f"  -> {ps['protein']}g Protein | {ps['carbs']}g Carbs ({ps['fiber']}g Fiber) | {ps['fat']}g Fat | {ps['cals']} kcal")

    print("\n" + "=" * 80)
    print("PROFILE 2: MILD DEFICIT & ENDO BALANCE (Mild Deficit & Endo Balance: 35-44g Protein | ~380 kcal)")
    print("=" * 80 + "\n")
    for r_id, spec in RECIPE_SPECS.items():
        res = calc_nutrition(spec["deficit_servings"], spec["deficit_ingredients_raw"])
        ps = res["per_serving"]
        print(f"{r_id}: {spec['title']} (Deficit)")
        print(f"  -> {ps['protein']}g Protein | {ps['carbs']}g Carbs ({ps['fiber']}g Fiber) | {ps['fat']}g Fat | {ps['cals']} kcal")
        print(f"  Plate Split: {spec['deficit_portion_tip']}\n")
