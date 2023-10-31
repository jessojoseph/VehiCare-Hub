import pandas as pd
import random
from datetime import datetime, timedelta

# Create an empty DataFrame
data = {
    'Bike_Model': [],
    'Age': [],
    'Service_Type': [],
    'Service_History': [],
    'Service_Time (hours:minutes)': [],
    'Build_Year': [],
    'Mileage (km)': [],
    'Last_Serviced_Date (months)': [],
    'Current_Year': []
}

# Generate 2000 rows of synthetic data
bike_models = [
    'Yamaha FZ 250', 'Yamaha FZ V1', 'Yamaha FZ V2', 'Yamaha FZ V3',
    'Yamaha R15 V1', 'Yamaha R15 V2', 'Yamaha R15 V3', 'Yamaha R15 V4',
    'Yamaha MT15 v1', 'Yamaha MT15 v2', 'Yamaha FZ X'
]

service_types = [
    'Oil Change', 'Air Filter Change', 'Coolant Oil Change', 'Brake Fluid Change',
    'Fork Oil Change', 'Brake Inspection', 'Chain Inspection', 'Complete Check Up'
]

current_year = 2023

for _ in range(2000):
    bike_model = random.choice(bike_models)
    build_year = random.randint(2010, 2023)  # Build year from 2010 onwards
    age = current_year - build_year
    
    # Assign mileage based on age with added randomness
    mileage = random.randint(2000 + 1000 * (age // 2), 40000 + 5000 * (age // 2))
    mileage += random.randint(-5000, 5000)  # Introduce randomness

    service_type = random.choice(service_types)
    service_history = random.randint(0, 30)  # Random service history
    service_history += random.randint(-5, 5)  # Introduce randomness

    # Calculate service time based on age and service type with randomness
    if service_type == 'Complete Check Up':
        service_time_hours = min(age * 2, 25)  # Maximum 25 hours for "Complete Check Up"
    else:
        service_time_hours = age  # Default service time for other service types
    service_time_hours += random.randint(-3, 3)  # Introduce randomness

    # Convert service time to hours and minutes with randomness
    service_time_minutes = random.randint(0, 59)
    service_time_minutes += random.randint(-30, 30)  # Introduce randomness
    service_time_str = f"{service_time_hours:02}:{service_time_minutes:02}"

    # Generate a random number of months for the last serviced date with randomness
    months_ago = random.randint(1, 12)
    months_ago += random.randint(-3, 3)  # Introduce randomness

    data['Bike_Model'].append(bike_model)
    data['Age'].append(age)
    data['Service_Type'].append(service_type)
    data['Service_History'].append(service_history)
    data['Service_Time (hours:minutes)'].append(service_time_str)
    data['Build_Year'].append(build_year)
    data['Mileage (km)'].append(mileage)
    data['Last_Serviced_Date (months)'].append(months_ago)
    data['Current_Year'].append(current_year)

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the dataset to a CSV file
df.to_csv('bike_service_dataset.csv', index=False)
