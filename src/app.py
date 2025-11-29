from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

def validate_post_data(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if not data.get('name') or not isinstance(data['name'], str):
        return False
    if data.get('age') and not isinstance(data['age'], int):
        return False
    return True

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return str(a + b)

@app.route('/calculator', methods=['GET'])
def calculator():
    """
    HTML калькулятор
    """
    html_form = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Калькулятор</title>
    </head>
    <body>
        <div class="calculator">
            <h1>Калькулятор</h1>
            <form id="calcForm">
                <div class="input-group">
                    <label for="a">Первое число:</label>
                    <input type="number" id="a" name="a" step="any" required>
                </div>
                
                <div class="input-group">
                    <label for="operation">Операция:</label>
                    <select id="operation" name="operation" required>
                        <option value="add">Сложение (+)</option>
                        <option value="subtract">Вычитание (-)</option>
                        <option value="multiply">Умножение (×)</option>
                        <option value="divide">Деление (÷)</option>
                    </select>
                </div>
                
                <div class="input-group">
                    <label for="b">Второе число:</label>
                    <input type="number" id="b" name="b" step="any" required>
                </div>
                
                <button type="submit">Вычислить</button>
            </form>
            
            <div id="result"></div>
        </div>

        <script>
            document.getElementById('calcForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const a = document.getElementById('a').value;
                const b = document.getElementById('b').value;
                const operation = document.getElementById('operation').value;
                const resultDiv = document.getElementById('result');
                
                // Создаем URL для соответствующего маршрута
                let url = '';
                switch(operation) {
                    case 'add':
                        url = `/add?a=${a}&b=${b}`;
                        break;
                    case 'subtract':
                        url = `/subtract?a=${a}&b=${b}`;
                        break;
                    case 'multiply':
                        url = `/multiply?a=${a}&b=${b}`;
                        break;
                    case 'divide':
                        url = `/divide?a=${a}&b=${b}`;
                        break;
                }
                
                // Выполняем запрос
                fetch(url)
                    .then(response => response.text())
                    .then(data => {
                        resultDiv.innerHTML = `<div class="result">Результат: ${data}</div>`;
                    })
                    .catch(error => {
                        resultDiv.innerHTML = `<div class="error">Ошибка: ${error}</div>`;
                    });
            });
        </script>
    </body>
    </html>
    '''
    return html_form

@app.route('/subtract', methods=['GET'])
def subtract():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return str(a - b)

@app.route('/multiply', methods=['GET'])
def multiply():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return str(a * b)

@app.route('/divide', methods=['GET'])
def divide():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    if b == 0:
        return 'Ошибка: деление на ноль!'
    return str(a / b)

@app.route('/api', methods=['GET', 'POST'])
def api():
    """
    /api entpoint
    GET - returns json= {'status': 'test'}
    POST -  {
            name - str not null
            age - int optional
            }
    :return:
    """
    if request.method == 'GET':
        return jsonify({'status': 'test'})
    elif request.method == 'POST':
        if validate_post_data(request.json):
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': 'bad input'}), 400

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()