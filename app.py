from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 使用 Render PostgreSQL DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')  # Render 會自動提供 DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 留言資料表
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.Text)

# 首頁顯示留言板
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        if name and message:
            new_comment = Comment(name=name, message=message)
            db.session.add(new_comment)
            db.session.commit()
        return redirect('/')
    comments = Comment.query.all()
    return render_template('index.html', comments=comments)

# 後端刪除留言（前端隱藏）
@app.route('/delete/<int:comment_id>', methods=['POST'])
def delete(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return '', 204

if __name__ == '__main__':
    # 建立資料表
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
