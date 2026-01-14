import pandas as pd
import random
from datetime import datetime

# Load the data
df = pd.read_excel('HR Cleaned Data 01.09.26.xlsx', sheet_name='Data')

# Remove time from Calendar Year, Year Joined, and Resignation Date
df['Calendar Year'] = pd.to_datetime(df['Calendar Year'], errors='coerce').dt.date
df['Year Joined'] = pd.to_datetime(df['Year Joined'], errors='coerce').dt.date
df['Resignation Date'] = pd.to_datetime(df['Resignation Date'], errors='coerce').dt.date

# Function to randomize month and day while keeping the year
def randomize_date(date):
    if pd.isna(date):
        return date
    try:
        dt = pd.to_datetime(date)
        year = dt.year
        month = random.randint(1, 12)
        # To avoid invalid dates, use day 1-28
        day = random.randint(1, 28)
        return pd.Timestamp(year=year, month=month, day=day).date()
    except:
        return date

# Apply the randomization
df['Year Joined'] = df['Year Joined'].apply(randomize_date)

# Save to new file
df.to_excel('HR Cleaned Data Randomized.xlsx', index=False)

print('New file created: HR Cleaned Data Randomized.xlsx')