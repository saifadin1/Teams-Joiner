import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- CONFIGURATION ---
CHANNEL_NAME = "PD_Lab2"   # Name of the channel to watch
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
    Handles the 'Join Now' screen (camera/mic setup).
    Includes fixes for nested text and iframes.
    """
    print("⏳ Handling Pre-Join Lobby...")

    # Define robust selectors (Priority order)
    # 1. data-tid is the most stable ID used by MS developers
    # 2. aria-label handles accessibility tags
    # 3. contains(., 'text') finds text even if wrapped in spans/divs
    join_btn_xpaths = [
        "//button[@data-tid='prejoin-join-button']",
        "//button[contains(@aria-label, 'Join now')]",
        "//button[contains(., 'Join now')]",
        "//button[contains(@class, 'join-btn')]"
    ]

    try:
        # Wait a moment for the new window/UI to fully render
        time.sleep(5)

        # --- FIX 1: IFRAME CHECK ---
        # Sometimes the meeting lobby is inside an iframe. We check for that.
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"   (Found {len(iframes)} iframes. Checking content...)")
            # Usually the main meeting frame is the last one loaded
            driver.switch_to.frame(iframes[-1])

        # --- FIX 2: ROBUST CLICKER ---
        found_btn = None
        for xpath in join_btn_xpaths:
            try:
                # We use a short wait for each selector attempt
                found_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                if found_btn:
                    print(f"✅ Found button using: {xpath}")
                    found_btn.click()
                    break
            except:
                continue
        
        if not found_btn:
            # If we switched to an iframe and failed, switch back to main just in case
            driver.switch_to.default_content()
            raise Exception("Could not find 'Join now' button with any known selector.")

        print("🚀 JOIN SUCCESSFUL!")
        
        # Wait 10 seconds for connection, then raise hand
        time.sleep(10)
        print("🖐️ Raising hand...")
        
        # Ensure we are focused on the body before sending keys
        driver.switch_to.default_content()
        webdriver.ActionChains(driver)\
            .key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('k')\
            .key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
            
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