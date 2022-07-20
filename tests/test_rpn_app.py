"""
To run the tests:

'pytest -v' in current directory
"""
import requests

try:
    from app import OPERATORS
except ImportError:
    import sys
    sys.path.append("..")
    from app import OPERATORS


BASE_URL = "http://localhost:5000"


def test_server_working():
    "Simple ping to root to test that the server is up and running"
    
    response    = requests.get(BASE_URL)

    assert response.status_code == 201


def test_get_operators():
    "Testing that we get the right list of operators when getting to /rpn/op"

    response    = requests.get(BASE_URL + '/rpn/op')
    actual_op   = response.json()

    assert response.status_code == 201
    assert actual_op['list_operators'] == list(OPERATORS.keys())

######################## TEST RPN CALCULATOR PIPELINE ########################
"""
# Here below we test a whole RPN pipeline: from stack creation, to math operations and result output
# We will first add the operands (in this order, from left to right): 10, 5, 2
# We'll then use the "/" and "+" operators successively (in this order, from left to right)
# We should get 12.5 as a final result

Pipeline:
- create stack
- list stack
- add operand
- add operand
- add operand
- execute operator
- execute operator
- get stack
"""

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

def test_create_stack():
    """
    """    
    URL         = BASE_URL + '/rpn/stack'
    response    = requests.post(URL, data="", headers=headers)

    assert int(response.status_code) == 201


def test_add_operands():
    """
    """    
    URL         = BASE_URL + '/rpn/stack/1/val/10'
    requests.post(URL)

    URL         = BASE_URL + '/rpn/stack/1/val/5'
    requests.post(URL)

    URL         = BASE_URL + '/rpn/stack/1/val/2'
    response    = requests.post(URL)

    assert int(response.status_code) == 201



def test_enter_operator():
    """
    Testing that the operator are correctly sent and executed to/in the stack
    """

    print("test_enter_operator called.")
    # DIVISION
    URL         = BASE_URL + '/rpn/op/d/stack/1'
    print("URL: ", URL)
    requests.post(URL, data="", headers=headers )

    # ADDITION
    URL         = BASE_URL + '/rpn/op/+/stack/1'
    response    = requests.post(URL, data="", headers=headers)

    assert int(response.status_code) == 201


def test_get_result():
    """
    Testing that the operator were correctly applied through the result of the
    arithmetic operations
    """
    
    URL         = BASE_URL + '/rpn/stack/1'
    response    = requests.get(URL)
    result      = response.json()

    assert result[0] == 12.5




