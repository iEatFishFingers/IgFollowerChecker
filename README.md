# Instagram Unfollower Checker

This repository contains two different implementations to identify Instagram users who don't follow you back:

1. **IgFollowerChecker.py** - Uses the Instaloader library
2. **IgFollowerSelenium.py** - Uses Selenium for web automation

Both scripts achieve the same goal but use different methods, each with their own advantages and limitations.

## Features

- Log into your Instagram account
- Collect your follower list
- Collect your following list
- Identify users who don't follow you back
- Save the unfollowers list to a text file

## Option 1: Instaloader Implementation

### Requirements
- Python 3.6 or higher
- Instaloader package

### Installation
```
pip install instaloader
```
### Usage
1. Run the script:
```
python IgFollowerChecker.py
```
2. Enter your Instagram username and password when prompted
3. Results will be saved to `[username]_unfollowers.txt`

### Limitations
- Instagram may rate-limit or temporarily block automated access
- May not work if Instagram has recently updated its API
- You might encounter the error: "Please wait a few minutes before you try again"

## Option 2: Selenium Implementation

### Requirements
- Python 3.6 or higher
- Chrome browser
- ChromeDriver (matching your Chrome version)
- Selenium package

### Installation
```pip install selenium```

### Usage
1. Download the appropriate ChromeDriver for your Chrome version from:
   https://sites.google.com/chromium.org/driver/
2. Place the ChromeDriver executable in your system PATH or in the same directory as the script
3. Run the script:
```python IgFollowerSelenium.py```
4. Enter your Instagram username and password when prompted
5. Results will be saved to `[username]_unfollowers.txt`

### Known Issues & Workarounds

#### 1. Login Timing Issues
Sometimes the script may navigate to your profile before you can enter your credentials. If this happens:
- Type your credentials quickly when the login page appears
- If you miss the window, restart the script and try again

#### 2. "Save Login Info" Dialog
The automatic handling of the "Save Login Info" dialog may sometimes fail:
- Be prepared to manually click "Not Now" if the dialog appears and isn't automatically closed
- This won't affect the overall functionality of the script

#### 3. Scrolling Issues
For complete data collection, you may need to assist with scrolling:
- When the followers or following dialog appears, manually scroll to the bottom to ensure all users are loaded
- Let the script continue from there to collect the data

## Which Implementation Should I Use?

### Try the Instaloader version first if:
- You want a simpler solution with fewer dependencies
- You have a smaller number of followers/following
- You don't mind waiting if you get rate-limited

### Use the Selenium version if:
- The Instaloader version is getting rate-limited by Instagram
- You have a large number of followers/following
- You don't mind potentially helping with manual scrolling

## Troubleshooting

- If you encounter connection issues, Instagram might be rate-limiting your account. Wait a few hours before trying again.
- If the script fails to collect any followers or following, try running it again or check if your account has any temporary restrictions.
- For large accounts (thousands of followers/following), the scripts may take several minutes to run.

## Security Considerations

- Both scripts require your Instagram login credentials
- Credentials are only used for the current session and are not stored permanently
- For added security, consider using Instagram's two-factor authentication
- Use the scripts responsibly and infrequently to avoid triggering Instagram's automated systems

## Disclaimer

These tools are for personal use only. Frequent use may violate Instagram's Terms of Service. Use responsibly and at your own risk.
