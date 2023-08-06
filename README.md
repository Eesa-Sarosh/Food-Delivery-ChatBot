# Food Delivery Chatbot

This repository contains the code for a Food Delivery Chatbot built using FastAPI, Dialogflow, and MySQL. The chatbot allows users to place food orders, track their orders, add or remove items from their orders, and complete their orders.

## Features

- **Order Placement**: Users can interact with the chatbot to place food orders by specifying the food items and quantities they want.

- **Order Tracking**: Users can inquire about the status of their orders by providing their order IDs.

- **Add to Order**: Users can add more food items to their existing orders.

- **Remove from Order**: Users can remove food items from their existing orders.

- **Complete Order**: Users can complete their orders, and the system will calculate the total bill and provide them with an order ID.

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [Dialogflow](https://cloud.google.com/dialogflow): A natural language understanding platform that makes it easy to design and integrate conversational user interfaces into applications.
- [MySQL](https://www.mysql.com/): An open-source relational database management system.
- [codebasics.io](https://www.youtube.com/c/codebasics): Credits to codebasics.io for providing guidance and tutorials on building the chatbot.

## Setup Instructions

1. Clone the repository: `git clone https://github.com/eesa-sarosh/food-delivery-chatbot.git`
2. Install the required Python packages.
3. Set up your MySQL database and update the database credentials in the `db_helper.py` file.
4. Create a Dialogflow agent and configure the fulfillment webhook to interact with the FastAPI application.
5. Deploy the FastAPI application to a server or run it locally using `uvicorn`.

## Usage

1. Users interact with the chatbot using natural language queries and commands.
2. The chatbot processes the user's input using Dialogflow's intent recognition.
3. The FastAPI application handles the fulfillment logic based on the recognized intent.
4. Users can place orders, track orders, add or remove items, and complete orders through the chatbot interface.

## Credits

- The core logic and structure of this chatbot were inspired by the tutorials and guidance provided by [codebasics.io](https://www.youtube.com/c/codebasics).

