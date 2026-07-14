# Streamlit Blog App

A simple blog application built with Streamlit that allows users to write and view blogs. This app is designed to operate within the Streamlit free tier and does not require an API key.

## Features
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
4. Open the app in your browser and start writing or viewing blogs!

## Directory Structure
- `app.py`: The main Streamlit application file.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: This file.
- `blog_posts/`: Directory where blog posts are stored as JSON files.

## Notes
- Blog posts are stored locally in the `blog_posts` directory as JSON files.
- Ensure you have sufficient space in your Streamlit Cloud environment if deploying there.