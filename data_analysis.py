import numpy as np

def analyze_data(data):
    if not data:
        print("No data to analyze")
        return None
    
    try:
        analysis_results = np.mean(data)
        return analysis_results
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None