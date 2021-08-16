from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views",__name__)

@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html",user=current_user,posts=posts)

@views.route("/create-post",methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Post cannot be empty.",category="error")
        else:
            post = Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created.",category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html",user=current_user)

# the <id> in the url route for delete-post is passed as the id parameter in the delete_post function
# the html delete button in home.html has its href = /delete-post/{{post.id}}, so it passes the
# post id (the post being selected for deletion) when clicked
@views.route("/delete-post/<id>",methods=["GET","POST"])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.",category="error")
    elif current_user.id != post.author:
        flash("You lack permission to delete this post.",category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted.",category="success")

    return redirect(url_for("views.home"))

@views.route("/posts/<username>",methods=["GET","POST"])
@login_required
def show_user_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User does not exist.",category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("user_posts.html",user=current_user,posts=posts,author=user)

# the <id> is the id of the post that is being commented on
@views.route("/posts/create-comment/<post_id>",methods=["POST","GET"])
@views.route("/create-comment/<post_id>",methods=["POST","GET"])
@login_required
def create_comment(post_id):
    comment_text = request.form.get("text")

    if not comment_text:
        flash("Comment cannot be empty.",category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if not post:
            flash("Post does not exist.",category="error")
        else:
            comment = Comment(text=comment_text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment created.",category="success")

    return redirect(url_for("views.home"))

@views.route("/delete-comment/<comment_id>",methods=["POST","GET"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist.",category="error")
    elif comment.author != current_user.id:
        flash("You do not have permission to delete this comment.",category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted.",category="success")

    return redirect(url_for("views.home"))

@views.route("/like-post/<post_id>",methods=["GET","POST"])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first() # check of the post being liked even exists
    like = Like.query.filter_by(author=current_user.id,post_id=post_id).first() # check if a like already exists for this post from the current user

    if not Post:
        return jsonify({"error":"Post does not exist."}, 400) # 400 = bad request
    elif like:
        # if the current user is liking a post he already liked, then this is interpreted as taking away his like for this post
        db.session.delete(like)
        db.session.commit();
    else:
        # add a like for this post if the current user has not already liked it
        new_like = Like(author=current_user.id,post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

    # returns number of post likes and when the current user liked the post
    return jsonify({"likes": len(post.likes),"liked": current_user.id in map(lambda x: x.author, post.likes)})
