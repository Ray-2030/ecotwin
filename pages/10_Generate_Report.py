import streamlit as st
import qrcode
import io

st.set_page_config(page_title="Ranger Report Tools", page_icon="📊")
st.title("📊 Ecology Report Tools")

st.markdown("""
### 🖨️ Embed your Platform in your Report
Generate a custom QR code that points directly to your live **Sentinel Alpha** website. 
You can paste this image directly into your Ecology assignment to allow your lecturer to visit the platform.
""")

# Input for the website URL
url_input = st.text_input("Enter your full Streamlit website URL:", 
                           "https://ray-2030-ecotwin-ecotwin-app-9x5j1p.streamlit.app/")

if st.button("Generate QR Code"):
    with st.spinner("Generating secure code..."):
        # Create QR code object
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url_input)
        qr.make(fit=True)
        
        # Create an image from the QR Code instance
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # Save image to a BytesIO object so Streamlit can use it
        buf = io.BytesIO()
        img_qr.save(buf)
        buf.seek(0)
        
        # Display the image
        st.divider()
        st.subheader("Final QR Code")
        st.image(buf, caption=f"QR Code for Sentinel Alpha")
        
        # Download button
        st.download_button(
            label="💾 Download QR Image for Report",
            data=buf,
            file_name="Sentinel_Alpha_QR.png",
            mime="image/png"
        )