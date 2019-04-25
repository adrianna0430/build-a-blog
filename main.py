from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:NewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']= True
db= SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(120))
    body= db.Column(db.String(280))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#ALL BLOG POSTS
# @app.route('/blog')
# def index():
#     all_blog_posts = Blog.query.all()
#     return render_template('blog.html', posts=all_blog_posts)

# INDIVIDUAL BLOG POSTS
@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        individual_post = Blog.query.get(post_id)
        return render_template('single_blog.html', individual_post=individual_post)
    else:
        all_blog_posts = Blog.query.all()
        return render_template('blog.html', posts=all_blog_posts)

# EMPTY FORM
def blank_form(x):
    if x=="":
        return False
    else:
        return True

# REDIRECT AND ERROR MESSAGES (FAILURE)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':
        title_error = ""
        blog_body_error = ""

    
        post_title = request.form['blog_title']
        post_entry = request.form['blog_body']
        post_new = Blog(post_title, post_entry)

       
        if blank_form(post_title) and blank_form(post_entry): 
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not blank_form(post_title) and not blank_form(post_entry):
                title_error = "Please enter text for blog title"
                blog_body_error = "Please enter text for blog entry"
                return render_template('new_blog.html', blog_body_error=blog_body_error, title_error=title_error)
            elif not blank_form(post_title):
                title_error = "Please enter text for blog title"
                return render_template('new_blog.html', title_error=title_error, post_entry=post_entry)
            elif not blank_form(post_entry):
                blog_body_error = "Please enter text for your blog post"
                return render_template('new_blog.html', blog_body_error=blog_body_error, post_title=post_title)

   
    else:
        return render_template('new_blog.html')
        


if __name__ == '__main__':
    app.run()

























