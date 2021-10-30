import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class TextModerator():
    '''Zero Shot Text Classifier based on Natural Language Inference for Filtering Messages'''

    def __init__(self, threshold=0.4, filters_path='text_filters.txt', model_path='nli_model', device=None):

        # Download model if it doesn't exist locally
        if not os.path.exists(model_path):
            model_path = "valhalla/distilbart-mnli-12-3"

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path).to(self.device)
        self.threshold = threshold

        self.hypothesis_template = "This text is about {}"
        self.filters_path = filters_path

    def preprocess(self, text):
        '''Preprocesses an input text to align with each filter topic'''

        # Load the filters
        with open(self.filters_path) as f:
            self.filters = f.read().strip().split('\n') + ['normal message']

        # create the hypotheses for each class
        hypotheses = [self.hypothesis_template.format(c) for c in self.filters]

        # preprocess the inputs
        inputs = self.tokenizer(
            [text] * len(self.filters),
            hypotheses,
            return_tensors='pt',
            truncation='only_first',
            padding=True
        )['input_ids']

        return inputs.to(self.device)

    def post_process(self, logits):
        '''Post-processes the model output to get the entailment logits and get the class prediction'''
        # Get the entailment probabilities
        idx = self.model.config.label2id['entailment']
        probabilities = torch.softmax(logits[:, idx], dim=0)

        # Get full outputs with probabilities for debugging purposes
        full_outputs = []
        for i, prob in enumerate(probabilities.tolist()):
            full_outputs.append(
                (self.filters[i], round(prob, 4))
            )

        full_outputs = sorted(full_outputs, key=lambda x: x[1], reverse=True)

        # Check if the message should be filtered
        pred_idx = probabilities.argmax()
        if pred_idx != len(self.filters) - 1 and probabilities.max() > self.threshold:
            result = True, self.filters[pred_idx]
        else:
            result = False, self.filters[pred_idx]

        return result, full_outputs

    def predict(self, text):
        '''Returns the final predictions for the inputs'''

        inputs = self.preprocess(text)
        logits = self.model(inputs).logits
        output = self.post_process(logits)

        return output
