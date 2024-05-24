# app.py

from aioflask import Flask, jsonify
import asyncio
from gptWork import function_one, function_two

app = Flask(__name__)

@app.route('/function_one', methods=['GET'])
async def call_function_one():
    result = await function_one()
    return jsonify({"result": result})

@app.route('/function_two', methods=['GET'])
async def call_function_two():
    result = await function_two()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)