import json
import os
from collections import Counter
import matplotlib.pyplot as plt

def plot_distribution(vanilla_data, adblock_data, title):
    # Convert dict_values to lists of values (frequencies)
    vanilla_values = list(vanilla_data.values())
    adblock_values = list(adblock_data.values())
    
    plt.figure(figsize=(10, 6))
    plt.hist([vanilla_values, adblock_values], bins=30, label=['Vanilla Mode', 'Adblock Mode'], alpha=0.7)
    plt.xlabel('Count of Third-Party Cookies')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.show()

def extract_cookies(data):
    cookies = []
    domains = []
    if 'data' in data:
        if 'cookies' in data['data']:
            cookies.extend(data['data']['cookies'])  # JavaScript cookies
            for cookie in data['data']['cookies']:
                domain = cookie.get('domain', '')
                if domain:
                    domains.append(domain)

        if 'savedCalls' in data['data']:
            for call in data['data']['savedCalls']:
                if 'cookies' in call:
                    cookies.extend(call['cookies'])  # Cookies set by JavaScript
                    for cookie in call['cookies']:
                        domain = cookie.get('domain', '')
                        if domain:
                            domains.append(domain)

    # Return cookie names or values for counting and domains for domain counts
    return [cookie.get('name', '') or cookie.get('value', '') for cookie in cookies], domains

def analyze_cookies(vanilla_folder, adblock_folder):
    vanilla_cookies = []
    adblock_cookies = []
    vanilla_domains = []
    adblock_domains = []

    # Extract cookies from vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            with open(os.path.join(vanilla_folder, filename), 'r') as f:
                try:
                    data = json.load(f)
                    cookies, domains = extract_cookies(data)
                    vanilla_cookies.extend(cookies)
                    vanilla_domains.extend(domains)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {filename}")

    # Extract cookies from adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                try:
                    data = json.load(f)
                    cookies, domains = extract_cookies(data)
                    adblock_cookies.extend(cookies)
                    adblock_domains.extend(domains)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {filename}")

    # Count cookie occurrences (for distribution plot)
    vanilla_cookie_counts = Counter(vanilla_cookies)
    adblock_cookie_counts = Counter(adblock_cookies)

    # Count domain occurrences (for top-10 domains)
    vanilla_domain_counts = Counter(vanilla_domains)

    # Print out the counts of the most common cookies
    print("Top-10 Vanilla Mode Third-Party Cookies:")
    for cookie, count in vanilla_cookie_counts.most_common(10):
        print(f"{cookie}: {count}")

    # Print out the most common domains (top-10)
    print("\nTop-10 Domains Setting Third-Party Cookies in Vanilla Mode:")
    for domain, count in vanilla_domain_counts.most_common(10):
        print(f"{domain}: {count}")

    # Plot distribution of third-party cookies
    plot_distribution(vanilla_cookie_counts, adblock_cookie_counts, "Number of Third-Party Cookies in Vanilla and Adblock Modes")

# Call the function for Task 3
analyze_cookies('vanilla_data', 'adblock_data')
