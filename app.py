import streamlit as st
import json
import os
import sys
import base64

# Determine base path for static assets (images, downloads, logo)
if getattr(sys, 'frozen', False):
    # Running from a PyInstaller bundle
    asset_path = os.path.dirname(sys.executable)
else:
    # Running from script
    asset_path = os.path.dirname(os.path.abspath(__file__))

# Paths
json_file_path = os.path.join(asset_path, "troubleshooting_data.json")
images_folder = os.path.join(asset_path, "images")
downloads_folder = os.path.join(asset_path, "downloads")
logo_path = os.path.join(asset_path, "logo.png")

def main():
    st.set_page_config(page_title="ATE Operator Helper", page_icon="🤖", layout="centered")

    # Debug info - remove after confirming paths
    st.write("### Debug Info")
    st.write(f"Running frozen: {getattr(sys, 'frozen', False)}")
    st.write(f"Executable path: {sys.executable}")
    st.write(f"Asset path: {asset_path}")
    st.write(f"JSON file path: {json_file_path}")
    st.write(f"JSON file exists: {os.path.exists(json_file_path)}")
    st.write(f"Logo path: {logo_path}")
    st.write(f"Logo exists: {os.path.exists(logo_path)}")
    st.write(f"Images folder exists: {os.path.exists(images_folder)}")
    st.write(f"Downloads folder exists: {os.path.exists(downloads_folder)}")
    st.markdown("---")

    # Custom CSS
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
        .doc-category {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
        }
        .selected-category {
            border-left: 4px solid #1f77b4;
            background-color: #e6f2ff;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header with logo
    if os.path.exists(logo_path):
        logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
        st.markdown(
            f"""
            <div class="sticky-header">
                <h1>🤖 ATE Operator Assistant</h1>
                <img src="data:image/png;base64,{logo_base64}" width="180" height="80">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="sticky-header">
                <h1>🤖 ATE Operator Assistant</h1>
                <p>⚠️ Logo not found</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)

    # Load troubleshooting JSON
    if not os.path.exists(json_file_path):
        st.error("❌ File not found: troubleshooting_data.json")
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

    # Show troubleshooting steps
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

    # Filter Support_Documents out of main selection
    troubleshooting_categories = {
        k: v for k, v in troubleshooting_data.items() if k != "Support_Documents"
    }

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

    # Support Document Downloads
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
        if os.path.exists(downloads_folder):
            files = os.listdir(downloads_folder)
            pdf_files = [f for f in files if f.lower().endswith(".pdf")]
            if pdf_files:
                selected_pdf = st.selectbox("Select a file to download:", pdf_files)
                file_path = os.path.join(downloads_folder, selected_pdf)
                with open(file_path, "rb") as f:
                    st.download_button(label="Download PDF", data=f, file_name=selected_pdf, mime="application/pdf")
            else:
                st.info("No PDF files available in the downloads folder.")
        else:
            st.warning("⚠️ Downloads folder not found.")

if __name__ == "__main__":
    main()
