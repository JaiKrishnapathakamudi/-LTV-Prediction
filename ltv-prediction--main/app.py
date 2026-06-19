import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from report_generator import generate_pdf_report
from streamlit_autorefresh import st_autorefresh
from auth_google import google_login
from database import (
    save_prediction,
    fetch_predictions,
    fetch_prediction_dataframe,
    fetch_dashboard_data,
    get_dashboard_summary,
    fetch_login_history
)

# -------------------------------------
# PAGE CONFIG
# -------------------------------------
st.set_page_config(
    page_title="Customer LTV Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_style("darkgrid")
plt.style.use("dark_background")

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: linear-gradient(180deg, #071025 0%, #111827 100%);
        color: #f8fafc;
    }
    .css-18e3th9 {
        background: rgba(15, 23, 42, 0.78) !important;
        box-shadow: 0 30px 90px rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
    }
    .css-1d391kg {
        color: #f8fafc !important;
    }
    .css-1v0mbdj, .css-1avcm0n {
        background: rgba(15, 23, 42, 0.95) !important;
        border-radius: 18px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div>div,
    .stTextArea>div>div>textarea {
        background: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 14px !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #e2e8f0 !important;
    }
    .sidebar .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%) !important;
        border-radius: 22px;
    }
    .sidebar .stButton>button {
        width: 100%;
    }
    .metrics-card {
        padding: 1rem 1.2rem;
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    .hero-banner {
        padding: 1.5rem 1.6rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.24), rgba(6, 182, 212, 0.18));
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.6rem;
        margin-bottom: 0.6rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    .section-subtitle {
        color: #94a3b8;
        margin-bottom: 1.4rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------
# LOGIN CHECK
# -------------------------------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# -------------------------------------
# USER INFO
# -------------------------------------

def render_section(title, subtitle=None):
    subtitle_html = f"<p class='section-subtitle'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class='section-header'>{title}</div>
        {subtitle_html}
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")
st.sidebar.success(
    f"👤 {st.session_state.username}"
)

render_section(
    "📊 Customer LTV Prediction Dashboard",
    f"Explore customer lifetime value predictions, trends, and business intelligence powered by your dataset."
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Logged In User",
        st.session_state.username
    )

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print("BASE_DIR =", BASE_DIR)
from auth_guard import require_login
from database import save_prediction, fetch_predictions

# Login protection
require_login()

# -------------------------------------
# LOAD MODEL
# -------------------------------------
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "ltv_model.pkl"
)

model = joblib.load(MODEL_PATH)

# -------------------------------------
# LOAD DATA
# -------------------------------------
@st.cache_data
def load_data():

    data = pd.read_csv(
    os.path.join(BASE_DIR, "data", "online_retail.csv")
)

    # Cleaning
    data.dropna(inplace=True)

    data.drop_duplicates(inplace=True)

    data = data[data['Quantity'] > 0]

    data = data[data['UnitPrice'] > 0]

    # Revenue column
    data['TotalPrice'] = (
        data['Quantity'] * data['UnitPrice']
    )

    return data


data = load_data()

# -------------------------------------
# SIDEBAR
# -------------------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(

    "Go to",

    [
        "Dashboard",
        "LTV Prediction",
        "Prediction History",
         "AI Analytics",
          "Real-Time Analytics",
         "Reports",
        "Customer Insights",
        "Business Analytics"
    ]
)

