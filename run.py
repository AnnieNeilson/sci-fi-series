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
        
        if validate_menu_response(response):
            break
    return response


def validate_menu_response(response):
    """
    Inside the try the string value is converted into integers,
    It raises ValueError if it can't convert into ints or if there are too 
    many numbers
    """
    try:
        [int(response)]
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
    chosen_search(category, column)


def chosen_search(chosen, column):
    """
    Prints instructions to the user regarding their last input
    """
    keyword = input(f"You've chosen to search by {chosen}. Type in a relevant search term:\n>")
    search_columns(keyword.strip(), chosen, column)


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
    try:
        if key.isdigit() == False:
            raise ValueError("That is not an option")
        elif int(key) > (len(dictionary) -1):
            raise KeyError("That is not an option")
    except (KeyError, ValueError) as e:
        print(f"Invalid response: {e}, please try again.\n")
        return False
    return True


def validate_category_choice(key):
    """
    Ensures the user input, category choice, is a valid number
    """
    try:
        if key.isdigit() == False:
            raise ValueError("That is not an option")
        elif int(key) > 9 or int(key) < 1:
            raise KeyError("That is not an option")
    except (KeyError, ValueError) as e:
        print(f"Invalid response: {e}, please try again.\n")
        return False
    return True


def reformat_info(information):
    """
    Takes a string of information and splits it into
    a list. It then joins the items of the list into
    a new string, each item separated by a comma. This
    is used to make the information more presentable.
    """
    list_split = information.split('/')
    new_info = ', '.join(list_split)
    return new_info


def final_search_results(show, info_category, info):
    """ 
    Using information already received from the user, show title and 
    area of interest this function returns the relevant information
    in an easy to understand format.
    """
    if info_category == 1:
        print(f"{show}:\n{info}")
    elif info_category == 2:
        genres = reformat_info(info)
        print(f"Aside from science fiction, {show} has the following sub-genre/s:\n{genres}")
    elif info_category == 3:
        creators = reformat_info(info)
        print(f"{show} was created by:\n{creators}")
    elif info_category == 4:
        cast = reformat_info(info)
        print(f"The cast of {show} includes:\n{cast}")
    elif info_category == 5:
        print(f"{show} was first released in {info}")
    elif info_category == 6:
        print(f"I need to add more detail to the WS but for now : {info}")
    elif info_category == 7:
        print(f"{show} has {info} seasons.")
    elif info_category == 8:
        print(f"{show} received and audience score of {info} on Rotten Tomatoes.")
    else:
        print("something went wrong")

def final_results_return_all(row):
    """
    If the user wants to know all the available information on
    a show this function is called.
    It retrieves all the relevant data and returns it to the
    user in a way that is easy to read and understand.
    """
    show_info = SHEET.worksheet('data').row_values(row)
    print(f"All available information on {show_info[0]}:\nDescription:\n{show_info[1]}\n")
    sub_genres = reformat_info(show_info[2])
    creators = reformat_info(show_info[3])
    actors = reformat_info(show_info[4])
    print(f"Sub-genres:\n{sub_genres}\n\nCreated by:\n{creators}\n\nStarring:\n{actors}\n")
    print(f"Release Date:\n{show_info[0]} first aired in {show_info[5]}\n\nStill Running?\n{show_info[6]}\n\nNo. of Seasons:\n{show_info[0]} has {show_info[7]} seasons.\n\nAudience Score:\n{show_info[0]} was given a score of {show_info[8]} on Rotten Tomatoes.")


def search_in_dictionary(dictionary):
    """
    Checks length of dictionary, if more than 1, requests user choose an item.
    Offers user choice of categories for more information.
    """
    
    print(len(dictionary))
    while True:
        if len(dictionary) > 1:
            dict_num = input("Which result would you like more information on?\n>")
        else:
            dict_num = input("If you would like more information please type 0\n>")
        if validate_dict_keys(dict_num, dictionary):
            break
    print(dict_num)
    show_title = str(dictionary[int(dict_num)].split('-')[0]).strip()
    while True:
        category_choice = input(f"What would you like to know about {show_title}?\n{instructions.CATEGORIES}\n>")
        if validate_category_choice(category_choice):
            break
    cell = str(SHEET.worksheet('data').find(show_title))
    item_row = find_row(cell)
    item_col = int(category_choice) + 1
    info = str(SHEET.worksheet('data').cell(item_row, item_col).value)
    if int(category_choice) < 9:
        final_search_results(show_title, int(category_choice), info)
    else:
        final_results_return_all(item_row)



def search_columns(keyword, chosen, column):
    """
    Searches through the column of seleted category and compares the keyword
    to the items in the column.
    """
    whole_chosen_col = SHEET.worksheet('data').col_values(column)
    chosen_col = whole_chosen_col[1:]
    search_results = []
    if column != 1:   
        for item in chosen_col:
            if keyword.lower() in item.lower():
                cell = str(SHEET.worksheet('data').find(item))
                item_row = find_row(cell)
                item_title = SHEET.worksheet('data').cell(item_row, 1).value
                full_item = item_title + " - " + item
                search_results.append(full_item)          
        if search_results != []:
            d1= dict(enumerate(search_results))
            print(f"The following items matched your search:\n{d1}")
            search_in_dictionary(d1)
        elif search_results == []:
            print("No matching results, please try again.")
            chosen_search(chosen, column)
    elif column == 1:
        for item in chosen_col:
            if keyword.lower() in item.lower():
                search_results.append(item)            
        if search_results != []:
            d1= dict(enumerate(search_results))
            print(f"The following items matched your search:\n{d1}")
            search_in_dictionary(d1)
        elif search_results == []:
            print("No matching results, please try again.")
            chosen_search(chosen, column)


def main():
    """
    runs the program
    """
    print(instructions.INSTRUCTIONS_DESCRIPTION)
    print(instructions.MENU)
    validated_response = user_response_int()
    menu_answers(validated_response)
    
    
print(instructions.WELCOME)
main()

