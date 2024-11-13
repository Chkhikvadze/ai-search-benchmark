import json
import matplotlib.pyplot as plt
import os

# Load JSON data
with open('category_area_percentages.json', 'r') as f:
    percentage_data = json.load(f)

# Prepare data for pie chart (Knowledge vs News)
summary_categories = ['Knowledge', 'News']
summary_percentages = [sum(percentage_data[cat].values()) for cat in summary_categories]

# Create pie chart for Knowledge vs News
plt.figure(figsize=(8, 6))
colors = plt.cm.tab10.colors  # Use a colormap with enough distinct colors
plt.pie(summary_percentages, labels=summary_categories, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Summary of Knowledge and News Categories')
plt.tight_layout()

# Save the summary pie chart as a PNG file
output_dir = 'docs/assets'
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, 'summary_category_percentages.png'), transparent=True)

# Prepare data for bar chart (each subcategory)
categories = []
percentages = []

for category, subcategories in percentage_data.items():
    for subcategory, percentage in subcategories.items():
        categories.append(f"{category} - {subcategory}")
        percentages.append(percentage)

# Create bar chart for each subcategory
plt.figure(figsize=(12, 8))
plt.bar(categories, percentages, color=colors)
plt.xticks(rotation=90)
plt.title('Category Area Percentages by Subcategory')
plt.ylabel('Percentage')
plt.tight_layout()

# Save the bar chart as a PNG file
plt.savefig(os.path.join(output_dir, 'subcategory_percentages.png'), transparent=True)

# Show the plots (optional)
# plt.show()