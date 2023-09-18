import pandas as pd
import psycopg2
from django.http import HttpResponse
import requests
import preprocessor as p
import pickle
import nltk
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from newAPI.models import *
from newAPI.serializers import *
import json
from rest_framework.decorators import api_view
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor
import os
from multiprocessing import Pool
import time
import logging
from operator import itemgetter
import sys
from psycopg2 import Error
import psycopg2.extras as extras

params_dic = {
    "host": "",
    "database": "",
    "user": "",
    "password": "",
}
conn = None
try:
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params_dic)
    if conn:
        print("DB Connected")
        cursor = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    sys.exit(1)

logging.info("Application started", exc_info=True)
logging.info("Sent the keyword request from browser url, e.g: ip/index/keyword", exc_info=True)

try:
    infile = open('sent_pkl', 'rb')
    new_model = pickle.load(infile)
    logging.info("sentiment pickle loaded", exc_info=True)

except Exception as e:
    logging.error("sentiment pickle is not found", exc_info=True)

import re


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # removing @mentions
    text = re.sub("#[A-Za-z0-9_]+", "", text)
    # text = re.sub(r'#', '',text)#removing '#' symbol
    text = re.sub(r'RT[\s]+', '', text)  # removing RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # removing hyperlink
    return text


def sent_print(my_list):
    new_dict = {}
    str_match = list(map(itemgetter('label'), my_list))
    for text in str_match:
        new_dict = text
    return new_dict


def analysis(tweet):
    a = new_model(tweet)
    return a


def index(request, search):
    search = search.replace('#', '')
    search = search.replace(' ', '_')
    df1 = pd.read_csv(r"C:\Users\userdata.csv")
    print("Raw data", df1)
    df1 = df1.drop_duplicates(subset=['id'])
    df1['preprocess_tweet'] = df1['tweet'].iloc[:].apply(cleanTxt)
    try:
        logging.info("Sentiment Analysis Started", exc_info=True)
        startt = time.time()
        df1['overall_analysis'] = df1['preprocess_tweet'].apply(analysis)
        print("Sentiment Time ==", time.time() - startt)
        logging.info("Sentiment Analysis Completed", exc_info=True)
    except Exception as e:
        logging.error("Sentiment Model is not working", exc_info=True)

    try:
        logging.info("Labels Enhancement Started", exc_info=True)
        df1['Sentiment'] = df1['overall_analysis'].apply(sent_print)
        logging.info("Labels Enhancement Completed", exc_info=True)
    except Exception as e:
        logging.error("Label Enhancement Approach Error", exc_info=True)
    simple_count = df1['Sentiment'].value_counts(ascending=True)
    print("simple count========", simple_count)
    df1.to_csv(r'C:\Users\user_data_SENTIMENT.csv')
  
    return HttpResponse('done', content_type='application/json')


def profile(request, search):
    search = search.replace('#', '')
    search = search.replace(' ', '_')
    response = requests.get("your crawler link" + search).json()
    df1 = pd.DataFrame(response)
    df1 = df1.drop_duplicates(subset=['id'])
    logging.info("Data duplication Removed", exc_info=True)
    start = time.time()
    df1['preprocess_tweet'] = df1['tweet'].iloc[:].apply(cleanTxt)
    end = time.time()
    print("Preprocessing time on 20 tweets==", end - start)

    logging.info('Tweets preprocessing completed', exc_info=True)
    try:
        logging.info("Sentiment Analysis Started", exc_info=True)
        startt = time.time()
        df1['overall_analysis'] = df1['preprocess_tweet'].apply(analysis)
        print("Sentiment time on 20 tweets==", time.time() - startt)
        logging.info("Sentiment Analysis Completed", exc_info=True)
    except Exception as e:
        logging.error("Sentiment Model is not working", exc_info=True)

    try:
        logging.info("Labels Enhancement Started", exc_info=True)
        df1['Sentiment'] = df1['overall_analysis'].apply(sent_print)
        logging.info("Labels Enhancement Completed", exc_info=True)
    except Exception as e:
        logging.error("Label Enhancement Approach Error", exc_info=True)

    count1 = df1['sentiment'].value_counts()
    print(df1['sentiment'])
    print(count1)
    df2 = df1.to_json(orient="records")

    return HttpResponse(df2, content_type='application/json')
