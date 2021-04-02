from django.shortcuts import render
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer  # to encode text to int
from tensorflow.keras.preprocessing.sequence import pad_sequences   # to do padding or truncating
from tensorflow.keras.models import load_model   # load saved model
from django.http import HttpResponse
import re
from .models import Movie
import pickle
from keras_preprocessing.text import tokenizer_from_json
import json








# Create your views here.
def form(request):
    return render(request,'form.html')

#Helper function for classifying
def classify_review(review_stmt):#returns 1 for positive,0 for negative
    english_stops = set(stopwords.words('english'))
    max_length=130#From train data
    #Loading stored model
    loaded_model = load_model('/home/kartik/APIsoftlab/Data Analysis/Sentiment-Analysis/review/sentiment.h5')
    # Pre-process input
    regex = re.compile(r'[^a-zA-Z\s]')
    review_stmt = regex.sub('', review_stmt)
    print('Cleaned: ', review_stmt)

    words = review_stmt.split(' ')
    filtered = [w for w in words if w not in english_stops]
    filtered = ' '.join(filtered)
    filtered = [filtered.lower()]

    # print('Filtered: ', filtered)
    token = Tokenizer(lower=False)
    tokenize_words = token.texts_to_sequences(filtered)
    tokenize_words = pad_sequences(tokenize_words, maxlen=max_length, padding='post', truncating='post')
    # print(tokenize_words)
    result = loaded_model.predict(tokenize_words)
    #print(result)
    if result >= 0.5:
        #print('positive')
        return True#1
    else:
        #print('negative')
        return False#0

def review_process(request):
    if request.method=='POST':
        review_stmt=request.POST.get('review')
        english_stops = set(stopwords.words('english'))
        max_length=130#From train data
        #Loading stored model
        loaded_model = load_model('/home/kartik/APIsoftlab/Data Analysis/Sentiment-Analysis/review/sentiment.h5')
        # Pre-process input
        regex = re.compile(r'[^a-zA-Z\s]')
        review_stmt = regex.sub('', review_stmt)
        print('Cleaned: ', review_stmt)

        words = review_stmt.split(' ')
        filtered = [w for w in words if w not in english_stops]
        filtered = ' '.join(filtered)
        filtered = [filtered.lower()]

        print('Filtered: ', filtered)
        with open('/home/kartik/APIsoftlab/Data Analysis/Sentiment-Analysis/review/data.txt') as json_file:
            token = json.load(json_file)
        token=tokenizer_from_json(token)
        print("TOKEN:" ,token)
        tokenize_words = token.texts_to_sequences(filtered)
        tokenize_words = pad_sequences(tokenize_words, maxlen=max_length, padding='post', truncating='post')
        print('tokenize words',tokenize_words)
        result = loaded_model.predict(tokenize_words)
        print(result)
        if result >= 0.5:
            print('positive')
            return HttpResponse('Positive review')
        else:
            print('negative')
            return HttpResponse('Negative review')
    else:
        return render(request,'form.html')

def updateReviews(request):
    if request.method=='POST':
        #Get the movie id
        print('Req received')
        m_id = request.POST.get('question')
        print('Client sent movie id:'+str(m_id))
        review_stmt = request.POST.get('review')
        print("review: ",review_stmt)
        isPositive = classify_review(review_stmt)
        Movie_object = Movie.objects.get(id=m_id)
        if isPositive:
            Movie_object.num_positive+=1
        else:
            Movie_object.num_negative+=1
        Movie_object.save()
        movies=Movie.objects.all()
        return render(request,'index1.html',{'movies':movies})
        #return HttpResponse('Recorded')

    else:
        #movie=Movie.objects.get(id=2)
        movies=Movie.objects.all()
        #print(movie.id)
        #print(movie.poster)
        return render(request,'index1.html',{'movies':movies})
        #return HttpResponse('Here will be kartik\'s page')

def movieData(request):
    movie=Movie.objects.get(id=2)
    print(movie.id)
    print(movie.poster)
    return render(request,'movie.html',{'movie':movie})