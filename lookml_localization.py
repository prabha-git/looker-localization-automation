import os
import json
import re
from google.cloud import translate_v2 as translate
from html import unescape

# Define patterns for extracting fields and detecting hidden elements
field_pattern = re.compile(r'(dimension|measure|filter|parameter):\s*\w+\s*{([^}]*)}', re.DOTALL)
hidden_pattern = re.compile(r'hidden:\s*yes', re.IGNORECASE)
label_pattern = re.compile(r'\blabel:\s*"(.+?)"', re.DOTALL)
description_pattern = re.compile(r'\bdescription:\s*"(.+?)"', re.DOTALL)

# Prepare an empty dictionary to store results
output = {}

# Define target languages
languages = ['en', 'es']

# Instantiate Google Cloud Translate API Client
translate_client = translate.Client()

# Walk through each file in the current directory and its subdirectories recursively
for root, dirs, files in os.walk("."):
    for file in files:
        # Only consider .view.lkml files
        if file.endswith(".view.lkml"):
            with open(os.path.join(root, file), 'r') as f:
                content = f.read()
                fields = field_pattern.findall(content)
                for field_type, field_content in fields:
                    # Ignore hidden elements
                    if not hidden_pattern.search(field_content):
                        label_match = label_pattern.search(field_content)
                        description_match = description_pattern.search(field_content)
                        if label_match:
                            label = label_match.group(1)
                            output[label] = label
                        if description_match:
                            description = description_match.group(1)
                            output[description] = description

# Translate and save results for each language
for language in languages:
    # Load existing translations if file exists
    filename = f'{language}_strings.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            output_translated = json.load(f)
    else:
        output_translated = {}

    # Update with new translations
    for key, value in output.items():
        # Only translate and add new entries
        if key not in output_translated:
            if language == 'en':
                output_translated[key] = value
            else:
                # Translate text using Google Cloud Translate API
                translation = translate_client.translate(value, target_language=language)['translatedText']
                # Unescape HTML characters
                translation = unescape(translation)
                output_translated[key] = translation

    # Save results to '{language}.strings.json' in the root directory
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_translated, f, ensure_ascii=False, indent=2)
