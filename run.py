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
    search_columns(keyword, chosen, column)


def find_row(item_cell):
    """ 
    Finds the row of a specific cell, so other items can be found from this number.
    """
    row_index = item_cell.index("R",1)
    col_ind = item_cell.index("C",2)
    row_ind = row_index + 1
    row_num = item_cell[row_ind:col_ind]
    return row_num


def search_in_dictionary(dictionary):
    """
    Checks length of dictionary, if more than 1 requests user choose an item.
    Offers user choice of categories for more information.
    """
    if len(dictionary) > 1:
        dict_num = int(input("Which result would you like more information on?\n>"))
        print(dictionary[dict_num])
    category_choice = input(f"What would you like to know about {dictionary[dict_num]}?\n{instructions.CATEGORIES}\n>")
    print(category_choice)



def search_columns(keyword, chosen, column):
    """
    Searches through the column of seleted category and compares the keyword
    to the items in the column.
    """
    #will have to add if statements to catch release year and actors categories
    #rethink how I want the results to look
    whole_chosen_col = SHEET.worksheet('data').col_values(column)
    chosen_col = whole_chosen_col[1:]
    search_results = []
    if column != 1:   
        for item in chosen_col:
            if keyword.lower() in item.lower():
                cell = str(SHEET.worksheet('data').find(item))
                item_row = find_row(cell)
                item_title = SHEET.worksheet('data').cell(item_row, 1).value
                full_item = item_title + " : " + item
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

