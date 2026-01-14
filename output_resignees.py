import pandas as pd

# Load the Excel file
df = pd.read_excel('HR Cleaned Data 01.09.26.xlsx')

# Filter for LEAVERs
leavers = df[df['Resignee Checking'] == 'LEAVER'].copy()  # Use .copy() to avoid warnings

# Extract year and month from Resignation Date
leavers['Year'] = leavers['Resignation Date'].dt.year
leavers['Month'] = leavers['Resignation Date'].dt.month

# Filter for years 2020 to 2025
leavers_filtered = leavers[(leavers['Year'] >= 2020) & (leavers['Year'] <= 2025)]

# Group by Year and Month, count
resignees_count = leavers_filtered.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Sort by Year and Month
resignees_count = resignees_count.sort_values(['Year', 'Month'])

# Save to Excel
resignees_count.to_excel('Resignees_Output.xlsx', index=False)

print("Output saved to Resignees_Output.xlsx")