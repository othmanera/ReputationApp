from django.shortcuts import render
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from transformers import pipeline
from django.contrib.auth.decorators import login_required



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
    Request=None
    if request.method =='POST':
        q = request.POST.get('q', '')  # Get the value of the 'q' input field
        selected_value = request.POST.get('ModelSelection')
        Request = 'post'
        if selected_value== "Vader":
            sentiment_result = sentiment_Vader(q)  # Pass the 'q' value to the sentiment analysis function
        elif  selected_value == "roBERTa":
            # sentiment_classifier = pipeline("sentiment-analysis", model="roberta-base")
            # sentiment_result = sentiment_classifier(q)[0]['label']
            pass
    return render(request, 'home.html', {'sentiment_result': sentiment_result,  "Radio":selected_value,"Q":q ,"Request":Request})


#login page
def login(request):
    return render(request, 'login.html')
@login_required
def home(request):
    return render(request, 'home.html')
   