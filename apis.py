import json
import os
from collections import Counter
import matplotlib.pyplot as plt
from urllib.parse import urlparse

def plot_distribution(vanilla_data, adblock_data, title):
    # Convert dicts to lists
    vanilla_values = list(vanilla_data.values())
    adblock_values = list(adblock_data.values())
    
    # Plotting the distribution of counts
    plt.figure(figsize=(10, 6))
    plt.hist([vanilla_values, adblock_values], bins=30, label=['Vanilla Mode', 'Adblock Mode'], alpha=0.7)
    plt.xlabel('Number of API Calls')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.show()

def extract_api_calls(data, first_party_domain):
    third_party_domains = []
    
    if 'data' in data and 'apis' in data['data']:
        # Process callStats
        for source, api_methods in data['data']['apis'].get("callStats", {}).items():
            domain = urlparse(source).netloc
            if domain != first_party_domain:
                for api_call, count in api_methods.items():
                    third_party_domains.append(domain)

        
        # Process savedCalls
        for saved_call in data['data']['apis'].get("savedCalls", []):
            source = saved_call.get("source")
            description = saved_call.get("description")
            domain = urlparse(source).netloc
            if domain != first_party_domain:
                third_party_domains.append(domain)

    
    return third_party_domains
    
def analyze_api_calls(vanilla_folder, adblock_folder):
    vanilla_api_calls = []
    adblock_api_calls = []

    first_party_domain = None

    # Extract API calls from the Vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(vanilla_folder, filename), 'r') as f:
                    data = json.load(f)
                    if 'initialUrl' in data:
                        initial_url = data['initialUrl']
                        first_party_domain = urlparse(initial_url).netloc
                    domains = extract_api_calls(data, first_party_domain)
                    vanilla_api_calls.extend(domains)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")
                continue  # Skip invalid JSON files

    # Extract API calls from the Adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                data = json.load(f)
                # Extract the first-party domain from initialUrl
                if 'initialUrl' in data:
                    initial_url = data['initialUrl']
                    first_party_domain = urlparse(initial_url).netloc
                # Proceed with extracting API calls
                domains = extract_api_calls(data, first_party_domain)
                adblock_api_calls.extend(domains)
           

    # Count the occurrences of each third-party domain
    vanilla_api_counts = Counter(vanilla_api_calls)
    adblock_api_counts = Counter(adblock_api_calls)


    # Top 10 in Vanilla Mode
    print("Top-10 Third-Party Domains in Vanilla Mode:")
    for domain, count in vanilla_api_counts.most_common(10):
        print(f"{domain}: {count}")

    # Top 10 in Adblock Mode
    print("\nTop-10 Third-Party Domains in Adblock Mode:")
    for domain, count in adblock_api_counts.most_common(10):
        print(f"{domain}: {count}")

    plot_distribution(vanilla_api_counts, adblock_api_counts, "Third-Party API Calls")

# Call the function for task 4
analyze_api_calls('vanilla_data', 'adblock_data')
