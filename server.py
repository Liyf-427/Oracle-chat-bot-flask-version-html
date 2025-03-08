from flask import Flask, request,render_template, jsonify
import os

print("Template Path Exists:", os.path.exists("templates/index.html"))
app = Flask(__name__, static_folder='static', template_folder='templates')
# simple router
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', result=None)
# ico
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # get input data
    category = request.form.get('category')  # 获取下拉菜单的选择
    input_data = request.form.get('user_input')
    prd = f"Oracle has received your question in {category}: '{input_data}'"
    try:
        # processing data
        numbers = [float(x) for x in input_data.split(',')]
        prediction = sum(numbers)  # do work -later change to AI
        result = f"The prediction is: {prediction}"
    except Exception as e:
        result = f"Error: {str(e)}"
    return render_template('index.html', result=result,prd=prd, user_input=input_data)  # return result

# boot
if __name__ == '__main__':
    app.run(port=5000, debug=True)  # operate at '5000' port