"""Authentication and role-based access."""
from tests.base import AppTestCase


class TestAuth(AppTestCase):
    def test_student_register_and_me(self):
        self.register_student()
        me = self.client.get("/api/auth/me", headers=self.hdr("s@t.com", "secret1"))
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.get_json()["data"]["user"]["role"], "student")

    def test_duplicate_email_rejected(self):
        self.register_student()
        again = self.register_student()
        self.assertEqual(again.status_code, 409)

    def test_company_starts_pending(self):
        res = self.register_company()
        self.assertEqual(res.get_json()["data"]["profile"]["approval_status"], "pending")

    def test_admin_cannot_be_registered(self):
        res = self.client.post("/api/auth/register", json={
            "role": "admin", "email": "x@y.com", "password": "secret1"})
        self.assertEqual(res.status_code, 400)

    def test_bad_password_rejected(self):
        self.register_student()
        res = self.client.post("/api/auth/login", json={"email": "s@t.com", "password": "nope"})
        self.assertEqual(res.status_code, 401)

    def test_missing_token_rejected(self):
        self.assertEqual(self.client.get("/api/auth/me").status_code, 401)

    def test_student_blocked_from_admin(self):
        self.register_student()
        res = self.client.get("/api/admin/stats", headers=self.hdr("s@t.com", "secret1"))
        self.assertEqual(res.status_code, 403)

    def test_blacklisted_user_cannot_login(self):
        self.register_student()
        admin = self.admin()
        uid = self.client.get("/api/admin/students", headers=admin).get_json()["data"][0]["user_id"]
        self.client.post(f"/api/admin/users/{uid}/blacklist", json={"blacklisted": True}, headers=admin)
        res = self.client.post("/api/auth/login", json={"email": "s@t.com", "password": "secret1"})
        self.assertEqual(res.status_code, 403)
