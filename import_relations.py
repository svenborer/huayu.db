from app import app, db
from app.models import asoc_translation_example, asoc_grammar_example
import csv

with open('csv/tbl_translation_example_asoc.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            pass
        else:
            translation_id = row[0]
            example_id = row[1]
            s = asoc_translation_example.insert().values(translation_id=translation_id, example_id=example_id)
            db.session.execute(s)
            line_count += 1
    db.session.commit()
    print('Processed {} lines.'.format(line_count))

with open('csv/tbl_grammar_example_asoc.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            pass
        else:
            grammar_id = row[0]
            example_id = row[1]
            s = asoc_grammar_example.insert().values(grammar_id=grammar_id, example_id=example_id)
            db.session.execute(s)
            line_count += 1
    db.session.commit()
    print('Processed {} lines.'.format(line_count))