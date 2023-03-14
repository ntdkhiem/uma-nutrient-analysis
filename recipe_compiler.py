import json

from bs4 import BeautifulSoup

from menu_compiler import parse_name

CHOSEN_LIST = [
    "Berkshire_Dining_Commons__Friday_March_10.html",
    "Berkshire_Dining_Commons__Friday_March_24.html",
    "Berkshire_Dining_Commons__Monday_March_27.html",
    "Berkshire_Dining_Commons__Sunday_March_26.html",
    "Franklin_Dining_Commons__Sunday_March_19.html",
    "Franklin_Dining_Commons__Friday_March_10.html",
    "Franklin_Dining_Commons__Wednesday_March_22.html",
    "Franklin_Dining_Commons__Monday_March_27.html",
    "Hampshire_Dining_Commons__Tuesday_March_21.html",
    "Hampshire_Dining_Commons__Sunday_March_12.html",
    "Hampshire_Dining_Commons__Thursday_March_16.html",
    "Hampshire_Dining_Commons__Monday_March_27.html",
    "Worcester_Dining_Commons__Monday_March_20.html",
    "Worcester_Dining_Commons__Sunday_March_19.html",
    "Worcester_Dining_Commons__Tuesday_March_21.html",
    "Worcester_Dining_Commons__Wednesday_March_22.html",
]


def format_fn(recipe_name):
    # format to valid file name
    return "".join(c for c in recipe_name if c.isalnum())


if __name__ == "__main__":
    # 1) pick three random days from the four dining commons
    recipes_db = json.load(open("database.json", "r"))
    recipes_list = {}
    for day in CHOSEN_LIST:
        name, date = parse_name(day)
        if name not in recipes_list:
            recipes_list[name] = {}
        # append menu from database.json for this day
        for obj in recipes_db[name]:
            if obj["date"] == date:
                recipes_list[name][date] = obj["meals"]

        soup = BeautifulSoup(open(f"html_content/{day}", "r"), "html.parser")
        # get longmenu.aspx
        # for each shortmenumenus in this day
        for menu in recipes_list[name][date].keys():
            el = soup.find("div", string=menu)
            # locate the link: should be its parent's next sibling
            print(el.parent.find_next_sibling("td").find("a").get("href"))
        # -- locate the shortmenus
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
