from transformers import pipeline

classifier = None


def load_classifier():
    global classifier
    classifier = pipeline(
        'zero-shot-classification', model='facebook/bart-large-mnli'
    )


def get_data(sequence_to_classify, candidate_labels, multi_label=True):
    if classifier is None:
        raise Exception('Classifier model not loaded')
    toReturn = classifier(
        sequence_to_classify, candidate_labels, multi_label=True
    )
    return toReturn
