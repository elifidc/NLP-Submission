import requests
import matplotlib
import matplotlib.pyplot as plt


# Constants
BLOB_URL = "https://ncf2025largediststore.blob.core.windows.net/spy-files/spy_file_10_MB.txt"
CHUNK_SIZE = 10_000
AZURE_FUNCTION_URL = "https://nlp-function-elif.azurewebsites.net/api/analyze_verbs?code=GJzfqfX9OJOn998OItirm0YXRxO46osZMgNmx7rN-45iAzFuM8sQIA=="



def download_file(url, chunk_size):
    """Stream and yield chunks of the file."""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk.decode("utf-8", errors="ignore")

def send_chunk_to_function(chunk_text):
    """Send a chunk of text to the Azure function."""
    try:
        response = requests.post(AZURE_FUNCTION_URL, json={"text": chunk_text})
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


# Function to plot verb statistics as a bar chart
def plot_verb_stats(verb_counts):
    """Generate and save a simple bar chart of verb statistics."""
    plt.figure(figsize=(8, 5))
    plt.bar(verb_counts.keys(), verb_counts.values(), color='skyblue')
    plt.xlabel("Verb Tense")
    plt.ylabel("Count")
    plt.title("Verb Tense Distribution")
    plt.xticks(rotation=25)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("verb_stats.png")
    print("📊 Verb statistics saved as 'verb_stats.png'.")


# Function to plot a pie chart of verb statistics
def plot_verb_pie_chart(verb_counts):
    """Generate and save a pie chart of verb statistics."""
    plt.figure(figsize=(7, 7))
    plt.pie(verb_counts.values(), labels=verb_counts.keys(), autopct='%1.1f%%', startangle=90,
            colors=['skyblue', 'lightgreen', 'orange', 'salmon', 'lightcoral', 'lightyellow'])
    plt.title("Verb Tense Proportions")
    plt.savefig("verb_pie_chart.png")
    print("📊 Verb pie chart saved as 'verb_pie_chart.png'.")


# Function to plot a histogram of verb counts
def plot_verb_histogram(verb_counts):
    """Generate and save a histogram of verb counts."""
    plt.figure(figsize=(8, 5))
    plt.hist(verb_counts.values(), bins=10, color='lightblue', edgecolor='black')
    plt.xlabel("Verb Count")
    plt.ylabel("Frequency")
    plt.title("Histogram of Verb Counts")
    plt.savefig("verb_histogram.png")
    print("📊 Verb histogram saved as 'verb_histogram.png'.")


# Function to generate and save multiple verb visualizations automatically
def plot_all_verb_visuals(verb_counts):
    """Generate and save multiple verb visualizations."""
    plot_verb_stats(verb_counts)  # Bar chart
    plot_verb_pie_chart(verb_counts)  # Pie chart
    plot_verb_histogram(verb_counts)  # Histogram


# Your orchestrator function where verb counts are aggregated
def orchestrate_processing():
    """Orchestrates downloading and processing."""
    total_verbs = {"past": 0, "present": 0, "future": 0, "base": 0, "gerund": 0, "participle": 0}
    print(f"🔄 Processing {BLOB_URL} in {CHUNK_SIZE}-byte chunks...")

    # Loop through the chunks and process the file
    for chunk in download_file(BLOB_URL, CHUNK_SIZE):
        result = send_chunk_to_function(chunk)
        if result:
            for key in total_verbs.keys():
                total_verbs[key] += result.get(key, 0)

    print(f"✅ Processing Complete. Total verbs: {total_verbs}")

    # Automatically generate and save all visualizations
    plot_all_verb_visuals(total_verbs)


# Run the orchestrator
if __name__ == "__main__":
    orchestrate_processing()