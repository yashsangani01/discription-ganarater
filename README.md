# discription-ganarater

A small Flask web app that generates creative product descriptions using the OpenAI API.

## Summary

- Web form UI that accepts a product name or short prompt and returns a generated product description.
- Built with Flask (backend), vanilla JavaScript (frontend), and the OpenAI API for generation.

## Features

- Clean, responsive UI
- Asynchronous form submission with loading state
- Basic input validation and error handling

## Quickstart

1. Clone the repo.
2. Create and activate a virtual environment (Linux/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and set your OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the application:

```bash
python app.py/app.py
```

Open http://127.0.0.1:5000/ in your browser.

## Usage

- Enter a product name or short prompt and click "Generate" to receive a description from the model.

## Project structure

- `app.py/` — application entrypoint and Flask code
- `requirements.txt` — Python dependencies

## Notes

- Ensure your machine has internet access for API calls and your OpenAI key has quota.
- If you prefer Flask's development server, set `FLASK_ENV=development` and run with `flask run` (adjust `FLASK_APP` as needed).

**Security note:** Never commit secrets (like `OPENAI_API_KEY`) into the repository. Use a local `.env` file that is listed in `.gitignore` and add production secrets into GitHub repository **Secrets** (Settings → Secrets → Actions) when using GitHub Actions or other CI. If you accidentally committed a secret, revoke/rotate it immediately.

## Contributing

- Feel free to open issues or PRs for bug fixes, improvements, or additional features.

## License

This repository is provided for educational purposes.

