from unittest import mock

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Scripts


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', 'alice@example.com', 'S3cret!pass')

    def test_login_with_username(self):
        response = self.client.post(reverse('login'), {'username_email': 'alice', 'password': 'S3cret!pass'})
        self.assertRedirects(response, reverse('index'), fetch_redirect_response=False)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_with_email(self):
        self.client.post(reverse('login'), {'username_email': 'ALICE@example.com', 'password': 'S3cret!pass'})
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_wrong_password(self):
        self.client.post(reverse('login'), {'username_email': 'alice', 'password': 'nope'})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_signup_then_login_again(self):
        self.client.post(reverse('signup'), {
            'username': 'bob', 'email': 'bob@example.com',
            'password1': 'An0ther!Pass', 'password2': 'An0ther!Pass',
        })
        self.client.logout()
        self.client.post(reverse('login'), {'username_email': 'bob', 'password': 'An0ther!Pass'})
        self.assertIn('_auth_user_id', self.client.session)

    def test_index_without_group_redirects_to_scripts(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('scripts'), fetch_redirect_response=False)

    def test_pages_require_login(self):
        for name in ('index', 'scripts'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response['Location'])


class ScriptPermissionTests(TestCase):
    def setUp(self):
        group = Group.objects.create(name='Content Creator')
        self.owner = User.objects.create_user('owner', password='x')
        self.owner.groups.add(group)
        self.other = User.objects.create_user('other', password='x')
        self.script = Scripts.objects.create(user=self.owner, title='T', idea='I', generated_script='S')

    def test_other_user_cannot_edit(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('edit_script', args=[self.script.pk]), {'generated_script': 'hacked'})
        self.assertEqual(response.status_code, 404)
        self.script.refresh_from_db()
        self.assertEqual(self.script.generated_script, 'S')

    def test_other_user_cannot_delete(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('delete_script', args=[self.script.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Scripts.objects.filter(pk=self.script.pk).exists())

    def test_owner_can_edit_and_delete(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse('edit_script', args=[self.script.pk]), {'generated_script': 'new', 'quiz': 'q'})
        self.assertEqual(response.status_code, 200)
        self.script.refresh_from_db()
        self.assertEqual(self.script.generated_script, 'new')
        response = self.client.post(reverse('delete_script', args=[self.script.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Scripts.objects.filter(pk=self.script.pk).exists())

    def test_anonymous_cannot_delete(self):
        response = self.client.post(reverse('delete_script', args=[self.script.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Scripts.objects.filter(pk=self.script.pk).exists())

    def test_edit_requires_csrf_token(self):
        client = self.client_class(enforce_csrf_checks=True)
        client.force_login(self.owner)
        response = client.post(reverse('edit_script', args=[self.script.pk]), {'generated_script': 'new'})
        self.assertEqual(response.status_code, 403)


class GenerationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('owner', password='x')
        self.client.force_login(self.user)

    def fake_response(self, text):
        response = mock.Mock(status_code=200)
        response.json.return_value = {'choices': [{'message': {'content': f'  {text}  '}}]}
        return response

    @mock.patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @mock.patch('Learn.views.requests.post')
    def test_generate_script_saves_result(self, post):
        post.return_value = self.fake_response('A script')
        response = self.client.post(reverse('generate_script'), {'title': 'T', 'idea': 'I'})
        self.assertEqual(response.json(), {'message': 'Script generated successfully'})
        self.assertEqual(Scripts.objects.get().generated_script, 'A script')
        self.assertEqual(post.call_args.kwargs['headers']['Authorization'], 'Bearer test-key')

    @mock.patch.dict('os.environ', {}, clear=True)
    @mock.patch('Learn.views.requests.post')
    def test_generate_script_without_api_key(self, post):
        response = self.client.post(reverse('generate_script'), {'title': 'T', 'idea': 'I'})
        self.assertIn('error', response.json())
        post.assert_not_called()

    @mock.patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @mock.patch('Learn.views.requests.post')
    def test_generate_quiz_saves_to_script(self, post):
        post.return_value = self.fake_response('Q1?')
        script = Scripts.objects.create(user=self.user, title='T', idea='I', generated_script='S')
        response = self.client.post(reverse('generate_quiz'), {
            'script_id': script.pk, 'title': 'T', 'generated_script': 'S',
        })
        self.assertEqual(response.json()['quiz'], 'Q1?')
        script.refresh_from_db()
        self.assertEqual(script.quiz, 'Q1?')
