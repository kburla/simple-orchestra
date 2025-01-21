from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/kburla/simple-orchestra.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="my_workflow.py:show_stars",  # Correct the path here
    ).deploy(
        name="my-first-deployment",
        parameters={
            "url": "https://jsonplaceholder.typicode.com/posts",
            "filename": "result.json"
        },
        work_pool_name="firstpool",
        cron="0 * * * *",  # Run every hour
    )