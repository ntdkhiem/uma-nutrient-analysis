import os
import string
import json

from bs4 import BeautifulSoup


def format_string(text):
    # format string to remove non-ascii and only display printable strings
    return "".join(filter(lambda x: x in set(string.printable), text))


def get_recipes(meal):
    result = []
    current_category = ""
    current_category_recipes = []
    # get parent of the menu's meal (6 levels above)
    meal_parent_container = meal.parent.parent.parent.parent.parent.parent
    # get recipes' container
    el = meal_parent_container.find("div", class_="shortmenucats")
    recipes_parent_container = el.parent.parent.parent

    for element in recipes_parent_container.children:
        if element.name:
            if el := element.find("div", class_="shortmenucats"):
                # add previous category's recipes to result
                if current_category:
                    result.append(
                        {
                            "category": current_category,
                            "recipes": current_category_recipes,
                        }
                    )
                current_category = el.text.replace("-- ", "").replace(" --", "")
                current_category_recipes = []
            else:
                current_category_recipes.append(
                    {
                        "name": format_string(
                            element.find("div", class_="shortmenurecipes").text
                        ),
                        "nutrition_labels": [el.get("src") for el in element.find_all("img")],
                        # "nutrition_facts": {},
                        # "portion": {"quantity": 0, "unit": ""},  # unit: oz, whole
                    }
                )
    return result


def parse_name(file_name):
    file_name = file_name[: file_name.rfind(".")]
    # print(file_name)
    name = file_name[: file_name.find("__")]
    date = file_name[file_name.find("__") + 2 :]
    # print(name, date)
    _, month, day = date.split("_")
    date = f"{3 if month == 'March' else 4 if month == 'April' else 5}/{day}/2023"
    return name, date


if __name__ == "__main__":
    final_result = {}
    for file in os.listdir("html_content"):
        name, date = parse_name(file)

        print(f"Parsing {name}: {date}")
        # if does not exist, create empty list
        if name not in final_result:
            final_result[name] = []

        # refer to sample.json
        result = {"date": date, "meals": {}}

        soup = BeautifulSoup(open(f"html_content/{file}", "rb"), "html.parser")

        # make sure the date has meals
        if soup.find("div", class_="shortmenuinstructs").text != "No Data Available":
            meals = soup.find_all("div", class_="shortmenumeals")
            for meal in meals:
                result["meals"][meal.text] = get_recipes(meal)

        final_result[name].append(result)

    # Dumping to json
    with open("database.json", "w+") as f:
        print("Dumping to database.json")
        json.dump(final_result, f, ensure_ascii=False)
