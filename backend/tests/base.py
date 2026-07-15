"""Shared test case: fresh in-memory app per test, plus flow helpers.

Each request goes through the test client so it manages its own app context;
pushing a long-lived context here would fight SQLite `:memory:` isolation.
"""
import unittest

from app import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    # --- auth helpers -----------------------------------------------------
    def hdr(self, email, password):
        res = self.client.post("/api/auth/login", json={"email": email, "password": password})
        return {"Authorization": f"Bearer {res.get_json()['data']['token']}"}

    def admin(self):
        return self.hdr("coehemang@gmail.com", "admin123")

    # --- fixtures ---------------------------------------------------------
    def register_company(self, email="co@t.com", name="Acme"):
        return self.client.post("/api/auth/register", json={
            "role": "company", "email": email, "password": "secret1", "company_name": name})

    def register_student(self, email="s@t.com", roll="CS1", branch="CSE", cgpa=8, year=2026):
        return self.client.post("/api/auth/register", json={
            "role": "student", "email": email, "password": "secret1", "name": "Sam",
            "roll_no": roll, "branch": branch, "grad_year": year, "cgpa": cgpa})

    def approve_first_company(self):
        admin = self.admin()
        cid = self.client.get("/api/admin/companies?status=pending", headers=admin).get_json()["data"][0]["id"]
        self.client.post(f"/api/admin/companies/{cid}/approval", json={"status": "approved"}, headers=admin)
        return cid

    def make_drive(self, company_hdr, **overrides):
        body = {
            "job_title": "SDE", "job_description": "x", "deadline": "2027-01-01",
            "eligible_branches": ["CSE"], "min_cgpa": 7, "eligible_years": [2026],
        }
        body.update(overrides)
        return self.client.post("/api/company/drives", json=body, headers=company_hdr).get_json()["data"]["id"]

    def approve_drive(self, drive_id):
        self.client.post(f"/api/admin/drives/{drive_id}/approval", json={"status": "approved"}, headers=self.admin())
