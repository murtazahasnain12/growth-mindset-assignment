# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# # Set up Our App
# st.set_page_config(page_title="Data Sweeper", layout="wide")
# st.title("💿 Data Sweeper")
# st.write("Transform your files between CSV and Excel format with built-in data cleaning and visualization.")

# uploaded_files = st.file_uploader("Upload your files (CSV or Excel)", type=['csv', 'xlsx'], accept_multiple_files=True)

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

#         if file_ext == '.csv':
#             df = pd.read_csv(uploaded_file)
#         elif file_ext == '.xlsx': 
#             df = pd.read_excel(uploaded_file)
#         else:
#             st.error(f'Unsupported file format: {file_ext}')
#             continue

#         # Display info about the file
#         st.write(f"**File Name:** {uploaded_file.name}")
#         st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

#         # Show 5 rows of our dataframe
#         st.subheader("Preview of the DataFrame")
#         st.dataframe(df.head())

#         # Options for data cleaning
#         st.subheader("Data Cleaning Options")
#         if st.checkbox(f"Clean Data for {uploaded_file.name}"):
#             col1, col2 = st.columns(2)

#             with col1:
#                 if st.button(f"Remove Duplicates from {uploaded_file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("✅ Duplicates Removed")

#             with col2:
#                 if st.button(f"Fill Missing Values for {uploaded_file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].apply(lambda col: col.fillna(col.mean()))
#                     st.write("✅ Missing Values Filled")

#         # Choose Specific Columns to Keep
#         st.subheader("Select Columns to Keep")
#         columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
#         df = df[columns]

#         # Data Visualization
#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
#             st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

#         # Convert the File to CSV or Excel
#         st.subheader("📂 Conversion Options")
#         conversion_type = st.radio(f"Convert {uploaded_file.name} to", ['CSV', 'Excel'], key=uploaded_file.name)

#         if st.button(f"Convert {uploaded_file.name}"):
#             buffer = BytesIO()

#             if conversion_type == 'CSV':
#                 df.to_csv(buffer, index=False)
#                 new_file_name = uploaded_file.name.replace(file_ext, '.csv')
#                 mime_type = 'text/csv'

#             elif conversion_type == 'Excel':
#                 df.to_excel(buffer, index=False, engine='openpyxl')
#                 new_file_name = uploaded_file.name.replace(file_ext, '.xlsx')
#                 mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

#             buffer.seek(0)

#             # Download Button
#             st.download_button(
#                 label=f"Download {new_file_name}",
#                 data=buffer,
#                 file_name=new_file_name,
#                 mime=mime_type
#             )

# st.success("✅ Thanks for using App.")
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.write("Transform your files between CSV and Excel format with built-in data cleaning and visualization.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel)", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        try:
            # Step 1: Read the file based on its extension
            if file_ext == '.csv':
                df = pd.read_csv(uploaded_file)
            elif file_ext == '.xlsx':
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f'Unsupported file format: {file_ext}')
                continue

            # Step 2: Display file info
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

            # Step 3: Show a preview of the DataFrame
            st.subheader("Preview of the DataFrame")
            st.dataframe(df.head())

            # Step 4: Data cleaning options
            st.subheader("Data Cleaning Options")
            if st.checkbox(f"Clean Data for {uploaded_file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Remove Duplicates from {uploaded_file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("✅ Duplicates Removed")

                with col2:
                    if st.button(f"Fill Missing Values for {uploaded_file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].apply(lambda col: col.fillna(col.mean()))
                        st.success("✅ Missing Values Filled")

            # Step 5: Select columns to keep
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Step 6: Data visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    st.bar_chart(df[numeric_cols].iloc[:, :2])
                else:
                    st.warning("Not enough numeric columns for visualization.")

            # Step 7: File conversion options
            st.subheader("📂 Conversion Options")
            conversion_type = st.radio(f"Convert {uploaded_file.name} to", ['CSV', 'Excel'], key=uploaded_file.name)

            if st.button(f"Convert {uploaded_file.name}"):
                buffer = BytesIO()

                if conversion_type == 'CSV':
                    df.to_csv(buffer, index=False)
                    new_file_name = uploaded_file.name.replace(file_ext, '.csv')
                    mime_type = 'text/csv'
                elif conversion_type == 'Excel':
                    try:
                        df.to_excel(buffer, index=False, engine='openpyxl')
                        new_file_name = uploaded_file.name.replace(file_ext, '.xlsx')
                        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    except ImportError:
                        st.error("The 'openpyxl' library is required for Excel conversion. Please install it using `pip install openpyxl`.")
                        continue

                buffer.seek(0)

                # Step 8: Download button
                st.download_button(
                    label=f"Download {new_file_name}",
                    data=buffer,
                    file_name=new_file_name,
                    mime=mime_type
                )

        except Exception as e:
            st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

st.success("✅ Thanks for using Data Sweeper!")