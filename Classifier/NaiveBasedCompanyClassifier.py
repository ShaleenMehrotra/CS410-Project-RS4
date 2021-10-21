import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names


def __word_feats(words):
    return dict([(word, True) for word in words])

positive_vocab = ['awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)']
negative_vocab = ['dissatisfied',  ':(']
neutral_vocab = ['satisfied', 'ok']

positive_features = [(__word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(__word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(__word_feats(neu), 'neu') for neu in neutral_vocab]

train_set = negative_features + positive_features + neutral_features

classifier = NaiveBayesClassifier.train(train_set)


def is_good(rating_descption):
    # Predict
    neg = 0
    pos = 0
    sentence = rating_descption.lower()
    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(__word_feats(word))
        print(classResult)
        if classResult == 'neg' or classResult == 'neu':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1
    rating = (float(pos) / len(words)) > (float(neg) / len(words))
    return rating

if __name__ == '__main__':
    print ("Starting classifier")