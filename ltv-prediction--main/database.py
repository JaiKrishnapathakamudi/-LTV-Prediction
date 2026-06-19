import mysql.connector
import pandas as pd

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ltv_project"
)

cursor = connection.cursor()

# -----------------------------------
# CREATE TABLE IF NOT EXISTS
# -----------------------------------
create_table_query = """

CREATE TABLE IF NOT EXISTS customers (

    id INT PRIMARY KEY AUTO_INCREMENT,

    customer_name VARCHAR(255),

    recency INT,

    frequency INT,

    monetary FLOAT,

    predicted_ltv FLOAT,

    customer_segment VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

"""

cursor.execute(create_table_query)
connection.commit()

# -----------------------------------
# INSERT CUSTOMER DATA
# -----------------------------------
def save_prediction(
    customer_name,
    recency,
    frequency,
    monetary,
    predicted_ltv,
    customer_segment
):

    query = """

    INSERT INTO customers(

        customer_name,
        recency,
        frequency,
        monetary,
        predicted_ltv,
        customer_segment

    )

    VALUES (%s, %s, %s, %s, %s, %s)

    """

    values = (
        customer_name,
        recency,
        frequency,
        monetary,
        predicted_ltv,
        customer_segment
    )

    cursor.execute(query, values)
    connection.commit()

    print("Prediction saved successfully!")

# -----------------------------------
# FETCH CUSTOMER DATA
# -----------------------------------
def fetch_predictions():

    query = """

    SELECT

        id,
        customer_name,
        recency,
        frequency,
        monetary,
        predicted_ltv,
        customer_segment,
        created_at

    FROM customers

    ORDER BY id DESC

    """

    cursor.execute(query)

    data = cursor.fetchall()

    columns = [
        "id",
        "customer_name",
        "recency",
        "frequency",
        "monetary",
        "predicted_ltv",
        "customer_segment",
        "created_at"
    ]

    df = pd.DataFrame(
        data,
        columns=columns
    )

    return df

# -----------------------------------
# DELETE PREDICTION
# -----------------------------------
def delete_prediction(prediction_id):

    query = """

    DELETE FROM customers

    WHERE id = %s

    """

    cursor.execute(
        query,
        (prediction_id,)
    )

    connection.commit()

# -----------------------------------
# GET CUSTOMER SEGMENT COUNTS
# -----------------------------------
def get_segment_counts():

    query = """

    SELECT

        customer_segment,
        COUNT(*) as total

    FROM customers

    GROUP BY customer_segment

    """

    cursor.execute(query)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "customer_segment",
            "total"
        ]
    )

    return df

# -----------------------------------
# GET TOTAL PREDICTED REVENUE
# -----------------------------------
def get_total_revenue():

    query = """

    SELECT SUM(predicted_ltv)

    FROM customers

    """

    cursor.execute(query)

    result = cursor.fetchone()

    total = result[0]

    if total is None:
        total = 0

    return total

# -----------------------------------
# GET VIP CUSTOMER COUNT
# -----------------------------------
def get_vip_count():

    query = """

    SELECT COUNT(*)

    FROM customers

    WHERE customer_segment = 'VIP Customer'

    """

    cursor.execute(query)

    result = cursor.fetchone()

    return result[0]

# -----------------------------------
# GET AVERAGE LTV
# -----------------------------------
def get_average_ltv():

    query = """

    SELECT AVG(predicted_ltv)

    FROM customers

    """

    cursor.execute(query)

    result = cursor.fetchone()

    avg_ltv = result[0]

    if avg_ltv is None:
        avg_ltv = 0

    return avg_ltv

# -----------------------------------
# FETCH ALL DATA AS DATAFRAME
# -----------------------------------
def fetch_prediction_dataframe():

    query = """

    SELECT
        id,
        customer_name,
        recency,
        frequency,
        monetary,
        predicted_ltv,
        customer_segment,
        created_at

    FROM customers

    ORDER BY created_at DESC

    """

    df = pd.read_sql(query, connection)

    return df
# -------------------------------
# DASHBOARD DATAFRAME
# -------------------------------
def fetch_dashboard_data():

    query = """
    SELECT
        customer_name,
        predicted_ltv,
        customer_segment,
        created_at
    FROM customers
    ORDER BY created_at DESC
    """

    df = pd.read_sql(query, connection)

    return df
# -------------------------------
# KPI SUMMARY
# -------------------------------
def get_dashboard_summary():

    query = """

    SELECT

        COUNT(*) as total_predictions,

        COALESCE(SUM(predicted_ltv),0) as total_predicted_revenue,

        COALESCE(AVG(predicted_ltv),0) as avg_ltv

    FROM customers

    """

    cursor.execute(query)
    result = cursor.fetchone()
    return result
# -------------------------------
# SAVE USER
# -------------------------------
def save_user(
    google_id,
    name,
    email,
    picture
):

    query = """

    INSERT INTO users (
        google_id,
        name,
        email,
        picture
    )

    VALUES (%s,%s,%s,%s)

    ON DUPLICATE KEY UPDATE

    name=VALUES(name),
    email=VALUES(email),
    picture=VALUES(picture)

    """

    values = (
        google_id,
        name,
        email,
        picture
    )

    cursor.execute(query, values)

    connection.commit()


# -------------------------------
# LOGIN HISTORY
# -------------------------------
def log_user_login(email):

    query = """

    INSERT INTO login_history (
        email
    )

    VALUES (%s)

    """

    cursor.execute(
        query,
        (email,)
    )

    connection.commit()


# -------------------------------
# FETCH LOGIN HISTORY
# -------------------------------
def fetch_login_history():

    query = """

    SELECT
        email,
        login_time

    FROM login_history

    ORDER BY login_time DESC

    """

    cursor.execute(query)

    return cursor.fetchall()