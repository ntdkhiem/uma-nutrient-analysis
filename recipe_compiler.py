import json
import random
from datetime import datetime

from bs4 import BeautifulSoup

from menu_compiler import parse_name

def format_fn(recipe_name):
    # format to valid file name
    return "".join(c for c in recipe_name if c.isalnum())

def format_fnd(dining_hall, date):
    # format date
    date = datetime.strptime(date, '%m/%d/%Y')
    return f"{dining_hall}__{date.strftime('%A_%B_%#d')}.html"


def pick_dates(recipes_db):
    """Pick 3 random dates from each dining hall that have recipes in the database"""
    dates = []
    for dining_hall in recipes_db.keys():
        hall_dates = []
        i = 0
        while i < 3:
            date_obj = random.choice(recipes_db[dining_hall])
            if date_obj not in hall_dates and date_obj["meals"]:
                hall_dates.append(format_fnd(dining_hall, date_obj["date"]))
                i += 1
        dates.extend(hall_dates)
    return dates


if __name__ == "__main__":
    recipes_db = json.load(open("database.json", "r"))
    recipes_list = {}
    chosen_dates = pick_dates(recipes_db)
    for day in chosen_dates:
        name, date = parse_name(day)
        if name not in recipes_list:
            recipes_list[name] = {}
        # append menu from database.json for this day
        for obj in recipes_db[name]:
            if obj["date"] == date:
                recipes_list[name][date] = obj["meals"]

        soup = BeautifulSoup(open(f"html_content/{day}", "r"), "html.parser")
        # get longmenu.aspx for each short menu
        for menu in recipes_list[name][date].keys():
            # -- locate the shortmenus
            el = soup.find("div", string=menu)
            # locate the link: should be its parent's next sibling
            print(el.parent.find_next_sibling("td").find("a").get("href"))
        # -- find the longmenu.aspx link

    # for dining_hall in recipes_db:
    #     is_satisfied = False
    #     while not is_satisfied:
    #         recipes_list[dining_hall] = random.sample(recipes_db[dining_hall], 3)
    #         # make sure each chosen day has menu
    #         if all(obj["meals"] for obj in recipes_list[dining_hall]):
    #             is_satisfied = True

    #     # 2) collect longmenu.aspx link
    #     for obj in recipes_list[dining_hall]:
    #         soup = BeautifulSoup(
    #             open(f'html_content/{dining_hall}__{obj["date"].replace("/","_")}')
    #         )
    # 3) go to longmenu.aspx
    # 3a) for each element that matches any element in shortmenurecipes,
    #  download its page from its label.aspx
