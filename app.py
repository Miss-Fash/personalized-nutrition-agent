import streamlit as st

from database import (
    create_tables,
    create_user,
    authenticate_user,
    save_nutrition_profile,
    get_nutrition_profile,
    save_daily_progress,
    get_daily_progress,
    get_progress_history,
)

from nutritionist_ai import (
    generate_nutrition_advice,
    generate_meal_plan,
    generate_daily_tip,
)


# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="Nutrilead AI Nutrition Adviser",
    page_icon="🥗",
    layout="wide",
)


# ---------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------

create_tables()


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ---------------------------------------------------
# LOGIN / CREATE ACCOUNT
# ---------------------------------------------------

if not st.session_state.logged_in:

    st.title("🥗 Nutrilead AI Nutrition Adviser")

    st.write(
        "Your personal nutrition assistant for practical and "
        "healthier food choices."
    )

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # ------------------------------------------------
    # LOGIN
    # ------------------------------------------------

    with login_tab:

        st.subheader("Welcome Back")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not email or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                user = authenticate_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "Dashboard"

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    # ------------------------------------------------
    # CREATE ACCOUNT
    # ------------------------------------------------

    with signup_tab:

        st.subheader("Create Your Account")

        full_name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not full_name or not email or not password:

                st.error(
                    "Please fill in all the required fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password should be at least 6 characters."
                )

            else:

                success, message = create_user(
                    full_name,
                    email,
                    password
                )

                if success:

                    st.success(message)
                    st.info(
                        "You can now login using your email and password."
                    )

                else:

                    st.error(message)

    st.stop()


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

user = st.session_state.user

st.sidebar.title("🥗 Nutrilead")

st.sidebar.write(
    f"Welcome, {user['full_name']}"
)

st.sidebar.divider()

pages = [
    "Dashboard",
    "My Nutrition Profile",
    "Edit Profile",
]

