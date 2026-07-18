import requests
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# Fetch Data from Public API
# -----------------------------
url = "https://disease.sh/v3/covid-19/countries"

response = requests.get(url)

data = response.json()

# Convert JSON to DataFrame
df = pd.DataFrame(data)

print(df.head())

# -----------------------------
# Select Required Columns
# -----------------------------
df = df[['country','cases','todayCases','deaths','recovered']]

# -----------------------------
# Clean Data
# -----------------------------
df.fillna(0, inplace=True)

# -----------------------------
# Save Processed Data
# -----------------------------
df.to_csv("processed_covid_data.csv", index=False)

df.to_json("processed_covid_data.json", orient="records")

# -----------------------------
# Top 10 Countries
# -----------------------------
top10 = df.sort_values(by="cases", ascending=False).head(10)

print(top10)

# -----------------------------
# Bar Chart
# -----------------------------
plt.figure(figsize=(10,5))
plt.bar(top10["country"], top10["cases"])
plt.title("Top 10 Countries by COVID Cases")
plt.xlabel("Country")
plt.ylabel("Cases")
plt.xticks(rotation=45)
plt.show()

# -----------------------------
# Line Chart
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(top10["country"], top10["recovered"], marker="o")
plt.title("Recovered Cases")
plt.xlabel("Country")
plt.ylabel("Recovered")
plt.xticks(rotation=45)
plt.show()

# -----------------------------
# Pie Chart
# -----------------------------
plt.figure(figsize=(7,7))
plt.pie(
    top10["cases"],
    labels=top10["country"],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("COVID Cases Distribution")
plt.show()

# -----------------------------
# Generate PDF Report
# -----------------------------
styles = getSampleStyleSheet()

pdf = SimpleDocTemplate("covid_report.pdf")

story = []

story.append(Paragraph("<b>COVID-19 Data Analysis Report</b>", styles['Title']))

story.append(Paragraph(f"Total Countries: {len(df)}", styles['Normal']))

story.append(Paragraph(f"Highest Cases: {df['cases'].max():,}", styles['Normal']))

story.append(Paragraph(f"Average Cases: {df['cases'].mean():,.2f}", styles['Normal']))

story.append(Paragraph("Processed data saved as CSV and JSON.", styles['Normal']))

pdf.build(story)

print("Project Completed Successfully!")
