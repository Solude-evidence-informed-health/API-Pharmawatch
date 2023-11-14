class BigQueryDataRetrievalService:
    def __init__(self, bigquery_client):
        self.client = bigquery_client

    def execute_query(self, query):
        query_job = self.client.query(query)
        results = query_job.result()
        return results

    def get_total_pages(self, total_items, page_size):
        return (total_items + page_size - 1) // page_size