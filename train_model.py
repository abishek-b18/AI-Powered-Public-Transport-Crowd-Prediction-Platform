import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("dataset/passenger_data.csv")

# Encode categorical columns
le_vehicle = LabelEncoder()
le_weather = LabelEncoder()
le_crowd = LabelEncoder()

df['Vehicle_Type'] = le_vehicle.fit_transform(df['Vehicle_Type'])
df['Weather'] = le_weather.fit_transform(df['Weather'])
df['Crowd_Level'] = le_crowd.fit_transform(df['Crowd_Level'])

# Features
X = df[['Vehicle_Type', 'Weather', 'Holiday', 'Passenger_Count', 'Occupancy']]

# Target
y = df['Crowd_Level']

# Train Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save model
pickle.dump(model, open("crowd_model.pkl", "wb"))

print("Model Trained Successfully!")