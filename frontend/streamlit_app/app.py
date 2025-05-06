# frontend/streamlit_app/app.py

import streamlit as st
import requests

# ─── 1) MUST be the very first Streamlit call ───────────────
st.set_page_config(page_title="LLM‑CookBook", layout="wide")

# ─── 2) CSS injection (now safe) ─────────────────────────────
st.markdown(
    """
    <style>
      /* ── indent & bullet the UL/LI inside each expander ───────── */
      .streamlit-expanderContent ul {
        list-style-position: inside !important;
        padding-left: 1.5rem   !important;
        margin-bottom: 1rem    !important;
      }
      .streamlit-expanderContent li {
        margin-bottom: 0.5rem  !important;
      }

      /* ── hide any literal “None” text in those header lines ────── */
      .streamlit-expanderContent p, .streamlit-expanderContent span {
        visibility: visible;
      }
      /* this will target the “None” spans and hide them */
      .streamlit-expanderContent span {
        /* override any span that *only* contains None */
        font-size: 0px;
        line-height: 0;
      }
      /* show everything else normally */
      .streamlit-expanderContent span:not(:contains("None")) {
        font-size: initial;
        line-height: initial;
      }

      /* ── add a bit more breathing room around the title line ─── */
      .streamlit-expanderHeader {
        margin-bottom: 0.5rem !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─── 3) Now the rest of your UI ───────────────────────────────
API_URL = "http://localhost:8000"

st.title("🍲 AI-Based Recipe Finder & Generator")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    ingredients_input = st.text_input(
        "Ingredients (comma-separated)", placeholder="e.g. chicken, garlic, onion"
    )
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["", "vegan", "vegetarian", "gluten‑free", "keto", "paleo"],
    )
    max_prep = st.slider("Max Prep Time (min)", 0, 120, 10)
    max_cook = st.slider("Max Cook Time (min)", 0, 190, 20)
    allergens = st.multiselect(
        "Exclude Allergens",
        [
            "milk",
            "eggs",
            "fish",
            "shellfish",
            "peanuts",
            "tree nuts",
            "wheat",
            "soy",
            "sesame",
        ],
    )
    preferred_cuisine = st.selectbox(
        "Preferred Cuisine", ["", "Italian", "Mexican", "Indian", "Thai", "American"]
    )
    search_clicked = st.button("🔍 Search Recipes")


def build_payload():
    ings = [i.strip() for i in ingredients_input.split(",") if i.strip()]
    payload = {"ingredients": ings}
    if dietary_pref:
        payload["dietary_preference"] = dietary_pref
    if max_prep > 0:
        payload["max_prep_time"] = max_prep
    if max_cook > 0:
        payload["max_cook_time"] = max_cook
    if allergens:
        payload["excluded_allergens"] = allergens
    if preferred_cuisine:
        payload["preferred_cuisine"] = preferred_cuisine
    return payload


# ─── Search block ─────────────────────────────────────────────
if search_clicked:
    if not ingredients_input.strip():
        st.sidebar.error("Enter at least one ingredient!")
    else:
        payload = build_payload()
        with st.spinner("Searching…"):
            try:
                res = requests.post(
                    f"{API_URL}/recipes/search", json=payload["ingredients"], timeout=10
                )
                res.raise_for_status()
                results = res.json().get("results", [])
            except Exception as e:
                st.error(f"Search failed: {e}")
                results = []

        if results:
            st.success(f"Found {len(results)} matching recipes:")
            for r in results:
                with st.expander(r["title"]):
                    st.markdown(
                        f"Preparation Time: {str(r.get('prep_time', 'N/A'))}   Serves: {str(r.get('servings', 'N/A'))}"
                    )
                    st.subheader("Ingredients")
                    for ing in r["ingredients"]:
                        st.write(f"- {ing}")
                    st.subheader("Instructions")
                    for step in r["instructions"]:
                        st.write(f"- {step}")
        else:
            st.info("No matches found. Try “Generate New Recipe” below.")


# ─── Generate block ───────────────────────────────────────────
st.markdown("---")
if st.button("🤖 Generate New Recipe"):
    if not ingredients_input.strip():
        st.error("Enter at least one ingredient!")
    else:
        payload = build_payload()
        with st.spinner("Generating recipe…"):
            try:
                res = requests.post(
                    f"{API_URL}/recipes/generate", json=payload, timeout=30
                )
                res.raise_for_status()
                data = res.json().get("recipe", {})
            except Exception as e:
                st.error(f"Generation failed: {e}")
                data = {}

        if data.get("error"):
            st.error(data["error"])
            data = data.get("recipe", {})

        if data:
            st.success(f"📝 {data.get('##title','##Untitled Recipe')}")
            st.markdown(
                f"**Prep Time:** {data.get('prep_time','N/A')}  &nbsp; "
                f"**Cook Time:** {data.get('cook_time','N/A')}  &nbsp; "
                f"**Servings:** {data.get('servings','N/A')}"
            )
            if data.get("cuisine"):
                st.markdown(f"**Cuisine:** {data['cuisine']}")
            st.subheader("Ingredients")
            for ing in data.get("ingredients", []):
                st.write(f"- {ing}")
            st.subheader("Instructions")
            for step in data.get("instructions", []):
                st.write(f"- {step}")

st.markdown("---")
st.caption("Powered by FastAPI + FAISS + Ollama LLM")
