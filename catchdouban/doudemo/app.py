from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

"""
@app.route('/index_text')
def index_text():
    time = datetime.date.today()  # 普通变量
    name = ['张三', '李四', '王五', '赵六']  # 列表
    task = {"任务": "打扫卫生", "时间": "3小时"} # 字典
    return render_template("index_text.html", var=time, name=name, task=task)

# 表单提交
"""


@app.route('/')
def default():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/portfolio.html')
def portfolio():
    datalist = []
    con =sqlite3.connect("movie.db")
    cur = con.cursor()
    sql = "select imgsrc,title,id,otitle,link  from top250 ;"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()

    return render_template('portfolio.html', movies=datalist)


if __name__ == '__main__':
    app.run()

