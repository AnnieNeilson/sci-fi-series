import gspread
from google.oauth2.service_account import Credentials
import instructions

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sci_fi_series_database')

series_data = SHEET.worksheet('data')
titles = series_data.get_all_values()


def user_response_int():
    """
    gets response from the user
    """
    while True:
        response = input(">")
        if is_response_menu(response):
            break
        if validate_menu_response(response):
            break
    return response


def is_response_menu(response):
    """
    Checks the user input and calls the new search function
    which brings up the menu so the user can start a new
    search
    """
    if response.lower().strip() == "menu":
        new_search()


def validate_menu_response(response):
    """
    Inside the try the string value is converted into integers,
    It raises ValueError if it can't convert into ints or if there are too
    many numbers
    """
    try:
        if int(response) > 5:
            raise ValueError("Enter a number from 1-5")
        elif int(response) < 1:
            raise ValueError("Enter a number from 1-5")
    except ValueError as e:
        print(f"Invalid response: {e}, please try again.\n")
        return False
    return True


def menu_answers(choice):
    """
    selects category depending on users intial response
    """
    if int(choice) == 1:
        category = "title"
        column = 1
    elif int(choice) == 2:
        category = "sub-genre"
        column = 3
    elif int(choice) == 3:
        category = "release year"
        column = 6
    elif int(choice) == 4:
        category = "creator"
        column = 4
    elif int(choice) == 5:
        category = "actors"
        column = 5
    else:
        print("Error")
    # chosen_search(category, column)
    return category, column


def chosen_search(chosen, column):
    """
    Prints instructions to the user regarding their last input
    """
    keyword = str(input(f"You've chosen to search by {chosen}. Type in a relevant"
                    " search term:\n>")).strip()
    # search_columns(keyword, chosen, column)
    return keyword


def find_row(item_cell):
    """
    Finds the row of a specific cell, so other items can be found from
    this number.
    """
    row_index = item_cell.index("R", 1)
    col_ind = item_cell.index("C", 2)
    row_ind = row_index + 1
    row_num = item_cell[row_ind:col_ind]
    return row_num


def validate_dict_keys(key, dictionary):
    """
    Ensures the user input is a valid number
    """
    is_response_menu(key)
    try:
        if key.isdigit() is False:
            raise ValueError("That is not an option")
        if int(key) > len(dictionary):
            raise KeyError("That is not an option")
    except (KeyError, ValueError) as e:
        print(f"Invalid response: {e}, please try again.\n")
        return False
    return True


def validate_category_choice(key):
    """
    Ensures the user input, category choice, is a valid number
    """
    is_response_menu(key)
    try:
        if key.isdigit() is False:
            raise ValueError("That is not an option")
        elif int(key) > 9 or int(key) < 1:
            raise KeyError("That is not an option")
    except (KeyError, ValueError) as e:
        print(f"Invalid response: {e}, please try again.\n")
        return False
    return True


def reformat_cell_info(information):
    """
    Takes a string of information and splits it into
    a list. It then joins the items of the list into
    a new string, each item separated by a comma. This
    is used to make the information more presentable.
    """
    list_split = information.split('/')
    new_info = ', '.join(list_split)
    return new_info


def validate_yes_or_no(answer):
    """
    Checks that the user has answered either y or n
    if not the user is asked to answer again.
    """
    is_response_menu(answer)
    if answer == "y":
        return True
    elif answer == "n":
        return True
    else:
        print("That is not at option, please try again.")
        return False


def final_search_results(show, info_category, info):
    """
    Using information already received from the user, show title and
    area of interest this function returns the relevant information
    in an easy to understand format.
    """
    if info_category == 1:
        print(f"{show}:\n{info}")
    elif info_category == 2:
        genres = reformat_cell_info(info)
        print(f"Aside from science fiction, {show} has the following sub-genre"
              f"/s:\n{genres}")
    elif info_category == 3:
        creators = reformat_cell_info(info)
        print(f"{show} was created by:\n{creators}")
    elif info_category == 4:
        cast = reformat_cell_info(info)
        print(f"The cast of {show} includes:\n{cast}")
    elif info_category == 5:
        print(f"{show} was first released in {info}")
    elif info_category == 6:
        print(info)
    elif info_category == 7:
        print(f"{show} has {info} season/s.")
    elif info_category == 8:
        print(f"{show} received an audience score of {info} on Rotten Tomat"
              "oes.")
    else:
        print("something went wrong")
    while True:
        more_info = input(f"Would you like to find out more about {show}? y/n"
                          "\n>").lower().strip()
        if validate_yes_or_no(more_info):
            break
    if more_info == "y":
        search_in_show_choice(show)
    elif more_info == "n":
        new_search()


def new_search():
    """
    Asks the user if they would like to start a new search,
    if not the program exits
    """
    while True:
        start_new_search = input("Would you like to start a new search? y/n"
                                 "\n>").lower().strip()
        if validate_yes_or_no(start_new_search):
            break
    if start_new_search == "y":
        main()
    elif start_new_search == "n":
        print("I hope you found everything you were looking for,\nGoodbye!")
        exit()


