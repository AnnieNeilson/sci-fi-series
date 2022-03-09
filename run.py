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



def welcome():
    """
    Prints welcome message and navigation instructions to the user
    """
    print(instructions.WELCOME)
    print(instructions.INSTRUCTIONS_DESCRIPTION)
    print(instructions.MENU)


def user_response_int():
    """
    gets response from the user
    """
    while True:
        response = input(">")
        
        if validate_response(response):
            break
    return response


def validate_response(response):
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
    keyword = input(f"You've chosen to search by {chosen}. Type in a relevant keyword:\n>")
    search_columns(keyword, chosen, column)


def search_columns(keyword, chosen, column):
    """
    Searches through the column of seleted category and compares the keyword
    to the items in the column.
    """
    #will have to add if statements to catch release year and actors categories
    #figure out how to bring up titles with search results e.g. subgenres
    #rethink how I want the results to look
    chosen_col = SHEET.worksheet('data').col_values(column)
    search_results = []
    for item in chosen_col:
        if keyword.lower() in item.lower():
            search_results.append(item)
    print(f"The following items matched your search:\n{search_results}")
    if not search_results:
        print("No matching results, please try again.")
        chosen_search(chosen, column)


def main():
    """
    runs the program
    """
    welcome()
    validated_response = user_response_int()
    menu_answers(validated_response)
    
    

main()

