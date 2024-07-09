import streamlit as st
from pages.tools.scrapermain import scraper_main
import pandas as pd
from pymongo import MongoClient
import base64
from io import BytesIO
from bson import ObjectId

from menu import menu_with_redirect

menu_with_redirect()

# MongoDB connection details
# mongo_uri = 'mongodb://localhost:27017/'
database_name = 'scraped'
collection_name = 'history'
# data_collection = 'scrap_info'

# Connect to MongoDB
# client = MongoClient(mongo_uri)
client = MongoClient("mongodb://root:Edubild_123@mongodb:27017")
db = client[database_name]
history_collection = db[collection_name]
data_collection = db['scrap_info']

# Fetch data from MongoDB
data = list(history_collection.find().sort('date_and_time', -1))

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)


st.markdown(
    """
    <style>
    .header-text {
        font-size: 28px; 
        font-weight: bold;
        color:red;
    }
    .custom-radio-label{
        font-size: 24px;
        font-weight: bold;
    }
    .table-title{
    font-size: 20px;
    font-weight: bold;
    }
    </style>
    <div class="header-text">Web Scrapper</div>
    """,
    unsafe_allow_html=True
)


st.markdown("""<div class="custom-radio-label">Enter a link or Upload Excel sheet with multiple links</div>""", unsafe_allow_html=True)

type = st.radio(
    "",
    ["Enter Link", "Upload Excel Sheet"],
    captions=["Enter a single link.", "Upload a single file with links in a single column"]
)

if type == "Enter Link":
    link = st.text_input("Enter Link")
else:
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    column_name = st.text_input("Enter the column name to extract:")
    



# Callback function to be called when the button is clicked
def on_submit():
    if type == "Enter Link":
        if link == "" or link.strip() == "":
            st.warning("Link Can Not Be None!")
            return False
        urls = [link]
        scraper_main(urls, link)
        st.write(f"Scrapping Completed, {link}")
    else:
        # Load the Excel file
        df = pd.read_excel(uploaded_file)

        # Specify the column name you want to extract
        # column_name = column_name

        # Extract the column values and convert to a list
        column_values = df[column_name].tolist()

        scraper_main(column_values, uploaded_file.name)


# Create a form
with st.form(key='my_form'):
    submit_button = st.form_submit_button(
            label="Submit",
            help="Click to submit the form",
            on_click=on_submit,
            # args=(title, type),
            type="primary",
            disabled=False,
            use_container_width=True
        )


if '_id' in df.columns:
    df['_id'] = df['_id'].astype(str)


# Display the DataFrame in Streamlit
st.markdown("""<div class="custom-radio-label">History</div>""", unsafe_allow_html=True)
# st.dataframe(df)


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


for index, row in df.iterrows():
    st.write(row.to_dict())
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Download button for Excel
        if st.button('Download Excel', key=f"{index}-1"):
            # Fetch data from 'data_collection' based on '_id' from 'history'
            row_id = ObjectId(row['_id'])
            another_data = list(data_collection.find({'history': row_id}))
            print("***")
            print(row['_id'], "another_data = ", another_data)
            print("***")
            # Convert fetched data to DataFrame (example)
            another_df = pd.DataFrame(list(another_data))
            
            if not another_df.empty:
                # Convert DataFrame to Excel
                excel_data = BytesIO()
                with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
                    another_df.to_excel(writer, sheet_name='Sheet1', index=False)
                
                excel_data.seek(0)
                b64 = base64.b64encode(excel_data.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx">Download Excel</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.write("No data found in 'data_collection' for this _id")
    
    with col2:
        # Delete button
        if st.button('Delete', key=f"{index}-2"):
            print("delete")
            row_id = ObjectId(row['_id'])
            data_collection.delete_many({'history': row_id})
            history_collection.delete_one({'_id': row_id})
            st.write("Deleted row with ID:", row['_id'])
            st.experimental_rerun()