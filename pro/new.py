import pandas as pd
import random

# Define the number of records you want
num_records = 200

# Lists of possible values for each column
models = ["Yamaha YZF R1", "Yamaha MT-07", "Yamaha FZ-09", "Yamaha YZF R6", "Yamaha MT-09", "Yamaha FZ-07", "Yamaha YZF R3", "Yamaha MT-10", "Yamaha FZ-10", "Yamaha XSR700"]
years = [random.randint(2010, 2023) for _ in range(num_records)]
mileages = [random.randint(5000, 30000) for _ in range(num_records)]
engine_temperatures = [random.randint(70, 95) for _ in range(num_records)]
oil_levels = [1 if random.random() < 0.3 else 0 for _ in range(num_records)]  # 1 for 'Yes', 0 for 'No'
service_required = [1 if random.random() < 0.4 else 0 for _ in range(num_records)]  # 1 for 'Yes', 0 for 'No'
time_required = [round(random.uniform(2.0, 4.0), 1) if service == 1 else round(random.uniform(1.5, 3.0), 1) for service in service_required]

# Create a DataFrame without the 'bike_id' column
data = pd.DataFrame({
    'model': [random.choice(models) for _ in range(num_records)],
    'year': years,
    'mileage': mileages,
    'engine_temperature': engine_temperatures,
    'oil_level': oil_levels,
    'service_required': service_required,
    'time_required': time_required,
    'engine_health': [random.choice([0, 1]) for _ in range(num_records)],  # 0 for "bad," 1 for "good"
    'oil_quality': [random.choice([0, 1]) for _ in range(num_records)]  # 0 for "bad," 1 for "good"
})

# Save the data to a CSV file
data.to_csv('D:\pro\yamaha_bike.csv', index=False)
