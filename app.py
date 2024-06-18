from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

notes = []

@app.route('/')
def index():
    load_notes()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    note_text = request.form['note_text']
    note_color = request.form['note_color']
    
    if note_text != '':
        notes.append({'text': note_text, 'color': note_color})
        save_notes()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if 0 <= note_id < len(notes):
        del notes[note_id]
        save_notes()
    return redirect(url_for('index'))

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'POST':
        text = request.form['note_text']
        color = request.form['note_color']
        notes[note_id] = {"text": text, "color": color}
        save_notes()
        return redirect(url_for('index'))
    return render_template('edit_note.html', note=notes[note_id], note_id=note_id)

def load_notes():
    global notes
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []

def save_notes():
    with open('notes.json', 'w') as file:
        json.dump(notes, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
