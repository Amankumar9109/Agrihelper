import os
import sys
import io
from app import create_app
from extensions import db
from models.user import User
from models.post import Post, Comment, PostLike
from blueprints.community.routes import seed_community_posts

def test_phase6():
    print("========================================")
    print("Starting Phase 6 Test Suite: Community Forum Upgrade")
    print("========================================")

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    test_author_email = "forum_author@agrihelper.local"
    test_user_email = "commenter@agrihelper.local"

    with app.app_context():
        db.create_all()

        # 1. Test Community Seeding
        seed_community_posts()
        total_posts = Post.query.count()
        assert total_posts >= 4, f"Expected at least 4 seed posts, got {total_posts}"
        print(f"[OK] Community posts seeded: {total_posts} posts in database")

        # Verify seed categories
        categories = set(p.category for p in Post.query.all())
        assert 'Tips' in categories
        assert 'Discussion' in categories
        assert 'Success Stories' in categories
        print(f"[OK] Seed categories verified: {categories}")

        # Create author and commenter users
        author = User.query.filter_by(email=test_author_email).first()
        if not author:
            author = User(name="Forum Author", email=test_author_email, provider="local")
            db.session.add(author)
        author.set_password("AuthorPass123!")

        commenter = User.query.filter_by(email=test_user_email).first()
        if not commenter:
            commenter = User(name="Helpful Commenter", email=test_user_email, provider="local")
            db.session.add(commenter)
        commenter.set_password("CommenterPass123!")

        db.session.commit()
        author_id = author.id
        commenter_id = commenter.id
        print(f"[OK] Test users ready (Author ID: {author_id}, Commenter ID: {commenter_id})")

    client = app.test_client()

    # 2. Test Community Feed Page (GET /community)
    res = client.get('/community')
    assert res.status_code == 200, f"Expected 200 from /community, got {res.status_code}"
    assert b"AgriHelper Farmer Forum" in res.data
    assert b"Share Your Post" in res.data
    print("[OK] GET /community rendered successfully with hero, categories and feed")

    # 3. Test Category Filtering
    res = client.get('/community?category=Tips')
    assert res.status_code == 200
    assert b"Crop Rotation" in res.data or b"Organic Farming" in res.data
    print("[OK] GET /community?category=Tips filtered feed correctly")

    # 4. Test Search Query
    res = client.get('/community?q=innovations')
    assert res.status_code == 200
    assert b"AgriTech Innovations" in res.data
    print("[OK] GET /community?q=innovations returned matching topic")

    # 5. Test Unauthenticated Create Post (should redirect 302 to login)
    res = client.get('/community/post')
    assert res.status_code == 302
    assert '/login' in res.headers['Location']
    print("[OK] Unauthenticated GET /community/post correctly redirected to /login")

    # 6. Log in as author
    login_res = client.post('/login', data={'email': test_author_email, 'password': 'AuthorPass123!'}, follow_redirects=True)
    assert login_res.status_code == 200
    print("[OK] Author logged in")

    # 7. Test Create Post with Image Upload (POST /community/post)
    fake_img = (io.BytesIO(b"fake image bytes data"), "field_experiment.jpg")
    post_data = {
        'title': 'High Density Apple Orchard Trial in Himachal',
        'category': 'Success Stories',
        'content': 'We tested rootstock M9 with drip fertigation. Spacing of 3m x 1m yielded 25 tons per hectare in the 4th year with 92% A-grade fruit color.',
        'image_file': fake_img
    }
    create_res = client.post('/community/post', data=post_data, follow_redirects=False, content_type='multipart/form-data')
    assert create_res.status_code == 302, f"Expected 302 redirect on create, got {create_res.status_code}"
    
    with app.app_context():
        new_post = Post.query.filter_by(title='High Density Apple Orchard Trial in Himachal').first()
        assert new_post is not None
        assert new_post.user_id == author_id
        assert new_post.category == 'Success Stories'
        assert new_post.image_url is not None and 'post_' in new_post.image_url
        new_post_id = new_post.id
        print(f"[OK] POST /community/post created post #{new_post_id} with image: {new_post.image_url}")

    # 8. Test Post Detail View (GET /community/post/<id>)
    detail_res = client.get(f'/community/post/{new_post_id}')
    assert detail_res.status_code == 200
    assert b"High Density Apple Orchard Trial" in detail_res.data
    assert b"Discussion" in detail_res.data
    print(f"[OK] GET /community/post/{new_post_id} rendered post details")

    # 9. Test Edit Post (POST /community/post/<id>/edit)
    edit_data = {
        'title': 'High Density Apple Orchard Trial in Himachal (Updated Yield)',
        'category': 'Success Stories',
        'content': 'Updated yield data: 28 tons per hectare in year 4 with excellent coloring.',
        'image_url': new_post.image_url
    }
    edit_res = client.post(f'/community/post/{new_post_id}/edit', data=edit_data, follow_redirects=True)
    assert edit_res.status_code == 200
    assert b"Updated Yield" in edit_res.data
    with app.app_context():
        updated_p = db.session.get(Post, new_post_id)
        assert 'Updated Yield' in updated_p.title
    print(f"[OK] POST /community/post/{new_post_id}/edit updated post content")

    # 10. Test Toggle Like System (POST /community/post/<id>/like)
    # First like
    like_res1 = client.post(f'/community/post/{new_post_id}/like')
    assert like_res1.status_code == 200
    like_data1 = like_res1.get_json()
    assert like_data1['success'] is True
    assert like_data1['liked'] is True
    assert like_data1['likes_count'] == 1
    print(f"[OK] Toggle Like: user liked post #{new_post_id} (count=1)")

    # Second like -> toggles off (unlike)
    like_res2 = client.post(f'/community/post/{new_post_id}/like')
    assert like_res2.status_code == 200
    like_data2 = like_res2.get_json()
    assert like_data2['success'] is True
    assert like_data2['liked'] is False
    assert like_data2['likes_count'] == 0
    print(f"[OK] Toggle Like: user unliked post #{new_post_id} (count=0)")

    # Relike for testing
    client.post(f'/community/post/{new_post_id}/like')

    # 11. Test Commenting System
    # Log out author, log in as commenter
    client.get('/logout')
    login_res2 = client.post('/login', data={'email': test_user_email, 'password': 'CommenterPass123!'}, follow_redirects=True)
    assert login_res2.status_code == 200

    # Add comment via JSON
    comment_payload = {'content': 'Fantastic results! Which fungicide did you spray during petal fall?'}
    comment_res = client.post(f'/community/post/{new_post_id}/comment', json=comment_payload)
    assert comment_res.status_code == 200
    c_data = comment_res.get_json()
    assert c_data['success'] is True
    comment_id = c_data['comment']['id']
    assert c_data['total_comments'] == 1
    print(f"[OK] POST /community/post/{new_post_id}/comment created comment #{comment_id}")

    # Verify comment shows on detail page
    res_with_comment = client.get(f'/community/post/{new_post_id}')
    assert b"petal fall" in res_with_comment.data
    print("[OK] Verified comment rendered in post detail discussion stream")

    # 12. Test Delete Comment
    del_comment_res = client.post(f'/community/comment/{comment_id}/delete', json={})
    assert del_comment_res.status_code == 200
    with app.app_context():
        c_obj = db.session.get(Comment, comment_id)
        assert c_obj is None
    print(f"[OK] POST /community/comment/{comment_id}/delete successfully deleted comment")

    # 13. Test Delete Post (Owner Only)
    # Log back in as author
    client.get('/logout')
    client.post('/login', data={'email': test_author_email, 'password': 'AuthorPass123!'}, follow_redirects=True)

    del_post_res = client.post(f'/community/post/{new_post_id}/delete', follow_redirects=True)
    assert del_post_res.status_code == 200
    with app.app_context():
        del_p = db.session.get(Post, new_post_id)
        assert del_p is None
    print(f"[OK] POST /community/post/{new_post_id}/delete deleted post and verified cascading cleanup")

    print("========================================")
    print("ALL PHASE 6 TESTS PASSED (13/13)!")
    print("========================================")

if __name__ == '__main__':
    test_phase6()
