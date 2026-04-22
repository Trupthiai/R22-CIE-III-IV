import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.set_page_config(page_title="Marks Splitter", layout="centered")
st.title("Total Marks Splitter (Part A + Part B)")

st.markdown("""
Upload Excel File:
- Column name must be `Total Marks`
- Each value should be between 0 and 30

Splitting:
- Part A (Q1–Q10): Only 1 or blank (max 10)
- Part B (Q11–Q16): Choose 4 out of 6, each max 5 marks (total ≤ 20)
""")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# Correct question list
questions = [f"Q{i}" for i in range(1, 17)]  # Q1–Q16

def distribute_marks(total):
    total = max(0, min(30, int(total)))

    # -------- Part A --------
    partA_total = min(random.randint(5, 10), total)  # between 5–10 but ≤ total
    a_marks = [''] * 10

    selected_A = random.sample(range(10), partA_total)
    for idx in selected_A:
        a_marks[idx] = 1

    # -------- Part B --------
    remaining = total - partA_total
    partB_total = min(20, remaining)

    b_marks = [''] * 6
    selected_B = random.sample(range(6), 4)

    for i in selected_B:
        if partB_total <= 0:
            break

        mark = random.randint(1, min(5, partB_total))
        b_marks[i] = mark
        partB_total -= mark

    return a_marks + b_marks


if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        if "Total Marks" not in df.columns:
            st.error("Column 'Total Marks' not found.")
        else:
            processed = []

            for val in df["Total Marks"]:
                row = distribute_marks(val)
                processed.append(row)

            output_df = pd.DataFrame(processed, columns=questions)
            output_df["Total Marks"] = df["Total Marks"]

            st.success("Marks distributed successfully!")
            st.dataframe(output_df)

            # Download
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                output_df.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="Download Split Marks Excel",
                data=buffer,
                file_name="Split_Marks_Output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")