# -------------------------------------
# DASHBOARD PAGE
# -------------------------------------
if page == "Dashboard":

    st.title("📊 Customer Lifetime Value Dashboard")

    st.markdown("---")

    total_revenue = data[
        'TotalPrice'
    ].sum()

    total_customers = data[
        'CustomerID'
    ].nunique()

    total_orders = data[
        'InvoiceNo'
    ].nunique()

    avg_order = data[
        'TotalPrice'
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    col2.metric(
        "👥 Customers",
        total_customers
    )

    col3.metric(
        "🛒 Orders",
        total_orders
    )

    col4.metric(
        "📦 Avg Order Value",
        f"₹{avg_order:.2f}"
    )

    st.markdown("---")

    # Top Countries Chart
    st.subheader("🌍 Top Countries by Revenue")

    top_countries = data.groupby(
        'Country'
    )['TotalPrice'].sum()

    top_countries = top_countries.sort_values(
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=top_countries.values,
        y=top_countries.index,
        ax=ax
    )

    ax.set_title(
        "Top Countries by Revenue"
    )

    st.pyplot(fig)

# -------------------------------------
# LTV PREDICTION PAGE
# -------------------------------------
elif page == "LTV Prediction":

    st.title(
        "🤖 Predict Customer Lifetime Value"
    )

    st.markdown(
        "Enter customer information below"
    )

    st.markdown("---")

    # Customer Name
    customer_name = st.text_input(
        "Customer Name"
    )

    # Input fields
    col1, col2, col3 = st.columns(3)

    with col1:

        recency = st.number_input(

            "Recency (days)",

            min_value=0,

            value=10

        )

    with col2:

        frequency = st.number_input(

            "Frequency",

            min_value=1,

            value=5

        )

    with col3:

        monetary = st.number_input(

            "Monetary Value",

            min_value=0.0,

            value=1000.0

        )

    # Predict button
    if st.button("Predict LTV"):

        # Features
        features = np.array([
            [recency, frequency, monetary]
        ])

        # Prediction
        prediction = model.predict(
            features
        )

        predicted_ltv = prediction[0]

        # Segmentation
        if predicted_ltv > 10000:

            segment = "VIP Customer"

        elif frequency > 5:

            segment = "Loyal Customer"

        else:

            segment = "Regular Customer"

        # Output
        st.success(

            f"Predicted Customer LTV: ₹{predicted_ltv:,.2f}"

        )

        st.info(
            f"Customer Segment: {segment}"
        )

        # Save
        save_prediction(

            customer_name=customer_name,

            recency=int(recency),

            frequency=int(frequency),

            monetary=float(monetary),

            predicted_ltv=float(predicted_ltv),

            customer_segment=segment

        )

        st.success(
            "✅ Prediction saved successfully!"
        )

# -------------------------------------
# PREDICTION HISTORY PAGE
# -------------------------------------
elif page == "Prediction History":

    st.title(
        "📊 Prediction History Dashboard"
    )

    st.markdown("---")

    predictions = fetch_prediction_dataframe()

    if not predictions.empty:

        # ---------------------------------
        # KPI METRICS
        # ---------------------------------
        total_predictions = len(
            predictions
        )

        avg_ltv = predictions[
            'predicted_ltv'
        ].mean()

        vip_count = len(

            predictions[

                predictions[
                    'customer_segment'
                ] == "VIP Customer"

            ]

        )

        total_revenue = predictions[
            'predicted_ltv'
        ].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📦 Total Predictions",
            total_predictions
        )

        col2.metric(
            "💰 Avg Predicted LTV",
            f"₹{avg_ltv:,.2f}"
        )

        col3.metric(
            "🌟 VIP Customers",
            vip_count
        )

        col4.metric(
            "📈 Total Predicted Revenue",
            f"₹{total_revenue:,.0f}"
        )

        st.markdown("---")

        # ---------------------------------
        # SEARCH
        # ---------------------------------
        search_customer = st.text_input(
            "🔍 Search Customer Name"
        )

        filtered_df = predictions.copy()

        if search_customer:

            filtered_df = filtered_df[

                filtered_df[
                    'customer_name'
                ].str.contains(

                    search_customer,

                    case=False,

                    na=False

                )

            ]

        # ---------------------------------
        # FILTER
        # ---------------------------------
        segment_filter = st.selectbox(

            "🎯 Filter by Segment",

            [

                "All",

                "VIP Customer",

                "Loyal Customer",

                "Regular Customer"

            ]

        )

        if segment_filter != "All":

            filtered_df = filtered_df[

                filtered_df[
                    'customer_segment'
                ] == segment_filter

            ]

        st.markdown("---")

        # ---------------------------------
        # TABLE
        # ---------------------------------
        st.subheader(
            "📋 Prediction Records"
        )

        st.dataframe(

            filtered_df,

            use_container_width=True

        )

        # ---------------------------------
        # DOWNLOAD BUTTON
        # ---------------------------------
        csv = filtered_df.to_csv(
            index=False
        ).encode('utf-8')

        st.download_button(

            label="⬇ Download CSV",

            data=csv,

            file_name='prediction_history.csv',

            mime='text/csv'

        )

        st.markdown("---")

        # ---------------------------------
        # SEGMENT CHART
        # ---------------------------------
        st.subheader(
            "📈 Customer Segments"
        )

        segment_count = filtered_df[
            'customer_segment'
        ].value_counts()

        fig1, ax1 = plt.subplots(
            figsize=(8, 4)
        )

        sns.barplot(

            x=segment_count.index,

            y=segment_count.values,

            ax=ax1

        )

        ax1.set_title(
            "Customer Segment Distribution"
        )

        st.pyplot(fig1)

        # ---------------------------------
        # TREND CHART
        # ---------------------------------
        st.subheader(
            "📊 Predicted LTV Trend"
        )

        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )

        ax2.plot(

            filtered_df.index,

            filtered_df[
                'predicted_ltv'
            ]

        )

        ax2.set_title(
            "Predicted LTV Trend"
        )

        ax2.set_xlabel(
            "Predictions"
        )

        ax2.set_ylabel(
            "Predicted LTV"
        )

        st.pyplot(fig2)

        # ---------------------------------
        # TIMELINE
        # ---------------------------------
        if 'created_at' in filtered_df.columns:

            st.subheader(
                "🕒 Prediction Timeline"
            )

            timeline_df = filtered_df.copy()

            timeline_df[
                'created_at'
            ] = pd.to_datetime(

                timeline_df[
                    'created_at'
                ]

            )

            timeline_group = timeline_df.groupby(

                timeline_df[
                    'created_at'
                ].dt.date

            ).size()

            fig3, ax3 = plt.subplots(
                figsize=(10, 5)
            )

            ax3.plot(

                timeline_group.index,

                timeline_group.values

            )

            ax3.set_title(
                "Daily Prediction Activity"
            )

            ax3.set_xlabel(
                "Date"
            )

            ax3.set_ylabel(
                "Predictions"
            )

            plt.xticks(rotation=45)

            st.pyplot(fig3)

        # ---------------------------------
        # CUSTOMER GROWTH
        # ---------------------------------
        st.subheader(
            "📈 Customer Growth"
        )

        growth_df = filtered_df.copy()

        growth_df[
            'customer_count'
        ] = range(
            1,
            len(growth_df) + 1
        )

        fig4, ax4 = plt.subplots(
            figsize=(10, 5)
        )

        ax4.plot(
            growth_df['customer_count']
        )

        ax4.set_title(
            "Customer Growth Over Time"
        )

        ax4.set_xlabel(
            "Predictions"
        )

        ax4.set_ylabel(
            "Customers"
        )

        st.pyplot(fig4)

    else:

        st.warning(
            "No prediction history found."
        )
