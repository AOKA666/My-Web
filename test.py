from datetime import datetime, timedelta
import unittest
from app import app,db
from app.models import User,Comments,Role


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_password_hashing(self):
        u = User(username='susan', role=Role(default=True))
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        
    def test_follow(self):
        u1 = User(username='john', email='john@example.com', role=Role(default=True))
        u2 = User(username='susan', email='susan@example.com', role=Role(default=True))
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followers.all(), [])
        
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')
        
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)
        
    def test_follow_comments(self):
        u1 = User(username='john', email='john@example.com', role=Role(default=True))
        u2 = User(username='susan', email='susan@example.com', role=Role(default=True))
        u3 = User(username='mary', email='mary@example.com', role=Role(default=True))
        u4 = User(username='david', email='david@example.com', role=Role(default=True))
        db.session.add_all([u1,u2,u3,u4])
        
        # 创建四条评论
        now = datetime.utcnow()
        c1 = Comments(body='comment from john', user=u1, 
                        timestamp=now + timedelta(seconds=1))
        c2 = Comments(body='comment from susan', user=u2, 
                        timestamp=now + timedelta(seconds=4))
        c3 = Comments(body='comment from mary', user=u3,
                        timestamp=now + timedelta(seconds=3))
        c4 = Comments(body='comment from david', user=u4,
                        timestamp=now + timedelta(seconds=2))
        db.session.add_all([c1,c2,c3,c4])
        db.session.commit()
        
        # 相互关注一波
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()
        
        # 检查粉丝的评论显示
        f1 = u1.followed_comments().all()
        f2 = u2.followed_comments().all()
        f3 = u3.followed_comments().all()
        f4 = u4.followed_comments().all()
        self.assertEqual(f1, [c2, c4, c1])
        self.assertEqual(f2, [c2, c3])
        self.assertEqual(f3, [c3, c4])
        self.assertEqual(f4, [c4])
        
if __name__ == '__main__':
    unittest.main(verbosity=2)