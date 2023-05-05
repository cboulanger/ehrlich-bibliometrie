import pandas as pd
from tqdm.notebook import tqdm
import json
import requests
import os
import re

def extract_year(metadata):
    if 'published-print' in metadata:
        pub_info = metadata['published-print']
    elif 'issued' in metadata:
        pub_info = metadata['issued']
    else:
        return None

    if 'date-parts' in pub_info:
        year = pub_info['date-parts'][0][0]
    elif 'raw' in pub_info:
        year = pub_info['raw'][:4]
    else:
        return None

    return int(year)

def extract_author(metadata):
    author = metadata.get('author', [])
    return author[0].get('family','') if len(author) > 0 else ''

def get_metadata(doi):
    cache_file = f'cache/{doi}.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            metadata = json.load(f)
    else:
        url = f'https://api.crossref.org/works/{doi}'
        response = requests.get(url)
        try:
            metadata = response.json()['message']
        except json.JSONDecodeError:
            print(f"CrossRef error: could not load metadata for {url}")
            metadata = None
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(metadata, f)
    return metadata

def extract_metadata_from_filename(input_string):
    pattern = r'^(?P<author>.*?)\s\((?P<year>\d{4})\)\s(?P<title>.*)\.txt$'
    match = re.match(pattern, input_string)

    if match:
        author = match.group('author')
        year = match.group('year')
        title = match.group('title')
        return author, year, title
    else:
        return None

def truncate(s, x):
    return s[:x] + '...' if len(s) > x else s

def create_corpus(corpus_dir):
    articles = []
    for filename in tqdm(os.listdir(corpus_dir), desc="Analyzing article corpus"):
        file_path = os.path.join(corpus_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                if filename.startswith('10.'):
                    doi = filename.replace('_', '/').strip('.txt')
                    metadata = get_metadata(doi)
                    if metadata is not None:
                        year = extract_year(metadata)
                        articles.append({
                            'doi': doi,
                            'text': text,
                            'year': year,
                            'title': metadata['title'][0],
                            'author': extract_author(metadata)
                        })
                elif (metadata := extract_metadata_from_filename(filename)) is not None:
                    author, year, title = metadata
                    articles.append({
                        'doi': None,
                        'text': text,
                        'year': year,
                        'title': title,
                        'author': author
                    })
    return pd.DataFrame(articles).sort_values(by='year')