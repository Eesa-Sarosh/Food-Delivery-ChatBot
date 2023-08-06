from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

inprogress_order = {}

app = FastAPI()


@app.post("/")
async def handle_request(request: Request):
    #Retrieve the Json Data Request
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_context = payload['queryResult']['outputContexts']


    session_id = generic_helper.extract_session_id(output_context[0]['name'])

    intent_handler = {
        "track.order - context: ongoing-order": track_order,
        "order.complete - context: ongoing-order": complete_order,
        'remove.order - context: ongoing-order': remove_order,
        "order.add - context: ongoing-order": add_to_order
    }

    return intent_handler[intent](parameters, session_id)



def add_to_order(parameters: dict, session_id: str):
    food_item = parameters['food-items']
    quantity = parameters['number']

    if len(food_item) != len(quantity):
        msg = "Sorry, I did not understand. Please clearly specify food items and its quantity"
    else:
        new_food_dict = dict(zip(food_item, quantity))

        if session_id in inprogress_order:
            prev_food = inprogress_order[session_id]
            new_food_dict.update(prev_food)
            inprogress_order[session_id] = new_food_dict
        else:
            inprogress_order[session_id] = new_food_dict

        the_order = generic_helper.get_string_from_dict(inprogress_order[session_id])
        msg = f"Your order is {the_order}. Do you want anything else?"

    return JSONResponse(content={
        'fulfillmentText': msg
    })


def remove_order(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-items"]
    current_order = inprogress_order[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        msg = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        msg = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        msg += " Your order is empty!"
    else:
        order_str = generic_helper.get_string_from_dict(current_order)
        msg += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": msg
    })


def complete_order(parameters: dict, session_id: str):
    if session_id in inprogress_order:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            msg = "I am having some problem with your order. Could you please place your order again."
        else:
            msg = "Your order is placed successfully.\n" \
                  f"Order ID: #{order_id}." \
                  f"Total bill: ${db_helper.get_total_price(order_id)}"

    else:
        msg = "I am having some problem with your order. Could you please place your order again."

    del inprogress_order[session_id]

    return JSONResponse(content={
        'fulfillmentText': msg
    })


def save_to_db(order: dict):
    next_order_id = db_helper.get_order_id()
    print(next_order_id)
    for food, quantity in order.items():
        rcode = db_helper.insert_order(food, quantity, next_order_id)

        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        msg = f'The Order ID #{order_id} and its Status: {order_status}'
    else:
        msg = f"There is no order for Order ID #{order_id}"

    return JSONResponse(content={
        'fulfillmentText': msg
    })