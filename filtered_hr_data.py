import pandas as pd

data = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Data")

# Print all column names
print("All columns in the dataset:")
print(data.columns.tolist())

# Normalize columns
if "Full Name" in data.columns:
    data["Full Name"] = data["Full Name"].str.strip().str.title()
if "Resignee Checking" in data.columns:
    data["Resignee Checking"] = data["Resignee Checking"].str.strip()
if "Gender" in data.columns:
    data["Gender"] = data["Gender"].str.strip().str.capitalize()
if "Calendar Year" in data.columns:
    data["Calendar Year"] = pd.to_datetime(data["Calendar Year"], errors='coerce')
    data["Year"] = data["Calendar Year"].dt.year

# Filter for 2020-2025
filtered = data[data["Year"].between(2020, 2025)]

# Filter for Active only
filtered = filtered[filtered["Resignee Checking"].isin(["ACTIVE", "Active"])]

# Deduplicate by Full Name
filtered = filtered.drop_duplicates(subset=["Full Name"])

# Filter for employees who joined in 2020-2025
if "Year Joined" in filtered.columns:
    filtered["Year Joined"] = pd.to_datetime(filtered["Year Joined"], errors='coerce').dt.year
    joined_filtered = filtered[filtered["Year Joined"].between(2020, 2025)]
    print(len(joined_filtered))
else:
    print("Year Joined column not found")

# Select columns for output
base_columns = ["Full Name", "Gender", "Tenure", "Position/Level", "Generation", "Resignee Checking", "Year"]
extra_columns = []
for col in ["Joined Date", "Resignation Date"]:
    if col in data.columns:
        extra_columns.append(col)
columns = base_columns + extra_columns

# Print the filtered data
print(len(filtered))
