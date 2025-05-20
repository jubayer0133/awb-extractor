
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="AWB Extractor", layout="wide")

st.title("📦 AWB Number Extractor")
st.markdown("Upload an Excel (.xlsx) file and extract all SUDO AWB numbers like `176-00956373` from any sheet.")

uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

def extract_awb_numbers_from_excel(file):
    xls = pd.read_excel(file, sheet_name=None)
    awb_numbers = []
    for sheet_name, df in xls.items():
        for col in df.columns:
            col_data = df[col].astype(str)
            found = col_data.apply(lambda x: re.findall(r'\b\d{3}-\d{8}\b', x))
            for sublist in found:
                awb_numbers.extend(sublist)
    return sorted(set(awb_numbers))

if uploaded_file:
    try:
        awb_list = extract_awb_numbers_from_excel(uploaded_file)
        st.success(f"Found {len(awb_list)} unique AWB numbers.")
        st.dataframe(pd.DataFrame(awb_list, columns=["AWB Numbers"]), use_container_width=True)

        csv = pd.DataFrame(awb_list, columns=["AWB Numbers"]).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download AWB List as CSV", csv, "awb_numbers.csv", "text/csv")
    except Exception as e:
        st.error(f"Error: {e}")
