import streamlit as st
import os
import shutil
from zipfile import ZipFile
import subprocess

def decompile_apk(file_path):
    try:
        command = f"apktool d {file_path}"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if process.returncode != 0:
            st.error(f"Error during decompilation: {error.decode('utf-8')}")
            return False
        else:
            return True
    except Exception as e:
        st.error(f"Error during decompilation: {str(e)}")
        return False

def main():
    st.title("APK Reverse Engineering Tool")

    st.write("Upload your APK file:")
    uploaded_file = st.file_uploader("Choose an APK file", type=["apk"])

    if uploaded_file is not None:
        # Save the uploaded file
        with open("uploaded_apk.apk", "wb") as f:
            f.write(uploaded_file.getvalue())

        st.write("APK file uploaded successfully!")

        # Use Apktool to decompile the APK file
        st.write("Decompiling the APK file...")
        decompilation_success = decompile_apk("uploaded_apk.apk")
        if decompilation_success:
            st.write("APK file decompiled successfully!")

            # Check if decompiled directory exists
            decompiled_directory = "uploaded_apk"
            if os.path.exists(decompiled_directory):
                # Create a zip file of decompiled files
                st.write("Creating zip file of decompiled files...")
                with ZipFile('decompiled_files.zip', 'w') as zipf:
                    for root, dirs, files in os.walk(decompiled_directory):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), decompiled_directory))
                st.write("Zip file created successfully!")

                # Offer the zip file for download
                st.write("Download the decompiled files:")
                with open("decompiled_files.zip", "rb") as f:
                    st.download_button(label="Download decompiled_files.zip", data=f, file_name="decompiled_files.zip", mime="application/zip")

                # Delete uploaded APK and decompiled files
                shutil.rmtree(decompiled_directory)
                os.remove("uploaded_apk.apk")
                os.remove("decompiled_files.zip")

                st.write("Data has been erased.")
            else:
                st.write("Error: Decompiled directory not found.")
        else:
            st.write("Error during decompilation.")

if __name__ == "__main__":
    main()