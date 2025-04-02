import pandas as pd

# Load the TSV file into a DataFrame
df = pd.read_csv('unitaryHACK_projects.tsv', sep='\t')

# Function to generate markdown header
def generate_markdown_header(row):
    tags_list = [tag.strip() for tag in str(row['tags']).split(',') if tag.strip()]
    tags_yaml = '\n  - '.join(tags_list)
    return f"""---
title: {row['title']}
emoji: {row['emoji'] if pd.notna(row['emoji']) else ''}
project_url: {row['project_url']}
metaDescription: {row['metaDescription']}
date: {row['date']}
summary: {row['summary']}
tags:
  - {tags_yaml}
---
"""

# Apply the function to each row
markdown_headers = df.apply(generate_markdown_header, axis=1)

# Combine into a single string for output
print("\n".join(markdown_headers.tolist()))

