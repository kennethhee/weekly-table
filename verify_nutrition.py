#!/usr/bin/env python3
"""
verify_nutrition.py
Deterministic nutritional verification engine for Weekly Table meal catalogue.
Sources:
  - FSANZ (Food Standards Australia New Zealand) AFCD (Release 2)
  - Australian Supermarket Mandatory NIP (Nutrition Information Panel) from Coles & Woolworths
"""

# Ground-truth nutrient composition per 100g (or 100ml)
# [Protein_g, Carbs_g, Fiber_g, Fat_g, Calories_kcal, Source]
FOOD_DATABASE = {
    # Proteins (Raw/Fresh)
    "chicken_breast_raw": {
        "name": "Chicken Breast, skinless, raw (Coles/Woolworths RSPCA)",
        "protein": 22.5, "carbs": 0.0, "fiber": 0.0, "fat": 1.5, "cals": 105,
        "source": "FSANZ AFCD F002258 / Pack NIP"
    },
    "turkey_mince_raw": {
        "name": "Turkey Breast Mince, raw (Ingham's / Woolworths)",
        "protein": 21.8, "carbs": 0.0, "fiber": 0.0, "fat": 2.5, "cals": 110,
        "source": "Ingham's NIP / FSANZ F008901"
    },
    "atlantic_salmon_raw": {
        "name": "Atlantic Salmon, raw skin-on fillet (Woolworths/Tassal)",
        "protein": 20.4, "carbs": 0.0, "fiber": 0.0, "fat": 13.0, "cals": 202,
        "source": "FSANZ AFCD F007551 / Tassal NIP"
    },
    "barramundi_raw": {
        "name": "Barramundi Fillet, raw skin-on (Coles/Woolworths)",
        "protein": 20.0, "carbs": 0.0, "fiber": 0.0, "fat": 2.5, "cals": 104,
        "source": "FSANZ AFCD F000492"
    },
    "cod_fillet_raw": {
        "name": "Cod / White Fish Fillets, raw",
        "protein": 18.0, "carbs": 0.0, "fiber": 0.0, "fat": 0.8, "cals": 82,
        "source": "FSANZ AFCD F003112"
    },
    "tofu_firm_macro": {
        "name": "Macro Organic Firm Tofu (Woolworths)",
        "protein": 12.0, "carbs": 1.2, "fiber": 1.8, "fat": 5.5, "cals": 106,
        "source": "Woolworths Macro NIP"
    },
    "bone_broth_chicken": {
        "name": "Chicken Bone Broth (Woolworths/Tonrick)",
        "protein": 3.6, "carbs": 0.4, "fiber": 0.0, "fat": 0.3, "cals": 19,
        "source": "Macro Bone Broth NIP"
    },

    # Legumes & Pulses (Canned, rinsed & drained per 100g)
    "chickpeas_canned_drained": {
        "name": "Chickpeas, canned, rinsed & drained",
        "protein": 6.8, "carbs": 15.2, "fiber": 5.8, "fat": 1.6, "cals": 116,
        "source": "Coles/Woolies Brand NIP / FSANZ"
    },
    "black_beans_canned_drained": {
        "name": "Black Beans, canned, rinsed & drained",
        "protein": 7.2, "carbs": 16.0, "fiber": 6.5, "fat": 0.8, "cals": 114,
        "source": "Edgell / Coles Brand NIP"
    },
    "cannellini_canned_drained": {
        "name": "Cannellini Beans, canned, rinsed & drained",
        "protein": 6.9, "carbs": 14.5, "fiber": 6.2, "fat": 0.6, "cals": 105,
        "source": "Coles/Woolies Brand NIP"
    },
    "butter_beans_canned_drained": {
        "name": "Butter Beans, canned, rinsed & drained",
        "protein": 6.5, "carbs": 14.0, "fiber": 5.5, "fat": 0.6, "cals": 102,
        "source": "Woolies Brand NIP"
    },
    "brown_lentils_canned_drained": {
        "name": "Brown Lentils, canned, rinsed & drained",
        "protein": 7.0, "carbs": 14.8, "fiber": 4.5, "fat": 0.5, "cals": 102,
        "source": "Woolies / FSANZ F004860"
    },

    # Grains (Dry / Raw per 100g)
    "jasmine_rice_dry": {
        "name": "Jasmine Fragrant White Rice, dry (SunRice)",
        "protein": 7.5, "carbs": 79.0, "fiber": 1.8, "fat": 0.8, "cals": 355,
        "source": "SunRice Pack NIP"
    },
    "brown_rice_dry": {
        "name": "Brown Rice, dry (SunRice)",
        "protein": 7.8, "carbs": 73.0, "fiber": 4.2, "fat": 2.5, "cals": 360,
        "source": "SunRice Pack NIP"
    },
    "quinoa_dry": {
        "name": "Quinoa, raw tricolour (Macro Organic)",
        "protein": 13.5, "carbs": 62.0, "fiber": 7.0, "fat": 5.8, "cals": 372,
        "source": "Macro Organic Pack NIP"
    },
    "wrap_gluten_free": {
        "name": "Simson's / Helga's Gluten-Free Wrap (per 100g ~ 2 wraps)",
        "protein": 4.2, "carbs": 48.0, "fiber": 5.2, "fat": 6.8, "cals": 280,
        "source": "Simson's / BFree NIP"
    },

    # Dairy / Fermented
    "chobani_greek_yogurt": {
        "name": "Chobani Whole Milk Plain Greek Yogurt",
        "protein": 9.2, "carbs": 3.8, "fiber": 0.0, "fat": 4.0, "cals": 88,
        "source": "Chobani 907g Tub NIP"
    },

    # Oils & Fats
    "extra_virgin_olive_oil": {
        "name": "Cobram Estate Extra Virgin Olive Oil",
        "protein": 0.0, "carbs": 0.0, "fiber": 0.0, "fat": 92.0, "cals": 828,
        "source": "Cobram Estate NIP (100ml = 92g fat)"
    },
    "tahini_unhulled": {
        "name": "Macro Organic Unhulled Tahini",
        "protein": 22.0, "carbs": 6.5, "fiber": 9.0, "fat": 54.0, "cals": 620,
        "source": "Macro Tahini NIP"
    },
    "avocado_fresh": {
        "name": "Hass Avocado, fresh flesh",
        "protein": 1.6, "carbs": 1.8, "fiber": 4.8, "fat": 15.0, "cals": 160,
        "source": "FSANZ AFCD F000216"
    },
    "kalamata_olives": {
        "name": "Kalamata Olives, pitted",
        "protein": 1.1, "carbs": 1.2, "fiber": 3.2, "fat": 16.0, "cals": 165,
        "source": "Always Fresh / FSANZ"
    },

    # Produce (per 100g raw)
    "tomatoes_crushed_canned": {
        "name": "Canned Diced / Crushed Italian Tomatoes",
        "protein": 1.2, "carbs": 3.8, "fiber": 1.1, "fat": 0.2, "cals": 24,
        "source": "Mutti / Woolies Italian NIP"
    },
    "cherry_tomatoes": {
        "name": "Cherry Tomatoes, fresh",
        "protein": 1.0, "carbs": 3.5, "fiber": 1.2, "fat": 0.2, "cals": 20,
        "source": "FSANZ AFCD F008681"
    },
    "broccoli_raw": {
        "name": "Broccoli / Broccolini, raw",
        "protein": 3.2, "carbs": 2.2, "fiber": 3.0, "fat": 0.4, "cals": 28,
        "source": "FSANZ AFCD F001155"
    },
    "zucchini_raw": {
        "name": "Zucchini, raw unpeeled",
        "protein": 1.4, "carbs": 2.1, "fiber": 1.1, "fat": 0.2, "cals": 16,
        "source": "FSANZ AFCD F009581"
    },
    "baby_spinach_raw": {
        "name": "Baby Spinach, fresh raw",
        "protein": 2.8, "carbs": 1.4, "fiber": 2.2, "fat": 0.4, "cals": 22,
        "source": "FSANZ AFCD F008323"
    },
    "button_mushrooms_raw": {
        "name": "White Button / Cup Mushrooms, raw",
        "protein": 2.5, "carbs": 2.0, "fiber": 1.5, "fat": 0.2, "cals": 22,
        "source": "FSANZ AFCD F005705"
    },
    "capsicum_raw": {
        "name": "Red Capsicum, raw",
        "protein": 1.0, "carbs": 4.5, "fiber": 1.8, "fat": 0.2, "cals": 26,
        "source": "FSANZ AFCD F001550"
    },
    "sweet_potato_raw": {
        "name": "Gold Sweet Potato, raw peeled",
        "protein": 1.5, "carbs": 18.0, "fiber": 3.0, "fat": 0.1, "cals": 86,
        "source": "FSANZ AFCD F008455"
    },
    "cucumber_raw": {
        "name": "Lebanese Cucumber, fresh unpeeled",
        "protein": 0.8, "carbs": 1.8, "fiber": 0.8, "fat": 0.1, "cals": 12,
        "source": "FSANZ AFCD F003440"
    },
    "sweet_corn_canned": {
        "name": "Sweet Corn kernels, canned drained",
        "protein": 2.8, "carbs": 14.5, "fiber": 2.5, "fat": 1.1, "cals": 80,
        "source": "Woolies NIP"
    }
}

