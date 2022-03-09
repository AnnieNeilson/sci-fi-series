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

response = ''


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
    global response
    response = input(">")
    validate_response_int(response)
    


def validate_response_int(response):
    """
    Inside the try the string value is converted into integers,
    It raises ValueError if it can't convert into ints or if there are too 
    many numbers
    """
    try:
        [int(response)]
        if len(response) != 1:
            raise ValueError("Only one number is required")
            user_response_int()
    except ValueError as e:
        print(f"Invalid response: {e}, please try again.\n")
        user_response_int()


def menu_answers(response):
    """
    selects category depending on users intial response
    """
    if int(response) == 1:
        category = "title"
    elif int(response) == 2:
        category = "sub-genre"
    elif int(response) == 3:
        category = "release year"
    elif int(response) == 4:
        category = "creator"
    elif int(response) == 5:
        category = "actors"
    elif int(response) == 6:
        category = "audience score"
    elif int(response) == 1:
        category = "title"
    else:
        print("What?")
    print(response)
    print(category)


def search_function(keyword, category):
    """
    Searches through the column of seleted category and compares the keyword
    to the items in the column.
    """
    column = SHEET.worksheet(category)
    search_results= []
    count = 0
    for item in column:
        if keyword.lower() in item.lower():
            match = search_results.append(item)
    print(search_results)        


welcome()
user_response_int()
menu_answers(response)

