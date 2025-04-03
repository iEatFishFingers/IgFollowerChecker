from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import getpass
import random
import re

def get_unfollowers():
    # Get login credentials
    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    
    # Set up Chrome browser
    print("Starting Chrome browser...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    followers = set()
    following = set()
    
    try:
        # Login to Instagram
        print("Navigating to Instagram...")
        driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(3, 5))
        
        # Accept cookies if the dialog appears
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
            )
            cookie_button.click()
            time.sleep(random.uniform(1, 2))
        except:
            print("No cookie dialog found or already accepted")
        
        # Enter username and password
        print("Logging in...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        
        username_input.send_keys(username)
        time.sleep(random.uniform(0.5, 1.5))
        password_input.send_keys(password)
        time.sleep(random.uniform(0.5, 1.5))
        password_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(3, 5))
        
        # Handle "Save Login Info" dialog
        try:
            print("Looking for 'Save Login Info' dialog...")
            save_info_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            save_info_button.click()
            print("Clicked 'Not Now' on 'Save Login Info' dialog")
            time.sleep(random.uniform(1, 2))
        except:
            print("No 'Save Login Info' dialog found")
        
        # Handle notification dialog if it appears
        try:
            print("Looking for notification dialog...")
            notification_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            notification_button.click()
            print("Clicked 'Not Now' on notification dialog")
            time.sleep(random.uniform(1, 2))
        except:
            print("No notification dialog found")
        
        # Navigate to your profile
        print(f"Navigating to profile page for {username}...")
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.uniform(3, 5))
        
        # Get follower and following counts
        follower_count = 0
        following_count = 0
        
        try:
            # Find and extract follower count
            print("Extracting follower and following counts...")
            
            # Try various approaches to find the counts
            count_elements = driver.find_elements(By.XPATH, "//li//span")
            for element in count_elements:
                text = element.text
                if text:
                    # Look for numbers in the text
                    if "follower" in text.lower():
                        count_str = re.search(r'(\d+(?:,\d+)?)', text)
                        if count_str:
                            follower_count = int(count_str.group(1).replace(',', ''))
                            print(f"Found follower count: {follower_count}")
                    elif "following" in text.lower():
                        count_str = re.search(r'(\d+(?:,\d+)?)', text)
                        if count_str:
                            following_count = int(count_str.group(1).replace(',', ''))
                            print(f"Found following count: {following_count}")
            
            # If the above method doesn't work, try to find the counts directly
            if follower_count == 0 or following_count == 0:
                meta_elements = driver.find_elements(By.XPATH, "//section//span")
                for element in meta_elements:
                    text = element.text
                    if text and text.isdigit():
                        # Assume first number is posts, second is followers, third is following
                        digit_elements = [e for e in meta_elements if e.text and e.text.isdigit()]
                        if len(digit_elements) >= 3:
                            follower_count = int(digit_elements[1].text.replace(',', ''))
                            following_count = int(digit_elements[2].text.replace(',', ''))
                            print(f"Found follower count: {follower_count}")
                            print(f"Found following count: {following_count}")
                            break
            
            print(f"Expecting approximately {follower_count} followers and {following_count} following")
        except Exception as e:
            print(f"Error getting counts: {e}")
            # Set default values if counts couldn't be detected
            follower_count = 100
            following_count = 100
            print(f"Using default values: {follower_count} followers and {following_count} following")
        
        # Click on followers
        print("Looking for followers link to click...")
        
        # Try different approaches to find and click the followers link/count
        try:
            # First attempt: Try to find a standard follower link
            followers_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
            )
            print("Found followers link, clicking...")
            followers_link.click()
        except Exception as e:
            print(f"Could not find standard followers link: {e}")
            try:
                # Second attempt: Look for any clickable element with 'followers' in it
                followers_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'follower') or contains(text(), 'Follower')]")
                if followers_elements:
                    print(f"Found {len(followers_elements)} potential follower elements, clicking first one...")
                    followers_elements[0].click()
                else:
                    # Third attempt: Find and click the follower count by its position (first count after profile name)
                    counts = driver.find_elements(By.XPATH, "//section//li")
                    if len(counts) >= 2:  # Assuming second item is followers
                        print("Clicking on count element that should be followers...")
                        counts[1].click()
                    else:
                        print("Could not find followers element to click")
            except Exception as e2:
                print(f"Error in alternative follower link attempts: {e2}")
        
        time.sleep(random.uniform(2, 4))
        
        # Now collect followers with improved scrolling logic
        print("Collecting followers...")
        
        try:
            # Wait for the followers list to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            
            # Find the scrollable area
            scroll_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow') or contains(@style, 'auto')]"))
            )
            
            # Calculate how many scrolls we need based on follower count
            estimated_scrolls = max(follower_count // 6, 10)  # Ensure we have enough scrolls
            
            print(f"Will perform approximately {estimated_scrolls} scrolls to capture all followers")
            
            # Scroll and collect using the improved method
            last_height = 0
            collected_usernames = set()
            
            for i in range(estimated_scrolls):
                if i % 5 == 0:  # Only print every 5 scrolls to reduce console spam
                    print(f"Scrolling followers ({i+1}/{estimated_scrolls})...")
                
                # Scroll down to load new content
                driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scroll_box)
                time.sleep(random.uniform(1.0, 1.5))  # Wait for content to load
                
                # Check if we've reached the end of the list
                new_height = driver.execute_script('return arguments[0].scrollHeight', scroll_box)
                
                # Get all currently visible usernames
                follower_elements = scroll_box.find_elements(By.XPATH, ".//a[@role='link']")
                current_batch = set()
                
                for elem in follower_elements:
                    try:
                        username_text = elem.text
                        if username_text and not username_text.startswith('#') and not '@' in username_text:
                            current_batch.add(username_text)
                    except:
                        continue
                
                # Add new usernames to our collection
                new_usernames = current_batch - collected_usernames
                followers.update(new_usernames)
                collected_usernames.update(current_batch)
                
                if i % 5 == 0:
                    print(f"  Found {len(new_usernames)} new followers (total: {len(followers)})")
                
                # Check if we're at the end of the list
                if i > 5 and new_height == last_height and len(new_usernames) == 0:
                    print("Reached end of followers list")
                    break
                
                last_height = new_height
            
            print(f"Collected {len(followers)} followers out of approximately {follower_count}")
            
            # Try multiple approaches to close the dialog
            try:
                # First try the most common close button selectors
                close_buttons = driver.find_elements(By.XPATH, "//div[@role='dialog']//button")
                for button in close_buttons:
                    try:
                        aria_label = button.get_attribute('aria-label')
                        if aria_label and ('Close' in aria_label or 'close' in aria_label):
                            print("Found close button by aria-label, clicking...")
                            button.click()
                            break
                    except:
                        continue
                else:
                    # Try using the SVG elements that are typically part of close buttons
                    svg_buttons = driver.find_elements(By.XPATH, "//div[@role='dialog']//button[.//svg]")
                    if svg_buttons:
                        print("Found close button with SVG, clicking...")
                        svg_buttons[0].click()
                    else:
                        # Try the Escape key
                        print("Trying to close dialog with Escape key...")
                        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            except Exception as e:
                print(f"Error closing dialog: {e}")
                # Last resort - refresh the page
                print("Refreshing page to escape dialog...")
                driver.refresh()
            
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"Error collecting followers: {e}")
        
        # Go back to profile page
        print("Going back to profile page...")
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.uniform(3, 5))
        
        # Now click on following
        print("Looking for following link to click...")
        try:
            following_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))
            )
            print("Found following link, clicking...")
            following_link.click()
        except Exception as e:
            print(f"Could not find standard following link: {e}")
            try:
                # Alternative approach: Look for any clickable element with 'following' in it
                following_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'following') or contains(text(), 'Following')]")
                if following_elements:
                    print(f"Found {len(following_elements)} potential following elements, clicking first one...")
                    following_elements[0].click()
                else:
                    # Try finding and clicking the following count by position (third count)
                    counts = driver.find_elements(By.XPATH, "//section//li")
                    if len(counts) >= 3:  # Assuming third item is following
                        print("Clicking on count element that should be following...")
                        counts[2].click()
                    else:
                        print("Could not find following element to click")
            except Exception as e2:
                print(f"Error in alternative following link attempts: {e2}")
        
        time.sleep(random.uniform(2, 4))
        
        # Now collect following with the same improved scrolling logic
        print("Collecting following...")
        
        try:
            # Wait for the following list to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            
            # Find the scrollable area
            scroll_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow') or contains(@style, 'auto')]"))
            )
            
            # Calculate how many scrolls we need based on following count
            estimated_scrolls = max(following_count // 6, 10)  # Ensure we have enough scrolls
            
            print(f"Will perform approximately {estimated_scrolls} scrolls to capture all following")
            
            # Scroll and collect using the improved method
            last_height = 0
            collected_usernames = set()
            
            for i in range(estimated_scrolls):
                if i % 5 == 0:  # Only print every 5 scrolls to reduce console spam
                    print(f"Scrolling following ({i+1}/{estimated_scrolls})...")
                
                # Scroll down to load new content
                driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scroll_box)
                time.sleep(random.uniform(1.0, 1.5))  # Wait for content to load
                
                # Check if we've reached the end of the list
                new_height = driver.execute_script('return arguments[0].scrollHeight', scroll_box)
                
                # Get all currently visible usernames
                following_elements = scroll_box.find_elements(By.XPATH, ".//a[@role='link']")
                current_batch = set()
                
                for elem in following_elements:
                    try:
                        username_text = elem.text
                        if username_text and not username_text.startswith('#') and not '@' in username_text:
                            current_batch.add(username_text)
                    except:
                        continue
                
                # Add new usernames to our collection
                new_usernames = current_batch - collected_usernames
                following.update(new_usernames)
                collected_usernames.update(current_batch)
                
                if i % 5 == 0:
                    print(f"  Found {len(new_usernames)} new following (total: {len(following)})")
                
                # Check if we're at the end of the list
                if i > 5 and new_height == last_height and len(new_usernames) == 0:
                    print("Reached end of following list")
                    break
                
                last_height = new_height
            
            print(f"Collected {len(following)} following out of approximately {following_count}")
            
        except Exception as e:
            print(f"Error collecting following: {e}")
        
        # Calculate unfollowers
        if followers and following:
            unfollowers = following - followers
            
            print(f"\nPeople who don't follow you back ({len(unfollowers)}):")
            for unfollower in sorted(unfollowers):
                print(unfollower)
            
            # Save to file
            filename = f"{username}_unfollowers.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for unfollower in sorted(unfollowers):
                    f.write(f"{unfollower}\n")
            
            print(f"Results saved to {filename}")
        else:
            print("Could not collect enough data to determine unfollowers")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    get_unfollowers()