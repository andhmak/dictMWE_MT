# Script parsing the IDION dataset, extracting the relevant data, constructing the GPT prompts and saving them to a .pkl file

import json
import pickle

# Open the dataset
idion_el_path = "../data/idion_el.json"

with open(idion_el_path, 'r') as j:
    idion_el = json.loads(j.read())

data = idion_el["result"]["data"]

# Create a list with all the sentences, the equivalent MWEs and the prompts
idion_for_aided_en_trans = []

# For every MWE
for index_to_open in range(len(data)):
    # Get all the relevant translations
    translations = []
    # For every definition of the MWE
    for definition in data[index_to_open]["definitions"]:
        # For every translation of the definition
        for translation in definition['idion_definition_translations']:
            # If the translation is in English
            if translation['language']['value'] == 'English':
                # Add the translation along with any comments
                if translation['definition_comment'] != None:
                    if translation['definition_comment'][0] != '(':
                        translations.append(translation['translation'] + ' (' + translation['definition_comment'] + ')')
                    else:
                        translations.append(translation['translation'] + ' ' + translation['definition_comment'])
                else:
                    translations.append(translation['translation'])
    # If there are no translations, skip
    if len(translations) == 0:
        continue
    # Create the part of the prompt providing the MWE translation to the model
    cont_prompt = 'For context, the Greek multi-word expression "' + '" or "'.join(data[index_to_open]["variants"]) +\
          '" can mean "'+ '" or "'.join(translations) + '".'
    
    # Get all the relevant example sentences
    examples = []
    # For every sentence with the MWE
    for diag in data[index_to_open]['diag']:
        for example in diag['examples']:
            # Save it if it is grammatical
            if example['acceptable'] in ['yes', 'acceptable']:
                examples.append(example['entry'])
    # If there are no sentences, skip
    if len(examples) == 0:
        continue
    # Create the prompts requesting a translation, without any extra context
    trans_prompts = ['Can you translate the Greek text "' + example + '" into English?' for example in examples]

    # Create an entry with all the data for this MWE
    new_dict = {}
    new_dict['id'] = index_to_open
    new_dict['translations'] = translations
    new_dict['cont_prompt'] = cont_prompt
    new_dict['examples'] = examples
    new_dict['trans_prompts'] = trans_prompts

    # Add the entry to the list
    idion_for_aided_en_trans.append(new_dict)

# Save the list as a .pkl file
with open('../data/idion_for_aided_en_trans.pkl', 'wb') as file:
    pickle.dump(idion_for_aided_en_trans, file) 