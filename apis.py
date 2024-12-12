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

def extract_api_calls(data):
    api_calls = []
    if 'data' in data and 'apis' in data['data']:
        for script, apis in data['data']['apis'].items():
            if isinstance(apis, list):  # Ensure we are dealing with a list of API calls
                for api in apis:
                    # If the API is a string, just add it to the list
                    if isinstance(api, str):
                        api_calls.append(api)
                    elif isinstance(api, dict):  # If it's a dictionary, extract the relevant details
                        url = api.get('url', '')
                        api_calls.append(url)
    return api_calls

def analyze_api_calls(vanilla_folder, adblock_folder):
    vanilla_api_calls = []
    adblock_api_calls = []

    # Extract API calls from vanilla mode folder
    for filename in os.listdir(vanilla_folder):
        if filename.endswith(".json"):
            with open(os.path.join(vanilla_folder, filename), 'r') as f:
                data = json.load(f)
                api_calls = extract_api_calls(data)
                vanilla_api_calls.extend(api_calls)

    # Extract API calls from adblock mode folder
    for filename in os.listdir(adblock_folder):
        if filename.endswith(".json"):
            with open(os.path.join(adblock_folder, filename), 'r') as f:
                data = json.load(f)
                api_calls = extract_api_calls(data)
                adblock_api_calls.extend(api_calls)

    # Count API call occurrences
    vanilla_api_counts = Counter(vanilla_api_calls)
    adblock_api_counts = Counter(adblock_api_calls)

    # Print out the counts of the most common API calls
    print("Top-10 Vanilla Mode Third-Party API Calls:")
    for api, count in vanilla_api_counts.most_common(10):
        print(f"{api}: {count}")

    # Plot distribution of third-party API calls
    plot_distribution(vanilla_api_counts, adblock_api_counts, "Number of Third-Party API Calls")

# Call the function for Task 4
analyze_api_calls('vanilla_data', 'adblock_data')

