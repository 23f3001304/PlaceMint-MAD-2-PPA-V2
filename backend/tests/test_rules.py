"""Milestone-6 rules: history, status tracking, eligibility, visibility."""
from tests.base import AppTestCase


class TestPlacementRules(AppTestCase):
    def setUp(self):
        super().setUp()
        self.register_company()
        self.co = self.hdr("co@t.com", "secret1")
        self.approve_first_company()

    def _open_drive(self, **kw):
        drive_id = self.make_drive(self.co, **kw)
        self.approve_drive(drive_id)
        return drive_id

    def test_company_needs_approval_to_post(self):
        self.register_company(email="co2@t.com", name="Beta")
        co2 = self.hdr("co2@t.com", "secret1")
        res = self.client.post("/api/company/drives", json={
            "job_title": "SDE", "job_description": "x", "deadline": "2027-01-01"}, headers=co2)
        self.assertEqual(res.status_code, 403)

    def test_only_approved_drives_visible(self):
        self.make_drive(self.co)  # left pending
        self._open_drive(job_title="Open Role")
        self.register_student()
        stu = self.hdr("s@t.com", "secret1")
        drives = self.client.get("/api/student/drives", headers=stu).get_json()["data"]
        titles = [d["job_title"] for d in drives]
        self.assertEqual(titles, ["Open Role"])

    def test_duplicate_application_prevented(self):
        drive_id = self._open_drive()
        self.register_student()
        stu = self.hdr("s@t.com", "secret1")
        first = self.client.post("/api/student/applications", json={"drive_id": drive_id}, headers=stu)
        second = self.client.post("/api/student/applications", json={"drive_id": drive_id}, headers=stu)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_eligibility_enforced(self):
        drive_id = self._open_drive(min_cgpa=9)
        self.register_student(cgpa=8)
        stu = self.hdr("s@t.com", "secret1")
        res = self.client.post("/api/student/applications", json={"drive_id": drive_id}, headers=stu)
        self.assertEqual(res.status_code, 403)

    def test_cannot_apply_to_pending_drive(self):
        pending = self.make_drive(self.co)  # not approved
        self.register_student()
        stu = self.hdr("s@t.com", "secret1")
        res = self.client.post("/api/student/applications", json={"drive_id": pending}, headers=stu)
        self.assertEqual(res.status_code, 403)

    def test_status_flow_creates_placement(self):
        drive_id = self._open_drive()
        self.register_student()
        stu = self.hdr("s@t.com", "secret1")
        app_id = self.client.post("/api/student/applications", json={"drive_id": drive_id}, headers=stu).get_json()["data"]["id"]
        self.client.patch(f"/api/company/applications/{app_id}", json={"status": "placed"}, headers=self.co)
        placements = self.client.get("/api/student/applications/placements", headers=stu).get_json()["data"]
        self.assertEqual(len(placements), 1)
        history = self.client.get("/api/student/applications", headers=stu).get_json()["data"]
        self.assertEqual(history[0]["status"], "placed")


class TestCaching(AppTestCase):
    def _companies(self, admin):
        return self.client.get("/api/admin/stats", headers=admin).get_json()["data"]["companies"]

    def test_admin_stats_cached_then_invalidated(self):
        admin = self.admin()
        first = self._companies(admin)  # cached
        self.register_company()
        self.assertEqual(self._companies(admin), first)  # cache hit: still stale
        self.approve_first_company()  # a write that invalidates the cache
        self.assertEqual(self._companies(admin), first + 1)  # refreshed
