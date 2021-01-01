import json
from tests.testcase import TestCase
from models.user import User
from models.token import Token
from models.post import Post


class PostsTestCase(TestCase):
    def test_posts_list_page(self):
        user = User(**{
            'email': 'postslist@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        post = Post(
            user_id=user.id,
            title='Заголовок',
            text='Текст',
        )
        post.save()

        response = self.app.get('/posts/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(post.title, data['posts'][0]['title'])
        self.assertEqual(post.text, data['posts'][0]['text'])

    def test_posts_create_page(self):
        user = User(**{
            'email': 'postscreate@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        response = self.app.post('/posts/')
        self.assertEqual(response.status_code, 401)

        response = self.app.post(f'/posts/?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        post_title = 'Заголовок'
        post_text = 'Текст'

        test_cases = {
            'missing_title': {
                'data': {
                    'text': post_text,
                },
                'status_code': 422
            }, 'missing_text': {
                'data': {
                    'title': post_title,
                },
                'status_code': 422
            },  'success': {
                'data': {
                    'title': post_title,
                    'text': post_text,
                },
                'status_code': 200
            }
        }

        for name, test_case in test_cases.items():
            response = self.app.post(f'/posts/?access_token={token.token}', json=test_case['data'])
            self.assertEqual(response.status_code, test_case['status_code'])

            if name == 'success':
                data = json.loads(response.data.decode('UTF-8'))
                self.assertEqual(post_title, data['title'])
                self.assertEqual(post_text, data['text'])

    def test_post_detail_page(self):
        user = User(**{
            'email': 'postdetail@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        post = Post(
            user_id=user.id,
            title='Заголовок',
            text='Текст',
        )
        post.save()

        response = self.app.get(f'/posts/0')
        self.assertEqual(response.status_code, 404)

        post.deleted = True
        post.save()

        response = self.app.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 404)

        post.deleted = False
        post.save()

        response = self.app.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.text, data['text'])

    def test_post_edit_page(self):
        user = User(**{
            'email': 'postedit@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        post = Post(
            user_id=user.id,
            title='Заголовок',
            text='Текст',
        )
        post.save()

        new_post_title = 'Новый заголовок'
        new_post_text = 'Новый текст'

        response = self.app.put(f'/posts/{post.id}', json={
            'title': new_post_title,
            'text': new_post_text,
        })
        self.assertEqual(response.status_code, 401)

        response = self.app.put(f'/posts/{post.id}?access_token={token.token}', json={
            'title': new_post_title,
            'text': new_post_text,
        })
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        post.deleted = True
        post.save()

        response = self.app.delete(f'/posts/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        response = self.app.put(f'/posts/{post.id}?access_token={token.token}', json={
            'title': new_post_title,
            'text': new_post_text,
        })
        self.assertEqual(response.status_code, 404)

        post.deleted = False
        post.save()

        response = self.app.put(f'/posts/{post.id}?access_token={token.token}', json={
            'title': '',
            'text': new_post_text,
        })
        self.assertEqual(response.status_code, 422)

        response = self.app.put(f'/posts/{post.id}?access_token={token.token}', json={
            'title': new_post_title,
            'text': new_post_text,
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(new_post_title, data['title'])
        self.assertEqual(new_post_text, data['text'])

    def test_post_delete_page(self):
        user = User(**{
            'email': 'postdelete@mail.ru',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '111111',
        })
        user.save()

        token = Token(user.id)
        token.save()

        post = Post(
            user_id=user.id,
            title='Заголовок',
            text='Текст'
        )
        post.save()

        response = self.app.delete(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 401)

        response = self.app.delete(f'/posts/{post.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 403)

        user.employee = 999
        user.save()

        response = self.app.delete(f'/posts/0?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        post.deleted = True
        post.save()

        response = self.app.delete(f'/posts/{post.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 404)

        post.deleted = False
        post.save()

        response = self.app.delete(f'/posts/{post.id}?access_token={token.token}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('success deleting', data['message'])
