import streamlit as st
import os
import shutil
from zipfile import ZipFile

def install_dependencies():
    os.system("sudo apt-get update")
    os.system("sudo apt-get install default-jre -y")
    os.system("sudo apt-get install aapt -y")
    os.system("wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool")
    os.system("wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.5.0.jar -O /usr/local/bin/apktool.jar")
    os.system("chmod +x /usr/local/bin/apktool")

def decompile_apk(file_path):
    os.system(f"apktool d {file_path}")

def create_zip(directory):
    with ZipFile('decompiled_files.zip', 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

def main():
    st.title("APK Reverse Engineering Tool")

    st.write("Upload your APK file:")
    uploaded_file = st.file_uploader("Choose an APK file", type=["apk"])

    if uploaded_file is not None:
        # Save the uploaded file
        with open("uploaded_apk.apk", "wb") as f:
            f.write(uploaded_file.getvalue())

        st.write("APK file uploaded successfully!")

        # Install dependencies
        st.write("Installing dependencies...")
        install_dependencies()
        st.write("Dependencies installed successfully!")

        # Use Apktool to decompile the APK file
        st.write("Decompiling the APK file...")
        decompile_apk("uploaded_apk.apk")
        st.write("APK file decompiled successfully!")

        # Create a zip file of decompiled files
        st.write("Creating zip file of decompiled files...")
        if os.path.exists("uploaded_apk"):
            create_zip("uploaded_apk")
            st.write("Zip file created successfully!")

            # Offer the zip file for download
            st.write("Download the decompiled files:")
            with open("decompiled_files.zip", "rb") as f:
                st.download_button(label="Download decompiled_files.zip", data=f, file_name="decompiled_files.zip", mime="application/zip")
                
            # Delete uploaded APK and decompiled files
            shutil.rmtree("uploaded_apk")
            os.remove("uploaded_apk.apk")
            os.remove("decompiled_files.zip")

            st.write("Data has been erased.")

        else:
            st.write("Error: Decompiled directory not found.")

if __name__ == "__main__":
    main()