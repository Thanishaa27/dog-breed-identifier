import random
import requests
from bs4 import BeautifulSoup

# Function to format the breed name to match the URL structure
def format_breed_name(breed):
    return breed.lower().replace(' ', '-')

# Function to get the page content using BeautifulSoup
def get_page_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }  # Add a user-agent header to mimic a browser request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None



def info(breed):
    breed_formatted = format_breed_name(breed)
    url = f"https://dogtime.com/dog-breeds/{breed_formatted}"
    soup = get_page_content(url)
    if soup:
        paragraphs = soup.find_all('p')
        if paragraphs:
            return "\n".join([para.get_text() for para in paragraphs[:3]]).strip()
    return "Information not available"

# Function to get a list of dog names based on gender from AKC
def name(gender):
    if gender.lower() == "male":
        url = "https://www.akc.org/expert-advice/lifestyle/top-100-boy-dog-names/"
    elif gender.lower() == "female":
        url = "https://www.akc.org/expert-advice/lifestyle/top-100-girl-dog-names/"
    else:
        return ["Invalid gender"]

    soup = get_page_content(url)
    if soup:
        names_section = soup.find('tbody')
        if names_section:
            names = names_section.get_text(separator="\n").strip().split("\n")
            return random.sample(names, 10)
    return ["No names available"]

# Function to get stats about a dog breed from DogTime
def stats(breed):
    breed_formatted = format_breed_name(breed)
    url = f"https://dogtime.com/dog-breeds/{breed_formatted}"
    soup = get_page_content(url)
    if soup:
        stats_section = soup.find('div', class_="breed-vital-stats-wrapper")
        if stats_section:
            stats_text = stats_section.get_text(separator="\n").strip().split("\n")
            stats_dict = {stat.split(":")[0].strip(): stat.split(":")[1].strip() for stat in stats_text if ":" in stat}
            breed_group = stats_dict.get("Breed Group", "N/A")
            height = stats_dict.get("Height", "N/A")
            weight = stats_dict.get("Weight", "N/A")
            lifespan = stats_dict.get("Life Span", "N/A")
            return f"Vital Stats\nDog Breed Group: {breed_group}\n\nHeight: {height}\n\nWeight: {weight}\n\nLife Span: {lifespan}"
    return "Vital Stats\nDog Breed Group: N/A\n\nHeight: N/A\n\nWeight: N/A\n\nLife Span: N/A"
