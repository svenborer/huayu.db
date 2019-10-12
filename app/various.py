unique_chars = []
totalNewChars = {}
cTotal = 0

chapter_list = [c.id for c in Chapter.query.all()]

for c in chapter_list:
    vocab_list = [v.hanzi for v in Vocabulary.query.filter(Vocabulary.chapter_id == c).all()]
    totalNewChars[c] = []
    for v in vocab_list:
        for index in range(len(v)):
            if v[index] not in unique_chars:
                unique_chars.append(v[index])
                cTotal += 1
    totalNewChars[c] = cTotal

totalNewChars