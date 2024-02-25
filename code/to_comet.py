# Script printing the source sentences, as well as the outputs of all models ("aided", "unaided" and NLLB) in a format usable by COMET

import pickle
import sys
import pandas as pd

# Open the .csv with the source sentences and the NLLB translations
with open('../data/NLLB_IDION_translations.pkl', 'rb') as file:
    NLLB_IDION_translations = pickle.load(file)

# Print all NLLB translations into the relevant file (removing possible duplicates)
old = set()
with open('../data/NLLB_for_COMET.en', 'w', encoding="utf-8") as sys.stdout:
    for mwe in NLLB_IDION_translations:
        for i, sentence in enumerate(mwe['trans_prompts']):
            if sentence[34:-15] in old:
                continue
            else:
                old.add(sentence[34:-15])
                print(mwe['responses'][i])

# Print source sentences into the relevant file (removing possible duplicates)
old = set()
with open('../data/source_for_COMET.el', 'w', encoding="utf-8") as sys.stdout:
    for mwe in NLLB_IDION_translations:
        for i, sentence in enumerate(mwe['trans_prompts']):
            if sentence[34:-15] in old:
                continue
            else:
                old.add(sentence[34:-15])
                print(" ".join(sentence[34:-15].splitlines()))
            
# Open the .csv with the GPT translations
IDION_df = pd.read_csv('../data/GPT_IDION_translations.csv', sep=',', encoding='utf-8')

# Print all "aided" GPT translations into the relevant file
with open('../data/GPT_aided_for_COMET.en', 'w', encoding="utf-8") as sys.stdout:
    for sentence in IDION_df["GPT_aided"]:
        print(" ".join(sentence.splitlines()))

# Print all "unaided" GPT translations into the relevant file
with open('../data/GPT_unaided_for_COMET.en', 'w', encoding="utf-8") as sys.stdout:
    for sentence in IDION_df["GPT_unaided"]:
        print(" ".join(sentence.splitlines()))