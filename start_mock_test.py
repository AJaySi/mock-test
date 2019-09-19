# Standard Lib import
from time import sleep

# third party python lib
from mock import patch, Mock
# Standard python assertions can be also be used instead.

# Local lib imports
from lib.endpoint_method import get_items, sys_utils,\
        get_uncompleted_todos

############################################
#
# For mocking REST APIs, the first step is to know the response 
# data sctructure against a request.
#
# Motivation:
# IF we know, response and request json formats,
# then mocked failures can be induced for any server.
# This helps in getting large number of failure discovery and auto remedy tested.
#
# What is the Unit test plan ? and dependent REST server/services ?
#
# Although, simulated, mocked/faked testing is Not a sunstitute
# for real hardware based testing. Main goal is specification testing
# and Not validation.
#
# Choice of software packages:
#
# 1). Mock(https://pypi.org/project/mock/)
# 2). python 3
#
#############################################


# Utility function to check if the API endpoint is alive/OK.
# This initial check can be part of the test suite constructor.
def test_response_ok():
	"""
	Check the response as OK for a given endpoint.
	Returns True Or asserts false.
	Input: Valid REST API URI
	"""
	
	# Send GET request to API given endpoint and store the response.
	response = get_items()

	# Confirm that the request-response cycle completed successfully.
	#assert_true(response.ok)
	if ('None' in response): print("Failed calling REST API: {}".format(response))
	else: print("TC Passed, Response OK: {}".format(response))


# patch() decorator function, passing in a reference to requests.get
@patch('lib.endpoint_method.requests.get')
# An example of mocked call to an endpoint.
def test_mock_get_ok(mock_get):
    """
    Checks for the same response, as without mock call.
    This examplifies mocking a REST API and sending back mocked
    response, without actual call to API server.
    """

    # Configure the mock to return response/OK status code.
    mock_get.return_value.ok = True

    # Send GET request to API given endpoint and store the response.
    response = get_items()

    # Confirm that the request-response cycle completed successfully.
    if ('None' in response):
        print("Failed calling REST API: {}".format(response))
    else:
        print("TC Passed, Response OK".format(response))


# Using a patcher to patch endpoint methods, without decorators.
# Mocking/patching with context manager and patcher allows for finer
# control on program logic and not having to define function with
# decorator referances. Patcher gives explicit start and end to mocking.
def test_mock_get_patcher():

    # Create a patcher object against the endpoint to patch.
    # The requests GET is defined in endpoint_method.py
    mock_get_patcher = patch('lib.endpoint_method.requests.get')

    print("Start patching request GET method call.")
    mock_get = mock_get_patcher.start()

    # Configure mocked GET response as some arbit JSON, this time.
    mock_get.return_value = [
                {'ClusterID': '514-794-6957', 'Disk_usage': 90, 'Fatal_errors': 1, 'Discovery': 0},
                {'ClusterID': '772-370-0117', 'Disk_usage': 99, 'Fatal_errors': 3, 'Discovery': 1},
                {'ClusterID': '176-290-7637', 'Disk_usage': 10, 'Fatal_errors': 0, 'Discovery': 2}
                ]

    # Call the function to get mocked response
    response = get_items()

    print("Stop patching the GET method, continue with normal logic flow.")
    mock_get_patcher.stop()

    print("The response is : {}".format(response))


# Patch a function call, useful to send mocked data from function.
@patch('lib.endpoint_method.get_items')
def test_mocked_api_function(mocked_get_items_func):
    # Configure mock to return None.
    mocked_get_items_func.return_value = None

    # Call the service, which will return mocked empty list.
    response = get_uncompleted_todos()

    # Check if the mocked function was called, indeed.
    if mocked_get_items_func.called:
        print("Mocked GET method returned: {}".format(response))
    else:
        print("Mocked method not Called.")


def mock_sys_utils_lib():
    # Mock datetime to control today's date
    datetime = Mock()

    # Mock .today() to return Tuesday
    print("MOck today to return Tuesday")
    datetime.datetime.today.return_value = 'tuesday'
    # tuesday is a weekday
    assert sys_utils()

    # MOck today to return Saturday, Not a weekday
    print("MOck today to return Saturday")
    datetime.datetime.today.return_value = 'saturday'
    #assert not sys_utils()


#------------------- Demo purposes ------------

print("Starting Without Mock, actual API call.")
test_response_ok()
print("---------------\n")
sleep(5)

print("Example of Mocking an API method, like GET. This test does make the")
print("actual but returns the expected response for TC to Pass.")
test_mock_get_ok()
print("---------------\n")
sleep(5)

print("Example of mocking using a Patcher, without decorator function.")
test_mock_get_patcher()
print("---------------\n")

print("Mocking product library fuctions")
print("Useful to fake cluster failures, without simulating failures.")
test_mocked_api_function()
print("---------------\n")

print("Mocking a standard python library like datetime")
mock_sys_utils_lib()
print("---------------\n")
