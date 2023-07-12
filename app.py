from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.app_context().push()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Article%r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create',methods=['POST','GET'])
def create():
    if  request.method=="POST":
        title=request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article=Article(title=title,intro=intro,text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create.html')


@app.route('/posts')
def posts():
    post=Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html',post=post)


@app.route('/posts/<int:id>')
def posts_detail(id):
    post=Article.query.get(id)
    return render_template('posts_detail.html',post=post)

@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    post=Article.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении ошибки произошла ошибка'


@app.route('/posts/<int:id>/update',methods=['POST','GET'])
def post_update(id):
    post = Article.query.get(id)
    if  request.method=="POST":
        post.title=request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:

            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:

        return render_template('post_update.html',post=post)


if __name__=='__main__':
    app.run(debug=True)