import numpy as np
import pandas as pd
import pickle
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from django.conf import settings
import os
import pandas as pd

base_dir = settings.MEDIA_ROOT
train = pd.read_pickle(os.path.join(base_dir, str('dataset/train.pckl')))
test = pd.read_pickle(os.path.join(base_dir, str('dataset/test.pckl')))

factory = StopWordRemoverFactory()
stop_word_list = factory.get_stop_words()
stop = stop_word_list + list(punctuation)

X_train = train['text']
X_test = test['text']
y_train = train['label']
y_test = test['label']

def predict(berita):

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
    
    model_svc = LinearSVC()
    model_svc.fit(X_train_tfidf, y_train)
    prediction = model_svc.predict(count_vect.transform([input_text]))
    output = str(prediction).strip("['']")

    return output


# berita_teks = "motor honda mobil APV otomotif"
# print(predict(berita_teks))