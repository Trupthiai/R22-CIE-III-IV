import streamlit as st
import pandas as pd
import random
import io

# Function to generate marks distribution
def generate_marks_distribution():

    # -------- Part A --------
    # 10 questions → 0 or 1 marks
    k = random.randint(5, 10)  # total marks between 5 and 10
    part_a = [0] * 10
    selected_a = random.sample(range(10), k)
    for i in selected_a:
        part_a[i] = 1

    # -------- Part B --------
    # 4 out of 6 questions, each ≤ 5 marks, total ≤ 20
    part_b = [random.randint(0, 5) for _ in range(4)]
    while sum(part_b) > 20:
        part_b = [random.randint(0, 5) for _ in range(4)]

    return part_a, part_b


# -------- Streamlit App --------
st.set_page_config(page_title="CIE Marks Distribution", layout="centered")
st.title("CIE Marks Distribution Generator")

st.markdown("""
### 📊 Marks Scheme:
- **Part A:** 10 Questions → 0 or 1 mark → Total **5 to 10**
- **Part B:** 6 Questions → Answer any 4 → Each ≤ 5 marks → Total ≤ 20
""")

uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if len(df) < 16:
            st.error("The file must contain at least 16 questions (10 Part A + 6 Part B).")
        else:
            part_a, part_b = generate_marks_distribution()

            # -------- Assign Part A --------
            df['Part A Marks'] = [*part_a, *[None] * (len(df) - 10)]

            # -------- Assign Part B --------
            part_b_section = list(range(10, 16))  # Q11–Q16
            selected_b = random.sample(part_b_section, 4)

            part_b_marks = [None] * len(df)
            for i, idx in enumerate(selected_b):
                part_b_marks[idx] = part_b[i]

            df['Part B Marks'] = part_b_marks

            # -------- Save Output --------
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Marks Distribution')
            output.seek(0)

            st.success("Marks distribution generated successfully!")

            st.download_button(
                label="Download Updated Excel",
                data=output,
                file_name="CIE-final-marks-distribution.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
