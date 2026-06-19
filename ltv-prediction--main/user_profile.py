import streamlit as st

from auth import update_profile

# -----------------------------------
# PROFILE PAGE
# -----------------------------------
st.title("👤 Edit Profile")

st.markdown("---")

if 'user_id' not in st.session_state:

    st.warning(
        "Please login first"
    )

else:

    username = st.text_input(
        "New Username"
    )

    phone = st.text_input(
        "New Phone Number"
    )
    gmail = st.text_input(
        "New Email"
    )

    if st.button("Update Profile"):

        update_profile(

            st.session_state.user_id,

            username,

            phone

        )

        st.success(
            "Profile updated successfully!"
        )