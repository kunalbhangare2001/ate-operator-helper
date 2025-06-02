import streamlit as st
import json
import os
import base64
import smtplib
from email.message import EmailMessage

# Determine base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Paths
json_file_path = os.path.join(base_path, "troubleshooting_data.json")
images_folder = os.path.join(base_path, "images")
downloads_folder = os.path.join(base_path, "downloads")
logo_path = os.path.join(base_path, "logo.png")
email_config_path = os.path.join(base_path, "email_config.json")

# Send email function
def send_email(subject, body):
    try:
        with open(email_config_path, "r") as f:
            email_config = json.load(f)

        from_email = email_config["EMAIL_ADDRESS"]
        to_email = email_config["TO_EMAIL"]
        smtp_server = email_config.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = email_config.get("SMTP_PORT", 587)
        password = os.getenv("EMAIL_PASSWORD")  # Environment variable for safety

        if not password:
            st.error("❌ EMAIL_PASSWORD environment variable is not set.")
            return False

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(from_email, password)
            smtp.send_message(msg)

        return True
    except Exception as e:
        st.error(f"❌ Email failed: {e}")
        return False

# Display troubleshooting steps
def display_steps(steps):
    for step in steps:
        if isinstance(step, dict):
            st.markdown(f"- {step.get('step', '')}")
            if "image" in step:
                image_path = os.path.join(images_folder, step["image"])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=False, width=600)
                else:
                    st.warning(f"⚠️ Image not found: {step['image']}")
        else:
            st.markdown(f"- {step}")

# Main Streamlit app
def main():
    st.set_page_config(page_title="ATE Operator Helper", page_icon="🤖", layout="centered")

    st.markdown("""
    <style>
        .sticky-header {
            position: sticky;
            top: 0;
            background-color: white;
            z-index: 999;
            padding: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .sticky-header h1 {
            color: #1f4e79;
            font-size: 32px;
            margin: 0;
        }
        .main-content {
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    if os.path.exists(logo_path):
        logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
        st.markdown(f"""
            <div class="sticky-header">
                <h1>🤖 ATE Operator Assistant</h1>
                <img src="data:image/png;base64,{logo_base64}" width="180" height="80">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="sticky-header">
                <h1>🤖 ATE Operator Assistant</h1>
                <p>⚠️ Logo not found</p>
            </div>
        """, unsafe_allow_html=True)

    if not os.path.exists(json_file_path):
        st.error(f"❌ File not found: troubleshooting_data.json\nExpected at: {json_file_path}")
        st.stop()

    try:
        with open(json_file_path, "r") as file:
            troubleshooting_data = json.load(file)
        st.success("✔️ Troubleshooting data loaded")
    except json.JSONDecodeError:
        st.error("❌ Error decoding JSON! Please check formatting.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.stop()

    troubleshooting_categories = {k: v for k, v in troubleshooting_data.items() if k != "Support_Documents"}
    st.markdown("### How can I help you today?")
    main_option = st.selectbox("Select a category:", list(troubleshooting_categories.keys()))

    if isinstance(troubleshooting_categories[main_option], list):
        st.subheader(main_option)
        display_steps(troubleshooting_categories[main_option])
    else:
        sub_options = list(troubleshooting_categories[main_option].keys())
        sub_option = st.selectbox("Select a specific issue:", sub_options)
        st.subheader(f"{main_option} → {sub_option}")
        display_steps(troubleshooting_categories[main_option][sub_option])

    st.markdown("---")
    st.markdown("### 📥 Download Support Files")
    if "Support_Documents" in troubleshooting_data:
        doc_categories = list(troubleshooting_data["Support_Documents"].keys())
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("#### Categories")
            selected_category = st.radio("", doc_categories)
        with col2:
            st.markdown(f"#### {selected_category} Documents")
            category_docs = troubleshooting_data["Support_Documents"][selected_category]
            if category_docs:
                selected_doc = st.selectbox("Select a document to download:", category_docs)
                file_path = os.path.join(downloads_folder, selected_doc)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"Download {selected_doc}",
                            data=f,
                            file_name=selected_doc,
                            mime="application/pdf"
                        )
                else:
                    st.warning(f"⚠️ File not found: {selected_doc}")
            else:
                st.info("No documents available for this category.")
    else:
        st.warning("⚠️ No 'Support_Documents' found in JSON.")

    st.markdown("---")
    st.markdown("### 📧 Send Custom Message to Support")

    with st.form("email_form"):
        subject = st.text_input("Subject", value="ATE Operator Support Request")
        body = st.text_area("Message")
        send_button = st.form_submit_button("Send Email")

        if send_button:
            if not body.strip():
                st.warning("⚠️ Message cannot be empty.")
            else:
                success = send_email(subject, body)
                if success:
                    st.success("✅ Email sent successfully.")

if __name__ == "__main__":
    main()