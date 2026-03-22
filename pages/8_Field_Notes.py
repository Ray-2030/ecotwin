import streamlit as st
import datetime

st.title("📓 Ranger Field Notes")

# --- THE CACHE (Initialization) ---
if "draft_note" not in st.session_state:
    st.session_state.draft_note = ""

# --- THE INPUT AREA ---
# We link the value to the session_state
note_input = st.text_area(
    "Write your observations...", 
    value=st.session_state.draft_note,
    placeholder="e.g., Spotted 3 hyenas near the watering hole...",
    height=200
)

# Every time you type, it updates the "Cache"
st.session_state.draft_note = note_input

# --- THE SAVE BUTTON ---
if st.button("💾 Finalize & Save to Database"):
    if note_input:
        # Here is where you'd put your MySQL/SQLAlchemy code
        st.success("Note officially logged! Draft cleared.")
        st.session_state.draft_note = "" # Clear cache after successful save
        st.balloons()
    else:
        st.error("Cannot save an empty note, Wolf.")

st.info("💡 Your progress is auto-cached. You can switch pages and come back, and your text will still be here!")