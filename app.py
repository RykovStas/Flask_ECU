from flask import Flask, jsonify
import json
import sqlite3
import codecs

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Data")
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        data = []
        for row in rows:
            item = dict(zip(columns, row))
            data.append(item)

        cursor.close()
        conn.close()

        with codecs.open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return "Файл data.json створений успішно."
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_data():
    with codecs.open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


@app.route('/get_data/<string:date>', methods=['GET'])
def get_data_by_date(date):
    data = load_data()
    filtered_data = [item for item in data if 'Дата' in item and item['Дата'].replace(".", "-") == date]

    if filtered_data:
        return json.dumps(filtered_data, ensure_ascii=False, indent=4), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return json.dumps({'error': 'Data not found for the given date.'}), 404


if __name__ == '__main__':
    app.run()
