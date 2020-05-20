from flask import Flask,render_template
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    time = datetime.date.today()  # 普通变量
    name = ['张三', '李四', '王五', '赵六']  # 列表
    task = {"任务": "打扫卫生", "时间": "3小时"} # 字典
    return render_template("index.html", var=time, name=name, task=task)

# 表单提交

if __name__ == '__main__':
    app.run()
