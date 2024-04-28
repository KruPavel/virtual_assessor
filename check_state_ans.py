import torch
from torch import nn
from transformers import BertTokenizer, BertModel


class QuestionAnsweringClassifier(nn.Module):
    def __init__(self, bert_model='bert-base-uncased', num_labels=2):
        super(QuestionAnsweringClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs[1]
        logits = self.classifier(cls_output)
        return logits


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

model = QuestionAnsweringClassifier().to(device)
model.load_state_dict(torch.load('model4.pth'))


def get_state(text, question, answer):
    input_sequence = f"[CLS] {text} [SEP] {question} [SEP] {answer}"
    tokenized = tokenizer(input_sequence, padding='max_length',
                          truncation=True, max_length=512)

    input_ids = torch.tensor([tokenized['input_ids']]).to(device)
    attention_masks = torch.tensor([tokenized['attention_mask']]).to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_masks)[0]
        print(outputs, torch.abs(outputs[0]), torch.abs(outputs[1]))
        if torch.abs(outputs[0]) > torch.abs(outputs[1]):
            return 0
        return 1