# -------------------------------------
# AI ANALYTICS PAGE
# -------------------------------------
elif page == "AI Analytics":

    st.title("🤖 AI Analytics Dashboard")

    st.markdown("---")

    # ---------------------------------
    # LOAD ANALYTICS FILES
    # ---------------------------------
    feature_df = pd.read_csv(

        os.path.join(BASE_DIR, "data", "feature_importance.csv")

    )
    

    comparison_df = pd.read_csv(

        os.path.join(BASE_DIR, "data", "model_comparison.csv")

    )

    # ---------------------------------
    # MODEL COMPARISON
    # ---------------------------------
    st.subheader("📊 Model Performance Comparison")

    st.dataframe(

        comparison_df,

        use_container_width=True

    )

    fig1, ax1 = plt.subplots(figsize=(7,4))

    sns.barplot(

        x='Model',

        y='R2 Score',

        data=comparison_df,

        ax=ax1

    )

    ax1.set_title("Model Accuracy Comparison")

    st.pyplot(fig1)

    st.markdown("---")

    # ---------------------------------
    # FEATURE IMPORTANCE
    # ---------------------------------
    st.subheader("🔥 Feature Importance Analysis")

    st.dataframe(

        feature_df,

        use_container_width=True

    )

    fig2, ax2 = plt.subplots(figsize=(8,5))

    sns.barplot(

        x='Importance',

        y='Feature',

        data=feature_df,

        ax=ax2

    )

    ax2.set_title("Feature Importance")

    st.pyplot(fig2)

    st.markdown("---")

    # ---------------------------------
    # AI INSIGHTS
    # ---------------------------------
    st.subheader("🧠 AI Business Insights")

    top_feature = feature_df.sort_values(

        by='Importance',

        ascending=False

    ).iloc[0]['Feature']

    st.success(

        f"Most important factor affecting customer LTV: {top_feature}"

    )

    best_model = comparison_df.sort_values(

        by='R2 Score',

        ascending=False

    ).iloc[0]['Model']

    st.info(

        f"Best performing ML model: {best_model}"

    )
# -------------------------------------
# REAL-TIME ANALYTICS PAGE
# -------------------------------------
elif page == "Real-Time Analytics":

    st.title("⚡ Real-Time Analytics Dashboard")

    # auto refresh every 5 sec
    st_autorefresh(
        interval=5000,
        key="realtime_refresh"
    )

    summary = get_dashboard_summary()

    total_predictions = summary[0]
    total_revenue = summary[1]
    avg_ltv = summary[2]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📈 Total Predictions",
        total_predictions
    )

    col2.metric(
        "💰 Total Predicted Revenue",
        f"₹{total_revenue:,.2f}"
    )

    col3.metric(
        "📊 Average LTV",
        f"₹{avg_ltv:,.2f}"
    )

    st.markdown("---")

    df = fetch_dashboard_data()

    if not df.empty:

        st.subheader("🕒 Latest Predictions")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        st.subheader("👥 Segment Distribution")

        segment_counts = (
            df["customer_segment"]
            .value_counts()
        )

        fig, ax = plt.subplots(figsize=(7,4))

        sns.barplot(
            x=segment_counts.index,
            y=segment_counts.values,
            ax=ax
        )

        ax.set_title(
            "Customer Segment Distribution"
        )

        st.pyplot(fig)

    else:

        st.info(
            "No predictions found yet."
        )


 # -------------------------------------
# REPORTS PAGE
# -------------------------------------
elif page == "Reports":

    st.title("📄 Export Reports")

    st.markdown("---")

    df = fetch_prediction_dataframe()

    st.subheader("📊 Prediction Records")

    st.dataframe(df, use_container_width=True)

    # CSV EXPORT
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download CSV Report",
        data=csv,
        file_name='customer_predictions.csv',
        mime='text/csv'
    )

    st.markdown("---")

    # PDF EXPORT
    if st.button("📑 Generate PDF Report"):

        pdf_file = generate_pdf_report(df)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="⬇ Download PDF Report",
                data=file,
                file_name="customer_ltv_report.pdf",
                mime="application/pdf"
            )


   

# -------------------------------------
# CUSTOMER INSIGHTS PAGE
# -------------------------------------
elif page == "Customer Insights":

    st.title("👥 Customer Insights")

    st.markdown("---")

    top_customers = data.groupby(
        'CustomerID'
    )['TotalPrice'].sum()

    top_customers = top_customers.sort_values(
        ascending=False
    ).head(10)

    st.subheader(
        "🏆 Top 10 Customers"
    )

    st.dataframe(top_customers)

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    sns.barplot(

        x=top_customers.index.astype(str),

        y=top_customers.values,

        ax=ax

    )

    plt.xticks(rotation=45)

    ax.set_title(
        "Top Customers by Revenue"
    )

    st.pyplot(fig)

# -------------------------------------
# BUSINESS ANALYTICS PAGE
# -------------------------------------
elif page == "Business Analytics":

    st.title("📈 Business Analytics")

    st.markdown("---")

    # Top products
    st.subheader(
        "🔥 Best Selling Products"
    )

    top_products = data.groupby(
        'Description'
    )['Quantity'].sum()

    top_products = top_products.sort_values(
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    sns.barplot(

        x=top_products.values,

        y=top_products.index,

        ax=ax

    )

    ax.set_title(
        "Top Selling Products"
    )

    st.pyplot(fig)

    # Revenue distribution
    st.subheader(
        "📊 Revenue Distribution"
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    sns.histplot(

        data['TotalPrice'],

        bins=50,

        ax=ax2

    )

    ax2.set_title(
        "Revenue Distribution"
    )

    st.pyplot(fig2)
    # -------------------------------------
# ADMIN PANEL
# -------------------------------------
elif page == "Admin Panel":

    # Only admin can access
    if st.session_state.get("role") != "admin":

        st.warning(
            "⚠️ Access denied. Admins only."
        )

    else:

        st.title(
            "🛠 Admin Panel"
        )

        st.markdown("---")

        history = fetch_login_history()

        history_df = pd.DataFrame(

            history,

            columns=[
                "Email",
                "Login Time"
            ]
        )

        st.subheader(
            "📋 User Login Activity"
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        st.metric(
            "Total Logins",
            len(history_df)
        )