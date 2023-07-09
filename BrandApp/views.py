from django.shortcuts import render
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import BertTokenizer, BertForSequenceClassification , pipeline , AutoTokenizer
import torch
from camel_tools.sentiment import SentimentAnalyzer
#BERT sentiment analysis function
class BERTClassifier:
    def __init__(self):
        self.model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)

    def classify_text(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_labels = torch.argmax(logits, dim=1)
        return predicted_labels.item()  



#VADER sentiment analysis function
def sentiment_Vader(text):
    over_all_polarity = sid.polarity_scores(text)

    if over_all_polarity['compound'] >= 0.05:
        print(over_all_polarity)
        return "positive"
        

    elif over_all_polarity['compound'] <= -0.05:
        print(over_all_polarity)
        return "negative"
    
    else:
        print(over_all_polarity)
        return "neutral"

sid = SentimentIntensityAnalyzer()




#landing page
def landing(request):

#    if not request.user.is_authenticated:
    return render(request, "landing.html" )


def home(request):
    sentiment_result = None
    selected_value = None
    q = None
    ButtonValue = None

    if request.method =='POST':
        q = request.POST.get('q', '')  # Get the value of the 'q' input field
        selected_value = request.POST.get('ModelSelection') #Get the value from the select component   
        submit_button = request.POST.get('submit_button')
        if submit_button=="Brand Reputation":
            ButtonValue = "BR"

        elif selected_value== "Vader":
            sentiment_result = sentiment_Vader(q)  # Pass the 'q' value to the sentiment analysis function
        
        elif  selected_value == "roBERTa for tweets":
            sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer=AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest"))
            sentiment_result=sentiment_task(q)
        
        elif selected_value == "roBERTa arabic":
            sa = SentimentAnalyzer("CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment")
            sa.predict(q)

        elif selected_value=="BERT":
           sentiment_result= BERTClassifier().classify_text(q)
    return render(request, 'home.html', {'sentiment_result': sentiment_result, "Radio":selected_value,"Q":q,"ButtonValue":ButtonValue})


#login page
def login(request):
    return render(request, 'login.html')

# @login_required
# def home(request):
#     return render(request, 'home.html')
   