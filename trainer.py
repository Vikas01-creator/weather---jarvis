import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

def train_weather_model():
    # Load your historical data
    df = pd.read_csv('data/historical_weather.csv')
    
    # Features: Today's Temp, Humidity, Pressure
    X = df[['temp', 'humidity', 'pressure']]
    y = df['temp_tomorrow'] # Target
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the model to a file
    joblib.dump(model, 'models/weather_model.pkl')
    print("Model trained and saved to models/weather_model.pkl")

if __name__ == "__main__":
    train_weather_model()