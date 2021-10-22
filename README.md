#OCR using Tesseract#

## Requirements

1. Create virtual environment ( recommended )
2. Install the neccessary packages by using **pip3 install -r requirements.txt**

## Running locally

1. For running locally, you can run **python3 manage.py runserver**. This will run the application in localhost 8000 port.
2. For running background tasks, we have to execute **python3 manage.py process_tasks**.

Note: background task is important for tesseract.

## Your modification

1. In tesseract -> settings.py, change the database setup and mail setup
2. In index -> background_task.py, change 30th line **youremail.com** to your smtp mail name.
