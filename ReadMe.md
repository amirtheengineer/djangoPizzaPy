# Joe's Pizza Voice Assistant
Project Code Name: djangoPizzaPy

## Introduction
Joe's Pizza Voice Assistant is a command-line interface application designed to facilitate the ordering process for customers calling Joe's Pizza. This application simulates voice-based interactions using text input to demonstrate the ordering process from start to finish.

## Features
- Order pizza through a simulated voice interaction using text commands.
- Utilize natural language processing (NLP) to understand and process user requests.
- Manage orders and customer data through a Django-administered backend.

## Getting Started
### Prerequisites
Ensure you have Python and Django installed on your system. This project uses Python 3.8 or newer and Django 3.2 or newer.

### Installation
**1. Clone the repo:**
```
git clone https://github.com/amirtheengineer/djangoPizzaPy.git
cd djangoPizzaPy
```
**2. Setup a virtual environment:**

* On Unix-based systems:
```
python3 -m venv venv
source venv/bin/activate
```
* On Windows:

```
python -m venv venv
.\venv\Scripts\activate
```

**Install the requirements:**

```
pip install -r requirements.txt
pip install spacy
python -m spacy download en_core_web_sm
```

**Set up the database:**

```
python manage.py makemigrations
python manage.py migrate
```

**Load initial data:**

```
python manage.py loaddata menu_items.json
```

**Create an admin user:**

```
python manage.py createsuperuser
```

## Running the Application

### Start the Django development server:

```
python manage.py runserver
```

### Run the assistant in a new terminal:

```
python run_assistant.py
```

### Access the Django Admin Panel:

Navigate to http://127.0.0.1:8000/admin/ to manage the application.

## Usage
Interact with the assistant through your terminal by following the voice assistant's prompts.

## Future Improvements
* Implement authentication for enterprise users.
* Capture and utilize customer IP or phone numbers for better service personalization.
* **Unit Testing**: Unit tests for CLI as well as each django app.
* **Automated Setup Script**: A single script or use Docker Compose to streamline the initial setup process, making it quick and easy for new developers or deployments.
* Adapt the database and user interface to support multiple pizza stores.
* Containerize the application using Docker for easier deployment.
* Develop a webchat dashboard and integrate actual call and voice synthesis APIs.
* Feature to suspend anyone that tries to add pineapple as a topping. JK

### Alternative Design and Implementation
* Consider using a GPT-based approach for more dynamic interactions. This could involve prompt engineering the flow and reinforcing it with each user interaction to ensure the model stays on script, offering a potentially more natural conversational experience.

## Conclusion
- This mouth watering take-home project is designed to demonstrate my expertise in backend development as a whole, rather than showcase depth in a single area. 
- Django apps and models were used to show off my ability to handle data structures like foreign keys and object associations effectively, although perhaps not as I would in a real scenario. 
- The CLI built on top of Django showcases my understanding and background integrating Python modules following best practices.
- This project somewhat resembles a basic IVR system, but I used spaCy to show off my understanding of natural language processing and again, Python modules.