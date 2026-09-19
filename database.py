
import sqlite3
import bcrypt


DATABASE_NAME = "nutrilead.db"


# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

def create_connection():
    return sqlite3.connect(DATABASE_NAME)


# ---------------------------------------------------
# CREATE TABLES
# ---------------------------------------------------

def create_tables():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nutrition_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            age INTEGER,
            sex TEXT,
            height REAL,
            weight REAL,
            dietary_preference TEXT,
            health_goal TEXT,
            activity_level TEXT,
            allergies TEXT,
            preferred_foods TEXT,
            avoided_foods TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            water REAL,
            healthy_meals INTEGER,
            fruit_vegetables INTEGER,
            physical_activity TEXT,
            wellness_rating INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    connection.commit()
    connection.close()


# ---------------------------------------------------
# CREATE USER
# ---------------------------------------------------

def create_user(full_name, email, password):

    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:

        cursor.execute(
            """
            INSERT INTO users (
                full_name,
                email,
                password
            )
            VALUES (?, ?, ?)
            """,
            (
                full_name,
                email,
                hashed_password
            )
        )

        connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    finally:

        connection.close()


# ---------------------------------------------------
# AUTHENTICATE USER
# ---------------------------------------------------

def authenticate_user(email, password):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, full_name, email, password
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    user_id, full_name, user_email, stored_password = user

    if bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    ):

        return {
            "id": user_id,
            "full_name": full_name,
            "email": user_email
        }

    return None


# ---------------------------------------------------
# SAVE NUTRITION PROFILE
# ---------------------------------------------------

def save_nutrition_profile(
    user_id,
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
):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO nutrition_profiles (
            user_id,
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            age = excluded.age,
            sex = excluded.sex,
            height = excluded.height,
            weight = excluded.weight,
            dietary_preference = excluded.dietary_preference,
            health_goal = excluded.health_goal,
            activity_level = excluded.activity_level,
            allergies = excluded.allergies,
            preferred_foods = excluded.preferred_foods,
            avoided_foods = excluded.avoided_foods
        """,
        (
            user_id,
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
    )

    connection.commit()
    connection.close()


# ---------------------------------------------------
# GET NUTRITION PROFILE
# ---------------------------------------------------

def get_nutrition_profile(user_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
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
        FROM nutrition_profiles
        WHERE user_id = ?
        """,
        (user_id,)
    )

    profile = cursor.fetchone()

    connection.close()

    if profile is None:
        return None

    return {
        "age": profile[0],
        "sex": profile[1],
        "height": profile[2],
        "weight": profile[3],
        "dietary_preference": profile[4],
        "health_goal": profile[5],
        "activity_level": profile[6],
        "allergies": profile[7],
        "preferred_foods": profile[8],
        "avoided_foods": profile[9]
    }


# ---------------------------------------------------
# SAVE DAILY PROGRESS
# ---------------------------------------------------

def save_daily_progress(
    user_id,
    water,
    healthy_meals,
    fruit_vegetables,
    physical_activity,
    wellness_rating
):

    from datetime import date

    connection = create_connection()
    cursor = connection.cursor()

    today = str(date.today())

    cursor.execute(
        """
        SELECT id
        FROM daily_progress
        WHERE user_id = ? AND date = ?
        """,
        (user_id, today)
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE daily_progress
            SET
                water = ?,
                healthy_meals = ?,
                fruit_vegetables = ?,
                physical_activity = ?,
                wellness_rating = ?
            WHERE user_id = ? AND date = ?
            """,
            (
                water,
                healthy_meals,
                fruit_vegetables,
                physical_activity,
                wellness_rating,
                user_id,
                today
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO daily_progress (
                user_id,
                date,
                water,
                healthy_meals,
                fruit_vegetables,
                physical_activity,
                wellness_rating
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                today,
                water,
                healthy_meals,
                fruit_vegetables,
                physical_activity,
                wellness_rating
            )
        )

    connection.commit()
    connection.close()


# ---------------------------------------------------
# GET TODAY'S PROGRESS
# ---------------------------------------------------

def get_daily_progress(user_id):

    from datetime import date

    connection = create_connection()
    cursor = connection.cursor()

    today = str(date.today())

    cursor.execute(
        """
        SELECT
            water,
            healthy_meals,
            fruit_vegetables,
            physical_activity,
            wellness_rating
        FROM daily_progress
        WHERE user_id = ? AND date = ?
        """,
        (user_id, today)
    )

    progress = cursor.fetchone()

    connection.close()

    if progress is None:
        return None

    return {
        "water": progress[0],
        "healthy_meals": progress[1],
        "fruit_vegetables": progress[2],
        "physical_activity": progress[3],
        "wellness_rating": progress[4]
    }


# ---------------------------------------------------
# GET PROGRESS HISTORY
# ---------------------------------------------------

def get_progress_history(user_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            date,
            water,
            healthy_meals,
            fruit_vegetables,
            physical_activity,
            wellness_rating
        FROM daily_progress
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    connection.close()

    return history


