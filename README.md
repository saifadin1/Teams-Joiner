# 🤖 MS Teams Auto-Joiner

A simple Python script that monitors a Microsoft Teams channel, automatically clicks meeting links or buttons, and raises your hand.

## ✨ Features

* **Safe Login:** Uses your existing Chrome window, so you log in manually (no password/2FA errors).
* **Dual Detection:** Works on both **Blue Text Links** and **Purple "Join" Buttons**.
* **Smart Tab Handling:** Automatically switches tabs if a link opens a new window.
* **Auto-Hand Raise:** Raises your hand 10 seconds after joining.

---

## 🛠️ Prerequisites

1. **Python** installed on your computer
2. **Google Chrome** installed
3. **Selenium** library

Install Selenium by running:

```bash
pip install selenium
```

---

## ⚙️ Setup (Important!)

This script controls a Chrome window that is already open.
You must open Chrome in **Debug Mode** for this to work.

### Step 1: Create the Chrome Shortcut

1. Close **ALL** open Chrome windows.
2. Press **Windows Key + R**.
3. Paste the following command and press **Enter**:

```text
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
```

A new Chrome window will open.

---

### Step 2: Prepare Teams

1. In the new Chrome window, go to:
   [https://teams.microsoft.com](https://teams.microsoft.com)
2. Log in with your account.
3. Make sure you can see the **Communities** tab on the left.

---

## 📝 Configuration

Open `auto_join_final.py` in a text editor (Notepad / VS Code) and check the settings at the top:

```python
# --- CONFIGURATION ---
CHANNEL_NAME = "ch"   # The exact name of the channel to click
CHECK_DELAY = 3       # How many seconds to wait between checks
# ---------------------
```

---

## 🚀 How to Run

1. Ensure your **Debug Chrome window** is open and logged into Teams.
2. Open a terminal in the folder containing the script.
3. Run:

```bash
python simple_joiner.py
```

### What the script does:

* Clicks the channel named **"ch"**
* Prints dots `.` while waiting for a meeting
* Automatically clicks the meeting link or Join button
* Raises your hand after joining

---

## ❓ Troubleshooting

### Error: **"Could not connect to Chrome"**

* Did you close **all** other Chrome windows first?
* Did you run the debug command correctly?
* Is Chrome running on port **9222**?

### Error: **"Element not found"**

* Make sure `CHANNEL_NAME` matches **exactly** what you see in Teams.
* Ensure the Teams window is visible (not minimized)
