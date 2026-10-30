from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models.post import Post, Comment
from . import community_bp

@community_bp.route('/community')
def community():
    # Will support dynamic posts in Phase 6, existing template renders fine
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@community_bp.route('/community/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'General')

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return render_template('post.html')

        new_post = Post(title=title, content=content, category=category, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash('Post submitted successfully!', 'success')
        return redirect(url_for('community.community'))

    return render_template('post.html')
