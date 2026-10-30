import os
import secrets
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from extensions import db
from models.user import User
from models.post import Post, Comment, PostLike
from . import community_bp

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def seed_community_posts():
    """Seeds initial 4 community posts if the posts table is empty."""
    if Post.query.count() > 0:
        return

    # Find or create a community champion user
    author = User.query.filter_by(email='community@agrihelper.in').first()
    if not author:
        author = User(
            name="AgriHelper Team",
            email="community@agrihelper.in",
            avatar_url="https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=300&auto=format&fit=crop&q=80",
            provider="local"
        )
        author.set_password("AgriHelperSeed2026!")
        db.session.add(author)
        db.session.commit()

    seed_posts = [
        {
            "title": "🌿 The Power of Organic Farming",
            "category": "Tips",
            "content": "Organic farming isn't just a trend—it's a sustainable future. By avoiding harmful synthetic pesticides and chemicals, organic practices protect soil microbiome, increase natural moisture retention, and produce nutrient-dense crops. Using vermicompost and neem cake is one of the easiest ways to start transitioning your farm.",
            "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6eb22509?w=800&auto=format&fit=crop&q=80",
            "upvotes": 14
        },
        {
            "title": "🤖 Top 5 AgriTech Innovations Every Farmer Should Watch",
            "category": "Discussion",
            "content": "Here are 5 agricultural technologies transforming yields across India:\n1. Kisan Drones for precision aerial pesticide & liquid fertilizer spraying.\n2. IoT Soil Moisture Sensors to automate drip irrigation.\n3. AI-powered pest diagnostics via smartphone photo.\n4. GPS-guided tractor attachments for laser land leveling.\n5. Automated solar insect light traps.\n\nWhich of these are you most excited to try on your land?",
            "image_url": "https://images.unsplash.com/photo-1589923188900-85dae523342b?w=800&auto=format&fit=crop&q=80",
            "upvotes": 21
        },
        {
            "title": "🔄 Why Crop Rotation Still Wins for Soil Health",
            "category": "Tips",
            "content": "Crop rotation isn't just traditional wisdom—it's verified agricultural science. Rotating legumes (like gram, soybean, or moong) with nitrogen-exhausting crops (like wheat or sugarcane) naturally restores soil nitrogen without heavy urea purchases. It also disrupts the life cycles of soil-borne pests and fungal pathogens.",
            "image_url": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800&auto=format&fit=crop&q=80",
            "upvotes": 18
        },
        {
            "title": "💧 Water Conservation: How We Cut Water Use by 45%",
            "category": "Success Stories",
            "content": "Last Kharif season, our farmer group in Nashik installed inline drip systems with subsidy support under PMKSY. Not only did our water consumption drop by 45%, but our fertilizer efficiency jumped because we applied water-soluble NPK directly to the root zone. Our tomato yield increased by 28 quintals per acre!",
            "image_url": "https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800&auto=format&fit=crop&q=80",
            "upvotes": 29
        }
    ]

    for item in seed_posts:
        p = Post(
            title=item['title'],
            category=item['category'],
            content=item['content'],
            image_url=item['image_url'],
            upvotes=item['upvotes'],
            user_id=author.id
        )
        db.session.add(p)
        db.session.flush()

        # Add a sample discussion comment
        c = Comment(
            post_id=p.id,
            user_id=author.id,
            content="Feel free to ask questions or share your personal experiences in the comments below!"
        )
        db.session.add(c)

    db.session.commit()

@community_bp.route('/community')
def community():
    seed_community_posts()

    selected_category = request.args.get('category', 'All').strip()
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 9

    query = Post.query

    if selected_category and selected_category.lower() != 'all':
        query = query.filter(Post.category.ilike(f"%{selected_category}%"))

    if search_query:
        term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Post.title.ilike(term),
                Post.content.ilike(term),
                Post.category.ilike(term)
            )
        )

    pagination = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    categories = ['All', 'Discussion', 'Questions', 'Tips', 'Success Stories']

    return render_template(
        'community.html',
        posts=posts,
        pagination=pagination,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query
    )

