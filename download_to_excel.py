import io
import pandas as pd
import streamlit as st


st.write("# Download Data in Excel")




# Function to convert DataFrame to Excel and return as a BytesIO object
file_name = "pledge_rtr_all_data"+date_string_pledge+".xlsx"
df = df_pledge
button_name = 'Download Excel File: '+ file_name
sheet_name = 'df_pledge'

def to_excel(df, sheet_name):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        for i, col in enumerate(df.columns):
            # Find the maximum length of the content for the current column
            column_len = max(df[col].astype(str).map(len).max(),  # length of largest item
                             len(str(col)))  # length of column header/title
            # Set the column width as max content length + a little extra margin
            column_len = column_len/2
            worksheet.set_column(i, i, column_len + 1)
    processed_data = output.getvalue()
    return processed_data

df_excel = to_excel(df, sheet_name) 
st.download_button(label=button_name,
                       data=df_excel,
                       file_name=file_name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Adjusted MIME type for .xlsx
    
    


# Function to convert DataFrame to Excel and return as a BytesIO object
file_name = "pledge_rtr_summary"+date_string_pledge+".xlsx"
df = df_pledge_summary
button_name = 'Download Excel File: '+ file_name
sheet_name = 'df_pledge_summary'

def to_excel(df, sheet_name):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        for i, col in enumerate(df.columns):
            # Find the maximum length of the content for the current column
            column_len = max(df[col].astype(str).map(len).max(),  # length of largest item
                             len(str(col)))  # length of column header/title
            # Set the column width as max content length + a little extra margin
            column_len = column_len/2
            worksheet.set_column(i, i, column_len + 1)
    processed_data = output.getvalue()
    return processed_data

df_excel = to_excel(df, sheet_name) 
st.download_button(label=button_name,
                       data=df_excel,
                       file_name=file_name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Adjusted MIME type for .xlsx
    
    
# Function to convert DataFrame to Excel and return as a BytesIO object
file_name = "gi_rtr_all_data"+date_string_gi+".xlsx"
df = df_gi
button_name = 'Download Excel File: '+ file_name
sheet_name = 'df_gi'

def to_excel(df, sheet_name):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        for i, col in enumerate(df.columns):
            # Find the maximum length of the content for the current column
            column_len = max(df[col].astype(str).map(len).max(),  # length of largest item
                             len(str(col)))  # length of column header/title
            # Set the column width as max content length + a little extra margin
            column_len = column_len/2
            worksheet.set_column(i, i, column_len + 1)
    processed_data = output.getvalue()
    return processed_data

df_excel = to_excel(df, sheet_name) 
st.download_button(label=button_name,
                       data=df_excel,
                       file_name=file_name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Adjusted MIME type for .xlsx
    
    
    
    

# Function to convert DataFrame to Excel and return as a BytesIO object
file_name = "gi_rtr_summary"+date_string_gi+".xlsx"
df = df_gi_summary
button_name = 'Download Excel File: '+ file_name
sheet_name = 'df_gi_summary'

def to_excel(df, sheet_name):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        for i, col in enumerate(df.columns):
            # Find the maximum length of the content for the current column
            column_len = max(df[col].astype(str).map(len).max(),  # length of largest item
                             len(str(col)))  # length of column header/title
            # Set the column width as max content length + a little extra margin
            worksheet.set_column(i, i, column_len + 1)
        column_len = column_len/2
    processed_data = output.getvalue()
    return processed_data

df_excel = to_excel(df, sheet_name) 
st.download_button(label=button_name,
                       data=df_excel,
                       file_name=file_name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Adjusted MIME type for .xlsx
    
    


# Function to convert DataFrame to Excel and return as a BytesIO object
file_name = "plan_submision_2023_rtr_all_data"+date_string_plan+".xlsx"
df = df_pledge
button_name = 'Download Excel File: '+ file_name
sheet_name = 'df_pledge'

def to_excel(df, sheet_name):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        for i, col in enumerate(df.columns):
            # Find the maximum length of the content for the current column
            column_len = max(df[col].astype(str).map(len).max(),  # length of largest item
                             len(str(col)))  # length of column header/title
            # Set the column width as max content length + a little extra margin
            column_len = column_len/2
            worksheet.set_column(i, i, column_len + 1)
    processed_data = output.getvalue()
    return processed_data

df_excel = to_excel(df, sheet_name) 
st.download_button(label=button_name,
                       data=df_excel,
                       file_name=file_name,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Adjusted MIME type for .xlsx
    
    