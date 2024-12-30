# Reddit Comment Scraper

A simple Python web application built with Flask and PRAW to scrape comments from Reddit threads.

## How to Run

1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `.\venv\Scripts\activate` (on Windows) or `source venv/bin/activate` (on macOS/Linux).
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`
7. Open your web browser and go to `http://127.0.0.1:5000`.

## Usages

Enter a Reddit thread URL in the input field and click "Scrape". The comments will be displayed in the text area below.

## Technologies Used

* Python
* Flask
* PRAW (Python Reddit API Wrapper)
* HTML
* CSSgit push -u origin master