import os
import json
from collections import Counter
import matplotlib.pyplot as plt

def plot_distribution(vanilla_counts, adblock_counts, title):
    # Check if there are any counts to plot
    if not vanilla_counts or not adblock_counts:
        print(f'No data to plot for {title}.')
        return
    
    # Get requests per website
    vanilla_request_counts = list(vanilla_counts.values())
    adblock_request_counts = list(adblock_counts.values())

    # Plot histogram for vanilla mode and adblock mode
    plt.figure(figsize=(10, 6)) 
    plt.hist([vanilla_request_counts, adblock_request_counts], bins=20, label=['Vanilla Mode', 'Adblock Mode'], alpha=0.7)
    plt.title(title)
    plt.xlabel('Number of Requests per Website')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show() 

def extract_requests(data):
    requests = []
    
    # Access requests from the 'data' field
    if 'data' in data and 'requests' in data['data']:
        for request in data['data']['requests']:
            domain = request.get('url', '')
            if domain:
                domain_name = domain.split('/')[2]  # Extract the domain name from the URL
                requests.append(domain_name)
    return requests

def analyze_third_party_requests(vanilla_folder, adblock_folder):
    vanilla_requests = []
    adblock_requests = []

    # Extract data from vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            with open(os.path.join(vanilla_folder, filename), 'r') as f:
                data = json.load(f)
                requests = extract_requests(data)
                vanilla_requests.extend(requests)

    # Extract data from adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                data = json.load(f)
                requests = extract_requests(data)
                adblock_requests.extend(requests)
    
    # Check how many requests were collected
    print(f"Vanilla mode requests count: {len(vanilla_requests)}")
    print(f"Adblock mode requests count: {len(adblock_requests)}")

    # Error if no third-party requests
    if not vanilla_requests or not adblock_requests:
        print("No third-party requests found.")
        return

    vanilla_counts = Counter(vanilla_requests)
    adblock_counts = Counter(adblock_requests)

    # Print out the counts of the most common domains
    print("\nTop-10 Vanilla Mode Third-Party Domains:")
    for domain, count in vanilla_counts.most_common(10):
        print(f"{domain}: {count}")

    # Plot distribution of third-party requests
    plot_distribution(vanilla_counts, adblock_counts, "Number of Third-Party Requests")

# Call the function for task 2
analyze_third_party_requests('vanilla_data', 'adblock_data')
