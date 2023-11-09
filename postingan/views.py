from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from . import ml
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
# data dictionary

# https://abhishekchhibber.com/2017/03/01/django-importing-a-csv-file-to-database-models/
posts = [
		
		{'editor' : 'rizkhita',
		'title' : 'what is nlp?',
		'category' : 'machine learning',
		'content' : 'first post',
		'date_post' : 'August 23, 2020'},

		{'editor' : 'kiki',
		'title' : 'what is computer vision?',
		'category' : 'machine learning',
		'content' : 'second post',
		'date_post' : 'August 28, 2020'}

		]


import numpy as np
import pandas as pd
import pickle
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


factory = StopWordRemoverFactory()
stop_word_list = factory.get_stop_words()
stop = stop_word_list + list(punctuation)
import os
import pandas as pd

base_dir = settings.MEDIA_ROOT
train = pd.read_pickle(os.path.join(base_dir, str('dataset/train.pckl')))
test = pd.read_pickle(os.path.join(base_dir, str('dataset/test.pckl')))

def predict(berita):

    factory = StopWordRemoverFactory()
    stop_word_list = factory.get_stop_words()
    stop = stop_word_list + list(punctuation)

    X_train = train['text']
    X_test = test['text']
    y_train = train['label']
    y_test = test['label']
    count_vect = CountVectorizer(stop_words=stop)
    tfidf_transformer = TfidfTransformer()

    X_train_counts = count_vect.fit_transform(X_train)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    X_test_counts = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)

    from sklearn.preprocessing import LabelEncoder
    labels = LabelEncoder()
    y_train_labels_fit = labels.fit(y_train)
    y_train_lables_trf = labels.transform(y_train)

    input_text = str(berita)
    # check_len = str(input_text).split(" ")

    # uniq = np.unique(check_len)

    # from langdetect import detect
    # lang = detect(input_text)

    # if (len(check_len)<8) or (len(uniq)<5):
    #     prediction='please check your input'
    # elif lang !='id':
    #     prediction='sorry, this system work for indonesian news only'
    # else :
    model_svc = LinearSVC()
    model_svc.fit(X_train_tfidf, y_train)
    prediction = model_svc.predict(count_vect.transform([input_text]))

    output = prediction
    nah = str(output).strip("['']")



    return nah


# def home(request):
# 	# add data dictionary's key
# 	# var : data
# 	## context = { 'postings' : Post.objects.all() }
# 	context = { 'postings' : Post.objects.all(),  'title' : 'Home' }
# 	# add {'title' : 'community'}
# 	return render(request, 'postingan/home.html', context)

context = { 'postings' : Post.objects.all(),  'title' : 'Home' }

class PostListView(ListView):
	model = Post
	template_name = 'postingan/home.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'postings'
	ordering = ['-date_post']

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	# Post.category = Post.content


	def form_valid(self, form):
		form.instance.editor = self.request.user
		val = ml.predict(str(form.instance.content))
		form.instance.category = val
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	template_name = 'postingan/post_update.html' 

	def form_valid(self, form):
		form.instance.editor = self.request.user
		val = str(form.instance.content).split()
		form.instance.category = val
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.editor:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.editor:
			return True
		return False


def about(request):
	# add {'title' : 'community'}
	return render(request, 'postingan/about.html',  {'title' : 'About'})