@community_bp.route('/community/post/<int:post_id>')
def post_detail(post_id):
    seed_community_posts()
    post = Post.query.get_or_404(post_id)
    is_liked = post.is_liked_by(current_user.id) if current_user.is_authenticated else False
    comments = post.comments.all()

    return render_template(
        'post_detail.html',
        post=post,
        comments=comments,
        is_liked=is_liked
    )

@community_bp.route('/community/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'Discussion')
        image_url = request.form.get('image_url', '').strip()

        # Handle Image File Upload
        file = request.files.get('image_file')
        if file and file.filename != '' and allowed_file(file.filename):
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'posts')
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"post_{secrets.token_hex(6)}_{secure_filename(file.filename)}"
            file.save(os.path.join(upload_dir, filename))
            image_url = url_for('static', filename=f'uploads/posts/{filename}')

        if not title or not content:
            flash('Both Title and Content are required.', 'danger')
            return render_template('post.html', title=title, content=content, category=category, image_url=image_url)

        new_post = Post(
            title=title,
            content=content,
            category=category,
            image_url=image_url or None,
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()

        flash('Your post has been published to the community!', 'success')
        return redirect(url_for('community.post_detail', post_id=new_post.id))

    return render_template('post.html', is_edit=False)

@community_bp.route('/community/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('community.post_detail', post_id=post.id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', post.category)
        image_url = request.form.get('image_url', post.image_url or '').strip()

        file = request.files.get('image_file')
        if file and file.filename != '' and allowed_file(file.filename):
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'posts')
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"post_{secrets.token_hex(6)}_{secure_filename(file.filename)}"
            file.save(os.path.join(upload_dir, filename))
            image_url = url_for('static', filename=f'uploads/posts/{filename}')

        if not title or not content:
            flash('Title and Content cannot be empty.', 'danger')
            return render_template('post.html', post=post, is_edit=True)

        post.title = title
        post.content = content
        post.category = category
        post.image_url = image_url or None
        post.updated_at = datetime.utcnow()
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('community.post_detail', post_id=post.id))

    return render_template('post.html', post=post, is_edit=True)

@community_bp.route('/community/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('community.post_detail', post_id=post.id))

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully.', 'info')
    return redirect(url_for('community.community'))

@community_bp.route('/community/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content', '').strip()

    if not content:
        data = request.get_json() or {}
        content = data.get('content', '').strip()

    if not content:
        if request.is_json:
            return jsonify({'error': 'Comment content cannot be empty'}), 400
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('community.post_detail', post_id=post.id))

    comment = Comment(
        post_id=post.id,
        user_id=current_user.id,
        content=content
    )
    db.session.add(comment)
    db.session.commit()

    if request.is_json:
        return jsonify({
            'success': True,
            'comment': comment.to_dict(),
            'total_comments': post.comments.count()
        })

    flash('Your comment has been added.', 'success')
    return redirect(url_for('community.post_detail', post_id=post.id))

@community_bp.route('/community/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id

    # Allow comment author or post author to delete comment
    if comment.user_id != current_user.id and comment.post.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Unauthorized'}), 403
        flash('Unauthorized to delete this comment.', 'danger')
        return redirect(url_for('community.post_detail', post_id=post_id))

    db.session.delete(comment)
    db.session.commit()

    if request.is_json:
        return jsonify({'success': True, 'total_comments': Post.query.get(post_id).comments.count()})

    flash('Comment removed.', 'info')
    return redirect(url_for('community.post_detail', post_id=post_id))

@community_bp.route('/community/post/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = PostLike(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        liked = True

    db.session.commit()

    likes_count = post.likes.count()
    post.upvotes = likes_count
    db.session.commit()

    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    })
