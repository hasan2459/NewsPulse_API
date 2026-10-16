import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")
BASE_URL = "https://gnews.io/api/v4"

# Page configuration
st.set_page_config(
    page_title="NewsPulse | News App",
    page_icon="📰",
    layout="wide",
)
# App heading

st.title("📰NewsPulse")
st.caption("Discover news from around the world")

# Available news categories

categories = {
    "General": "general",
    "World": "world",
    "US": "nation",
    "Business": "business",
    "Technology": "technology",
    "Entertainment": "entertainment",
    "Sports": "sports",
    "Science": "science",
    "Health": "health",
}


def fetch_news(category, keywords=""):
    """Fetch news articles from the Gnews API."""
    if not API_KEY:
        st.error(
            "API key missing. Please check your .env file."

        )
        return []
    if keywords.strip():
        endpoint = f"{BASE_URL}/search"
        params = {"q": keywords.strip()}
    else:
        endpoint = f"{BASE_URL}/top-headlines"
        params = {"category": category}

    params.update({
        "lang": "en",
        "country": "in",
        "max": 10,
        "apikey": API_KEY,
    })

    try:
        response = requests.get(
            endpoint,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        return data.get("articles", [])
    except requests.exceptions.Timeout:
        st.error(
            "The request timed out. Please try again later."
        )

    except requests.exceptions.HTTPError:
        status_code = response.status_code
        if status_code == 429:
            st.error(
                "API request limit reached. Try again later"
            )
        elif status_code in (401, 403):
            st.error(
                "API key invalid or access not permitted."
            
            )
        else:
            st.error(
                f"News API returned HTTP {status_code}"
            )
    except requests.exceptions.RequestException:
        st.error(
            "Network error. Check your internet connection."
        )
    except ValueError:
        st.error(
            "The API returned invalid JSON data."
        )

    return []

def display_article(article):
    """Display one news article"""

    title = article.get("title") or "Untitled article"
    description = (
        article.get("description")
        or "No description available"
    )
    source = article.get("source") or {}
    source_name = source.get("name", "Unknown source")
    article_url = article.get("url", "")
    image_url = article.get("image", "")
    published_at = article.get("publishedAt", "")

    with st.container(border=True):
        st.subheader(title)

        if image_url:
            st.image(image_url, width=350)

        st.write(description)
        st.caption(
            f"Source: {source_name} | Published: {published_at}"
        )
        if article_url:
            st.markdown(
                f"[Read full article ]({article_url})"
            )

# Sidebar control

st.sidebar.header("Explore News")

category_name = st.sidebar.selectbox(
    "Choose a category",
    list(categories.keys())
)
keywords = st.sidebar.text_input(
    "Search news",
    placeholder="e.g. python, AI, space",

)
fetch_clicked = st.sidebar.button(
    "Fetch news",
    type= "primary"
)

# Fetch news when the user clicks the button

if fetch_clicked:
    category = categories[category_name]
    with st.spinner("Fetching news..."):
        articles = fetch_news(category, keywords)
    st.session_state["articles"] = articles
    st.session_state["has_searched"] = True

# display the saved results
if st.session_state.get("has_searched", False):
    articles = st.session_state.get("articles", [])

    if articles:
        st.subheader(
            f"Latest News - {len(articles)} articles"
        )
        for article in articles:
            display_article(article)
    else:
        st.info(
            "No articles found. Try another category or keyword."
        )
else:
    st.info(
        "Choose a category or enter a keyword, then click Fetch news."
    )
# Footer
st.divider()
st.caption(
    "NewsPulse | Built with Python, Streamlit and GNews API"
)


