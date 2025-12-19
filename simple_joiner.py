import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- CONFIGURATION ---
CHANNEL_NAME = "ch"   # Name of the channel to watch
CHECK_DELAY = 3       # How fast to scan (seconds)
# ---------------------

def setup_driver():
    print("🔌 Connecting to Chrome...")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        return webdriver.Chrome(options=options)
    except:
        print("❌ Error: Run this command in Windows first:")
        print('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\selenium\\ChromeProfile"')
        return None

def find_and_enter_channel(driver):
    print(f"🔍 entering '{CHANNEL_NAME}'...")
    try:
        # Find the channel by text name
        xpath = f"//*[text()='{CHANNEL_NAME}']"
        channel = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        channel.click()
        print(f"✅ Clicked '{CHANNEL_NAME}'")
    except:
        print(f"⚠️  Already in channel (or couldn't find it). Continuing...")

def join_meeting_flow(driver):
    """
    This function handles the 'Join Now' screen (camera/mic setup)
    once the meeting window is open.
    """
    print("⏳ Waiting for the purple 'Join now' button...")
    try:
        # Look for the final join button
        join_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-tid, 'join') or contains(text(), 'Join now')]"))
        )
        join_btn.click()
        print("🚀 JOINED SUCCESSFUL!")
        
        # Wait 10 seconds for connection, then raise hand
        time.sleep(10)
        print("🖐️ Raising hand...")
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('k').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        print("✅ Hand raised. Script finished.")
        return True
    except Exception as e:
        print(f"❌ Failed at Join Now screen: {e}")
        return False

def watch_and_act(driver):
    print("\n👀 WATCHING FOR MEETINGS (Links OR Buttons)...")
    print("   (Press Ctrl+C to stop script)")
    
    while True:
        try:
            # --- STRATEGY 1: LOOK FOR LINKS ---
            # Looks for links containing "meet" or "teams.live.com"
            links = driver.find_elements(By.XPATH, "//a[contains(@href, '/meet/') or contains(@href, 'teams.live.com')]")
            
            # --- STRATEGY 2: LOOK FOR BUTTONS ---
            # Looks for buttons with text "Join" or title "Join"
            buttons = driver.find_elements(By.XPATH, "//button[contains(@title, 'Join') or text()='Join']")
            
            if links:
                print("\n🔗 FOUND A LINK! Clicking...")
                original_window = driver.current_window_handle
                links[0].click()
                time.sleep(3)
                
                # Switch to the new tab that opened
                for window in driver.window_handles:
                    if window != original_window:
                        driver.switch_to.window(window)
                        print("🔀 Switched to new tab")
                        break
                
                if join_meeting_flow(driver): break

            elif buttons:
                print("\n🔘 FOUND A BUTTON! Clicking...")
                buttons[0].click()
                time.sleep(3)
                # Buttons usually don't open new tabs, so we just run the flow
                if join_meeting_flow(driver): break
            
            else:
                # Nothing found, print a dot and wait
                print(".", end="", flush=True)
                time.sleep(CHECK_DELAY)

        except Exception as e:
            # If something weird happens, just print error and keep trying
            print(f"\n⚠️ Error: {e}")
            time.sleep(CHECK_DELAY)

if __name__ == "__main__":
    driver = setup_driver()
    if driver:
        find_and_enter_channel(driver)
        watch_and_act(driver)