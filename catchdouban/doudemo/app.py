from flask import Flask, render_template
import sqlite3

app = Flask(__name__)



def  connectdb(sql):
    datalist = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return datalist




@app.route('/')
def default():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/portfolio.html')
def portfolio():
    sql = "select imgsrc,title,id,otitle,link  from top250 ;"
    datalist = connectdb(sql)
    return render_template('portfolio.html', movies=datalist)

@app.route('/about.html')
def about():
    sql = "select *  from top250 ;"
    datalist = connectdb(sql)
    return render_template('about.html', movies=datalist)

@app.route('/resume.html')
def resume():
    sql = "select  rating,count(rating)  from top250  group by   rating;"
    datalist = connectdb(sql)
    rating = []
    rating_count = []
    for row in datalist:
        rating.append(row[0])
        rating_count.append(row[1])
    return render_template('resume.html', rating=rating, rating_count=rating_count)

@app.route('/contact.html')
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run()

