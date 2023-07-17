# LookML Localization Automation

This open-source code simplifies the localization of your LookML model files. The script parses through LookML files, extracts all user-facing strings (such as labels, descriptions, group_label, and group_item_label), and translates them using the Google Cloud Translate API. The translated strings are stored in a separate JSON file for each target language.

## Repository Structure

```plaintext
.
├── LICENSE
├── README.md
├── looker_google_translate_lang_mapping.json
├── lookml_localization.py
└── requirements.txt
```

## How to Use

Follow the steps below to use this tool:

1. Clone this repository to your local machine.
2. Clone the Looker Project to your local machine.
3. Set the 'GOOGLE_APPLICATION_CREDENTIALS' environment variable to point to your Google Cloud Service account key file. The service account should have the 'Cloud Translation API User' permission.

Use the following command to clone this repository:

```bash
git clone https://github.com/prabha-git/looker-localization-automation.git
```

Use the following command to clone your Looker Project:

```bash 
git clone <<your looker git repo url>>
```

To run the localization automation script, you must have Python installed on your machine along with the packages listed in the `requirements.txt` file. Install the requirements using the following command:

```bash
pip install -r looker-localization-automation/requirements.txt
```

Once the requirements are installed, execute the script from the command line. The directory path should be the first argument, followed by language codes. For example, to translate to French (fr_FR) and Spanish (es_ES), run:

```bash
python looker-localization-automation/lookml_localization.py /your_path_to_looker_project fr_FR es_ES
```

The script leverages the `looker_google_translate_lang_mapping.json` file to map language codes to their Google Translate counterparts. To add another language, simply update this file, adhering to the existing format.

Upon completion, the script will create localization files in the LookML root folder, denoted by the extension '.strings.json'.

Be sure to include the following snippet in the manifest.lkml file to incorporate the localization files into the project:

```bash
localization_settings: {
  default_locale: en
  localization_level: permissive
}
```

Finally, commit the localization files to your Looker Project and push to the remote repository.

## Supported Languages

The `looker_google_translate_lang_mapping.json` file currently includes the following languages:

| Language              | Locale Code and Strings Filename |
|-----------------------|----------------------------------|
| English               | en                               |
| Czech                 | cs_CZ                            |
| German                | de_DE                            |
| Spanish               | es_ES                            |
| French                | fr_FR                            |
| Hindi                 | hi_IN                            |
| Italian               | it_IT                            |
| Japanese              | ja_JP                            |
| Korean                | ko_KR                            |
| Lithuanian            | lt_LT                            |
| Norwegian (Bokmål)    | nb_NO                            |
| Dutch                 | nl_NL                            |
| Polish                | pl_PL                            |
| Brazilian Portuguese  | pt_BR                            |
| Portuguese            | pt_PT                            |
| Russian               | ru_RU                            |
| Swedish               | sv_SE                            |
| Thai                  | th_TH                            |
| Turkish               | tr_TR                            |
| Ukrainian             | uk_UA                            |
| Simplified Chinese    | zh_CN                            |
| Traditional Chinese   | zh_TW                            |

Please note that for languages with variants like Chinese (with zh_CN and zh_TW for Simplified and Traditional Chinese respectively), Google Translate only supports a single code (zh). Therefore, the same translation will be used for both variants.

## License

This project is licensed under the terms specified in the LICENSE file.