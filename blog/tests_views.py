from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment

# Create your tests here.

# Post List View Test
class TestPostListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('post_list')
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_post_list_view_status_code(self):
        """Test that the PostList view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template(self):
        """Test that the PostList view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post_list_view_context(self):
        """Test that the PostList view includes posts in the context."""
        Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['posts']), 1)


# Post Create View Test

class TestPostCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('post_create')
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_post_create_view_redirect_if_not_logged_in(self):
        """Test that the PostCreate view redirects if the user is not logged in."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_create_view_status_code_logged_in(self):
        """Test that the PostCreate view returns a 200 status code for logged-in users."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_view_template(self):
        """Test that the PostCreate view uses the correct template."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_create_view_form_submission(self):
        """Test that the PostCreate view creates a new post on form submission."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {
            'title': 'New Post',
            'content': 'This is a new post.'
        })
        self.assertEqual(Post.objects.count(), 1)
        self.assertRedirects(response, '/blog/user_posts/')


# Add Comment Test

class TestAddCommentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.url = reverse('add_comment', args=[self.post.id])

    def test_add_comment_redirect_if_not_logged_in(self):
        """Test that the add_comment view redirects if the user is not logged in."""
        response = self.client.post(self.url, {'body': 'Test Comment'})
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_comment_logged_in(self):
        """Test that the add_comment view adds a comment for logged-in users."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {'body': 'Test Comment'})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))


# Like Post Test

class TestLikePostView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.url = reverse('like_post', args=[self.post.id])

    def test_like_post_redirect_if_not_logged_in(self):
        """Test that the like_post view redirects if the user is not logged in."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_like_post_logged_in(self):
        """Test that the like_post view toggles the like for logged-in users."""
        self.client.login(username='testuser', password='password')
        # Like the post
        response = self.client.post(self.url)
        self.assertEqual(self.post.likes.count(), 1)
        # Unlike the post
        response = self.client.post(self.url)
        self.assertEqual(self.post.likes.count(), 0)