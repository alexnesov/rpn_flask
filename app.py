"""The Endpoints to operate on the STACKS in the context of an RPN calculator"""

from flask import Flask, jsonify, abort
import operator
from flask_swagger_ui import get_swaggerui_blueprint


OPERATORS = {'+': operator.add, 
             '-': operator.sub, 
             '*': operator.mul, 
             'd': operator.truediv} # using the string literal "d" and not "/" because "/" is a special character in the context of urls 
                                    # and can not be escaped with Swagger
                                    # https://github.com/swagger-api/swagger-ui/issues/4591
                                    # https://stackoverflow.com/questions/42335178/swagger-wildcard-path-parameters
                                    # --> "This [use of slash in url query params] is not supported as of OpenAPI 3.1"
                                    # It could be nonetheless encoded differently and passed through a more traditional HTML, JS frontend





STACKS                  = {}

class StackCount:

    def __init__(self, stack_count):
        self.stack_count = stack_count
    
    def add_stack(self):
        self.stack_count +=1


app                     = Flask(__name__)


SWAGGER_URL             = '/swagger'
API_URL                 = '/static/swagger.json'
app.secret_key          = "super secret key"


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'rpn_flask'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)


@app.route("/", methods=['GET'])
def Home():
    """
    """
    return "<p>Hello! <br> \
            <b><a href='http://127.0.0.1:5000/swagger'>Click here</a></b> <br> \
            to go to Swagger UI </p>", 201



@app.route("/rpn/op", methods=['GET'])
def get_list_operands():
    """
    Lists all the available operands
    @return: 201: an object with the literal string "list_operands" as key and an array of available operators as a value
    with application/json mimetype.
    """
    list_op = list(OPERATORS.keys())
    
    return jsonify({'list_operators':list_op, 
                    'information':'the letter "d" to be used as a division operator'}), 201



@app.route("/rpn/stack/<int:stack_id>", methods=['GET'])
def get_stack(stack_id):
    """
    Lists existing stack(s) 
    
    @param stack_id: get : ID of the stack on which we add an operand or apply an operator
    @return: 200: an array representing the content of the choosen stack
    with application/json mimetype.
    @raise 404: if stack_id not found
    """

    if stack_id in STACKS.keys():
        return jsonify(STACKS[stack_id])
    else:
        abort(404)
    


@app.route("/rpn/stack", methods=['GET'])
def get_stack_list():
    """
    Lists existing stack(s) 

    @return: 200: an array of existing stacks
    with application/json mimetype.
    """
    print('/rpn/stack get')

    return jsonify(STACKS)



@app.route("/rpn/stack", methods=['POST'])
def create_stack():
    """
    Create a brand new stack, a stack identifier will be automtically generated

    @return: 201: an empty payload.
    """
    obj_stack_count.stack_count         += 1
    STACKS[obj_stack_count.stack_count] = []

    return '', 201



@app.route("/rpn/stack/<int:stack_id>/val/<int:val>", methods=['POST'])
def push_val_to_stack(stack_id, val):
    """
    Adds a value to a stack, given a stack id
    The stack_id is givent as an URL parameter

    @param stack_id: post : ID of the stack on which we add an operand or apply an operator
    @param val: post : operand to be pushed to the stack
    @return: 201: an empty payload.
    """

    if stack_id in STACKS.keys():
        STACKS[stack_id].append(val)
    else:
        print("Stack ID unknown")

    return '', 201



@app.route("/rpn/stack/<int:stack_id>", methods=['DELETE'])
def delete_stack(stack_id):
    """
    Deletes a stack, given a stack id

    @param stack_id: delete : ID of the stack that we want to delete
    @return: 204: an empty payload.
    @raise 404: if stack_id not found
    """
    if stack_id not in STACKS.keys():
        abort(404)

    del STACKS[stack_id]

    return '', 204



@app.route("/rpn/op/<string:operator>/stack/<int:stack_id>", methods=['POST'])
def apply_operator(operator, stack_id):
    """
    Applies operator entered by user to two last values of a given stack

    @param operator: post : Operator to be applied on two last operands of the stack
    @param stack_id: post : ID of the stack on which we add an operand or apply an operator
    @return: 201: an empty payload.
    """

    first_pop       = STACKS[stack_id].pop() 
    second_pop      = STACKS[stack_id].pop()
    result          = OPERATORS[operator](second_pop, first_pop) 

    STACKS[stack_id].append(result)

    return '', 201


@app.route("/rpn/clear_stack/<int:stack_id>", methods=['DELETE'])
def clear_stack(stack_id):
    """
    Clears a stack, given a certain stack ID

    @param stack_id: delete : ID of the stack that we want to delete
    @return: 204: an empty payload.
    """

    STACKS[stack_id].clear()

    return '', 204

if __name__ == '__main__':
    obj_stack_count         = StackCount(0)
    app.run(debug=True)

