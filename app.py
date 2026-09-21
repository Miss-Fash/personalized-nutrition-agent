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


# ===================================================
# PAGE SETTINGS
# ===================================================

st.set_page_config(
    page_title="Nutrilead AI Nutrition Adviser",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ===================================================
# CREATE DATABASE TABLES
# ===================================================

create_tables()


# ===================================================
# SESSION STATE
# ===================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "My Nutrition Profile"

if "nutrition_advice" not in st.session_state:
    st.session_state.nutrition_advice = None

if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None

if "daily_tip" not in st.session_state:
    st.session_state.daily_tip = None


# ===================================================
# LOGIN / CREATE ACCOUNT
# ===================================================

if not st.session_state.logged_in:

    st.title("🥗 Nutrilead AI Nutrition Adviser")

    st.write(
        "Your personal nutrition assistant for practical "
        "and healthier food choices."
    )

    st.divider()

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

            if not email.strip() or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                user = authenticate_user(
                    email.strip().lower(),
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.session_state.page = (
                        "My Nutrition Profile"
                    )

                    st.session_state.nutrition_advice = None
                    st.session_state.meal_plan = None
                    st.session_state.daily_tip = None

                    st.rerun()

                else:

                    st.error(
                        "Wrong email or password."
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

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
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

            if (
                not full_name.strip()
                or not signup_email.strip()
                or not signup_password
            ):

                st.error(
                    "Please fill in all the required fields."
                )

            elif signup_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(signup_password) < 6:

                st.error(
                    "Password should be at least 6 characters."
                )

            else:

                success, message = create_user(
                    full_name.strip(),
                    signup_email.strip().lower(),
                    signup_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Account created successfully. "
                        "You can now login."
                    )

                else:

                    st.error(message)

    st.stop()


# ===================================================
# LOGGED-IN USER
# ===================================================

user = st.session_state.user


# ===================================================
# TOP NAVIGATION
# ===================================================

st.title("🥗 Nutrilead")

st.caption(
    f"Welcome, {user['full_name']}"
)

st.divider()


pages = [
    "My Nutrition Profile",
    "Dashboard",
    "Edit Profile",
    "Progress Track",
]


selected_page = st.selectbox(
    "Menu",
    pages,
    index=pages.index(st.session_state.page)
)


st.session_state.page = selected_page


# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------

if st.button(
    "Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "My Nutrition Profile"

    st.session_state.nutrition_advice = None
    st.session_state.meal_plan = None
    st.session_state.daily_tip = None

    st.rerun()


st.divider()


# ===================================================
# GET CURRENT PROFILE
# ===================================================

profile = get_nutrition_profile(
    user["id"]
)


# ===================================================
# MY NUTRITION PROFILE
# ===================================================

if st.session_state.page == "My Nutrition Profile":

    st.header("👤 My Nutrition Profile")

    st.write(
        "Your nutrition information helps Nutrilead "
        "provide more personalized guidance."
    )

    st.divider()

    # ------------------------------------------------
    # PROFILE EXISTS
    # ------------------------------------------------

    if profile is not None:

        st.subheader("Your Saved Profile")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Age",
                f"{profile['age']} years"
            )

            st.metric(
                "Weight",
                f"{profile['weight']} kg"
            )

            st.metric(
                "Height",
                f"{profile['height']} cm"
            )

            st.write(
                f"**Sex:** {profile['sex']}"
            )

        with col2:

            st.metric(
                "Health Goal",
                profile["health_goal"]
            )

            st.write(
                f"**Dietary Preference:** "
                f"{profile['dietary_preference']}"
            )

            st.write(
                f"**Activity Level:** "
                f"{profile['activity_level']}"
            )

            st.write(
                f"**Food Allergies:** "
                f"{profile['allergies'] or 'None provided'}"
            )

        st.divider()

        st.write(
            f"**Foods You Enjoy:** "
            f"{profile['preferred_foods'] or 'None provided'}"
        )

        st.write(
            f"**Foods You Want to Avoid:** "
            f"{profile['avoided_foods'] or 'None provided'}"
        )

        st.success(
            "Your nutrition profile is saved."
        )

        st.info(
            "Use the Menu above and select "
            "'Edit Profile' to update your information."
        )

    # ------------------------------------------------
    # CREATE PROFILE
    # ------------------------------------------------

    else:

        st.info(
            "Let's create your nutrition profile first."
        )

        with st.form(
            "nutrition_profile_form"
        ):

            st.subheader(
                "Personal Information"
            )

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

            with col2:

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

            st.subheader(
                "Food Information"
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

                st.session_state.nutrition_advice = None
                st.session_state.meal_plan = None
                st.session_state.daily_tip = None

                st.success(
                    "Your nutrition profile has been saved successfully!"
                )

                st.rerun()


# ===================================================
# DASHBOARD
# ===================================================

elif st.session_state.page == "Dashboard":

    st.header("🤖 AI Nutrition Dashboard")

    st.write(
        f"Hello, {user['full_name']}! "
        "Let's make healthier food choices together."
    )

    st.divider()

    if profile is None:

        st.warning(
            "Your nutrition profile has not been completed."
        )

        st.info(
            "Go to 'My Nutrition Profile' from the Menu "
            "to provide your information."
        )

    else:

        st.subheader(
            "Your Nutrition Summary"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Age",
                f"{profile['age']} years"
            )

            st.metric(
                "Weight",
                f"{profile['weight']} kg"
            )

        with col2:

            st.metric(
                "Height",
                f"{profile['height']} cm"
            )

            st.metric(
                "Health Goal",
                profile["health_goal"]
            )

        st.divider()

        # ------------------------------------------------
        # PERSONALIZED ADVICE
        # ------------------------------------------------

        st.subheader(
            "🤖 Personalized Nutrition Advice"
        )

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

                    st.session_state.nutrition_advice = advice

                except Exception as error:

                    st.error(
                        f"Unable to generate advice: {error}"
                    )

        if st.session_state.nutrition_advice:

            st.markdown(
                st.session_state.nutrition_advice
            )

        st.divider()

        # ------------------------------------------------
        # MEAL PLAN
        # ------------------------------------------------

        st.subheader(
            "🍽️ My One-Day Meal Plan"
        )

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

                    st.session_state.meal_plan = meal_plan

                except Exception as error:

                    st.error(
                        f"Unable to generate meal plan: {error}"
                    )

        if st.session_state.meal_plan:

            st.markdown(
                st.session_state.meal_plan
            )

        st.divider()

        # ------------------------------------------------
        # DAILY TIP
        # ------------------------------------------------

        st.subheader(
            "💡 Today's Nutrilead Tip"
        )

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

                    st.session_state.daily_tip = daily_tip

                except Exception as error:

                    st.error(
                        f"Unable to generate tip: {error}"
                    )

        if st.session_state.daily_tip:

            st.info(
                st.session_state.daily_tip
            )


# ===================================================
# EDIT PROFILE
# ===================================================

elif st.session_state.page == "Edit Profile":

    st.header("✏️ Edit Nutrition Profile")

    if profile is None:

        st.warning(
            "You do not have a nutrition profile yet."
        )

        st.info(
            "Go to 'My Nutrition Profile' to create one."
        )

    else:

        with st.form(
            "edit_profile_form"
        ):

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
                    index=sex_options.index(
                        current_sex
                    )
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

            with col2:

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
                    if profile["dietary_preference"]
                    in dietary_options
                    else "No specific preference"
                )

                dietary_preference = st.selectbox(
                    "Dietary Preference",
                    dietary_options,
                    index=dietary_options.index(
                        current_diet
                    )
                )

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
                    if profile["health_goal"]
                    in goal_options
                    else "General healthy eating"
                )

                health_goal = st.selectbox(
                    "Health Goal",
                    goal_options,
                    index=goal_options.index(
                        current_goal
                    )
                )

                activity_options = [
                    "Low",
                    "Moderate",
                    "High"
                ]

                current_activity = (
                    profile["activity_level"]
                    if profile["activity_level"]
                    in activity_options
                    else "Low"
                )

                activity_level = st.selectbox(
                    "Activity Level",
                    activity_options,
                    index=activity_options.index(
                        current_activity
                    )
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

                st.session_state.nutrition_advice = None
                st.session_state.meal_plan = None
                st.session_state.daily_tip = None

                st.success(
                    "Your nutrition profile has been updated successfully."
                )

                st.rerun()


# ===================================================
# PROGRESS TRACK
# ===================================================

elif st.session_state.page == "Progress Track":

    st.header("📊 Progress Track")

    st.write(
        "Track a few simple nutrition and wellness habits each day."
    )

    st.divider()

    # ------------------------------------------------
    # DAILY PROGRESS
    # ------------------------------------------------

    st.subheader(
        "📊 Today's Nutrition Progress"
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

    with st.form(
        "daily_progress_form"
    ):

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

    st.divider()

    # ------------------------------------------------
    # PROGRESS HISTORY
    # ------------------------------------------------

    st.subheader(
        "📈 Progress History"
    )

    history = get_progress_history(
        user["id"]
    )

    if history:

        for record in history:

            date = record[0]
            water = record[1]
            meals = record[2]
            fruits = record[3]
            activity = record[4]
            rating = record[5]

            with st.expander(
                str(date)
            ):

                st.write(
                    f"💧 Water: {water} L"
                )

                st.write(
                    f"🥗 Healthy meals: {meals}"
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


# ===================================================
# FOOTER
# ===================================================

st.divider()

st.caption(
    "Nutrilead — Promoting food as medicine through practical nutrition."
)