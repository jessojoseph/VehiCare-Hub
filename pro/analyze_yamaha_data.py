import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# Load the dataset (Use the path to your created dataset)
data = pd.read_csv("bike_service_dataset.csv")

# Split the data into features (X) and the target variable (y)
X = data.drop(['Service_Time (hours:minutes)'], axis=1)
y = data['Service_Time (hours:minutes)']

# Initialize and train the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X, y)

# Define a function to get user input, predict Service_Time, and recommend services
def predict_and_recommend_service():
    print("Predict Service Time and Recommend Services for a Bike:")
    model = input("Bike Model: ").strip()
    build_year = int(input("Build Year: "))
    mileage = int(input("Mileage (in km): "))
    service_type = input("Service Type: ").strip().lower()
    
    # You can add more user input features as needed
    
    # Create a DataFrame with user input
    user_input = pd.DataFrame({
        'Bike_Model': [model],
        'Build_Year': [build_year],
        'Mileage (km)': [mileage],
        'Service_Type': [service_type],
    })

    # Predict Service_Time for user input
    service_time_prediction = rf_regressor.predict(user_input)
    print("\nPredicted Service Time:", service_time_prediction[0], "hours")

    # Recommend services based on bike condition
    recommend_service(build_year, mileage, service_type, service_time_prediction[0])

# Define a function to recommend service based on bike condition
def recommend_service(build_year, mileage, service_type, predicted_service_time):
    recommendations = []

    # Customize recommendations based on your criteria
    if build_year < 2015:
        recommendations.append("Engine Upgrade")

    if service_type == 'oil change':
        recommendations.append("Air Filter Change")
    
    # Customize recommendations based on your criteria
    
    # Display recommendations
    if recommendations:
        print("Recommended Services:")
        for service in recommendations:
            print("-", service)
    else:
        print("No specific services recommended based on input criteria.")

# Call the function to predict Service_Time and recommend services based on user input
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
with open('bike_service_regressor.pkl', 'wb') as file:
    pickle.dump(rf_regressor, file)

print("Model saved as 'bike_service_regressor.pkl'")
