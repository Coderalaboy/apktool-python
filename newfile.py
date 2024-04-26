import streamlit as st
import os

def install_dependencies():
    os.system("sudo apt-get update")
    os.system("sudo apt-get install default-jre -y")
    os.system("sudo apt-get install aapt -y")
    os.system("wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool")
    os.system("wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.5.0.jar -O /usr/local/bin/apktool.jar")
    os.system("chmod +x /usr/local/bin/apktool")

def decompile_apk(file_path):
    os.system(f"apktool d {file_path}")

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

        # Show decompiled files
        st.write("Decompiled files:")
        decompiled_files = os.listdir("uploaded_apk")
        for file in decompiled_files:
            st.write(file)

if __name__ == "__main__":
    main()