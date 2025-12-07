from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentViewsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass1234')
        self.user2 = User.objects.create_user(username='bob', password='pass1234')
        self.post = Post.objects.create(title='Test Post', content='Post body', author=self.user1)
        # a comment by user1 (author)
        self.comment = Comment.objects.create(post=self.post, author=self.user1, content='First comment')

    def test_comments_show_on_post_detail(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        resp = self.client.get(url)
        self.assertContains(resp, 'First comment')
        self.assertContains(resp, self.user1.username)

    def test_create_comment_requires_login(self):
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # should redirect to login
        # posting anonymously should also redirect
        resp = self.client.post(url, {'content': 'Anon comment'})
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Comment.objects.filter(content='Anon comment').exists())

    def test_create_comment_as_authenticated_user(self):
        self.client.login(username='bob', password='pass1234')
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post!'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Comment.objects.filter(content='Nice post!', author=self.user2).exists())
        # ensure redirected back to post detail
        self.assertContains(resp, 'Nice post!')

    def test_create_comment_validation_empty(self):
        self.client.login(username='bob', password='pass1234')
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': ''})
        # Form invalid -> returns 200 and shows error
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'content', 'Comment cannot be empty.')

    def test_update_comment_only_author(self):
        update_url = reverse('comment-update', kwargs={'pk': self.comment.pk})
        # other user tries -> should be 403 (UserPassesTestMixin)
        self.client.login(username='bob', password='pass1234')
        resp = self.client.get(update_url)
        self.assertIn(resp.status_code, (302, 403))  # depending on mixin handling, typically 403
        # author updates successfully
        self.client.logout()
        self.client.login(username='alice', password='pass1234')
        resp = self.client.post(update_url, {'content': 'Edited comment'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Edited comment')

    def test_delete_comment_only_author(self):
        delete_url = reverse('comment-delete', kwargs={'pk': self.comment.pk})
        # other user cannot delete
        self.client.login(username='bob', password='pass1234')
        resp = self.client.post(delete_url)
        self.assertIn(resp.status_code, (302, 403))
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
        # author deletes
        self.client.logout()
        self.client.login(username='alice', password='pass1234')
        resp = self.client.post(delete_url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

