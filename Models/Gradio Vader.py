import gradio as gr
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_Vader(text):
    over_all_polarity = sid.polarity_scores(text)

    if over_all_polarity['compound'] >= 0.05:
        return "positive"
        

    elif over_all_polarity['compound'] <= -0.05:
        return "negative"
    
    else:
        return "neutral"

sid = SentimentIntensityAnalyzer()


data_file = pd.read_csv('E:\Brand reputation\Brand-Reputation-Possible-Models\Apple_iphone_11_reviews.csv')

data_file['sentiment_vader'] = data_file['text'].apply(lambda x: sentiment_Vader(x))


csv_data = data_file.to_csv('E:/Brand reputation/Brand-Reputation-Possible-Models/VADER_Analysis_Result.csv')



demo = gr.Interface(fn=sentiment_Vader, inputs="text", outputs="text")

demo.launch(share=True)   