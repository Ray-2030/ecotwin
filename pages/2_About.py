import streamlit as st
import feedparser
import time

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

# --- BRANDING ---
st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=70)
st.title("🛡️ Sentinel Alpha Project")

st.markdown("""
### 🌿 WIEM 102: Wildlife Ecology & Management
This platform was developed to digitize field observations for the **Wildlife Ecology (WIEM 102)** course. 
By combining Python with Gemini AI, we monitor Kenyan biodiversity with high precision.
""")

# --- 🚨 LIVE: AUTOMATED ENDANGERED SPECIES ALERTS ---
st.markdown("---")
st.error("### 🚨 Live Automated Species Alerts")
st.write("Fetching real-time updates from the IUCN Red List & Conservation News...")

# Cache the data so we don't spam the news site
@st.cache_data(ttl=3600) # Reload news only every 1 hour
def fetch_live_news():
    try:
        # Fetching data from the global IUCN news feed
        feed = feedparser.parse("https://www.iucnredlist.org/news/rss")
        if feed.entries:
            return feed.entries[:5] # Get the top 5 articles
        else:
            return []
    except:
        return []

live_data = fetch_live_news()

if live_data:
    for entry in live_data:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.caption(f"Published: {entry.published}")
        st.divider()
else:
    st.warning("⚠️ Central Command offline. Reverting to 2026 Kenyan baseline alerts.")
    # Show the baseline Kenyan endangered species alert as backup
    st.markdown("""
    1. **Mountain Bongo**: Critically endangered (~130 remain).
    2. **Grey Crowned Crane**: Rapid wetland habitat loss.
    3. **Black Rhino**: Priority poaching surveillance required.
    """)

st.info("💡 Developed by **Wolf (Dev 2)** — Software Dev & Wildlife Ecology Student.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")