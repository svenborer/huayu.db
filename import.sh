#!/bin/bash
if [ $(sed -n '1{/^id/p};q' csv/tbl_book.csv) ]; then
    sed -i '1d' csv/tbl_book.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_vocabulary.csv) ]; then
    sed -i '1d' csv/tbl_vocabulary.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_chapter.csv) ]; then
    sed -i '1d' csv/tbl_chapter.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_translation.csv) ]; then
    sed -i '1d' csv/tbl_translation.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_grammatical_term.csv) ]; then
    sed -i '1d' csv/tbl_grammatical_term.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_grammar.csv) ]; then
    sed -i '1d' csv/tbl_grammar.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_translation_example.csv) ]; then
    sed -i '1d' csv/tbl_translation_example.csv
fi
if [ $(sed -n '1{/^id/p};q' csv/tbl_grammar_example.csv) ]; then
    sed -i '1d' csv/tbl_grammar_example.csv
fi
sqlite3 app.db < csv/import.txt
python import_relations.py
