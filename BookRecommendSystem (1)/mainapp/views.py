from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from mainapp.forms import BookRecommendForm
from django.views.generic import View, TemplateView

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
# Create your views here.


class BookRecommend(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/bookrecommend.html')
    
    def post(self, request, *args, **kwargs):
        form = BookRecommendForm(request.POST)
        input = request.POST.get('input')

        def func(inp):
            df = pd.read_csv('static/books.csv',error_bad_lines = False)

            df2 = df.copy()
            df2.loc[ (df2['average_rating'] >= 0) & (df2['average_rating'] <= 1), 'rating_between'] = "between 0 and 1"
            df2.loc[ (df2['average_rating'] > 1) & (df2['average_rating'] <= 2), 'rating_between'] = "between 1 and 2"
            df2.loc[ (df2['average_rating'] > 2) & (df2['average_rating'] <= 3), 'rating_between'] = "between 2 and 3"
            df2.loc[ (df2['average_rating'] > 3) & (df2['average_rating'] <= 4), 'rating_between'] = "between 3 and 4"
            df2.loc[ (df2['average_rating'] > 4) & (df2['average_rating'] <= 5), 'rating_between'] = "between 4 and 5"
            rating_df = pd.get_dummies(df2['rating_between'])
            language_df = pd.get_dummies(df2['language_code'])
            features = pd.concat([rating_df, 
                                language_df, 
                                df2['average_rating'], 
                                df2['ratings_count']], axis=1)


            min_max_scaler = MinMaxScaler()
            features = min_max_scaler.fit_transform(features)

            model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
            model.fit(features)
            dist, idlist = model.kneighbors(features)

            def BookRecommender(book_name):
                book_list_name = []
                book_id = df2[df2['title'] == book_name].index
                book_id = book_id[0]
                for newid in idlist[book_id]:
                    book_list_name.append(df2.loc[newid].title)
                return book_list_name
                
            response = BookRecommender(inp)
            return response

        response = func(input)
        return render(request, 'mainapp/bookrecommend.html', {'data':response, 'inp':input})


class TopTenBooks(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/toptenbooks.html')

class TopTenWriters(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/toptenwriters.html')

class MostReviewedBooks(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/mostreviewedbooks.html')