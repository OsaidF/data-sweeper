import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title='Datasweeper ')

st.title("Datasweeper Sterling Integerateor")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization creating the project for quarter 3!")

uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["cvs", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {0}", file_ext)
            continue

        st.write("Preview the head of the dataframe")
        st.dataframe(df.head()) 

        st.subheader('Data Cleaning Options')
        if st.checkbox(f"Clean Data for {0}", file.name):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicate from file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicated Removed!")
            
            with col2:
                if st.button(f"Fill missing values for: {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing columns have been filled")

        st.subheader('Select Columns to keep')
        columns = st.multiselect(f"Choose column for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualisation

        st.subheader('Data Visualisation')
        if st.checkbox(f"Show visualisation for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2]
            )

        # conversion options
        conversion_types = st.radio(f'convert {file.name} to:', ["CVS", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_types == "CVS":
                df.to_csv(buffer, index = False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = 'application/vnd.openxmlformats-officedoument.spreadsheetml.sheet'
            buffer.seek(0)


            st.download_button(
                label=f"Download {file.name} as {conversion_types}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("All Files Processed Successfully!")
