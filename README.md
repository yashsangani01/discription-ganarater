7# Product Description Generator

A modern Flask web application that generates creative product descriptions using OpenAI's GPT-4o-mini model.

## Features

- Clean, responsive web interface with modern styling
- Asynchronous form submission (no page reload)
- Real-time loading indicators
- Error handling for API connections
- Input validation
- Built with Flask, OpenAI API, and vanilla JavaScript

## Setup

1. Clone or download the project.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
6. Run the app: `python app.py/app.py`

## Usage

- Open your browser and go to `http://127.0.0.1:5000/`
- Enter a product name and click "Generate" to get a description.

## Requirements

- Python 3.x
- OpenAI API key
- Internet connection for API calls

## License

This project is for educational purposes.