selected_page = st.sidebar.radio(
    "Menu",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = selected_page

st.sidebar.divider()

if st.sidebar.button(
    "Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "Dashboard"

    st.rerun()


# ---------------------------------------------------
# GET PROFILE
# ---------------------------------------------------

profile = get_nutrition_profile(
    user["id"]
)


# ===================================================
# DASHBOARD
# ===================================================

if st.session_state.page == "Dashboard":

    st.title("🥗 AI Nutrition Adviser")

    st.write(
        f"Hello, {user['full_name']}! "
        "Let's make healthier food choices together."
    )

    st.divider()

    if profile is None:

        st.warning(
            "Your nutrition profile has not been completed yet."
        )

        st.info(
            "Please go to 'My Nutrition Profile' to provide "
            "your information."
        )

    else:

        # ---------------------------------------------
        # PROFILE SUMMARY
        # ---------------------------------------------

        st.subheader("Your Nutrition Profile")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Age",
                f"{profile['age']} years"
            )

        with col2:
            st.metric(
                "Weight",
                f"{profile['weight']} kg"
            )

        with col3:
            st.metric(
                "Height",
                f"{profile['height']} cm"
            )

        with col4:
            st.metric(
                "Goal",
                profile["health_goal"]
            )

        st.divider()

        # ---------------------------------------------
        # AI NUTRITION ADVICE
        # ---------------------------------------------

        st.subheader("🤖 Personalized Nutrition Advice")

        if st.button(
            "Get My Nutrition Advice",
            use_container_width=True
        ):

            with st.spinner(
                "Preparing your personalized nutrition advice..."
            ):

                try:

                    advice = generate_nutrition_advice(
                        profile
                    )

                    st.session_state["nutrition_advice"] = advice

                except Exception as error:

                    st.error(
                        f"Unable to generate advice: {error}"
                    )

        if "nutrition_advice" in st.session_state:

            st.markdown(
                st.session_state["nutrition_advice"]
            )

        st.divider()

        # ---------------------------------------------
        # MEAL PLAN
        # ---------------------------------------------

        st.subheader("🍽️ My One-Day Meal Plan")

        if st.button(
            "Generate Meal Plan",
            use_container_width=True
        ):

            with st.spinner(
                "Creating your meal plan..."
            ):

                try:

                    meal_plan = generate_meal_plan(
                        profile
                    )

                    st.session_state["meal_plan"] = meal_plan

                except Exception as error:

                    st.error(
                        f"Unable to generate meal plan: {error}"
                    )

        if "meal_plan" in st.session_state:

            st.markdown(
                st.session_state["meal_plan"]
            )

        st.divider()

        # ---------------------------------------------
        # DAILY TIP
        # ---------------------------------------------

        st.subheader("💡 Today's Nutrilead Tip")

        if st.button(
            "Get Today's Tip",
            use_container_width=True
        ):

            with st.spinner(
                "Preparing today's tip..."
            ):

                try:

                    daily_tip = generate_daily_tip(
                        profile
                    )

                    st.session_state["daily_tip"] = daily_tip

                except Exception as error:

                    st.error(
                        f"Unable to generate tip: {error}"
                    )

        if "daily_tip" in st.session_state:

            st.info(
                st.session_state["daily_tip"]
            )


# ===================================================
# MY NUTRITION PROFILE
# ===================================================

elif st.session_state.page == "My Nutrition Profile":

    st.title("👤 My Nutrition Profile")

    st.write(
        "Tell us about yourself so Nutrilead can provide "
        "more personalized guidance."
    )

    with st.form("nutrition_profile_form"):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=25
            )

            sex = st.selectbox(
                "Sex",
                [
                    "Female",
                    "Male",
                    "Prefer not to say"
                ]
            )

            height = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=250.0,
                value=165.0,
                step=0.5
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=10.0,
                max_value=300.0,
                value=60.0,
                step=0.5
            )

            dietary_preference = st.selectbox(
                "Dietary Preference",
                [
                    "No specific preference",
                    "Vegetarian",
                    "Vegan",
                    "Pescatarian",
                    "Low carbohydrate",
                    "High protein"
                ]
            )

        with col2:

            health_goal = st.selectbox(
                "Health Goal",
                [
                    "General healthy eating",
                    "Weight management",
                    "Weight gain",
                    "Healthy weight loss",
                    "Muscle support",
                    "Better energy",
                    "Healthy digestion"
                ]
            )

            activity_level = st.selectbox(
                "Activity Level",
                [
                    "Low",
                    "Moderate",
                    "High"
                ]
            )

            allergies = st.text_area(
                "Food Allergies",
                placeholder="Example: peanuts, milk"
            )

            preferred_foods = st.text_area(
                "Foods You Enjoy",
                placeholder="Example: rice, beans, vegetables, fish"
            )

            avoided_foods = st.text_area(
                "Foods You Want to Avoid",
                placeholder="Example: sugary drinks, fried foods"
            )

        submitted = st.form_submit_button(
            "Save Nutrition Profile",
            use_container_width=True
        )

        if submitted:

            save_nutrition_profile(
                user["id"],
                age,
                sex,
                height,
                weight,
                dietary_preference,
                health_goal,
                activity_level,
                allergies,
                preferred_foods,
                avoided_foods
            )

            st.success(
                "Your nutrition profile has been saved successfully!"
            )

            st.rerun()


# ===================================================
# EDIT PROFILE
# ===================================================

elif st.session_state.page == "Edit Profile":

    st.title("✏️ Edit Nutrition Profile")

    if profile is None:

        st.warning(
            "You do not have a nutrition profile yet."
        )

        st.info(
            "Go to 'My Nutrition Profile' to create one."
        )

    else:

        with st.form("edit_profile_form"):

            col1, col2 = st.columns(2)

            with col1:

                age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=120,
                    value=int(profile["age"])
                )

                sex_options = [
                    "Female",
                    "Male",
                    "Prefer not to say"
                ]

                current_sex = (
                    profile["sex"]
                    if profile["sex"] in sex_options
                    else "Prefer not to say"
                )

                sex = st.selectbox(
                    "Sex",
                    sex_options,
                    index=sex_options.index(current_sex)
                )

                height = st.number_input(
                    "Height (cm)",
                    min_value=50.0,
                    max_value=250.0,
                    value=float(profile["height"]),
                    step=0.5
                )

                weight = st.number_input(
                    "Weight (kg)",
                    min_value=10.0,
                    max_value=300.0,
                    value=float(profile["weight"]),
                    step=0.5
                )

                dietary_options = [
                    "No specific preference",
                    "Vegetarian",
                    "Vegan",
                    "Pescatarian",
                    "Low carbohydrate",
                    "High protein"
                ]

                current_diet = (
                    profile["dietary_preference"]
                    if profile["dietary_preference"] in dietary_options
                    else "No specific preference"
                )

                dietary_preference = st.selectbox(
                    "Dietary Preference",
                    dietary_options,
                    index=dietary_options.index(current_diet)
                )

            with col2:

                goal_options = [
                    "General healthy eating",
                    "Weight management",
                    "Weight gain",
                    "Healthy weight loss",
                    "Muscle support",
                    "Better energy",
                    "Healthy digestion"
                ]

                current_goal = (
                    profile["health_goal"]
                    if profile["health_goal"] in goal_options
                    else "General healthy eating"
                )

                health_goal = st.selectbox(
                    "Health Goal",
                    goal_options,
                    index=goal_options.index(current_goal)
                )

                activity_options = [
                    "Low",
                    "Moderate",
                    "High"
                ]

                current_activity = (
                    profile["activity_level"]
                    if profile["activity_level"] in activity_options
                    else "Low"
                )

                activity_level = st.selectbox(
                    "Activity Level",
                    activity_options,
                    index=activity_options.index(current_activity)
                )

                allergies = st.text_area(
                    "Food Allergies",
                    value=profile["allergies"] or ""
                )

                preferred_foods = st.text_area(
                    "Foods You Enjoy",
                    value=profile["preferred_foods"] or ""
                )

                avoided_foods = st.text_area(
                    "Foods You Want to Avoid",
                    value=profile["avoided_foods"] or ""
                )

            submitted = st.form_submit_button(
                "Update Profile",
                use_container_width=True
            )

            if submitted:

                save_nutrition_profile(
                    user["id"],
                    age,
                    sex,
                    height,
                    weight,
                    dietary_preference,
                    health_goal,
                    activity_level,
                    allergies,
                    preferred_foods,
                    avoided_foods
                )

                st.success(
                    "Your nutrition profile has been updated."
                )

                st.rerun()


