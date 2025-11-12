

import json
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Attr
import re
from openai import OpenAI

client = OpenAI(api_key="sk-ktrgoptrgtrhghgfb")
dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
modules_table = dynamodb.Table("Modules")
area_data = dynamodb.Table("Areas")
starter_data = dynamodb.Table("Starters")

# === CLEAN GPT JSON ===
def clean_gpt_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

# === CALL GPT ===
def query_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=4096,
    )
    return response.choices[0].message.content

# === FETCH DATA ===
def get_area(area_name):
    result = area_data.scan(FilterExpression=Attr("RouteURL").eq(area_name))
    return result["Items"][0]

def get_modules(area_id):
    return modules_table.scan(FilterExpression=Attr("AreaID").eq(area_id))["Items"]

def get_starters(module_id):
    return starter_data.scan(FilterExpression=Attr("ModuleID").eq(module_id))["Items"]

# === MAIN LOGIC ===
area_name = "gtm-leadership"
area = get_area(area_name)
modules = get_modules(area["AreaID"])

output = []

area_description = "\n".join([f"{k}: {v}" for k, v in area.items()])
area_description_clean = re.sub(r"<.*?>", "", area_description)

for module in modules:
    module_name = module["Name"]
    starters = get_starters(module["ModuleID"])
    module_description = "\n".join([f"{k}: {v}" for k, v in module.items() if k != "Starters"])

    for starter in starters:
        starter_name = starter["Name"]
        starter_description = "\n".join([f"{k}: {v}" for k, v in starter.items()])

        # === PROMPT GPT ===
        prompt = f"""
You are a B2B marketing expert. Generate 15 Google search keyword strings based on the details below.
Return only a JSON array of objects with:
- search_string
- section (module name)
- category
- labels (e.g. ["Concept", "Tool"])
- intent (Informational, Navigational, Transactional)
- starter_name: {starter_name}
- module_name: {module_name}
- area_name: {area['Name']}

Area: {area_description_clean}
Module: {module_description}
Starter: {starter_description}
"""

        try:
            raw = query_gpt(prompt)
            cleaned = clean_gpt_json(raw)
            keywords = json.loads(cleaned)
            output.extend(keywords)
        except:
            print(f"❌ Skipped: {starter_name}")

# === SAVE CSV ===
df = pd.DataFrame(output)
df.to_csv("gtm_keywords.csv", index=False)
print("✅ Keywords saved to gtm_keywords.csv")
