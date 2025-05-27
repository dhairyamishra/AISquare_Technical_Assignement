import json
import unittest
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from django.test.runner import DiscoverRunner

class SummaryAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}',
            'Content-Type': 'application/json'
        }
        self.sample_text = "Albert Einstein developed the theory of relativity."

    def test_generate_summary_valid(self):
        response = self.client.post('/api/generate-summary/',
                                    {'text': self.sample_text},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)

    def test_generate_bullet_points_valid(self):
        response = self.client.post('/api/generate-bullet-points/',
                                    {'text': self.sample_text},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bullet_points', response.data)
        self.assertIsInstance(response.data['bullet_points'], list)

    def test_summary_missing_text(self):
        response = self.client.post('/api/generate-summary/',
                                    {},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_summary_empty_text(self):
        response = self.client.post('/api/generate-summary/',
                                    {'text': ''},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_bullet_points_missing_text(self):
        response = self.client.post('/api/generate-bullet-points/',
                                    {},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_bullet_points_empty_text(self):
        response = self.client.post('/api/generate-bullet-points/',
                                    {'text': ''},
                                    format='json',
                                    **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_token(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token invalidtoken',
            'Content-Type': 'application/json'
        }
        response = self.client.post('/api/generate-summary/',
                                    {'text': self.sample_text},
                                    format='json',
                                    **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required(self):
        response = self.client.post('/api/generate-summary/',
                                    {'text': self.sample_text},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# Custom runner to save results to a timestamped text file
class ReportRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        report_filename = f"test_report_{timestamp}.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            runner = unittest.TextTestRunner(stream=f, verbosity=2)
            result = runner.run(suite)
        print(f"✅ Test results saved to {report_filename}")
        return result
