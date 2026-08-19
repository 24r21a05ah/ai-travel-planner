
import os
import streamlit as st
from google import genai

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM TITLE
# ---------------------------------------------------------
st.title("✈️ AI Travel Planner")
st.write(
    "Plan a complete trip using AI based on your destination, "
    "budget, duration, and travel preferences."
)

st.divider()

# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning(
        "Gemini API key is not configured. "
        "Add GEMINI_API_KEY in your deployment environment variables."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    destination = st.text_input(
        "📍 Destination",
        placeholder="Example: Goa"
    )

    days = st.number_input(
        "📅 Number of Days",
        min_value=1,
        max_value=30,
        value=3
    )

    travelers = st.number_input(
        "👥 Number of Travelers",
        min_value=1,
        max_value=20,
        value=1
    )

with col2:
    budget = st.number_input(
        "💰 Total Budget (₹)",
        min_value=500,
        max_value=1000000,
        value=5000,
        step=500
    )

    travel_style = st.selectbox(
        "🎯 Travel Style",
        [
            "Budget",
            "Adventure",
            "Relaxation",
            "Family",
            "Friends",
            "Couple",
            "Food & Culture",
            "Nature"
        ]
    )

    starting_location = st.text_input(
        "🚆 Starting Location",
        placeholder="Example: Hyderabad"
    )

preferences = st.text_area(
    "✨ Additional Preferences",
    placeholder="Example: Beaches, local food, sightseeing, shopping, avoid expensive hotels..."
)

st.divider()

# ---------------------------------------------------------
# GENERATE TRAVEL PLAN
# ---------------------------------------------------------
if st.button("🚀 Generate My Travel Plan", use_container_width=True):

    if not destination:
        st.error("Please enter a destination.")
        st.stop()

    if not starting_location:
        st.error("Please enter your starting location.")
        st.stop()

    # -----------------------------------------------------
    # AGENTIC TRAVEL PLANNING PROMPT
    # -----------------------------------------------------
    prompt = f"""
You are an intelligent AI Travel Planning Agent.

Your job is to create a practical and budget-conscious travel
plan by performing these steps internally:

STEP 1: Understand the travel requirements.
STEP 2: Plan suitable activities and destinations.
STEP 3: Estimate transportation expenses.
STEP 4: Estimate accommodation expenses.
STEP 5: Estimate food expenses.
STEP 6: Estimate sightseeing and activity expenses.
STEP 7: Calculate the approximate total cost.
STEP 8: Compare the estimated cost with the user's budget.
STEP 9: If the plan exceeds the budget, optimize it by suggesting
cheaper alternatives.
STEP 10: Produce a clear final itinerary.

TRAVEL DETAILS:

Starting Location: {starting_location}
Destination: {destination}
Number of Days: {days}
Number of Travelers: {travelers}
Total Budget: ₹{budget}
Travel Style: {travel_style}
Additional Preferences: {preferences}

IMPORTANT INSTRUCTIONS:

1. Create a day-by-day itinerary.
2. Keep the plan realistic for the stated budget.
3. Clearly separate estimated expenses.
4. Give approximate prices in Indian Rupees.
5. Include transportation suggestions.
6. Include accommodation suggestions/categories.
7. Include food expenses.
8. Include sightseeing/activity expenses.
9. Calculate an approximate total budget.
10. Calculate the approximate remaining budget.
11. If the budget is insufficient, clearly explain why and
suggest ways to reduce the cost.
12. Do not claim that prices are exact or guaranteed.
13. Mention that prices can vary depending on season and availability.

FORMAT YOUR FINAL RESPONSE LIKE THIS:

# ✈️ Trip Overview

Destination:
Duration:
Travelers:
Travel Style:
Budget:

# 🗺️ Day-by-Day Itinerary

## Day 1
- Morning:
- Afternoon:
- Evening:
- Food:
- Estimated Day 1 Cost:

## Day 2
- Morning:
- Afternoon:
- Evening:
- Food:
- Estimated Day 2 Cost:

Continue for all days.

# 💰 Budget Breakdown

| Category | Estimated Cost |
|----------|----------------|
| Transportation | ₹ |
| Accommodation | ₹ |
| Food | ₹ |
| Activities | ₹ |
| Miscellaneous | ₹ |
| TOTAL | ₹ |

# 💡 Budget Optimization

Explain how to save money if necessary.

# 🎒 Travel Tips

Give useful practical tips.

# ⚠️ Important Note

Clearly state that prices and availability are estimates and
should be verified before booking.
"""

    # -----------------------------------------------------
    # AI RESPONSE
    # -----------------------------------------------------
    with st.spinner("🤖 AI Travel Agent is planning your trip..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.success("✅ Your travel plan is ready!")

            st.markdown(response.text)

        except Exception as e:
            st.error("Something went wrong while generating the plan.")
            st.code(str(e))

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "🤖 AI Travel Planner | Built using Streamlit and Google Gemini"
)
