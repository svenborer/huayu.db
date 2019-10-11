unique_chars = []
new_chars = {}
overview = {}

for c in chapter_list:
    new_chars[c] = 0
    vocab_list = [v.hanzi for v in Vocabulary.query.filter(Vocabulary.chapter_id == c).all()]
    overview[c] = []
    for v in vocab_list:
        for index in range(len(v)):
            if v[index] not in unique_chars:
                unique_chars.append(v[index])
                new_chars[c] += 1
                overview[c].append(v[index])