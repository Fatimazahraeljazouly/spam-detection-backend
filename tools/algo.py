import nltk
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
import string
import joblib

model = joblib.load('C:/Users/Eljazouly/Downloads/spam/spam/App/tools/svc_model.pkl')
vectorizer = joblib.load('C:/Users/Eljazouly/Downloads/spam/spam/App/tools//vectorizer.pkl')

ps = PorterStemmer()
def text_transform(txt): 
    txt = txt.lower() 
    txt = nltk.word_tokenize(txt) 

    y = []
    for i in txt: 
        if i.isalnum():    
            y.append(i)

    txt = y[:]
    y.clear()
    
    for i in txt: 
        if i not in stopwords.words('english') and i not in string.punctuation: 
            y.append(i)

    txt = y[:]
    y.clear()

    for i in txt: 
        y.append(ps.stem(i))

    return ' '.join(y)

def predict(txt): 
    new_text = text_transform(txt)
    data = vectorizer.transform([new_text]).toarray()

    prediction = model.predict(data)
    return prediction


print(f"Prédiction du modèle : {predict("Just wanted to let you know that the meeting has been rescheduled to 3 PM.")}")