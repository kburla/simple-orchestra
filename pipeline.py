# pipeline.py
from prefect import task, flow
import requests
import hashlib

# Step 1: Define a task to fetch data (this could be any kind of data)
@task(retries=3, retry_delay_seconds=5, timeout_seconds=10)
def fetch_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    response = requests.get(url)
    response.raise_for_status()  # Ensure this throws an error on failure
    return response.json()

# Step 2: Transform the fetched data (capitalize the title)
@task
def transform_data(data):
    transformed_title = data['title'].capitalize()
    data['title'] = transformed_title
    return data

# Step 3: Process the data (extract the title)
@task
def process_data(data):
    return data['title']

# Step 4: Save the result
@task
def save_results(result):
    with open("result.txt", "w") as file:
        file.write(f"Processed data: {result}")
    return "Data saved successfully!"

# Step 5: Define the flow
@flow
def simple_pipeline():
    data = fetch_data()
    transformed_data = transform_data(data)
    processed_data = process_data(transformed_data)
    save_results(processed_data)

# Step 5: Run the flow locally
if __name__ == "__main__":
    simple_pipeline()
