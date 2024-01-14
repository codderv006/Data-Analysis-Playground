# import sys
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import io
# import contextlib


# # Section 1: Upload Data
# st.sidebar.header('Upload Data files here')
# uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "sql"])

# show_data_head = st.sidebar.checkbox("Show Data Head", value=False)

# if uploaded_file is not None:
#     try:
#         data = pd.read_csv(uploaded_file)  # You can extend this for other file types
#         st.sidebar.success("Data loaded successfully!")
#     except Exception as e:
#         st.sidebar.error(f"Error: {e}")
# else:
#     st.sidebar.warning("Please upload a file.")

# # Section 2: Import Libraries
# st.sidebar.header('Import Libraries')
# selected_libraries = st.sidebar.multiselect("Select libraries to import", ["pandas", "matplotlib", "seaborn", "numpy"])

# # Section 3: Write Python Scripts
# st.header('Write Python Scripts \n [Data is loaded to variable named "data"]')
# user_code = st.text_area("Write your Python script here", height=200, key="code_editor", help="Use Ctrl+Space for suggestions")
# run_button = st.button("Run")

# if run_button and user_code.strip():  # Check if Run button is pressed and user_code is not empty
#     try:
#         # Import selected libraries
#         for library in selected_libraries:
#             exec(f"import {library} as {library[:3]}")

#         # Execute user code if it's not empty
#         exec(user_code, globals(), locals())  # Make sure to pass globals() and locals()

#         st.success("Code executed successfully!")
#     except Exception as e:
#         st.error(f"Error: {e}")

# @contextlib.contextmanager
# def capture_output():
#     new_stdout = io.StringIO()
#     old_stdout = sys.stdout
#     sys.stdout = new_stdout
#     yield new_stdout
#     sys.stdout = old_stdout

# # Section 4: Display Output
# st.header('Section 4: Output')
# output_code = st.empty()

# # Display output
# if 'data' in locals() and show_data_head:
#     num_rows_to_display = st.number_input("Number of rows to display", value=5, min_value=1, max_value=len(data))
#     output_code.table(data.head(num_rows_to_display))

# else:
#     # Execute user code and capture output
#     with capture_output() as output:
#         try:
#             exec(user_code, globals(), locals())
#         except Exception as e:
#             st.error(f"Error: {e}")
    
#     # Display captured output
#     output_value = output.getvalue()
#     if output_value:
#         st.text(output_value)
#     else:
#         output_code.text("No output yet.")

import sys
import streamlit as st
import pandas as pd
import numpy as np
import io
import contextlib
import traceback
from contextlib import redirect_stdout

# Function to capture print output
@contextlib.contextmanager
def capture_output():
    new_stdout = io.StringIO()
    with redirect_stdout(new_stdout):
        yield new_stdout

# Set app title and logo
st.set_page_config(page_title="Data Analysis Playground", page_icon=":bar_chart:")


# Section 1: Upload Data
st.sidebar.header('Upload Data files here')
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "sql"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)  # You can extend this for other file types
        st.sidebar.success("Data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
else:
    st.sidebar.warning("Please upload a file.")

# Section 2: Import Libraries
st.sidebar.header('Import Libraries')
selected_libraries = st.sidebar.multiselect("Select libraries to import", ["pandas", "matplotlib", "seaborn", "numpy"])


# Section 3: Write Python Scripts
st.header('Write Python Scripts \n [Data is loaded to variable named "data"]')
user_code = st.text_area("Write your Python script here", height=200, key="code_editor", help="Use Ctrl+Space for suggestions")
run_button = st.button("Run")

if run_button and user_code.strip():
    try:
        # Import selected libraries
        for library in selected_libraries:
            exec(f"import {library} as {library[:3]}")

        # Execute user code if it's not empty
        with capture_output() as output:
            exec(user_code, globals(), locals())

        st.success("Code executed successfully!")

        # Display the captured output
        captured_output = output.getvalue().strip()
        if captured_output:
            st.text("Output:")
            st.text(captured_output)

        # Check if user wants to display the head or tail
        if "data.head()" in user_code:
            st.text("Output:")
            num_rows_to_display = st.number_input("Number of rows to display", value=5, min_value=1, max_value=len(data))
            st.table(data.head(num_rows_to_display))
        elif "data.tail()" in user_code:
            st.text("Output:")
            num_rows_to_display = st.number_input("Number of rows to display", value=5, min_value=1, max_value=len(data))
            st.table(data.tail(num_rows_to_display))

    except Exception as e:
        st.error(f"Error: {e}")
        st.text("Traceback:")
        st.text(traceback.format_exc())