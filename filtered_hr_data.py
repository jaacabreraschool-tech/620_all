import pandas as pd

data = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Data")

# Print all column names
print("="*60)
print("All columns in the dataset:")
print("="*60)
for i, col in enumerate(data.columns.tolist(), 1):
    print(f"{i:2d}. {col}")
print("="*60)
print(f"Total columns: {len(data.columns)}")
print("="*60)

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

# Remove duplicates across ALL columns
print("\n" + "="*60)
print("Removing duplicates across all columns...")
print("="*60)
print(f"Rows before deduplication: {len(filtered)}")
filtered_all_dedup = filtered.drop_duplicates()
print(f"Rows after deduplication: {len(filtered_all_dedup)}")

# Export to Excel with all columns
output_filename = "HR_Data_Deduplicated.xlsx"
filtered_all_dedup.to_excel(output_filename, index=False, sheet_name="Data")
print(f"\n✓ Excel file saved: {output_filename}")
print(f"✓ Total columns exported: {len(filtered_all_dedup.columns)}")
print("="*60)