# ===================================================
# DAILY NUTRITION PROGRESS
# ===================================================

if st.session_state.logged_in:

    st.divider()

    st.title("📊 Daily Nutrition Progress")

    st.write(
        "Track a few simple habits each day."
    )

    existing_progress = get_daily_progress(
        user["id"]
    )

    if existing_progress:

        default_water = float(
            existing_progress["water"] or 0
        )

        default_meals = int(
            existing_progress["healthy_meals"] or 0
        )

        default_fruits = int(
            existing_progress["fruit_vegetables"] or 0
        )

        default_activity = (
            existing_progress["physical_activity"]
            or ""
        )

        default_rating = int(
            existing_progress["wellness_rating"] or 5
        )

    else:

        default_water = 0.0
        default_meals = 0
        default_fruits = 0
        default_activity = ""
        default_rating = 5

    with st.form("daily_progress_form"):

        col1, col2 = st.columns(2)

        with col1:

            water = st.number_input(
                "Water intake today (litres)",
                min_value=0.0,
                max_value=10.0,
                value=default_water,
                step=0.5
            )

            healthy_meals = st.number_input(
                "Healthy meals today",
                min_value=0,
                max_value=10,
                value=default_meals,
                step=1
            )

            fruit_vegetables = st.number_input(
                "Servings of fruits/vegetables",
                min_value=0,
                max_value=20,
                value=default_fruits,
                step=1
            )

        with col2:

            physical_activity = st.text_input(
                "Physical activity",
                value=default_activity,
                placeholder="Example: 30 minutes walking"
            )

            wellness_rating = st.slider(
                "How do you feel today?",
                min_value=1,
                max_value=10,
                value=default_rating
            )

        submitted = st.form_submit_button(
            "Save Today's Progress",
            use_container_width=True
        )

        if submitted:

            save_daily_progress(
                user["id"],
                water,
                healthy_meals,
                fruit_vegetables,
                physical_activity,
                wellness_rating
            )

            st.success(
                "Today's progress has been saved!"
            )

            st.rerun()


# ===================================================
# PROGRESS HISTORY
# ===================================================

if st.session_state.logged_in:

    st.divider()

    st.subheader("📈 Progress History")

    history = get_progress_history(
        user["id"]
    )

    if history:

        for record in history:

            date = record[0]
            water = record[1]
            healthy_meals = record[2]
            fruits = record[3]
            activity = record[4]
            rating = record[5]

            with st.expander(date):

                st.write(
                    f"💧 Water: {water} L"
                )

                st.write(
                    f"🥗 Healthy meals: {healthy_meals}"
                )

                st.write(
                    f"🍎 Fruits/vegetables: {fruits}"
                )

                st.write(
                    f"🏃 Physical activity: {activity}"
                )

                st.write(
                    f"⭐ Wellness rating: {rating}/10"
                )

    else:

        st.info(
            "No progress has been recorded yet."
        )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Nutrilead — Promoting food as medicine through practical nutrition."
)