def calc_recipe(name, servings, ingredients):
    """
    ingredients: list of (food_key, grams_total)
    """
    tot_p = 0.0
    tot_c = 0.0
    tot_fib = 0.0
    tot_f = 0.0
    tot_cal = 0.0

    breakdown = []
    for key, grams in ingredients:
        item = FOOD_DATABASE[key]
        ratio = grams / 100.0
        p = item["protein"] * ratio
        c = item["carbs"] * ratio
        fib = item["fiber"] * ratio
        f = item["fat"] * ratio
        cal = item["cals"] * ratio

        tot_p += p
        tot_c += c
        tot_fib += fib
        tot_f += f
        tot_cal += cal

        breakdown.append({
            "name": item["name"],
            "grams": grams,
            "protein": p,
            "carbs": c,
            "fiber": fib,
            "fat": f,
            "cals": cal,
            "source": item["source"]
        })

    per_serv = {
        "protein": round(tot_p / servings, 1),
        "carbs": round(tot_c / servings, 1),
        "fiber": round(tot_fib / servings, 1),
        "fat": round(tot_f / servings, 1),
        "cals": round(tot_cal / servings)
    }

    return {
        "name": name,
        "servings": servings,
        "per_serving": per_serv,
        "breakdown": breakdown
    }

# 12 Recipes from CATALOG
RECIPES = [
    # Container 1 (4 Servings)
    {
        "id": "c1_opt1",
        "name": "Greek Lemon-Oregano Chicken, Chickpea & Rice Glass Bake",
        "servings": 4,
        "ingredients": [
            ("chicken_breast_raw", 700),
            ("jasmine_rice_dry", 190),       # ~1 cup dry
            ("chickpeas_canned_drained", 240), # 1 tin drained
            ("cherry_tomatoes", 250),
            ("kalamata_olives", 50),
            ("bone_broth_chicken", 500),
            ("extra_virgin_olive_oil", 14),   # 1 tbsp
            ("cucumber_raw", 200)
        ]
    },
    {
        "id": "c1_opt2",
        "name": "Smoky Chipotle Chicken, Black Bean & Rice Glass Bake",
        "servings": 4,
        "ingredients": [
            ("chicken_breast_raw", 700),
            ("jasmine_rice_dry", 190),
            ("black_beans_canned_drained", 240),
            ("capsicum_raw", 250),
            ("sweet_corn_canned", 120),
            ("bone_broth_chicken", 500),
            ("extra_virgin_olive_oil", 14)
        ]
    },
    {
        "id": "c1_opt3",
        "name": "Tuscan Herb Chicken, Mushroom & Cannellini Glass Bake",
        "servings": 4,
        "ingredients": [
            ("chicken_breast_raw", 700),
            ("quinoa_dry", 180),
            ("cannellini_canned_drained", 240),
            ("button_mushrooms_raw", 300),
            ("baby_spinach_raw", 120),
            ("bone_broth_chicken", 500),
            ("extra_virgin_olive_oil", 14)
        ]
    },

    # Container 2 (6 Servings: Mon-Wed dinners for 2)
    {
        "id": "c2_opt1",
        "name": "Mediterranean Turkey & Cannellini Bean Cacciatore",
        "servings": 6,
        "ingredients": [
            ("turkey_mince_raw", 1000),         # 2 x 500g standard trays
            ("cannellini_canned_drained", 480), # 2 tins drained
            ("tomatoes_crushed_canned", 800),   # 2 tins
            ("button_mushrooms_raw", 400),
            ("zucchini_raw", 400),
            ("extra_virgin_olive_oil", 28),     # 2 tbsp
            ("kalamata_olives", 60)
        ]
    },
    {
        "id": "c2_opt2",
        "name": "Moroccan Turkey & Chickpea Tagine with Sweet Potato",
        "servings": 6,
        "ingredients": [
            ("turkey_mince_raw", 1000),         # 2 x 500g standard trays
            ("chickpeas_canned_drained", 480),
            ("sweet_potato_raw", 500),
            ("tomatoes_crushed_canned", 800),
            ("baby_spinach_raw", 200),
            ("extra_virgin_olive_oil", 28)
        ]
    },
    {
        "id": "c2_opt3",
        "name": "French Provençal Chicken & White Butter Bean Stew",
        "servings": 6,
        "ingredients": [
            ("chicken_breast_raw", 1000),       # 1kg diced breast
            ("butter_beans_canned_drained", 480),
            ("tomatoes_crushed_canned", 800),
            ("zucchini_raw", 400),
            ("button_mushrooms_raw", 350),
            ("extra_virgin_olive_oil", 28),
            ("bone_broth_chicken", 250)
        ]
    },

    # Container 3 (4 Servings: Thu-Fri dinners for 2)
    {
        "id": "c3_opt1",
        "name": "Crispy Tasmanian Salmon & Turmeric Lentils with Charred Broccolini",
        "servings": 4,
        "ingredients": [
            ("atlantic_salmon_raw", 600),       # 4 x 150g fillets
            ("brown_lentils_canned_drained", 480), # 2 tins
            ("broccoli_raw", 300),              # 2 bunches broccolini
            ("baby_spinach_raw", 150),
            ("extra_virgin_olive_oil", 20)      # 1.5 tbsp
        ]
    },
    {
        "id": "c3_opt2",
        "name": "Barramundi Fillets with Lemon Tahini Lentils & Sautéed Greens",
        "servings": 4,
        "ingredients": [
            ("barramundi_raw", 600),            # 4 x 150g fillets
            ("brown_lentils_canned_drained", 480),
            ("tahini_unhulled", 40),            # 2 tbsp
            ("broccoli_raw", 300),
            ("baby_spinach_raw", 150),
            ("extra_virgin_olive_oil", 14)
        ]
    },
    {
        "id": "c3_opt3",
        "name": "Spanish Paprika Cod & Cannellini Bean Skillet with Spinach",
        "servings": 4,
        "ingredients": [
            ("cod_fillet_raw", 700),            # 4 x 175g fillets
            ("cannellini_canned_drained", 480),
            ("tomatoes_crushed_canned", 400),
            ("capsicum_raw", 200),
            ("baby_spinach_raw", 200),
            ("kalamata_olives", 40),
            ("extra_virgin_olive_oil", 20)
        ]
    },

    # Container 4 (4 Servings: Sat-Sun wraps/bowls for 2)
    {
        "id": "c4_opt1",
        "name": "Grilled Spiced Chicken Souvlaki Wraps with Chobani Dill Tzatziki",
        "servings": 4,
        "ingredients": [
            ("chicken_breast_raw", 700),
            ("wrap_gluten_free", 200),          # 4 wraps (~50g ea)
            ("chobani_greek_yogurt", 250),      # ~1 cup Greek yogurt
            ("cucumber_raw", 150),              # grated into tzatziki
            ("cherry_tomatoes", 150),
            ("extra_virgin_olive_oil", 14)
        ]
    },
    {
        "id": "c4_opt2",
        "name": "Smoky Paprika Chicken & Black Bean Burrito Bowls with Avocado",
        "servings": 4,
        "ingredients": [
            ("chicken_breast_raw", 700),
            ("black_beans_canned_drained", 240),
            ("quinoa_dry", 160),
            ("avocado_fresh", 150),             # ~1 medium avocado
            ("cherry_tomatoes", 200),
            ("chobani_greek_yogurt", 150),
            ("extra_virgin_olive_oil", 14)
        ]
    },
    {
        "id": "c4_opt3",
        "name": "Herb-Marinated Grilled Tofu & Mediterranean Quinoa Bowl with Tzatziki",
        "servings": 4,
        "ingredients": [
            ("tofu_firm_macro", 900),           # 2 x 450g blocks
            ("quinoa_dry", 180),
            ("chobani_greek_yogurt", 250),
            ("cucumber_raw", 200),
            ("cherry_tomatoes", 200),
            ("kalamata_olives", 50),
            ("extra_virgin_olive_oil", 20)
        ]
    }
]

if __name__ == "__main__":
    print("================================================================================")
    print("NUTRITIONAL VERIFICATION AUDIT REPORT (FSANZ AFCD & AUSTRALIAN SUPERMARKET NIP)")
    print("================================================================================\n")

    for r in RECIPES:
        res = calc_recipe(r["name"], r["servings"], r["ingredients"])
        ps = res["per_serving"]
        print(f"RECIPE: {r['name']} ({r['servings']} servings)")
        print(f"PER SERVING MACROS: {ps['protein']}g Protein | {ps['carbs']}g Carbs ({ps['fiber']}g Fiber) | {ps['fat']}g Fat | {ps['cals']} kcal")
        print("-" * 80)
        print(f"{'Ingredient':<45} {'Weight':<8} {'Prot(g)':<8} {'Carb(g)':<8} {'Fib(g)':<8} {'Fat(g)':<8} {'kcal':<6}")
        print("-" * 80)
        for b in res["breakdown"]:
            print(f"{b['name'][:44]:<45} {b['grams']:>5}g   {b['protein']:>6.1f}   {b['carbs']:>6.1f}   {b['fiber']:>6.1f}   {b['fat']:>6.1f}  {b['cals']:>5.0f}")
        print("=" * 80 + "\n")
