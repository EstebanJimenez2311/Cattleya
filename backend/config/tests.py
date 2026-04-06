from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver", "127.0.0.1", "localhost"])
class AdminAuthenticationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.password = "ChangeMe123!"
        self.user = user_model.objects.create_user(
            username="admin",
            email="admin@example.com",
            password=self.password,
            is_staff=True,
            is_superuser=True,
        )
        self.client = Client()

    def test_admin_login_page_renders_custom_session_controls(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mantener sesion activa")
        self.assertContains(response, "cattleya-login-shell")

    def test_admin_login_with_remember_me_extends_session(self):
        response = self.client.post(
            "/admin/login/",
            {
                "username": self.user.username,
                "password": self.password,
                "remember_me": "on",
                "next": "/admin/",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/admin/")
        self.assertTrue(self.client.session.get("admin_remember_me"))
        self.assertIn("admin_last_activity_at", self.client.session)

    @override_settings(ADMIN_SESSION_IDLE_TIMEOUT=1)
    def test_admin_session_expires_after_inactivity(self):
        self.client.post(
            "/admin/login/",
            {
                "username": self.user.username,
                "password": self.password,
                "next": "/admin/",
            },
        )

        session = self.client.session
        session["admin_last_activity_at"] = 0
        session.save()

        response = self.client.get("/admin/monitor/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/admin/login/?next=%2Fadmin%2Fmonitor%2F")
