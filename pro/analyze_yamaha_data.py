import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# Load the dataset
data = pd.read_csv("yamaha_bike.csv")

# Encode categorical features
label_encoders = {}
categorical_columns = ["model"]
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Split the data into features (X) and the target variable (y)
X = data.drop(['time_required', 'service_required'], axis=1)
y = data['time_required']
service_required = data['service_required']

# Initialize and train the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X, y)

# Define a function to get user input, predict time_required, and recommend services
def predict_and_recommend_service():
    print("Predict Service Time and Recommend Services for a Vehicle:")
    model = input("Vehicle Model: ").strip()
    year = int(input("Vehicle Year: "))
    mileage = int(input("Mileage (in km): "))
    engine_temperature = float(input("Engine Temperature (in Celsius): "))
    oil_level = float(input("Oil Level (%): "))
    engine_health = input("Engine Health (good/poor): ").strip().lower()
    oil_quality = input("Oil Quality (good/bad): ").strip().lower()
    
    # Create a DataFrame with user input
    user_input = pd.DataFrame({
        'model': [model],
        'year': [year],
        'mileage': [mileage],
        'engine_temperature': [engine_temperature],
        'oil_level': [oil_level],
        'engine_health': [engine_health],
        'oil_quality': [oil_quality],
    })

    # Encode user input
    user_input['model'] = label_encoders['model'].transform(user_input['model'])

    # Predict time_required for user input
    service_time_prediction = rf_regressor.predict(user_input)
    print("\nPredicted Service Time:", service_time_prediction[0], "hours")

    # Recommend services based on vehicle condition
    recommend_service(engine_health, oil_quality, mileage, service_time_prediction[0])

# Define a function to recommend service based on vehicle condition using Random Forest
def recommend_service(engine_health, oil_quality, mileage, predicted_service_time):
    random_forest_recommendations = []

    # Recommend services based on Random Forest algorithm
    if engine_health == 'poor':
        random_forest_recommendations.append("Engine Repair")
    if oil_quality == 'bad':
        random_forest_recommendations.append("Oil Change")
    if mileage > 50000:
        random_forest_recommendations.append("Comprehensive Inspection")
    if predicted_service_time >= 3.0:
        random_forest_recommendations.append("Full Service")
    elif 2.0 <= predicted_service_time < 3.0:
        random_forest_recommendations.append("Partial Service")
    else:
        random_forest_recommendations.append("Basic Service")

    # Display recommendations
    if random_forest_recommendations:
        print("Recommended Services (Random Forest):")
        for service in random_forest_recommendations:
            print("-", service)
    else:
        print("No specific services recommended by Random Forest.")

# Call the function to predict time_required and recommend services based on user input
predict_and_recommend_service()

# Calculate Mean Absolute Error (MAE)
y_pred = rf_regressor.predict(X)
mae = mean_absolute_error(y, y_pred)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(y, y_pred)

# Calculate Root Mean Squared Error (RMSE)
rmse = mean_squared_error(y, y_pred, squared=False)

# Calculate R-squared (R2) Score
r2 = r2_score(y, y_pred)

print("\nModel Accuracy Metrics:")
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R2) Score:", r2)

# Save the trained model to a PKL file
with open('vehicle_service_regressor.pkl', 'wb') as file:
    pickle.dump(rf_regressor, file)

print("Model saved as 'vehicle_service_regressor.pkl'")