def final_results_return_all(row):
    """
    the user wants to know all the available information on
    a show this function is called.
    It retrieves all the relevant data and returns it to the
    user in a way that is easy to read and understand.
    """
    show_info = SHEET.worksheet('data').row_values(row)
    print(f"All available information on {show_info[0]}:\nDescription:"
          f"\n{show_info[1]}\n")
    sub_genres = reformat_cell_info(show_info[2])
    creators = reformat_cell_info(show_info[3])
    actors = reformat_cell_info(show_info[4])
    print(f"Sub-genres:\n{sub_genres}\n\nCreated by:\n{creators}\n\nStar"
          f"ring:\n{actors}\n")
    print(f"Release Date:\n{show_info[0]} first aired in {show_info[5]}\n"
          f"\nStill Running?\n{show_info[6]}\n\nNo. of Seasons:\n"
          f"{show_info[0]} has {show_info[7]} season/s.\n\nAudience Score:"
          f"\n{show_info[0]} was given a score of {show_info[8]} on Rotten"
          " Tomatoes.\n")
    new_search()


def search_in_show_choice(show):
    """
    Offers the user a selection of categories to choose from
    to find further information.
    """
    while True:
        category_choice = input(f"What would you like to know about {show}?"
                                f"\n{instructions.CATEGORIES}\n>")
        if validate_category_choice(category_choice):
            break
    cell = str(SHEET.worksheet('data').find(show))
    item_row = find_row(cell)
    item_col = int(category_choice) + 1
    info = str(SHEET.worksheet('data').cell(item_row, item_col).value)
    if int(category_choice) < 9:
        final_search_results(show, int(category_choice), info)
    else:
        final_results_return_all(item_row)


def search_in_dictionary(dictionary):
    """
    Checks length of dictionary, if more than 1, requests user choose an item.
    Offers user choice of categories for more information.
    """
    while True:
        if len(dictionary) > 1:
            dict_num = input("Which result would you like more information on?"
                             "\n>")
        else:
            dict_num = input("If you would like more information please type 1"
                             "\n>")
        if validate_dict_keys(dict_num, dictionary):
            break
    item_ind = int(dict_num) - 1
    show_title = str(dictionary[item_ind].split('-')[0]).strip()
    search_in_show_choice(show_title)


def results_list_to_string(result_lst):
    """
    Takes the list of search results and converts it to a string with
    numbers added for the user to use to make a new choice.
    """
    option = 0
    new_str = ''
    for item in result_lst:
        option += 1
        string = f"({option}) {item}\n"
        new_str += string
    return new_str


def add_title(search_term):
    """
    Takes a chosen search term and adds the relevant title
    returns a string with the two bits of data combined
    """
    cell = str(SHEET.worksheet('data').find(search_term))
    item_row = find_row(cell)
    item_title = SHEET.worksheet('data').cell(item_row, 1).value
    full_item = item_title + " - " + search_term
    return full_item


def print_search_results(lst):
    """
    Takes the returned search results, passes the
    list_to_string function, to make the results more aesthetically
    pleasing.
    Creates a dictionary of results so the separate items
    can still be accessed by the user.
    If there are no results it recalls the chosen_list function
    So the user can try a new search term.
    """
    if lst:
        results_str = results_list_to_string(lst)
        print(f"The following item/s matched your search:\n{results_str}")
        results_dict = dict(enumerate(lst))
        return True
        # search_in_dictionary(results_dict)
    elif not lst:
        print("No matching results, please try again.")
        return False
        # chosen_search(keyword, column)


def search_columns(keyword, column):
    """
    Searches through the column of selected category and compares the keyword
    to the items in the column.
    If any category other than 'title' is selected this function calls the
    add_title function, to create a new str with the appropriate title affixed
    If 'title' is selected this function is skipped.
    """
    is_response_menu(keyword)
    whole_chosen_col = SHEET.worksheet('data').col_values(column)
    chosen_col = whole_chosen_col[1:]
    search_results = []
    if column != 1:
        for item in chosen_col:
            if keyword.lower() in item.lower():
                full_item = add_title(item)
                search_results.append(full_item)
    elif column == 1:
        for item in chosen_col:
            if keyword.lower() in item.lower():
                search_results.append(item)
    return search_results
    # print_search_results(search_results)


def main():
    """
    Begins the program and when called again starts a new search
    """
    print(instructions.INSTRUCTIONS_DESCRIPTION)
    print(instructions.MENU)
    validated_response = user_response_int()
    category, column = menu_answers(validated_response)
    keyword = chosen_search(category, column)
    search_results = search_columns(keyword)
    if print_search_results(search_results):
        print("Remember where u were")
    if not print_search_results(search_results):
        print("jeez")




print(instructions.WELCOME)
main()
