import pandas as pd
from UDFs import preprocess
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load the data
dfjokes = pd.read_csv('jokes.csv')

# Preprocess 'text' and update the dataframe
dfjokes['text'] = dfjokes['text'].apply(preprocess)

# Transform data and split it into the training and test sets
dfjokes.humor.replace(True, 1, inplace = True)
dfjokes.humor.replace(False, 0, inplace = True)

X = dfjokes.text.values
y = dfjokes.humor.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

# Vectorize text data
vectorizer = CountVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Logistic regression (LR) with Stochastic Gradient Descent (SGD) training
lr_classifier = SGDClassifier(loss = 'log_loss', max_iter = 1000)
lr_classifier.fit(X_train, y_train)

# Multinomial Naive Bayes (MNB)
mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train, y_train)

# Save the trained vectorizer and models
joblib.dump(vectorizer, 'vectorizer.joblib')
joblib.dump(lr_classifier, 'lr_classifier.joblib')
joblib.dump(mnb_classifier, 'mnb_classifier.joblib')