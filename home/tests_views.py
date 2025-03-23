from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from members.models import UserOption
from blog.models import Post

# Create your tests here.

class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')  # Ensure the URL name for HomeView is 'home'
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create UserOptions for testing
        UserOption.objects.create(user=self.user, option='nintendo_switch')

        # Create posts for testing
        self.post1 = Post.objects.create(
            title='Nintendo Post',
            content='Content for Nintendo',
            author=self.user
        )
        self.post2 = Post.objects.create(
            title='Xbox Post',
            content='Content for Xbox',
            author=self.user
        )

    def test_home_view_status_code(self):
        """Test that the HomeView returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Test that the HomeView uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_home_view_context_option_counts(self):
        """Test that the HomeView includes correct option counts in the context."""
        response = self.client.get(self.url)
        self.assertIn('option_counts', response.context)
        self.assertEqual(response.context['option_counts'], {
            'nintendo_switch': 1,
            'xbox': 0,
            'pc': 0,
            'playstation': 0
        })

    def test_home_view_context_most_liked_posts(self):
        """Test that the HomeView includes the most liked posts in the context."""
        # Simulate likes for the posts
        self.post1.likes.add(self.user)  # Add a like to the Nintendo post
        response = self.client.get(self.url)
        self.assertIn('most_liked_posts', response.context)
        self.assertEqual(response.context['most_liked_posts']['nintendo_switch'], self.post1)
        self.assertIsNone(response.context['most_liked_posts']['xbox'])  # No Xbox posts liked