import streamlit as st
import random
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Growth Mindset Companion", page_icon=" 🌟", layout="wide")

# Custom CSS for unique styling
st.markdown("""
    <style>
    .main-title {
        color: #2E8B57;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .section-header {
        color: #4682B4;
        font-size: 24px;
    }
    .motivation-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Growth Mindset App
st.markdown('<div class="main-title">Growth Mindset Companion</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Daily Affirmations", "Goal Tracker", "Reflection"])

# Expanded list of affirmations
affirmations = [
    "I can learn anything with effort and practice.",
    "Challenges help me grow stronger.",
    "My potential is limitless when I keep trying.",
    "Mistakes are opportunities to learn.",
    "I embrace difficulties as chances to improve.",
    "Every step forward counts, no matter how small.",
    "I am capable of more than I realize.",
    "Growth begins where comfort ends."
]

# Motivational quotes
motivational_quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "It’s not that I’m so smart, it’s just that I stay with problems longer. - Albert Einstein",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill"
]

# Initialize session state
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'reflections' not in st.session_state:
    st.session_state.reflections = []

# Home Page
if page == "Home":
    st.markdown('<div class="section-header">Welcome to Your Growth Journey</div>', unsafe_allow_html=True)
    st.write("""
    This app helps you cultivate a growth mindset through:
    - Daily affirmations to boost positivity
    - Goal tracking with progress visualization
    - Reflection space for self-awareness
    """)
    st.markdown('<div class="motivation-box">Daily Motivation: ' + random.choice(motivational_quotes) + '</div>', unsafe_allow_html=True)

# Daily Affirmations Page
elif page == "Daily Affirmations":
    st.markdown('<div class="section-header">Daily Affirmation</div>', unsafe_allow_html=True)
    if st.button("Get Today's Affirmation"):
        daily_affirmation = random.choice(affirmations)
        st.markdown(f'<div class="motivation-box">{daily_affirmation}</div>', unsafe_allow_html=True)
    st.write("Refresh daily for new inspiration!")

# Goal Tracker Page
elif page == "Goal Tracker":
    st.markdown('<div class="section-header">Goal Tracker</div>', unsafe_allow_html=True)
    
    # Add new goal
    with st.form("goal_form"):
        new_goal = st.text_input("Enter a new goal")
        submit_goal = st.form_submit_button("Add Goal")
        if submit_goal and new_goal:
            st.session_state.goals.append({
                "goal": new_goal,
                "date_added": datetime.now().strftime("%Y-%m-%d"),
                "completed": False,
                "progress": 0  # New progress tracking
            })
            st.success(f"Goal '{new_goal}' added!")

    # Display goals and progress
    if st.session_state.goals:
        st.subheader("Your Goals")
        goals_df = pd.DataFrame(st.session_state.goals)
        
        # Calculate completion percentage
        completed_count = sum(1 for goal in st.session_state.goals if goal['completed'])
        total_goals = len(st.session_state.goals)
        progress = (completed_count / total_goals * 100) if total_goals > 0 else 0
        st.progress(int(progress))
        st.write(f"Overall Progress: {progress:.1f}%")

        # Goal list with completion and progress
        for i, goal in enumerate(st.session_state.goals):
            col1, col2 = st.columns([3, 1])
            with col1:
                completed = st.checkbox(f"{goal['goal']} (Added: {goal['date_added']})", 
                                      value=goal['completed'], 
                                      key=f"goal_{i}")
                st.session_state.goals[i]['completed'] = completed
            with col2:
                progress_val = st.slider("Progress", 0, 100, goal['progress'], key=f"prog_{i}")
                st.session_state.goals[i]['progress'] = progress_val
        
        # Styled goals table
        st.dataframe(goals_df.style.apply(lambda x: ['background: lightgreen' if x['completed'] else '' 
                                                    for i in x], axis=1))

# Reflection Page
elif page == "Reflection":
    st.markdown('<div class="section-header">Daily Reflection</div>', unsafe_allow_html=True)
    
    with st.form("reflection_form"):
        reflection = st.text_area("What did you learn today? What challenges did you face?")
        mood = st.selectbox("How do you feel about today?", ["Good", "Okay", "Challenging","Great"])
        submit_reflection = st.form_submit_button("Save Reflection")
        if submit_reflection and reflection:
            st.session_state.reflections.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "reflection": reflection,
                "mood": mood
            })
            st.success("Reflection saved!")
    
    # Display previous reflections with mood
    if st.session_state.reflections:
        st.subheader("Your Reflections")
        reflections_df = pd.DataFrame(st.session_state.reflections)
        st.dataframe(reflections_df.style.apply(lambda x: ['background: #98FB98' if x['mood'] == 'Great' else 
                                                         'background: #F0F8FF' if x['mood'] == 'Good' else 
                                                         'background: #FFFACD' if x['mood'] == 'Okay' else 
                                                         'background: #FFB6C1' for i in x], axis=1))

# Footer
st.sidebar.write("---")
st.sidebar.write("Built with ❤️ using Streamlit")
st.sidebar.write("Built by Muhammad Farooq")
st.sidebar.write(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")