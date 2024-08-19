from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

# Функция анализа тональности
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Применение анализа тональности ко всем данным
def sentiment_analysis(data):
    sentiment_results = {}
    for source, texts in data.items():
        sentiment_results[source] = [analyze_sentiment(text) for text in texts]
    return sentiment_results

# Функция для извлечения ключевых слов
def extract_keywords(texts, num_keywords=10):
    vectorizer = CountVectorizer(max_df=0.85, stop_words='english')
    X = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()
    total_counts = X.toarray().sum(axis=0)
    
    keywords_with_counts = sorted(zip(keywords, total_counts), key=lambda x: x[1], reverse=True)
    return [keyword for keyword, count in keywords_with_counts[:num_keywords]]

# Применение извлечения ключевых слов ко всем данным
def keyword_analysis(data, num_keywords=10):
    keyword_results = {}
    for source, texts in data.items():
        combined_text = " ".join(texts)
        keywords = extract_keywords([combined_text], num_keywords)
        keyword_results[source] = keywords
    return keyword_results

# Основная функция анализа данных
def analyze_data(data):
    sentiment_results = sentiment_analysis(data)
    keyword_results = keyword_analysis(data)
    
    analysis_results = {
        'sentiment': sentiment_results,
        'keywords': keyword_results
    }
    
    return analysis_results