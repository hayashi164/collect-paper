import arxiv
import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from ..crawler.collect_from_arxiv import collect_paper

app = func.FunctionApp()

connection_string = os.environ("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)

container_name = "arxiv"
container_client = blob_service_client.get_container_client(container_name)

# 日本時間午前６時=UTC21:00


@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    client = arxiv.Client()
    query = "RAG"
    if " " in query:
        query = query.replace(" ", " AND ")
    dir_path = "/tmp/"
    collect_paper(client, query, dir_path)
    files = os.listdir(dir_path)
    for file in files:
        with open(os.path.join(dir_path, file), "rb") as f:
            container_client.upload_blob(file, f)

    # ダウンロードした論文をblob_storageにアップロードする

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
