"""
Code for analysis of PDF files (and - likely - other files as well).

"""
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types import FileObject

from ai_2025.common import AI_MODELS

"""
Works with openai provider only (others have other file api).
"""

def get_client() -> OpenAI:
    config = AI_MODELS['gpt-simple']
    key = os.getenv(config.key_name)
    client = OpenAI(api_key=key, base_url=config.base_url)
    return client


def upload_input_file(client, file_name: str = "q1.jsonl", purpose="batch") -> FileObject:
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


if __name__ == '__main__':
    load_dotenv()
    client = get_client()
    up_file = upload_input_file(client, "faktura2.pdf", purpose="user_data")
    print(up_file)
    fid = up_file.id

    keys = ["nr_faktury", "data_wystawienia", "data_sprzedaży", "sprzedawca_nazwa",
            "sprzedawca_nip", "nabywca_nazwa", "nabywca_nip", "razem_brutto",
            "razem_netto"]

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": fid,
                    },
                    {
                        "type": "input_text",
                        "text": "Przeanalizuj załączony PDF. "
                                f"Zwróć json z następującymi polami: {keys}",
                    },
                ],
            },
        ],
    )

    print(response.output_text)
