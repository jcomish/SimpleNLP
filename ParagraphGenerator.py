import json
import random
import math

def pick_word(dct, orig_dct, is_first=True):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        if is_first:
            total += v['freq']
        else:
            total += v
        if rand_val <= total:
            if k in orig_dct.keys():
                return (k, orig_dct[k])
            else:
                return (k, None)
    assert False, 'unreachable'

def calc_entropy():
    entropy = 0
    for key in data:
        entropy += (-1 * data[key]['freq']) * math.log(data[key]['freq'])

    print(entropy)

def calc_sum(data):
    word_sum = 0
    for key in data:
        word_sum += data[key]['freq']
    return word_sum

def calc_probabilities(data, word_sum):
    for key in data:
        # data[key] = data[key] / word_sum
        data[key]['freq'] = data[key]['freq'] / word_sum
    return data





with open('wordcount.json') as f:
    data = json.load(f)

data = calc_probabilities(data, calc_sum(data))
calc_entropy()  # Entropy: 8.139

para = []
for i in range(100):
    words = []
    for j in range(100):
        if j == 0:
            words.append(pick_word(data, data))
        elif words[j - 1][1]:
            new_word = pick_word(words[j - 1][1]['next_word'], data, False)
            if new_word[0] != words[j - 1][0] and (len(new_word[0]) > 1 or new_word[0] == 'a'):
                words.append(new_word)
            else:
                words.append(pick_word(data, data))
        else:
            break
        i += 1
    para.extend([word[0] for word in words])

        # i += 1

print(*para)
