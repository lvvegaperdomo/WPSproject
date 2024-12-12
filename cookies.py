import json
import os
from collections import Counter
import matplotlib.pyplot as plt

def plot_distribution(vanilla_data, adblock_data, title):
    # Convert dict_values to lists of values
    vanilla_values = list(vanilla_data.values())
    adblock_values = list(adblock_data.values())
    
    plt.figure(figsize=(10, 6))
    plt.hist([vanilla_values, adblock_values], bins=30, label=['Vanilla Mode', 'Adblock Mode'], alpha=0.7)
    plt.xlabel('Count')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.show()

def extract_cookies(data):
    cookies = []
    if 'data' in data:
        if 'cookies' in data['data']:
            cookies.extend(data['data']['cookies'])  # JavaScript cookies
        if 'savedCalls' in data['data']:
            for call in data['data']['savedCalls']:
                if 'cookies' in call:
                    cookies.extend(call['cookies'])  # Cookies set by JavaScript
    # Extract only cookie names or values (depending on your use case)
    return [cookie.get('name', '') or cookie.get('value', '') for cookie in cookies]

def analyze_cookies(vanilla_folder, adblock_folder):
    vanilla_cookies = []
    adblock_cookies = []

    # Extract cookies from vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            with open(os.path.join(vanilla_folder, filename), 'r') as f:
                data = json.load(f)
                cookies = extract_cookies(data)
                vanilla_cookies.extend(cookies)

    # Extract cookies from adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                data = json.load(f)
                cookies = extract_cookies(data)
                adblock_cookies.extend(cookies)

    # Count cookie occurrences
    vanilla_cookie_counts = Counter(vanilla_cookies)
    adblock_cookie_counts = Counter(adblock_cookies)

    # Print out the counts of the most common cookies
    print("Top-10 Vanilla Mode Third-Party Cookies:")
    for cookie, count in vanilla_cookie_counts.most_common(10):
        print(f"{cookie}: {count}")

    # Plot distribution of third-party cookies
    plot_distribution(vanilla_cookie_counts, adblock_cookie_counts, "Number of Third-Party Cookies")

# Call the function for Task 3
analyze_cookies('vanilla_data', 'adblock_data')
