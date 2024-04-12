import logging
import os
import django
import spacy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoPizzaPy.settings')
django.setup()

from orders.models import Order, OrderItem
from menu.models import Pizza, Topping

logging.basicConfig(level=logging.INFO)

nlp = spacy.load("en_core_web_sm")

# Due to time constraint, I am leaving an untested theoretical implementation for the timeout handler function:
# def timeout_handler(signum, frame):
#     raise TimeoutError
#
# # Set the signal alarm handler
# signal.signal(signal.SIGALRM, timeout_handler)
#
# def input_with_timeout(prompt, timeout=5):
#     try:
#         signal.alarm(timeout)
#         return input(prompt)
#     except TimeoutError:
#         print("\nHey, are you still there?")
#         return None
#     finally:
#         # Disable the alarm
#         signal.alarm(0)

# Stage Constants for code readability
GREETING = 0
GETTING_PIZZA_QUOTE = 1
ASKING_NUMBER_OF_PIZZAS = 2
ASKING_PIZZA_SIZE = 3
ASKING_PIZZA_TYPE = 4
GETTING_CUSTOMER_NAME = 5
ORDER_CONFIRMATION = 6
REQUESTED_OPERATOR = 7

size_map = {
    "S": "small",
    "M": "medium",
    "L": "large"
}

conversation_prompts = [
    "Hi! Thanks for calling Joe's Pizza. How can I help you today? Press 0 for an operator.",
    "Our large pizzas are $20, and our small pizzas are $10. Pepperoni or vegetarian pizzas cost $2 extra. Would you "
    "like to place an order?",
    "Great! How many pizzas will you be ordering?",
    "Let's get the details for pizza number {}. What size will the pizza be?",
    "A {} pizza. What kind of pizza will you have? You can say 'cheese', 'pepperoni', or 'vegetarian'.",
    "Thanks! I need a name for the order. What's your name?",
    "Ok {}. Your order will be ready in 30 minutes. See you soon!",
    "I'll send you to an operator now."
]


def end_call():
    exit(0)


def connect_operator():
    print(conversation_prompts[REQUESTED_OPERATOR])
    end_call()


def is_intent_order(user_input):
    doc = nlp(user_input)
    return any(token.lemma_ in ["order", "new"] and "pizza" in [t.text for t in doc] for token in doc)
    # TODO: modify to work for "new order" which is more vague in case we want to work with other menu items


def get_number_from_input(user_input):
    doc = nlp(user_input)
    for token in doc:
        if token.like_num:
            return min(max(1, int(token.text)), 9)  # Restrict to 1-9 pizzas. Better way would be to let user know!
    return None


def get_pizza_details_from_input(user_input, detail_type):
    if detail_type == "size":
        reverse_size_map = {v: k for k, v in size_map.items()}
        for size_input, size_letter in reverse_size_map.items():
            if size_input in user_input.lower():
                return size_letter
    elif detail_type == "type":
        types = ["cheese", "pepperoni", "vegetarian"]
        for pizza_type in types:
            if pizza_type in user_input.lower():
                return pizza_type
    return None


def interrupt_sequence_check(user_input, stage):
    if "0" in user_input or "operator" in user_input:
        connect_operator()
        stage = REQUESTED_OPERATOR
        return True, stage
    elif "go back" in user_input:
        if stage <= GETTING_PIZZA_QUOTE:
            stage = GREETING
        else:
            stage -= 1
        return True, stage
    elif "repeat" in user_input or "*" in user_input:
        return True, stage
    elif "how much is a pizza" in user_input or "pizza quote" in user_input:
        stage = 1  # Skip stage 1 and go directly to number_of_pizzas
        return True, stage
    else:
        return False, stage


def main():
    stage = GREETING
    pizza_count = 0
    current_pizza_details = {}
    order_details = []

    # UNCOMMENT TO SKIP TO FINAL STEP FOR TESTING:
    # order_details = [{'size': 'L', 'type': 'cheese'}, {'size': 'S', 'type': 'pepperoni'}]
    # stage = GETTING_CUSTOMER_NAME
    # pizza_count = 2

    while stage < len(conversation_prompts):
        if stage == GREETING:
            user_input = input(conversation_prompts[stage] + "\n> ").lower()
            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            elif is_intent_order(user_input):
                stage = 2
            else:
                print("Please say 'order pizza' or 'new order' to start.")
        elif stage == GETTING_PIZZA_QUOTE:
            user_input = input(conversation_prompts[stage] + "\n> ")
            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            elif "yes" in user_input:
                stage += 1
            elif "no" in user_input:
                print("Thank you for calling Joe's Pizza. Have a nice day.")
                return
            else:
                print("Please say 'yes' to place an order or 'no' to exit.")
        elif stage == ASKING_NUMBER_OF_PIZZAS:  # Quantity
            user_input = input(conversation_prompts[stage] + "\n> ")
            number = get_number_from_input(user_input)
            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            elif number:
                pizza_count = number
                stage += 1
            else:
                print("Please enter a number between 1 and 9.")
        elif stage == ASKING_PIZZA_SIZE:
            prompt = conversation_prompts[stage].format(len(order_details) + 1)
            user_input = input(prompt + "\n> ")
            size = get_pizza_details_from_input(user_input, "size")

            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            elif size:
                current_pizza_details["size"] = size
                stage += 1
            else:
                print("Please specify the pizza size: 'large', 'medium', or 'small'.")
        elif stage == ASKING_PIZZA_TYPE:
            prompt = conversation_prompts[stage].format(size_map[current_pizza_details["size"]])
            user_input = input(prompt + "\n> ")
            pizza_type = get_pizza_details_from_input(user_input, "type")
            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            if pizza_type:
                current_pizza_details["type"] = pizza_type
                order_details.append(current_pizza_details)
                current_pizza_details = {}
                if len(order_details) < pizza_count:
                    stage -= 1  # Go back to get next pizza's details
                else:
                    stage += 1  # Proceed to get customer name
            elif "repeat" in user_input:
                continue
            else:
                print("Please specify the type of pizza: 'cheese', 'pepperoni', or 'vegetarian'.")
        elif stage == GETTING_CUSTOMER_NAME:
            user_input = input(conversation_prompts[stage] + "\n> ")
            skip, stage = interrupt_sequence_check(user_input, stage)
            if skip:
                pass
            if user_input.isalpha():  # Simple check for a valid name
                customer_name = user_input
                # Create the order in the database
                # user = User.objects.get_or_create(username='default_user')[0]
                print(conversation_prompts[stage + 1].format(customer_name))
                order = Order.objects.create(customer_name=customer_name, status='P')
                order_items_details = []
                total_money = 0
                for pizza_detail in order_details:
                    topping_name = pizza_detail['type'].strip().capitalize()
                    pizza = Pizza.objects.get(size=pizza_detail['size'], name=topping_name)

                    # Create the OrderItem linked to the Order.
                    order_item = OrderItem.objects.create(order=order, pizza=pizza)

                    topping = Topping.objects.get(name=topping_name)
                    order_item.toppings.add(topping)
                    total_money += pizza.price
                    order_items_details.append(f"{pizza.get_size_display()} {pizza.name} Pizza")
                stage = ORDER_CONFIRMATION

                logging.info("Order Confirmation, total money made: " + str(total_money))
                order_items_str = ", ".join(order_items_details)

                logging.info(f'{customer_name} ordered: {order_items_str}')
                return
            else:
                print("Please enter a valid name.")


if __name__ == "__main__":
    main()
