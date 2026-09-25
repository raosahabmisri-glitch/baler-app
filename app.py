import streamlit as st
import pandas as pd
import os

# Page layout & styling
st.set_page_config(page_title="Baler Seva Portal", page_icon="🚜", layout="centered")

DEMAND_FILE = "demands.csv"
OWNER_FILE = "owners.csv"

# Admin login credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# CSV data storage check
if not os.path.exists(DEMAND_FILE):
    pd.DataFrame(columns=["Kisan Naam", "Mobile", "Gaav", "Acre", "Date", "Status"]).to_csv(DEMAND_FILE, index=False)

if not os.path.exists(OWNER_FILE):
    pd.DataFrame(columns=["Owner Naam", "Mobile", "Gaav/Area", "Machine Type", "Rate/Acre"]).to_csv(OWNER_FILE, index=False)

st.title("🚜 Baler Seva Kendra")
st.caption("Kisano aur Baler Owners ko jodne ka aasan madhyam")

tab1, tab2, tab3 = st.tabs(["🌾 Baler Chahiye (Farmer)", "📞 Baler Owners List", "🔐 Admin Login"])

# ----------------- TAB 1: FARMER DEMAND -----------------
with tab1:
    st.subheader("Baler ke liye Demand Register karein")
    with st.form("farmer_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        phone = st.text_input("Mobile Number (10 digits)")
        village = st.text_input("Gaav aur Tehsil/District")
        acres = st.number_input("Kitne Acre khet me baler chalwana hai?", min_value=1, step=1)
        req_date = st.date_input("Kis tareekh ko Baler chahiye?")
        submit = st.form_submit_button("Demand Bhejein")

        if submit:
            if name.strip() and phone.strip() and village.strip():
                df = pd.read_csv(DEMAND_FILE)
                new_data = pd.DataFrame([{
                    "Kisan Naam": name, 
                    "Mobile": phone, 
                    "Gaav": village, 
                    "Acre": acres, 
                    "Date": str(req_date),
                    "Status": "Pending"
                }])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DEMAND_FILE, index=False)
                st.success("✅ Aapki demand darj ho gayi hai! Baler owners aapse sampark karenge.")
            else:
                st.error("Kripya Naam, Mobile aur Gaav ki poori jankari bharein.")

# ----------------- TAB 2: PUBLIC BALER OWNERS -----------------
with tab2:
    st.subheader("Available Baler Owners")
    owners_df = pd.read_csv(OWNER_FILE)
    if not owners_df.empty:
        for idx, row in owners_df.iterrows():
            with st.container(border=True):
                st.markdown(f"**👤 {row['Owner Naam']}** ({row['Machine Type']})")
                st.write(f"📍 **Area:** {row['Gaav/Area']}")
                st.write(f"💰 **Rate:** {row['Rate/Acre']}")
                st.markdown(f"📞 [Direct Call karein: {row['Mobile']}](tel:{row['Mobile']})")
    else:
        st.info("Abhi tak koi Baler owner listed nahi hai.")

# ----------------- TAB 3: ADMIN PANEL -----------------
with tab3:
    st.subheader("Admin Control Panel")
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        u_id = st.text_input("Admin Username")
        u_pwd = st.text_input("Admin Password", type="password")
        if st.button("Login Karein"):
            if u_id == ADMIN_USER and u_pwd == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Galat ID ya Password!")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success("Aap logged-in hain.")
        with col2:
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.divider()
        st.write("### ➕ Naya Baler Owner Add Karein")
        with st.form("add_owner_form", clear_on_submit=True):
            o_name = st.text_input("Owner ka Naam")
            o_phone = st.text_input("Owner ka Mobile No.")
            o_area = st.text_input("Kaun-kaun se gaav cover karte hain?")
            o_type = st.selectbox("Machine Type", ["Round Baler", "Square Baler", "Dono (Both)"])
            o_rate = st.text_input("Rate per Acre (e.g. ₹1000/Acre ya Negotiable)")
            add_btn = st.form_submit_button("Owner Directory me Jodein")

            if add_btn:
                if o_name.strip() and o_phone.strip():
                    odf = pd.read_csv(OWNER_FILE)
                    new_owner = pd.DataFrame([{
                        "Owner Naam": o_name,
                        "Mobile": o_phone,
                        "Gaav/Area": o_area,
                        "Machine Type": o_type,
                        "Rate/Acre": o_rate
                    }])
                    odf = pd.concat([odf, new_owner], ignore_index=True)
                    odf.to_csv(OWNER_FILE, index=False)
                    st.success("Baler owner successfully list ho gaya!")
                    st.rerun()

        st.divider()
        st.write("### 📋 Kisano ki Demands ki List")
        demands_df = pd.read_csv(DEMAND_FILE)
        st.dataframe(demands_df, use_container_width=True)
