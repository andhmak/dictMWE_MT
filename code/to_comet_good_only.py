# Script printing "aided" translations ranked as excellent by human evaluators, as well as the equivalent source sentences and the
# translations of the other models ("unaided" and NLLB) in a format usable by COMET

import pickle
import sys
import pandas as pd

# Open the .csv with the source sentences and the NLLB translations
with open('../data/NLLB_IDION_translations.pkl', 'rb') as file:
    NLLB_IDION_translations = pickle.load(file)

# Open the .pkl with the source sentences translated well by "aided"
with open('../data/goods_el.pkl', 'rb') as file:
    goods_greek = set(pickle.load(file))

# Print relevant NLLB translations into the relevant file (removing possible duplicates)
old = set()
with open('../data/NLLB_for_COMET_good.en', 'w', encoding="utf-8") as sys.stdout:
    for mwe in NLLB_IDION_translations:
        for i, sentence in enumerate(mwe['trans_prompts']):
            if (sentence[34:-15] in old) or (sentence[34:-15] not in goods_greek):
                continue
            else:
                old.add(sentence[34:-15])
                print(mwe['responses'][i])

# Print well-translated source sentences into the relevant file (removing possible duplicates)
old = set()
with open('../data/source_for_COMET_good.el', 'w', encoding="utf-8") as sys.stdout:
    for mwe in NLLB_IDION_translations:
        for i, sentence in enumerate(mwe['trans_prompts']):
            if (sentence[34:-15] in old) or (sentence[34:-15] not in goods_greek):
                continue
            else:
                old.add(sentence[34:-15])
                print(" ".join(sentence[34:-15].splitlines()))
            
# Open the .csv with the source sentences and the NLLB translations
IDION_df = pd.read_csv('../data/GPT_IDION_translations.csv', sep=',', encoding='utf-8').values.tolist()

# Print good "aided" GPT translations into the relevant file
with open('../data/GPT_aided_for_COMET_good.en', 'w', encoding="utf-8") as sys.stdout:
    for instance in IDION_df:
        if instance[2] in goods_greek:
            print(" ".join(instance[3].splitlines()))

# Print relevant "unaided" GPT translations into the relevant file
with open('../data/GPT_unaided_for_COMET_good.en', 'w', encoding="utf-8") as sys.stdout:
    for instance in IDION_df:
        if instance[2] in goods_greek:
            print(" ".join(instance[4].splitlines()))
