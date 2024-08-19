from data_collection import collect_data
from text_processing import preprocess_text
from data_analysis import analyze_data

def main():
    currency = input("Введите криптовалюту: ")
    date = input("Введите дату (ГГГГ-ММ-ДД): ")
    
    raw_data = collect_data(currency, date)
    processed_data = preprocess_text(raw_data)
    analysis_results = analyze_data(processed_data)
    
    print("Результаты анализа тональности:")
    for source, sentiments in analysis_results['sentiment'].items():
        print(f"{source}: {Counter(sentiments)}")
    
    print("\nКлючевые слова:")
    for source, keywords in analysis_results['keywords'].items():
        print(f"{source}: {keywords}")

if __name__ == "__main__":
    main()