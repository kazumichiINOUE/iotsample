from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# 初期状態の行データ（IDごとに空データを設定）
rows = {i: f"None" for i in range(1, 26)}  # 1〜25行の例

# HTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        .grid-item {
            padding: 20px;
            border: 1px solid #ddd;
            text-align: center;
            background-color: #f4f4f4;
            border-radius: 5px;
        }
        h1 {
            text-align: center;
        }
    </style>
    <script>
        // データを更新する関数
        function updateData(id, value) {
            const item = document.getElementById('item-' + id);
            item.innerHTML = "<strong>ID: " + id + "</strong><br>" + "Value: " + value;
        }

        // データを定期的に取得して更新する
        function fetchData() {
            fetch("/data")
            .then(response => response.json())
            .then(data => {
                data.rows.forEach(item => {
                    updateData(item.id, item.value);
                });
            })
            .catch(error => console.error("Error fetching data:", error));
        }

        // 初期のデータ取得
        window.onload = fetchData;

        // 5秒ごとにデータを更新
        setInterval(fetchData, 1000);
    </script>
</head>
<body>
    <h1>Data Grid</h1>
    <div class="grid-container">
        {% for id, content in rows.items() %}
            <div class="grid-item" id="item-{{ id }}">
                <strong>ID: {{ id }}</strong><br>
                {{ content }}  <!-- 'Value: ' を削除し、純粋な値のみ表示 -->
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # データをブラウザに表示
    return render_template_string(HTML_TEMPLATE, rows=rows)

@app.route("/send", methods=["POST"])
def receive_message():
    global rows
    # メッセージを受信
    message = request.form.get("message")
    if message:
        try:
            # IDと数値を分解
            id_str, value = message.split(",")
            id = int(id_str)

            # 行番号が範囲内であれば更新
            if id in rows:
                rows[id] = value  # 値をそのまま設定
                # 更新したIDと値をJSON形式で返す
                return jsonify({"success": True, "id": id, "value": value})
            else:
                return jsonify({"success": False, "error": f"Error: ID {id} is out of range."}), 400
        except ValueError:
            return jsonify({"success": False, "error": "Error: Invalid message format."}), 400

    return jsonify({"success": False, "error": "Error: No message received."}), 400

@app.route("/data")
def get_data():
    # 現在のデータをJSON形式で返す
    rows_data = [{"id": id, "value": value} for id, value in rows.items()]
    return jsonify({"rows": rows_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
