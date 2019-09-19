# Standard library imports
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
# Third-party imports
import requests
# Local imports
from config import BASE_URL, USERS_URL


# Common REST endpoint GET method abstraction.
# This method does a GET method call on the given URL.
def get_items():
    TODOS_URL = urljoin(BASE_URL, 'todos')
    print("\nCall REST GET at API: {}\n".format(TODOS_URL))

    response = requests.get(TODOS_URL)
    #print("Actual API call, without mock response: {}".format(response.text))
    return(response)


def get_uncompleted_todos():
    response = get_items()
    if response is None:
        return []
    else:
        todos = response.json()
        return [todo for todo in todos if todo.get('completed') == False]


# Function demostrating, mocking of standard python packages and utilities.
# This is useful to send/report errorneous fake test system data.
def sys_utils():
    # Import the standard datetime python library.
    import datetime
    today = datetime.datetime.today()
    print("Today is: {}".format(today))
    # Python's datetime lib: Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)
