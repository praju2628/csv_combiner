
import streamlit as st
# for front end and also for file uploader
import  pandas as pd
# for data processing,
import base64
# for encoding it in base64 to make it suitable for web usage( put in web header)

st.set_page_config(page_title="Data Cleaning Tool ")
hide_streamlilt_style="""
<style>
#MianMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlilt_style,unsafe_allow_html=True)
st.title("CSV Data Cleaning Tool")
st.markdown("Upload one or multiple CSV files to preprocess and lean your files quickly")
# acts as a standard file objects stays in memory
uploaded_files = st.file_uploader('chose CSV files',type="csv",accept_multiple_files=True)
dataframes = []

if uploaded_files:
    for file in uploaded_files:
        file.tell()
        file.seek(0)
        file.tell()
        df = pd.read_csv(file)
        dataframes.append(df)


    if len(dataframes)>1:
        merge = st.checkbox("Merge upload CSV files")
        if merge:
            keep_first_header_only = st.selectbox("keep only the header(first row) of the first file",["yes","no"])
            remove_duplicate_rows = st.selectbox("Remove duplicate rows", ["no", "yes"])
            remove_empty_rows = st.selectbox("Remove empty rows", ["yes", "no"])
            end_line = st.selectbox("End line", ["\\n", "\\r\\n"])
            try:
                if keep_first_header_only == "yes":
                    for i, df in enumerate(dataframes[1:]):
                        df.columns = dataframes[0].columns.intersection(df.columns)
                        dataframes[i+1] =df
                merged_df = pd.concat(dataframes,ignore_index=True,join='outer')
                st.write("Before:", len(merged_df))
                if remove_duplicate_rows == 'yes':
                    merged_df.drop_duplicates(inplace=True)


                if remove_empty_rows == 'yes':
                    merged_df.dropna(inplace=True,how='all')
                dataframes = [merged_df]
            except ValueError as e:
                st.error("please make sure columns match in all files. If you don't want them to match ,select 'No' in the first opttion. ")
                st.stop()
            st.write("After:", len(merged_df))

        show_dataframes = st.checkbox("show DataFrames",value=True)
        if show_dataframes:
            for i, df in enumerate(dataframes):
                st.write(f"DataFrame {i + 1}")
                st.dataframe(df)
        if st.button("Download cleaned data"):
            for i,df in enumerate(dataframes):
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href = "data:file/csv; base64,{b64}" download="cleande_data_{i+1}.csv'
                st.markdown(href,unsafe_allow_html=True)
else:

    st.warning("please upload CSV files")

st.markdown("")
st.markdown("----")
st.markdown("")
st.markdown("i will put git hub link here ")







