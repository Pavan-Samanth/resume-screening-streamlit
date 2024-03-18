import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# st.set_page_config(
#     page_title="Resume Screening",
#     page_icon="👋",
# )
# register_link = "[register]http://localhost:8501/register_page"
# login_link = "[login]http://localhost:8501/login_page"
html_str = f"""<html><body>
                <p> Welcome to Resume Screening App! 👋 </p>
                <p> In today's industry its difficult to go through each resume and select that particular candidates who are associated to a Job Description .</p>
                <p> So we designed this app, Where you will give the input of JD file and a set of resumes and it will return the top 5 resumes whose score matches to the given Job Description. </p>
                <p> Click on the left arrow to register, login and then upload the files of Job Description and multiple resume files.</p>
                <p> If you hadn't registered {'<a href="https://resume-screening-6exf2w3vbii.streamlit.app/register_page" target="_self">click here!</a>'}</p>
                <p> If you are already a registered user {'<a href="https://resume-screening-6exf2w3vbii.streamlit.app/login_page" target="_self">click here!</a>'}</p>
                </html></body>"""

st.markdown(html_str, unsafe_allow_html=True)

