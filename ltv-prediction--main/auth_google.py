import streamlit as st
from streamlit_oauth import OAuth2Component
from database import save_user, log_user_login
import requests

# -----------------------------------
# GOOGLE CONFIG
# -----------------------------------
CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]

CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"

TOKEN_URL = "https://oauth2.googleapis.com/token"

USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# -----------------------------------
# OAUTH COMPONENT
# -----------------------------------
oauth2 = OAuth2Component(

    CLIENT_ID,

    CLIENT_SECRET,

    AUTHORIZE_URL,

    TOKEN_URL
)


# -----------------------------------
# GOOGLE LOGIN
# -----------------------------------
def google_login():

    result = oauth2.authorize_button(

        "🔐 Continue with Google",

        redirect_uri="http://localhost:8501",

        scope="openid email profile",

        key="google"
    )

    if result and "token" in result:

        access_token = result["token"]["access_token"]

        response = requests.get(

            USERINFO_URL,

            headers={

                "Authorization":
                f"Bearer {access_token}"

            }
        )

        if response.status_code == 200:

            user_data = response.json()

            # Save user into database
            save_user(

                google_id=user_data["sub"],

                name=user_data["name"],

                email=user_data["email"],

                picture=user_data["picture"]

            )

            # Save login history
            log_user_login(

                user_data["email"]

            )

            return user_data

    return None