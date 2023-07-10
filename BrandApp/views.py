from django.shortcuts import render
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline , AutoTokenizer
from camel_tools.sentiment import SentimentAnalyzer
import json
from django.http import JsonResponse


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
    with open('E:\PFA\Interface\BrandReputation\BrandApp\src\output.json', encoding='utf-8') as file:
        data = json.load(file)
    comments = [item['Text'] for item in data]  # Extract 'text' field from each item
    

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
            sentiment_result=sa.predict(q)
    return render(request, 'home.html', {'sentiment_result': sentiment_result, "Radio":selected_value,"Q":q,"ButtonValue":ButtonValue,'comments': comments})


#login page
def login(request):
    return render(request, 'login.html')

#Charts page 
def charts(request):
    return render(request, 'charts.html')

#Data api to display on charts page
def get_data(request, *args, **kwargs):
    with open("E:\PFA\Interface\BrandReputation\BrandApp\src\output.json" ,encoding="utf-8") as file:
        data = json.load(file)

    return JsonResponse(data, safe=False)