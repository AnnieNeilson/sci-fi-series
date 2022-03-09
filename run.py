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


def user_response():
    """
    gets response from the user
    """
    response = input(">")
    print(response)
    validate_response_int(response)
    
    


def validate_response_int(response):
    """
    Inside the try the string value is converted into integers,
    It raises ValueError if it can't convert into ints or if there are too many numbers
    """
    try:
        if len(response) != 1:
            raise ValueError(
                f"Only one number is required, please try again.\n"
            )
    except ValueError as e:
        print(f"Invalid response: {e}")


welcome()
user_response()

