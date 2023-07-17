import os
import json
import re
import sys
from google.cloud import translate_v2 as translate
from html import unescape

# Define patterns for extracting fields and detecting hidden elements
field_pattern = re.compile(r'(dimension|measure|filter|parameter):\s*\w+\s*{([^}]*)}', re.DOTALL)
hidden_pattern = re.compile(r'hidden:\s*yes', re.IGNORECASE)
label_pattern = re.compile(r'\blabel:\s*"(.+?)"', re.DOTALL)
description_pattern = re.compile(r'\bdescription:\s*"(.+?)"', re.DOTALL)
group_label_pattern = re.compile(r'\bgroup_label:\s*"(.+?)"', re.DOTALL)
group_item_label_pattern = re.compile(r'\bgroup_item_label:\s*"(.+?)"', re.DOTALL)

# Prepare an empty dictionary to store results
output = {}

# Load language mapping
with open('./looker-localization-automation/looker_google_translate_lang_mapping.json') as f:
    language_mapping = json.load(f)

if len(sys.argv) < 3:
    print("Error: You must provide the path to the LookML directory and at least one language code as arguments.")
    with open('looker_google_translate_lang_mapping.json', 'r') as f:
        lang_mapping = json.load(f)
    print("Available options are:")
    for code, details in lang_mapping.items():
        print(f"{code} ( {details['name']})")
    sys.exit()

# Define target languages and LookML directory from the user input. The first argument (index 0) is the script name itself.
lookml_root_folder = sys.argv[1]
user_languages = sys.argv[2:]

# Always add English to the user languages
if 'en' not in user_languages:
    user_languages.append('en')

# Validate user input
for lang in user_languages:
    if lang not in language_mapping:
        print(f"Language code {lang} is not supported. Please choose from the following options:")
        for code, details in language_mapping.items():
            print(f"{code} ( {details['name']})")
        exit(1)

# Create the Translate client using the key dictionary
translate_client = translate.Client()

# Walk through each file in the specified directory and its subdirectories recursively
for root, dirs, files in os.walk(lookml_root_folder):
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
                        group_label_match = group_label_pattern.search(field_content)
                        group_item_label_match = group_item_label_pattern.search(field_content)
                        if label_match:
                            label = label_match.group(1)
                            output[label] = label
                        if description_match:
                            description = description_match.group(1)
                            output[description] = description
                        if group_label_match:
                            group_label = group_label_match.group(1)
                            output[group_label] = group_label
                        if group_item_label_match:
                            group_item_label = group_item_label_match.group(1)
                            output[group_item_label] = group_item_label

# Translate and save results for each language
for user_language in user_languages:
    google_language = language_mapping[user_language]['google_translate_code']
    output_translated = {}
    for key, value in output.items():
        if google_language == 'en':
            output_translated[key] = value
        else:
            # Translate text using Google Cloud Translate API
            translation = translate_client.translate(value, target_language=google_language)['translatedText']
            # Unescape HTML characters
            translation = unescape(translation)
            output_translated[key] = translation

    # Save results to '{language}.string.json' in the specified directory
    with open(os.path.join(lookml_root_folder, f'{user_language}.strings.json'), 'w', encoding='utf-8') as f:
        json.dump(output_translated, f, ensure_ascii=False, indent=2)
