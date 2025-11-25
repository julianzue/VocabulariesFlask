from flask import Flask, render_template, request, redirect, url_for
import time
import json
import os


app = Flask(__name__)


@app.route('/')
def home():

    languages = []

    for entry in os.scandir('static/languages/'):
        languages.append(entry.name.split(".")[0])

    return render_template('home.html', languages=languages)


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        language = request.form.get('language')

        with open(f'static/languages/{language}.json', 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/language/<language>', methods=['GET', 'POST'])
def language(language):

    if request.method == 'POST':

        filtered_vocabularies = []

        query = request.form.get('query').lower()

        with open(f'static/languages/{language}.json', 'r', encoding='utf-8') as f:
            vocabularies = json.load(f)

        for voc in vocabularies:
            if query in voc['word'].lower() or query in voc["pronounciation"].lower() or query in voc['translation'].lower():
                filtered_vocabularies.append(voc)

        for i in range(len(filtered_vocabularies)):
            filtered_vocabularies[i]['count'] = "{0:03d}".format(i + 1)

        return render_template('language.html', language=language, vocabularies=filtered_vocabularies, count=len(filtered_vocabularies), query=query)

    with open(f'static/languages/{language}.json', 'r', encoding='utf-8') as f:
        vocabularies = json.load(f)

    count = len(vocabularies)

    for i in range(count):
        vocabularies[i]['count'] = "{0:03d}".format(i + 1)

    return render_template('language.html', language=language, vocabularies=vocabularies, count=count)


@app.route('/language/<language>/add', methods=['GET', 'POST'])
def vocab_add(language):

    if request.method == 'POST':
        word = request.form.get('word')
        translation = request.form.get('translation')
        pronounciation = request.form.get('pronounciation')
        date = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(f'static/languages/{language}.json', 'r', encoding='utf-8') as f:
            vocabularies = json.load(f)

        vocabularies.append({
            'date': date,
            'word': word,
            'translation': translation,
            'pronounciation': pronounciation
        })

        with open(f'static/languages/{language}.json', 'w', encoding='utf-8') as f:
            json.dump(vocabularies, f, indent=4)

        return redirect(url_for('language', language=language))

    return render_template('add-vocab.html', language=language)


if __name__ == '__main__':
    app.run(debug=True)