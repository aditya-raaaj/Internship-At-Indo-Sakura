'ctrl+shift+v'

# Voice-Controlled Smart App

## 📂 Project Structure

```
YourProject/
├── Core/
│   └── main.py
```

---

## 🚀 Getting Started

### Step-by-Step Instructions

1. **Open Visual Studio Code (VS Code).**

2. Navigate to the `Core` folder.

3. Open the `main.py` file.

4. Run the file. This will automatically open a terminal inside VS Code.

5. In the terminal (make sure it's in bash or the right shell), enter the command below:

   ```bash
   streamlit run <full path to main.py>
   ```

   Example:

   ```bash
   streamlit run C:/Users/Adi/Documents/YourProject/Core/main.py
   ```

6. This will open your default browser and launch the Streamlit web app.

---

## 🎙️ Voice Command Guide

### 🛑 **Wake Words** (say one of these to begin giving commands):

* "lucy"
* "Roxie"
* "beauty"
* "duty"
* "chitti"

### 💡 **Action Commands** (after wake word):

Examples:

* "Turn on the living room lights"
* "Switch off the kitchen lights"
* "Turn off all the lights"

### 👋 **Exit Words** (to stop voice listening):

* "tata"
* "bye"
* "bye-bye"
* "thank you for the service"
* "thank you"
* "see you later"
* "goodbye"
* "good night"
* "stop"
* "see you"

📌 **Note:**
After an exit command, the system will **not accept further voice commands** until a wake word is spoken again.

---

## 🧠 Notes

* Ensure your microphone is working and permissions are granted.
* Background noise might affect voice recognition.
* Streamlit must be installed: `pip install streamlit`

---

Happy Hacking! 🤖✨
