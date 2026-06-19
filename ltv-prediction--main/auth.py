# auth.py

import mysql.connector
import random
import bcrypt

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ltv_project"
    )


# -----------------------------------
# REGISTER USER
# -----------------------------------
def register_user(
    name,
    mobile,
    password
):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Check if mobile already exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE mobile = %s
        """,
        (mobile,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        cursor.close()
        conn.close()

        return False

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            mobile,
            password_hash,
            role
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            name,
            mobile,
            password_hash,
            "user"
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return True


# -----------------------------------
# LOGIN USER
# -----------------------------------
def login_user(
    mobile,
    password
):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE mobile = %s
        """,
        (mobile,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        return None

    stored_hash = user["password_hash"]

    if stored_hash and bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        return user

    return None


# -----------------------------------
# GENERATE RESET CODE
# -----------------------------------
def generate_reset_code():

    return str(
        random.randint(
            100000,
            999999
        )
    )


# -----------------------------------
# SAVE RESET CODE
# -----------------------------------
def save_reset_code(
    mobile,
    reset_code
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET reset_code = %s
        WHERE mobile = %s
        """,
        (
            reset_code,
            mobile
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


# -----------------------------------
# VERIFY RESET CODE
# -----------------------------------
def verify_reset_code(
    mobile,
    reset_code
):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE mobile = %s
        AND reset_code = %s
        """,
        (
            mobile,
            reset_code
        )
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# -----------------------------------
# RESET PASSWORD
# -----------------------------------
def reset_password(
    mobile,
    new_password
):

    conn = get_connection()

    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        UPDATE users
        SET password_hash = %s,
            reset_code = NULL
        WHERE mobile = %s
        """,
        (
            password_hash,
            mobile
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


# -----------------------------------
# UPDATE PROFILE
# -----------------------------------
def update_profile(
    user_id,
    name,
    mobile
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET
            name = %s,
            mobile = %s
        WHERE id = %s
        """,
        (
            name,
            mobile,
            user_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()