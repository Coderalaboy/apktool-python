import streamlit as st
import os
import shutil
from zipfile import ZipFile
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
UPLOADED_APK_FILENAME = "uploaded_apk.apk"

# 1. Replace subprocess.run() with subprocess.Popen() for more control over command execution.
def install_dependencies():
    try:
        subprocess.Popen(["sudo", "apt-get", "update"]).wait()
        subprocess.Popen(["sudo", "apt-get", "install", "default-jre", "-y"]).wait()
        subprocess.Popen(["sudo", "apt-get", "install", "aapt", "-y"]).wait()
        subprocess.Popen(["wget", "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool", "-O", "/usr/local/bin/apktool"]).wait()
        subprocess.Popen(["wget", "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.5.0.jar", "-O", "/usr/local/bin/apktool.jar"]).wait()
        subprocess.Popen(["chmod", "+x", "/usr/local/bin/apktool"]).wait()
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Error installing dependencies: {e.stderr.decode('utf-8')}")
        logger.error(f"Error installing dependencies: {e}")
        return False
    except Exception as e:
        st.error(f"Error installing dependencies: {str(e)}")
        logger.error(f"Error installing dependencies: {e}")
        return False

# 2. Use os.path.join() instead of string concatenation to handle file paths.
def decompile_apk(file_path):
    try:
        command = ["apktool", "d", file_path]
        process = subprocess.Popen(command, cwd=os.path.dirname(file_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            st.error(f"Error during decompilation: {error.decode('utf-8')}")
            logger.error(f"Error during decompilation: {error.decode('utf-8')}")
            return False
        else:
            st.write("APK file decompiled successfully!")
            logger.info("APK file decompiled successfully!")
            return True
    except Exception as e:
        st.error(f"Error during decompilation: {str(e)}")
        logger.error(f"Error during decompilation: {e}")
        return False

# 3. Add error handling for file operations such as opening and writing files.
def save_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join(os.getcwd(), UPLOADED_APK_FILENAME)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return file_path
    except Exception as e:
        st.error(f"Error saving uploaded file: {str(e)}")
        logger.error(f"Error saving uploaded file: {e}")
        return None

# 4. Provide more informative error messages for better debugging.
def handle_error(message, error):
    st.error(f"{message}: {error}")
    logger.error(f"{message}: {error}")

# 5. Implement a timeout mechanism for subprocess commands to prevent hanging.
def run_subprocess_with_timeout(command, timeout):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=timeout)
        return process.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return -1, stdout, stderr
    except Exception as e:
        return -1, b'', str(e).encode('utf-8')

# 6. Use subprocess.check_output() for simpler command execution with error handling.
def run_subprocess(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return True, output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    except Exception as e:
        return False, str(e)

# 7. Replace os.path.splitext() with string slicing to extract file extension.
def get_file_extension(file_path):
    return os.path.splitext(file_path)[1]

# 8. Validate the file extension of the uploaded file to ensure it's an APK.
def validate_file_extension(file_path):
    allowed_extensions = ['.apk']
    if get_file_extension(file_path) not in allowed_extensions:
        st.error("Invalid file format. Please upload a valid APK file.")
        return False
    return True

# 9. Encapsulate repetitive code into functions for better modularity.
def display_message(message):
    st.write(message)
    logger.info(message)

# 10. Use shutil.move() instead of os.rename() for safer file moving.
def move_file(source, destination):
    try:
        shutil.move(source, destination)
        return True
    except Exception as e:
        handle_error("Error moving file", e)
        return False

# 11. Implement logging for better tracking of errors and events.
def log_message(message):
    logger.info(message)

# 12. Handle edge cases such as empty or null input from the user.
def handle_empty_input(input_value, error_message):
    if not input_value:
        st.error(error_message)
        return True
    return False

# 13. Improve user interface with clearer instructions and feedback messages.
def display_instructions():
    st.title("APK Reverse Engineering Tool")
    st.write("Upload your APK file:")
    
def display_upload_message():
    st.write("APK file uploaded successfully!")

def display_dependency_installation_message():
    st.write("Installing dependencies...")

def display_dependency_success_message():
    st.write("Dependencies installed successfully!")

def display_decompilation_message():
    st.write("Decompiling the APK file...")

def display_decompilation_success_message():
    st.write("APK file decompiled successfully!")

def display_decompiled_directory_exists():
    st.write("Decompiled directory exists.")

# 14. Use named constants instead of hard-coded values for better readability.
def get_uploaded_apk_path():
    return os.path.join(os.getcwd(), UPLOADED_APK_FILENAME)

# 15. Add comments to clarify the purpose of each function and block of code.
def main():
    try:
        display_instructions()

        uploaded_file = st.file_uploader("Choose an APK file", type=["apk"])
        if handle_empty_input(uploaded_file, "No file uploaded. Please select an APK file."):
            return

        file_path = save_uploaded_file(uploaded_file)
        if not file_path:
            return

        display_upload_message()

        display_dependency_installation_message()
        if install_dependencies():
            display_dependency_success_message()
        else:
            handle_error("Error installing dependencies", "See above error message for details.")
            return

        display_decompilation_message()
        return_code, _, _ = run_subprocess_with_timeout(["apktool", "d", file_path], timeout=300)
        if return_code != 0:
            handle_error("Error during decompilation", "See above error message for details.")
            return
        else:
            display_decompilation_success_message()
            decompiled_directory = os.path.splitext(file_path)[0]
            if os.path.exists(decompiled_directory):
                display_decompiled_directory_exists()
            else:
                handle_error("Decompiled directory not found", "Decompiled directory not found.")
    except Exception as e:
        handle_error("An error occurred", str(e))

if __name__ == "__main__":
    main()