import json
import os
from time import sleep

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI
from openai.types import Batch, FileObject

from ai_2025.common import AI_MODELS


def get_client() -> OpenAI:
    config = AI_MODELS['gpt-simple']
    key = os.getenv(config.key_name)
    client = OpenAI(api_key=key, base_url=config.base_url)
    return client


def upload_input_file(client, file_name: str = 'q1.jsonl', purpose="batch") -> FileObject:
    """

    :param client:
    :param file_name:
    :param purpose: "batch" or "user_data"
    :return:
    """
    input_file = client.files.create(
        file=open(file_name, "rb"),
        purpose=purpose
    )

    return input_file


def create_batch(client, file_id: str) -> Batch:
    batch_input_file_id = file_id
    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "nightly eval job"
        }
    )
    return batch


def check_status(client, batch_id) -> Batch:
    batch = client.batches.retrieve(batch_id)
    return batch


def get_results(client, result_file_id) -> dict:
    file_response = client.files.content(result_file_id)
    print(file_response.text)
    response_dict: dict = json.loads(file_response.text)
    return response_dict


def process_batch(input_file: str, batch_id: str = None) -> dict:
    # 0
    client = get_client()
    logger.info('client connected')

    if batch_id is None:
        logger.info('creating batch')
        # 1
        batch_input_file = upload_input_file(client, input_file)
        file_id = batch_input_file.id
        logger.info('batch file upload complete')
        # 2
        batch = create_batch(client, file_id)
        batch_id = batch.id
        logger.info(f'batch processing started, id={batch_id}')

    # 3
    sleep(1)
    logger.info('waiting for batch to complete')
    while True:
        batch = check_status(client, batch_id)
        if batch.status == 'completed':
            break
        logger.info('batch not completed')
        sleep(20)

    # 4
    output_file_id = batch.output_file_id
    logger.info(f'pulling batch results with file_id={output_file_id}')
    results = get_results(client, output_file_id)

    print(results)


if __name__ == '__main__':
    import os

    load_dotenv()
    process_batch(input_file='q2.jsonl', batch_id='batch_68431e758eac819090abf2b58e740f39')
    # todo: create or find some nice dataclass to capture the output of the batch results
    # client = get_client()

    # 1)
    # upload_input_file(client)
    # FileObject(id='file-1uwPmyvLiCZGB8vjbxXdE3', bytes=549, created_at=1748626542, filename='q1.jsonl', object='file', purpose='batch', status='processed', expires_at=None, status_details=None)
    # FileObject(id='file-96xgwUmRZP9JuHfH9ejKxm', bytes=549, created_at=1748627399, filename='q1.jsonl', object='file', purpose='batch', status='processed', expires_at=None, status_details=None)

    # file_id = 'file-96xgwUmRZP9JuHfH9ejKxm'

    # 2)
    # batch = create_batch(client, file_id)

    """
    Batch(id='batch_6839ed2d2d14819096f4d404d663d7ad', completion_window='24h', created_at=1748626733, endpoint='/v1/chat/completions', 
    input_file_id='file-1uwPmyvLiCZGB8vjbxXdE3', object='batch', status='validating', 
    cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, 
    expires_at=1748713133, failed_at=None, finalizing_at=None, in_progress_at=None, 
    metadata={'description': 'nightly eval job'}, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))
    """
    # batch_id = batch.id
    # batch_id = 'batch_6839efddd1f8819086b3b8bd0e290aca'
    # 3) checking status
    # batch = check_status(client, batch_id)
    """
    Batch(id='batch_6839ed2d2d14819096f4d404d663d7ad', completion_window='24h', created_at=1748626733, endpoint='/v1/chat/completions', 
    input_file_id='file-1uwPmyvLiCZGB8vjbxXdE3', object='batch', status='completed', 
    cancelled_at=None, cancelling_at=None, completed_at=1748626799, error_file_id=None, errors=None, expired_at=None, 
    expires_at=1748713133, failed_at=None, finalizing_at=1748626798, in_progress_at=1748626734, 
    metadata={'description': 'nightly eval job'}, 
    output_file_id='file-RQNZaYaLALXyy7ZCGWf6ij', 
    request_counts=BatchRequestCounts(completed=2, failed=0, total=2))
    """
    # output_file_id = batch.output_file_id

    # 4) pulling result
    # output_file_id = 'file-Dgxm3cbUD58sN1aZ74xHoR'
    # get_results(client, 'file-Dgxm3cbUD58sN1aZ74xHoR')

    """
    {"id": "batch_req_6839f060cd048190ae368433d4361c3a", "custom_id": "request-1", "response": {"status_code": 200, "request_id": "e9fbe9f5ae06db8c9a08aa42685496f9", 
        "body": {"id": "chatcmpl-BcyA4UsSARLAVcTkHGvA6a53CuNzj", "object": "chat.completion", "created": 1748627424, 
            "model": "gpt-4.1-2025-04-14", "choices": [{"index": 0, "message": {"role": "assistant", 
                "content": "The capital of Poland is Warsaw.", "refusal": null, "annotations": []}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 22, "completion_tokens": 7, "total_tokens": 29, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}, "service_tier": "default", "system_fingerprint": "fp_799e4ca3f1"}}, "error": null}
    {"id": "batch_req_6839f060d90c8190a483aff349fd5acc", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "fbf01fe2ab61fa5e920d7edc8253f14b", 
        "body": {"id": "chatcmpl-BcyA5EiUwCMJ1n0Nb26C7pdqmHDll", "object": "chat.completion", "created": 1748627425, 
            "model": "gpt-4.1-2025-04-14", "choices": [{"index": 0, "message": {"role": "assistant", 
                "content": "The capital of Guatemala is Guatemala City.", "refusal": null, "annotations": []}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 24, "completion_tokens": 8, "total_tokens": 32, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}, "service_tier": "default", "system_fingerprint": "fp_b3f1157249"}}, "error": null}
    """
