# Streamlit Blog App

A simple blog application built with Streamlit that helps users plan, draft, publish, and view blog posts. The writing assistant is fully built into the app, so it does not require an API key or paid AI credits.

## Features
- Generate a lightweight writing kit with a suggested title, outline, starter draft, and revision checklist
- Write and publish blogs
- View all published blogs
- Simple and intuitive interface

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-blog-app.git
   cd streamlit-blog-app
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the app in your browser and start generating drafts, writing, or viewing blogs!

## Directory Structure
- `app.py`: The main Streamlit application file.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: This file.
- `blog_posts/`: Directory where blog posts are stored as JSON files.

## Notes
- Blog posts are stored locally in the `blog_posts` directory as JSON files.
- The writing assistant uses built-in templates and text generation rules, so it does not spend API credits.
- Ensure you have sufficient space in your Streamlit Cloud environment if deploying there.