import json
import os
import re
import uuid
from datetime import datetime, timezone

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog_posts")
GENERAL_AUDIENCE = "General readers"

os.makedirs(BLOG_DIR, exist_ok=True)


def build_blog_path():
    filename = f"blog-{uuid.uuid4().hex}.json"
    return os.path.join(BLOG_DIR, filename)


def created_at_key(blog):
    fallback_created_at = datetime(1970, 1, 1, tzinfo=timezone.utc)
    created_at = blog.get("created_at")
    if not created_at:
        return fallback_created_at
    try:
        return datetime.fromisoformat(created_at)
    except ValueError:
        return fallback_created_at


def save_blog(title, content):
    payload = {
        "title": title.strip(),
        "content": content.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with open(build_blog_path(), "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def load_blogs():
    blogs = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(BLOG_DIR, filename), "r", encoding="utf-8") as file:
                blogs.append(json.load(file))

    return sorted(blogs, key=created_at_key, reverse=True)


def parse_key_points(raw_points):
    points = []
    for line in raw_points.splitlines():
        cleaned = re.sub(r"^\s*(?:[-*•>]+|\d+[.)])?\s*", "", line).strip()
        if cleaned:
            points.append(cleaned)
    return points[:5]


def normalize_spacing(text):
    return re.sub(r"\s+", " ", text).strip()


def describe_audience(audience):
    return "readers" if audience == GENERAL_AUDIENCE else audience.lower()


def populate_editor_fields(assistant_result, overwrite_existing):
    if overwrite_existing or not st.session_state["blog_title"].strip():
        st.session_state["blog_title"] = assistant_result["title"]
    if overwrite_existing or not st.session_state["blog_content"].strip():
        st.session_state["blog_content"] = assistant_result["draft"]


def generate_assistance(topic, audience, tone, goal, raw_points):
    topic_text = normalize_spacing(topic)
    key_points = parse_key_points(raw_points)
    audience_text = describe_audience(audience)
    audience_suffix = "" if audience == GENERAL_AUDIENCE else f" for {audience.lower()}"
    title = f"{topic_text}: A {tone.lower()} guide{audience_suffix}"

    outline = [
        f"Introduction: why {topic_text} matters to {audience_text}",
        f"Core idea 1: explain the main challenge tied to {goal.lower()}",
        f"Core idea 2: break the topic into practical steps or lessons",
    ]

    for point in key_points:
        outline.append(f"Supporting section: cover {point}")

    outline.append("Conclusion: recap the key takeaway and next action")

    talking_points = "\n".join(
        f"- {point}" for point in (key_points or ["A relatable example", "A practical takeaway"])
    )
    draft = f"""# {title}

## Introduction
{topic_text} is easier to act on when it is explained in a {tone.lower()} way for {audience_text}. In this post, focus on {goal.lower()} so readers quickly understand why the topic matters and what to do next.

## Main Takeaways
{talking_points}

## First Section
Start with the reader's current situation, then explain the biggest obstacle around {topic_text.lower()}. Keep the examples concrete so the post feels useful instead of abstract.

## Second Section
Turn the topic into a short sequence of actions, lessons, or principles. Use short paragraphs and make each one move the reader closer to {goal.lower()}.

## Conclusion
Close by summarizing the most important point and inviting readers to try one specific next step today.
"""

    checklist = [
        f"Use a {tone.lower()} tone from the opening paragraph onward.",
        f"Keep the article focused on helping {audience_text}.",
        f"Make sure every section supports the goal of {goal.lower()}.",
        "Add one concrete example, story, or result to build trust.",
        "End with a clear takeaway or call to action.",
    ]

    return {"title": title, "outline": outline, "draft": draft.strip(), "checklist": checklist}


st.set_page_config(page_title="Streamlit Blog App", page_icon="📝")
st.title("Streamlit Blog App")
st.caption("Write, plan, and publish blog posts without using paid AI credits.")

page = st.sidebar.selectbox("Choose a page", ["Write Blog", "View Blogs"])

st.session_state.setdefault("blog_title", "")
st.session_state.setdefault("blog_content", "")
st.session_state.setdefault("assistant_result", None)

if page == "Write Blog":
    st.header("Write a New Blog")
    st.subheader("Need help getting started?")

    topic = st.text_input("Topic", placeholder="Example: Budget travel tips for families")
    audience = st.selectbox(
        "Audience",
        [GENERAL_AUDIENCE, "Beginners", "Busy professionals", "Small business owners", "Students"],
    )
    tone = st.selectbox("Tone", ["Helpful", "Friendly", "Professional", "Encouraging"])
    goal = st.selectbox(
        "Goal",
        ["Teach the basics", "Share practical tips", "Explain a process", "Inspire action"],
    )
    key_points = st.text_area(
        "Key points to cover (optional, one per line)",
        placeholder="Example:\nCommon mistakes\nTools to use\nSimple next steps",
        height=120,
    )

    if st.button("Create writing kit"):
        if topic.strip():
            st.session_state["assistant_result"] = generate_assistance(topic, audience, tone, goal, key_points)
            populate_editor_fields(st.session_state["assistant_result"], overwrite_existing=False)
            st.success("Writing kit created. Review it below, then publish when ready.")
        else:
            st.error("Add a topic to generate a writing kit.")
    st.caption('Creating a new writing kit will not overwrite your current editor text unless you click "Load starter draft into editor."')

    assistant_result = st.session_state.get("assistant_result")
    if assistant_result:
        st.markdown("### Suggested title")
        st.write(assistant_result["title"])
        st.markdown("### Outline")
        for item in assistant_result["outline"]:
            st.write(f"- {item}")
        st.markdown("### Revision checklist")
        for item in assistant_result["checklist"]:
            st.write(f"- {item}")
        if st.button("Load starter draft into editor"):
            populate_editor_fields(assistant_result, overwrite_existing=True)

    title = st.text_input("Blog Title", key="blog_title")
    content = st.text_area("Blog Content", key="blog_content", height=320)

    if st.button("Publish"):
        if title.strip() and content.strip():
            save_blog(title, content)
            st.session_state["blog_title"] = ""
            st.session_state["blog_content"] = ""
            st.session_state["assistant_result"] = None
            st.success("Blog published successfully!")
            st.rerun()
        else:
            st.error("Please fill in both title and content.")

elif page == "View Blogs":
    st.header("View Blogs")
    blogs = load_blogs()
    if blogs:
        for blog in blogs:
            st.subheader(blog["title"])
            if blog.get("created_at"):
                st.caption(f"Published {blog['created_at']}")
            st.write(blog["content"])
            st.markdown("---")
    else:
        st.info("No blogs available. Write one now!")