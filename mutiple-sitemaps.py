# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the file names
words_file = "words.txt" # The file that contains the words to search
sitemaps_file = "sitemaps.txt" # The file that contains the sitemap urls of different websites
output_file = "output.xlsx" # The file that will store the output

# Define a function to extract links from a sitemap url
def extract_links(url):
    # Open an XML sitemap and find content wrapped in loc tags
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = [element.text for element in soup.findAll("loc")]
    return links

# Define a function to check if a word is in a link
def check_word(word, link):
    # Convert both word and link to lowercase
    word = word.lower()
    link = link.lower()
    # Check if word is in link
    return word in link

# Read the words from the words file
with open(words_file, "r") as f:
    words = f.read().splitlines()

# Read the sitemap urls from the sitemaps file
with open(sitemaps_file, "r") as f:
    sitemap_urls = f.read().splitlines()

# Create an empty list to store the output data
output_data = []

# Loop through each sitemap url
for sitemap_url in sitemap_urls:
    # Extract the links from the sitemap url
    sitemap_links = extract_links(sitemap_url)
    # Loop through each word
    for word in words:
        # Loop through each link
        for link in sitemap_links:
            # Check if the word is in the link
            if check_word(word, link):
                # Append the word, link and sitemap url to the output data list
                output_data.append([word, link, sitemap_url])

# Print the number of matches found
print(f"Found {len(output_data)} matches")

# Save the output data to an excel file
df = pd.DataFrame(output_data, columns=["Word", "Link", "Sitemap URL"])
df.to_excel(output_file, index=False)

# Save the output data to a text file
with open(output_file.replace(".xlsx", ".txt"), "w") as f:
    for row in output_data:
        f.write("\t".join(row) + "\n")