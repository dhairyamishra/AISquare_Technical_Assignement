from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from unittest.mock import patch

class QuizViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="quizuser", password="pass1234")
        self.token = Token.objects.create(user=self.user)

    def test_quiz_requires_login(self):
        response = self.client.get(reverse("play-quiz"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    @patch("quizui.views.requests.post")
    def test_quiz_renders_with_valid_token(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "title": "Mock Title",
            "quiz": [
                {
                    "question": "Mock Q?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A"
                }
            ]
        }

        self.client.login(username="quizuser", password="pass1234")
        response = self.client.get(reverse("play-quiz"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mock Q?")

    @patch("quizui.views.requests.post")
    def test_quiz_post_scores_quiz(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "title": "Mock Title",
            "quiz": [
                {
                    "question": "Q1?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A"
                }
            ]
        }

        self.client.login(username="quizuser", password="pass1234")
        get_response = self.client.get(reverse("play-quiz"))

        post_data = {
            "questions": '[{"question": "Q1?", "options": ["A", "B", "C", "D"], "answer": "A"}]',
            "q0": "A"
        }
        post_response = self.client.post(reverse("play-quiz"), post_data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "You scored")

    @patch("quizui.views.requests.post")
    def test_quiz_api_error_handling(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.side_effect = ValueError("Mocked JSON decoding error")
        mock_post.return_value.text = "not valid json"

        self.client.login(username="quizuser", password="pass1234")
        response = self.client.get(reverse("play-quiz"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz could not be loaded")

