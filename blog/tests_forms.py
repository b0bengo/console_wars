from django.test import TestCase
from blog.forms import PostForm, CommentForm

# Create your tests here.

class TestPostForm(TestCase):
    def test_post_form_valid_data(self):
        """Test that the PostForm is valid with correct data."""
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'status': 'published'
        })
        self.assertTrue(form.is_valid())

    def test_post_form_missing_title(self):
        """Test that the PostForm is invalid if the title is missing."""
        form = PostForm(data={
            'title': '',
            'content': 'This is a test post content.',
            'status': 'published'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_post_form_missing_content(self):
        """Test that the PostForm is invalid if the content is missing."""
        form = PostForm(data={
            'title': 'Test Post',
            'content': '',
            'status': 'published'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_post_form_invalid_status(self):
        """Test that the PostForm is invalid if the status is invalid."""
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'status': 'invalid_status'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)

    def test_post_form_empty_data(self):
        """Test that the PostForm is invalid with no data."""
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # All fields are required


class TestCommentForm(TestCase):
    def test_comment_form_valid_data(self):
        """Test that the CommentForm is valid with correct data."""
        form = CommentForm(data={
            'body': 'This is a test comment.'
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_missing_body(self):
        """Test that the CommentForm is invalid if the body is missing."""
        form = CommentForm(data={
            'body': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_comment_form_empty_data(self):
        """Test that the CommentForm is invalid with no data."""
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Only the body field is required