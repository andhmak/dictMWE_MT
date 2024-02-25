# Script using NLLB to translate the sentences from the IDION dataset, saving the results to a .pkl file

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pickle

# Open the list with the relevant data, as generated in "parse_idion.py"
with open('../data/idion_for_aided_en_trans.pkl', 'rb') as file:
    idion_for_aided_en_trans = pickle.load(file)

# Load the model
tokenizer = AutoTokenizer.from_pretrained(
    "facebook/nllb-200-distilled-600M", token=False, src_lang="ell_Latn"
) 

model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", token=False)

# Get the results
results = []

# For every MWE
for mwe in idion_for_aided_en_trans:
    # Save all NLLB responses
    responses = []
    # For every prompt associated with the MWE
    for sentence in mwe['trans_prompts']:
        # Keep only the source sentence
        prompt = sentence[34:-15]
        print(prompt)

        # Give it to the model to translate
        inputs = tokenizer(prompt, return_tensors="pt")

        translated_tokens = model.generate(
            **inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"], max_length=30
        )

        # Save the response
        response = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

        # Add the response to the list of responses for the sentences associated with this MWE
        responses.append(response)

    # Add the NLLB outputs to the list of data associated with this MWE
    mwe['responses'] = responses
    # Add the updated MWE data to a new list
    results.append(mwe)

# Save the data to the relevant .pkl file
with open("../data/NLLB_IDION_translations.pkl", 'wb') as file:
    pickle.dump(results, file)