from flask import Flask ,render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# App Setup
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///dataase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db=SQLAlchemy(app)

#DATA CLASS
class MyTask(db.Model):
   id=db.Column(db.Integer,primary_key=True)
   content=db.Column(db.String(100),nullable=False)
   complete=db.Column(db.Integer,default=0)
   created=db.Column(db.DateTime,default=datetime.utcnow)

   def __repr__(self)-> str:
      return f"Task{self.id}"
   
with app.app_context():
      db.create_all()

# Routes
@app.route("/",methods=["POST","GET"])
def index():
#ADD TASK
  if request.method=="POST":
    current_task=request.form['content']
    new_task=MyTask(content=current_task)
    try:
       db.session.add(new_task)
       db.session.commit()
       return redirect("/")
    except Exception as e:
       print(f"Error:{e}")
       return f"Error:{e}"
    
  else:
     tasks=MyTask.query.order_by(MyTask.created).all()
     return  render_template('index.html',tasks=tasks)

#DELETE AN ITEM
@app.route("/delete/<int:id>")
def delete(id:int):
   delete_task=MyTask.query.get_or_404(id)
   try:
      db.session.delete(delete_task)
      db.session.commit()
      return redirect("/")
   except Exception as e:
      return f"Error{e}"

#UPDATE AN ITEM
@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id:int):
   task=MyTask.query.get_or_404(id)
   if request.method=="POST":
      task.content=request.form['content']
      try:
         db.session.commit()
         return redirect("/")
      except Exception as e:
         return f"Error{e}"
   else:
      return render_template('edit.html',task=task)


if __name__ == "__main__":
   
   app.run(debug=True) 