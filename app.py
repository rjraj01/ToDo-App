from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    


@app.route("/" , methods=['GET', 'POST'])
def hello_world():

    if request.method=="POST":
        title= request.form['title']
        desc= request.form['desc']

        todo= ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=ToDo.query.all()
    print(allTodo)
    return render_template("index.html", allTodo=allTodo)



@app.route("/update/<int:sno>", methods= ['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        to_upd=ToDo.query.filter_by(sno=sno).first()
        to_upd.title=title
        to_upd.desc=desc
        db.session.add(to_upd)
        db.session.commit()
        return redirect("/")

    to_upd=ToDo.query.filter_by(sno=sno).first()    
    return render_template("update.html", to_upd=to_upd)


@app.route("/delete/<int:sno>")
def delete(sno):
    to_del=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(to_del)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)