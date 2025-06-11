from flask import Flask, render_template_string, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

history = []

def is_valid_input(string):
    pattern = r'^[a-zA-Z0-9]*$'
    return re.match(pattern, string) is not None

def is_palindrome(string):
    clean_string = string.lower()
    return clean_string == clean_string[::-1]

def analyze_string(string):
    letters = sum(1 for c in string if c.isalpha())
    digits = sum(1 for c in string if c.isdigit())
    length = len(string)
    reversed_str = string[::-1]
    
    return {
        'length': length,
        'letters': letters,
        'digits': digits,
        'reversed': reversed_str
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Palindrome Checker - Flask</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .content {
            padding: 40px;
        }
        
        .input-group {
            margin-bottom: 30px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1rem;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1.1rem;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        button {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-primary {
            background: #27ae60;
            color: white;
        }
        
        .btn-secondary {
            background: #95a5a6;
            color: white;
        }
        
        .result {
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
        }
        
        .result.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .result.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .analysis {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .analysis h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #3498db;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 5px;
        }
        
        .history {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .history h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .history-item {
            padding: 10px;
            background: white;
            margin-bottom: 10px;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .history-string {
            font-family: monospace;
            font-weight: bold;
        }
        
        .history-status {
            font-weight: bold;
        }
        
        .history-status.palindrome {
            color: #27ae60;
        }
        
        .history-status.not-palindrome {
            color: #e74c3c;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 PALINDROME CHECKER</h1>
            <p>Praktikum Otomata - Pengenalan String Palindrom</p>
        </div>
        
        <div class="content">
            <form id="palindromeForm">
                <div class="input-group">
                    <label for="inputString">Masukkan String (Huruf + Angka):</label>
                    <input type="text" id="inputString" name="inputString" placeholder="Contoh: racecar, 12321, a1b2b1a..." required>
                </div>
                
                <div class="button-group">
                    <button type="submit" class="btn-primary">✅ CEK PALINDROM</button>
                    <button type="button" class="btn-secondary" onclick="clearForm()">🗑️ CLEAR</button>
                </div>
            </form>
            
            <div id="result" class="hidden"></div>
            <div id="analysis" class="hidden"></div>
            <div id="history" class="hidden"></div>
        </div>
    </div>

    <script>
        document.getElementById('palindromeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            checkPalindrome();
        });

        async function checkPalindrome() {
            const inputString = document.getElementById('inputString').value.trim();
            
            if (!inputString) {
                alert('Silakan masukkan string terlebih dahulu!');
                return;
            }

            try {
                const response = await fetch('/check', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ string: inputString })
                });

                const data = await response.json();
                
                if (data.error) {
                    showResult(data.error, false);
                    return;
                }

                showResult(data.message, data.is_palindrome);
                showAnalysis(data.analysis);
                updateHistory(data.history);
                
            } catch (error) {
                alert('Terjadi kesalahan: ' + error.message);
            }
        }

        function showResult(message, isPalindrome) {
            const resultDiv = document.getElementById('result');
            resultDiv.className = isPalindrome ? 'result success' : 'result error';
            resultDiv.textContent = message;
            resultDiv.classList.remove('hidden');
        }

        function showAnalysis(analysis) {
            const analysisDiv = document.getElementById('analysis');
            analysisDiv.innerHTML = `
                <h3>📊 Analisis String:</h3>
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">${analysis.length}</div>
                        <div class="stat-label">Panjang</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${analysis.letters}</div>
                        <div class="stat-label">Huruf</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${analysis.digits}</div>
                        <div class="stat-label">Angka</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${analysis.reversed}</div>
                        <div class="stat-label">Terbalik</div>
                    </div>
                </div>
            `;
            analysisDiv.classList.remove('hidden');
        }

        function updateHistory(historyData) {
            const historyDiv = document.getElementById('history');
            
            if (historyData.length === 0) {
                historyDiv.classList.add('hidden');
                return;
            }

            let historyHTML = '<h3>📈 Riwayat Pengecekan:</h3>';
            historyData.slice(-10).reverse().forEach(item => {
                const statusClass = item.is_palindrome ? 'palindrome' : 'not-palindrome';
                const icon = item.is_palindrome ? '✅' : '❌';
                historyHTML += `
                    <div class="history-item">
                        <span class="history-string">${item.string}</span>
                        <span class="history-status ${statusClass}">${icon} ${item.status}</span>
                    </div>
                `;
            });
            
            historyDiv.innerHTML = historyHTML;
            historyDiv.classList.remove('hidden');
        }

        function clearForm() {
            document.getElementById('inputString').value = '';
            document.getElementById('result').classList.add('hidden');
            document.getElementById('analysis').classList.add('hidden');
            document.getElementById('inputString').focus();
        }

        document.getElementById('inputString').focus();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check_palindrome():
    global history
    
    data = request.json
    input_string = data.get('string', '').strip()
    
    if not input_string:
        return jsonify({'error': 'Input tidak boleh kosong!'})
    
    if not is_valid_input(input_string):
        return jsonify({'error': 'Input hanya boleh berisi huruf dan angka!'})
    
    palindrome_result = is_palindrome(input_string)
    analysis = analyze_string(input_string)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    status = "PALINDROM" if palindrome_result else "BUKAN PALINDROM"
    
    history_entry = {
        'string': input_string,
        'is_palindrome': palindrome_result,
        'status': status,
        'timestamp': timestamp
    }
    
    history.append(history_entry)
    
    if palindrome_result:
        message = f"✓ '{input_string}' ADALAH PALINDROM"
    else:
        message = f"✗ '{input_string}' BUKAN PALINDROM"
    
    return jsonify({
        'message': message,
        'is_palindrome': palindrome_result,
        'analysis': analysis,
        'history': history
    })

if __name__ == '__main__':
    print("Starting Palindrome Checker Flask App...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)