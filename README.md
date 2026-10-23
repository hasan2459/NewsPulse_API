
# 📰 NewsPulse — News App Using APIs

NewsPulse is a Python-based news web application that
fetches news articles using the GNews API.

## Features

- Fetch top headlines by category
- Search news by keyword
- Display article titles and descriptions
- Show source names and publication dates
- Open original articles
- Handle API and network errors
- Keep API keys outside the source code

## Technologies Used

- Python
- Requests
- Streamlit
- GNews API
- python-dotenv

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies:

   pip install -r requirements.txt

4. Create a `.env` file in the project root.
5. Add your GNews API key:

   GNEWS_API_KEY=your_api_key_here

6. Run the application:

   streamlit run main.py

## Security

Never commit your `.env` file or expose your API key.

## License

MIT
