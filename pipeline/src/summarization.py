from transformers import pipeline
import torch


if torch.cuda.is_available():    
    device = torch.device("cuda:0")
    print('GPU used for summarizer: {}'.format(torch.cuda.get_device_name(0)))
else:
    device = torch.device("cpu")

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)


def summarize_text(text, max_len=128):
    global summarizer
    
    # truncate input somewhat (due to model max length)
    # TODO split context into chunks of max len, concat later?
    maxlen = 700
    if type(text) == str:
        text = ' '.join([txt for txt in text.split(' ')[:maxlen]])
    else:
        text = [' '.join([txt for txt in subtext.split(' ')[:maxlen]]) for subtext in text]

    summarized_text = summarizer(text, min_length=min(10, len(text)), max_length=max_len)

    if type(text) != str:
        summarized_text = [txt['summary_text'] for txt in summarized_text]
    else:
        summarized_text = summarized_text[0]['summary_text']
        
    return summarized_text