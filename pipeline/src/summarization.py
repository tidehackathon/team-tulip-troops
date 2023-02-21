from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    global summarizer
    
    # truncate input somewhat (due to model max length)
    # TODO split context into chunks of max len, concat later?
    maxlen = 700
    if type(text) == str:
        text = ' '.join([txt for txt in text.split(' ')[:maxlen]])
    else:
        text = [' '.join([txt for txt in subtext.split(' ')[:maxlen]]) for subtext in text]

    summarized_text = summarizer(text, min_length=min(10, len(text)), max_length=128)

    if type(text) != str:
        summarized_text = [txt['summary_text'] for txt in summarized_text]
    else:
        summarized_text = summarized_text[0]['summary_text']
        
    return summarized_text