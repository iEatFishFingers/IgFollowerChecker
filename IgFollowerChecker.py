import instaloader
import getpass
import time
import random

# Create an instance of Instaloader with slower settings
L = instaloader.Instaloader(
    sleep=True,        # Sleep between requests
    quiet=False,       # Show what's happening
    download_pictures=False,  # Don't download posts
    download_videos=False,    # Don't download videos
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False
)

# Login code remains the same
username = input("Enter your Instagram username: ")
password = getpass.getpass("Enter your Instagram password: ")

print(f"Logging in as {username}...")
try:
    L.login(username, password)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit(1)

# Get your profile
print("Loading your profile...")
profile = instaloader.Profile.from_username(L.context, username)

# Get followers with delay
followers = set()
print("Collecting followers (this may take some time)...")
try:
    for follower in profile.get_followers():
        followers.add(follower.username)
        # Add random delay between processing each follower
        time.sleep(random.uniform(1, 3))
        if len(followers) % 10 == 0:
            print(f"Collected {len(followers)} followers so far...")
except Exception as e:
    print(f"Error while collecting followers: {e}")
    print(f"Partial data collected: {len(followers)} followers")

# Get following with delay
following = set()
print("Collecting following (this may take some time)...")
try:
    for followee in profile.get_followees():
        following.add(followee.username)
        # Add random delay between processing each following
        time.sleep(random.uniform(1, 3))
        if len(following) % 10 == 0:
            print(f"Collected {len(following)} following so far...")
except Exception as e:
    print(f"Error while collecting following: {e}")
    print(f"Partial data collected: {len(following)} following")

# Only proceed if we have data
if followers and following:
    # Find people who don't follow you back
    unfollowers = following - followers

    # Print results
    print(f"\nPeople who don't follow you back ({len(unfollowers)}):")
    for unfollower in sorted(unfollowers):
        print(unfollower)

    # Save to a file
    filename = f"{username}_unfollowers.txt"
    print(f"\nSaving results to {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        for unfollower in sorted(unfollowers):
            f.write(f"{unfollower}\n")

    print(f"Done! Unfollowers saved to {filename}")
else:
    print("Not enough data collected to determine unfollowers.")