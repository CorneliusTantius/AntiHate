import torch
from transformers import BertTokenizer
import torch.nn.functional as F


# tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')
# tokenizer.save_pretrained('./lib/tokenizer/indobert-base-p1-v1')
tokenizer = BertTokenizer.from_pretrained('./lib/tokenizer/indobert-base-p1-v1')
w2i, i2w = {'positive': 1, 'negative': 0}, {1: 'positive', 0: 'negative'}

text = 'Woi dasar kau anjing babi antek komunis'
subwords = tokenizer.encode(text)
model = torch.load("./lib/model/model_v1_87_11.pkl", map_location='cpu')
subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

logits = model(subwords)[0]
label = torch.topk(logits, k=1, dim=-1)[1].squeeze().item()

print(f'Text: {text} | Label : {i2w[label]} ({F.softmax(logits, dim=-1).squeeze()[label] * 100:.3f}%)')