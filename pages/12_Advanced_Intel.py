import streamlit as st

st.title("🛡️ Advanced Intel")

# --- 21. TWO-FACTOR AUTH (Ranger Key) ---
st.subheader("🔒 Secure Pride Access")
key = st.text_input("Enter Ranger Secret Key", type="password")
if key == "Wolf2026":
    st.write("🔓 Pride Chat Unlocked.")
    # --- 10. SPECIES COMPARISON ---
    col1, col2 = st.columns(2)
    col1.image("https://example.com/bird1.jpg", caption="Grey Crane")
    col2.image("https://example.com/bird2.jpg", caption="Black Crane")
    st.info("💡 Difference: Check the crown plumage density.")
else:
    st.warning("Restricted Area")

# --- 9. POACHING RISK HEATMAP ---
st.subheader("🔥 Poaching Risk Assessment")
st.progress(85, text="High Risk Zone: Northern Border")