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
    try:
        text = truncate_text(text, 700)
        summarized_text = summarizer(text, min_length=min(10, len(text)), max_length=max_len)
    except:
        text = truncate_text(text, 600)
        summarized_text = summarizer(text, min_length=min(10, len(text)), max_length=max_len)

    if type(text) != str:
        result = []
        for i, txt in enumerate(summarized_text):
            if len(txt['summary_text']) > len(text[i]):
                result.append(text[i])
            else:
                result.append(txt['summary_text'])
        return result
    else:
        summary = summarized_text[0]['summary_text']
        if len(summary) > len(text):
            return text
        else:
            return summary

def truncate_text(text, max_tokens):
    if type(text) == str:
        text = ' '.join([txt for txt in text.split(' ')[:max_tokens]])
    else:
        text = [' '.join([txt for txt in subtext.split(' ')[:max_tokens]]) for subtext in text]

    return text