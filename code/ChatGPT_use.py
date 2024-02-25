# Script calling GPT, using the previously constructed prompts for translating the IDION dataset,
# and saving the outputs to both a .txt and a .pkl file

from openai import OpenAI
import sys
import pickle

client = OpenAI(api_key="<key>")    # add your API key here

conditioned = True  # set to True for "aided" translation, False otherwise

# Open the list with the relevant data, including prompts, as generated in "parse_idion.py"
with open('../data/idion_for_aided_en_trans.pkl', 'rb') as file:
    idion_for_aided_en_trans = pickle.load(file)

# Reroute output to the relevant text file
if conditioned:
    output = open('../data/GPT_IDION_translations_conditioned.txt', 'w', encoding="utf-8")
else:
    output = open('../data/GPT_IDION_translations_unconditioned.txt', 'w', encoding="utf-8")
sys.stdout = output

# Add the GPT outputs to the list of data
results = []

# For every MWE
for mwe in idion_for_aided_en_trans:
    # Save all GPT responses
    responses = []
    # For every prompt associated with the MWE
    for sentence in mwe['trans_prompts']:
        # Add the MWE definition to the prompt, if doing "aided" translation
        if conditioned:
            prompt = sentence + ' ' + mwe['cont_prompt']
        # Otherwise don't
        else:
            prompt = sentence
        # Print the prompt
        print("\nPrompt:")
        print(prompt)
        print("Answer:")
        # Send the prompt to the model
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        # Save the response
        response = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        # Print the response
        print(response)
        # Add the response to the list of responses for the sentences associated with this MWE
        responses.append(response)
    # Add the GPT outputs to the list of data associated with this MWE
    mwe['responses'] = responses
    # Add the updated MWE data to a new list
    results.append(mwe)

# Close the output
output.close()

# Save the data to the relevant .pkl file
if conditioned:
    output_pkl = '../data/GPT_IDION_translations_conditioned.pkl'
else:
    output_pkl = '../data/GPT_IDION_translations_unconditioned.pkl'

with open(output_pkl, 'wb') as file:
    pickle.dump(idion_for_aided_en_trans, file)