import streamlit as st
import numpy as np
import pandas as pd
import base64
import random
import json
from google.oauth2 import service_account
from google.cloud import storage

credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"])

if "client" not in st.session_state:
    st.session_state["client"] = storage.Client(credentials=credentials)

def get_quote(character : str):
    client = st.session_state["client"]
    bucket = client.bucket(st.secrets["BUCKET_NAME"])
    blob = bucket.blob(st.secrets["BLOB_NAME"])
    quotes = blob.download_as_string()
    return list(filter(lambda q : \
            q.get("author").startswith(character),
            json.loads(quotes)
             ))

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_img_as_base64("images/geralt.jpg")
side_img = get_img_as_base64("images/symbol.jpg")

page_bg_img = f"""
    <style>
    .body {{
        font-size:200px;
    }}
    [data-testid="stHeader"]{{
        background-color: rgba(0,0,0,0);
    }}

    [data-testid="stMarkdownContainer"]{{
            font-size:large;
            font:20px;
            font-family:Comic Sans MS;
            color:white;
            background-position: center;
            text-align: center;

        }}

    [data-testid="stSidebar"]{{
        background-image: url("data:image/jpg;base64,{side_img}");
        background-position: center;
        background-repeat: no-repeat;
    }}

    [id="i-am-submitted"]{{
        margin-top:0px;
        background-color:black;
    }}

    [data-testid="stAppViewContainer"]
    {{
        background-image: url("data:image/jpg;base64,{bg_img}");
        background-position: center;
        background-repeat: no-repeat;
        }}

    .coolesttitle{{
        font-size:50px;
    }}

    .quote {{
        font-size:30px;
        font-family:Comic Sans MS;
        background-color:black;
        opacity:0.8;
        margin-top:100px;
    }}

    [data-testid="stForm"]{{
        background-color:black;
        opacity:0.8;
    }}
    </style>"""

st.markdown(page_bg_img , unsafe_allow_html=True)
st.markdown("<div class='coolesttitle'> Witcher 3: Quotes </div>",
            unsafe_allow_html=True)
#st.markdown("<span style='color:orange'> Hello World! </span>",
# unsafe_allow_html=True)

submitted = None

col1 , col2 = st.columns(2)
submitted = False

characters = [
    "Geralt", "Yennefer", "Ciri", "Cahir", "Triss", "Mousesack", "Tissaia",
    "Queen Calanthe", "Renfri"
]

with st.sidebar:
    st.empty()
    chosen_character = st.radio("Who is your favourite character?",
                characters,
                index = 1
    )
    st.markdown(chosen_character)
    st.markdown(
        f"<a href='https://witcher.fandom.com/wiki/Category:The_Witcher_images_-_Characters'> My link </a>"
     , unsafe_allow_html = True)


    #st.stop()

## CAMERA INPUT

# img_file_buffer = st.camera_input("Take a picture")

# if img_file_buffer is not None:
#     # To read image file buffer as bytes:
#     bytes_data = img_file_buffer.getvalue()
#     # Check the type of bytes_data:
#     # Should output: <class 'bytes'>
#     st.write(type(bytes_data))


## DOWNLOAD CSV REPORT FROM OUR PREDICTION!

# df = pd.DataFrame({"Fare":1312321},index=[0])

# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

# st.dataframe(df)#.head()
# csv = convert_df(df)

# st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='large_df.csv',
#     mime='text/csv',
# )

with col1:
    with st.form("Search"):
        choice = st.selectbox("Choose Character", characters)
        submitted = st.form_submit_button("Submit")

with col2:
    if submitted:
        st.markdown("# I am submitted")
        response_quote = get_quote(choice)
        random_quote = random.choice(response_quote)
        quote = random_quote.get("quote")
        author = random_quote.get("author")
        st.markdown(f"<div class='quote'> {quote} </div> <br> ~ Said by: {author} ",
                        unsafe_allow_html = True)
