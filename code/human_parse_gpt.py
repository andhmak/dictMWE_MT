# Script parsing the human-generated annotations comparing "aided" and "unaided" GPT translations, printing the relevant statistics,
# while also saving the "aided" translations given 5 stars by the human annotators in a .pkl

import json
import pickle
 
# Open the file with the annotations
f = open('../data/aided_unaided_annotations.json', encoding="utf8")

data = json.load(f)

f.close()

# Statistics
unaided_per = 0     # amount of correctly translated MWEs by "unaided"
aided_per = 0       # amount of correctly translated MWEs by "aided"
total_per = 0       # total amount for division
leftright = 0       # amount of "unaided" chosen as better
leftright_total = 0 # total amount for division
unaided = []        # scores given to "aided"
aided = []          # scores given to "unaided"
goods = []          # source sentences translated excellently by "aided"

# For every sentence
for i in data:
    with_ann_val = False    # whether translation has been rated as a whole
    with_ann_comp = False   # whether translation of MWE has been rated
    # for all annotations
    for j in i['annotations']:
        # for every field annotated
        for k in j['result']:
            # if it's choice of better translation
            if "selected" in k['value']:
                leftright_total += 1
                if k['value']['selected'] == 'left':
                    pass
                elif k['value']['selected'] == 'right':
                    leftright += 1
                else:
                    print("Should never be printed")
            # if it's total translation score
            elif "rating" in k['value']:
                if k['from_name'] == 'quality1':
                    unaided.append(k['value']['rating'])
                elif k['from_name'] == 'quality2':
                    aided.append(k['value']['rating'])
                    # if "aided" translation good, save the source sentence
                    if (k['value']['rating'] == 5) and (i["data"]["Greek"] not in goods):
                        goods.append(i["data"]["Greek"])
                else:
                    print("Should never be printed")
                with_ann_val = True # it's been annotated
            # if it's MWE translation judgement
            elif "choices" in k['value']:
                if k['from_name'] == 'vibes3':
                    continue
                total_per += 0.5
                if k['from_name'] == 'vibes1':
                    if k['value']['choices'] == ['Yes']:
                        unaided_per += 1
                    if k['value']['choices'] == ['Somewhat']:
                        unaided_per += 0.5  # give half points if somewhat correct
                if k['from_name'] == 'vibes2':
                    if k['value']['choices'] == ['Yes']:
                        aided_per += 1
                    if k['value']['choices'] == ['Somewhat']:
                        aided_per += 0.5    # give half points if somewhat correct
                with_ann_comp = True    # it's been annotated

# Print statistics
print("Average \"aided\" quality:")
print(sum(unaided)/len(unaided), "/ 5")
print("Average \"unaided\" quality:")
print(sum(aided)/len(aided), "/ 5")
print("Percentage of correct MWEs in \"aided\":")
print(100*unaided_per/total_per, "\b%")
print("Percentage of correct MWEs in \"unaided\":")
print(100*aided_per/total_per, "\b%")
print("Percentage \"unaided\" better than \"aided\":")
print(100*leftright/leftright_total, "\b%")

# Save sentences translated excellently by "aided" into a .pkl
with open('../data/goods_el.pkl', 'wb') as file:
    pickle.dump(goods, file)