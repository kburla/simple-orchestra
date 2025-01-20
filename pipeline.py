# pipeline.py
from prefect import task, flow, get_run_logger
import requests
import hashlib
import json

# Step 1: Define a task to fetch data (this could be any kind of data)
@task(retries=3, retry_delay_seconds=5, timeout_seconds=10)
def fetch_data(url):
    logger = get_run_logger()
    logger.info(f"Fetching data from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Ensure this throws an error on failure
    return response.json()

@task
def process_data(data):
    logger = get_run_logger()
    logger.info("Transforming data")

    first_words = []
    for post in data:
        first_word = post['body'].split()[0]
        first_words.append(first_word)
    
    return first_words

# Step 4: Save the result to a file
@task
def save_results(result, filename):
    logger = get_run_logger()
    logger.info(f"Saving results to {filename}")
    with open(filename, "w") as file:
        file.write(f"Processed data: {result}")
    return "Data saved successfully!"

# Step 5: Define the flow
@flow
def simple_pipeline(url: str, filename: str):
    data = fetch_data(url)
    transformed_data = process_data(data)
    save_results(transformed_data, filename)

# Step 6: Run the flow locally
if __name__ == "__main__":
    simple_pipeline(url="https://jsonplaceholder.typicode.com/posts", filename="result.txt")