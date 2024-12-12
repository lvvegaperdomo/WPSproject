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

def extract_http_headers(data):
    headers = []
    if 'data' in data and 'requests' in data['data']:
        for request in data['data']['requests']:
            if 'responseHeaders' in request:
                response_headers = request['responseHeaders']
                for header in response_headers:
                    headers.append(header.lower())  # Store headers in lowercase to avoid duplicates
    return headers

def analyze_http_headers(vanilla_folder, adblock_folder):
    vanilla_headers = []
    adblock_headers = []

    # Extract headers from vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            with open(os.path.join(vanilla_folder, filename), 'r') as f:
                data = json.load(f)
                headers = extract_http_headers(data)
                vanilla_headers.extend(headers)

    # Extract headers from adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                data = json.load(f)
                headers = extract_http_headers(data)
                adblock_headers.extend(headers)

    # Count header occurrences
    vanilla_header_counts = Counter(vanilla_headers)
    adblock_header_counts = Counter(adblock_headers)

    # Print out the counts of the most common headers
    print("Top-10 Vanilla Mode Non-Standard HTTP Headers:")
    for header, count in vanilla_header_counts.most_common(10):
        print(f"{header}: {count}")

    # Plot distribution of non-standard HTTP headers
    plot_distribution(vanilla_header_counts, adblock_header_counts, "Number of Non-Standard HTTP Headers")

# Call the function for Task 5
analyze_http_headers('vanilla_data', 'adblock_data')
