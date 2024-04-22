# import streamlit as st
# import streamlit_authenticator as stauth
# from streamlit_option_menu import option_menu
# from database import *
# from urllib.error import URLError

# st.set_page_config(page_title="Register")
# st.header("Registration")
# html_str = f"""<html><body>
#                 <p> click here to {'<a href="https://resume-screening-6exf2w3vbii.streamlit.app/login_page"target="_self">login</a>'}</p>
#                 </html></body>"""


# try:
#     username = st.text_input("User Name")
#     email = st.text_input("Email")
#     password = st.text_input("Password",type='password')
#     hashing_password = make_hashes(password)
#     if st.button("Register"):
#         result = fetch_email(email)
#         if (result!=None):
#             st.warning("User Already exists, Please click on Login button")
#             st.markdown(html_str, unsafe_allow_html=True)
#         else:
#             add_user(username,email,hashing_password)
#             st.success("Account registration successfull")
#             st.markdown(html_str, unsafe_allow_html=True)
            

# except URLError as e:
#     st.error(
#         """
#         **This page requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )

