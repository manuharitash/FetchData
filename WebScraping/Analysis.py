import csv
import codecs
import spacy
import re
from textstat.textstat import textstatistics
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor
from textstat import textstat
legacy_round = textstat._legacy_round
types_of_encoding = ["utf8", "cp1252"]
sentimentAnalyser = SentimentIntensityAnalyzer()

""""
Todo: 
POSITIVE SCORE
NEGATIVE SCORE
POLARITY SCORE
SUBJECTIVITY SCORE
AVG SENTENCE LENGTH

#PERCENTAGE OF COMPLEX WORDS
#FOG INDEX
#AVG NUMBER OF WORDS PER SENTENCE
#COMPLEX WORD COUNT
#WORD COUNT
#SYLLABLE PER WORD
#PERSONAL PRONOUNS
#AVG WORD LENGTH
"""

def readCSV(fileName):
    with open(fileName, mode ='r')as file:
        data=[]
        csvFile = csv.reader(file)
        for lines in csvFile:
            data.append(lines)
        data.pop(0)
    return data

def readText(fileName):
    for encoding_type in types_of_encoding:
        with codecs.open(fileName, encoding = encoding_type, errors ='replace') as file:
            data=""
            for x in file:
                data+=x
    return data

def polarity_score(text):
    return TextBlob(text).sentiment.polarity
def sentimental_analysis(text):
    return sentimentAnalyser.polarity_scores(text)
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def break_sentences(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return list(doc.sents)

def char_count(text):
    words = text.split()
    return sum(len(word) for word in words)

def word_count(text):
    sentences = break_sentences(text)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words
def average_word_length(text):
    return  char_count(text)/word_count(text)
def sentence_count(text):
    sentences = break_sentences(text)
    return len(sentences)

def syllables_count(word):
    return textstatistics().syllable_count(word)

def avg_syllables_per_word(text):
    syllable = syllables_count(text)
    words = word_count(text)
    ASPW = float(syllable) / float(words)
    return legacy_round(ASPW, 1)

def complex_words(text):

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [str(token) for token in sentence]
    diff_words_set = set()

    for word in words:
        syllable_count = syllables_count(word)
        if word not in nlp.Defaults.stop_words and syllable_count >= 2:
            diff_words_set.add(word)

    return len(diff_words_set)


def getAverageSentenceLength(text):
    words = word_count(text)
    sentences = sentence_count(text)
    average_sentence_length = float(words / sentences)
    return average_sentence_length

def percentage_of_complex_words(text):
    complex_words_ratio=complex_words(text)/word_count(text)
    return complex_words_ratio * 100;

def getFogIndex(text):
    return textstat.gunning_fog(text)

def averageNumberOfWordsPerSentence(text):
    words = word_count(text)
    sentences = sentence_count(text)
    average_words_per_sentence = float(words / sentences)
    return average_words_per_sentence

def personal_pronouns(text):
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    pronouns = pronounRegex.findall(text)
    return pronouns


def writeToCsvFile(outputData,fileName):
    with open(fileName, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(outputData)

def analyse_data(elm):
    urlId=elm[0]
    url=elm[1]
    fileName='OutputFiles/'+urlId+'.txt'
    text=readText(fileName)
    sentiment=sentimental_analysis(text)
    outRow=[urlId,
            url,
            sentiment['pos'],
            sentiment['neg'],
            polarity_score(text),
            getSubjectivity(text),
            getAverageSentenceLength(text),
            percentage_of_complex_words(text),
            getFogIndex(text),
            averageNumberOfWordsPerSentence(text),
            complex_words(text),
            word_count(text),
            avg_syllables_per_word(text),
            personal_pronouns(text),
            average_word_length(text)
            ]
    print(outRow)
    return outRow

def main():
    data=readCSV('Input.csv')
    executer=ThreadPoolExecutor(12)
    outputData=[]
    fieldRow=['urlId',
            'url',
            'POSITIVE SCORE',
            'NEGATIVE SCORE',
            'POLARITY SCORE',
            'SUBJECTIVITY SCORE',
            'AVG SENTENCE LENGTH',
            'PERCENTAGE OF COMPLEX WORDS',
            'FOG INDEX',
            'AVG NUMBER OF WORDS PER SENTENCE',
            'COMPLEX WORD COUNT',
            'WORD COUNT',
            'SYLLABLE PER WORD',
            'PERSONAL PRONOUNS',
            'AVG WORD LENGTH']

    print(fieldRow)
    outputData.append(fieldRow)
    futures=[]
    for elm in data:
             #outputData.append(analyse_data(elm))
             future=executer.submit(analyse_data,(elm))
             futures.append(future)

    executer.shutdown(wait=True)
    for future in futures:
        print(future.result())
        outputData.append(future.result())

    writeToCsvFile(outputData, 'OutputDataStructure.csv')

if __name__=="__main__":
    main()
