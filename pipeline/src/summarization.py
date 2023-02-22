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
    done = False
    trunc_len = 700
    while (not done) and (trunc_len > 300):
        print(trunc_len)
        try:
            text = truncate_text(text, trunc_len)
            summarized_text = summarizer(text, min_length=min(10, len(text)), max_length=max_len)
            done = True
        except:
            trunc_len -= 100

    if type(text) != str:
        summarized_text = [txt['summary_text'] for txt in summarized_text]
    else:
        summarized_text = summarized_text[0]['summary_text']
        
    return summarized_text

def truncate_text(text, max_tokens):
    if type(text) == str:
        text = ' '.join([txt for txt in text.split(' ')[:max_tokens]])
    else:
        text = [' '.join([txt for txt in subtext.split(' ')[:max_tokens]]) for subtext in text]

    return text