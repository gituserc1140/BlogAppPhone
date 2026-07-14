import streamlit as st
import os
import json

# Directory to store blog posts
BLOG_DIR = "blog_posts"

# Ensure the blog directory exists
os.makedirs(BLOG_DIR, exist_ok=True)

def save_blog(title, content):
    filename = os.path.join(BLOG_DIR, f"{title}.json")
    with open(filename, "w") as f:
        json.dump({"title": title, "content": content}, f)

def load_blogs():
    blogs = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(BLOG_DIR, filename), "r") as f:
                blogs.append(json.load(f))
    return blogs

st.title("Streamlit Blog App")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Write Blog", "View Blogs"])

if page == "Write Blog":
    st.header("Write a New Blog")
    title = st.text_input("Blog Title")
    content = st.text_area("Blog Content", height=300)
    if st.button("Publish"):
        if title and content:
            save_blog(title, content)
            st.success("Blog published successfully!")
        else:
            st.error("Please fill in both title and content.")

elif page == "View Blogs":
    st.header("View Blogs")
    blogs = load_blogs()
    if blogs:
        for blog in blogs:
            st.subheader(blog["title"])
            st.write(blog["content"])
            st.markdown("---")
    else:
        st.info("No blogs available. Write one now!")