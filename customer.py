from flask import Flask, render_template, request, session
from flask_session import Session
import os
import diy as d

print("Template Path Exists:", os.path.exists("templates/index.html"))
app = Flask(__name__, static_folder='static', template_folder='templates')

# 配置 Flask Session
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统存储会话数据
app.config['SECRET_KEY'] = 'supersecretkey'  # 用于安全加密会话数据
app.config['SESSION_FILE_DIR'] = './flask_session/'  # 存储会话文件的目录
app.config['SESSION_COOKIE_NAME'] = 'session'  # 显式设置 cookie 名称
Session(app)
# simple router
@app.route('/', methods=['GET', 'POST'])
def home():
    session['chat_history'] = []
    return render_template('idx.html')
# ico
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    category = request.form.get('category')  # 获取下拉菜单选择
    input_data = request.form.get('user_input')  # 获取用户输入
    prd = f"Oracle has received your question in {category}: '{input_data}'"
    try:
        # processing data
        #numbers = [float(x) for x in input_data.split(',')]
        prediction = d.main(category,input_data)  # do work -later change to AI
        result = d.print_result(category,input_data,prediction)
    except Exception as e:
        result = f"Error: {str(e)}"

    # 更新聊天记录
    session['chat_history'].append({'type': 'user', 'text': input_data})
    session['chat_history'].append({'type': 'server', 'text': prd})
    session['chat_history'].append({'type': 'oracle', 'text': result})
    session.modified = True  # 标记 session 已修

    return render_template('idx.html', chat_history=session['chat_history'])

# boot
if __name__ == '__main__':
    app.run(port=5000, debug=True)  # operate at '5000' port




