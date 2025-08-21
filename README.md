# Creator's Comic Kit 🎬📚

Thank you for purchasing Creator's Comic Kit! This powerful tool is designed to help you turn any comic book into a high-quality YouTube script in minutes.

This guide will walk you through the simple steps to get the application running on your own computer.

---

### ✅ Prerequisites

Before you begin, please make sure you have **Python 3** installed on your system.

- To check if you have Python, open your terminal (on Mac/Linux) or Command Prompt (on Windows) and type: `python --version` or `python3 --version`.
- If you don't have it, you can download it for free from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### ⚙️ Step 1: Setup Instructions

Follow these steps to get the application ready to run.

**1. Unzip the File**
- Unzip the `creators-comic-kit.zip` file you downloaded from Gumroad. This will create a new folder with all the application files.

**2. Open Your Terminal or Command Prompt**
- **On Mac:** Open the "Terminal" app.
- **On Windows:** Open the "Command Prompt" or "PowerShell".

**3. Navigate to the Project Folder**
- In your terminal, you need to move into the folder you just unzipped. Use the `cd` (change directory) command.
- For example, if you unzipped the folder to your Desktop, you would type:
  ```bash
  cd Desktop/script-gen-main
  ```

**4. Install the Required Packages**
- This application uses a few Python packages to work. You can install them all with a single command.
- Run the following command in your terminal:
  ```bash
  pip install -r requirements.txt
  ```
- This will read the `requirements.txt` file and automatically install everything you need.

---

### 🚀 Step 2: How to Run the Application

Once the setup is complete, you're ready to launch the app!

**1. Get Your Gemini API Key**
- This tool requires a Google Gemini API key to function.
- You can get your free API key from Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**2. Run the Streamlit Command**
- In your terminal (make sure you are still in the project folder), run the following command:
  ```bash
  streamlit run streamlit_app.py
  ```

**3. Open the App in Your Browser**
- After running the command, the application will automatically open in a new tab in your web browser. If it doesn't, your terminal will provide a local URL (like `http://localhost:8501`) that you can copy and paste into your browser.

---

### 📖 Step 3: How to Use the App

The application is designed to be simple and intuitive.

1.  **Enter Your API Key:** Paste your Gemini API key into the sidebar.
2.  **Upload Your Comic:** Drag and drop your `.cbr` or `.cbz` file into the uploader.
3.  **Set Your Options:** Adjust the creativity level, target word count, and other options in the sidebar.
4.  **Start Processing:** Click the "Start Processing Comic" button and watch the magic happen!

---

### ❓ Troubleshooting

- **"Command not found: streamlit"**: This means the Streamlit package didn't install correctly or isn't in your system's PATH.
  - **Solution:** Try running the installation command again: `pip install -r requirements.txt`. If that doesn't work, try `pip install streamlit` directly.

- **"No module named 'rarfile'"**: This can happen if the `rarfile` package installation fails.
  - **Solution:** You may need to install `unrar` on your system. For most users, sticking to `.cbz` files is the easiest path.

---

### 📄 License

Your purchase of Creator's Comic Kit grants you a license for personal and commercial use on your own projects. You are not permitted to resell, redistribute, or share the source code.

Thank you for your support, and happy creating!