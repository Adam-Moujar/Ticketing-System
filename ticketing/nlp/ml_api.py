import requests

# TODO have three APIs
API_URL = (
    'https://api-inference.huggingface.co/models/facebook/bart-large-mnli'
)
headers = {'Authorization': 'Bearer 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'}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_data(sequence_to_classify, candidate_labels):
    data = {
        'inputs': sequence_to_classify,
        'parameters': {
            'candidate_labels': candidate_labels,
            'multi_label': True,
        },
    }
    return query(data)
