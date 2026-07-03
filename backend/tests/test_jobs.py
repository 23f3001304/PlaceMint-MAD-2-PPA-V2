"""Backend jobs: CSV export (eager), ownership, reminders and reports."""
from app.tasks.reminders import run_daily_reminders
from app.tasks.reports import run_monthly_reports
from tests.base import AppTestCase


class TestJobs(AppTestCase):
    def _seed(self):
        self.register_company()
        co = self.hdr("co@t.com", "secret1")
        self.approve_first_company()
        drive_id = self.make_drive(co)
        self.approve_drive(drive_id)
        self.register_student()
        stu = self.hdr("s@t.com", "secret1")
        self.client.post("/api/student/applications", json={"drive_id": drive_id}, headers=stu)
        return co, stu

    def test_student_csv_export_end_to_end(self):
        _, stu = self._seed()
        start = self.client.post("/api/exports", headers=stu)
        self.assertEqual(start.status_code, 201)
        job_id = start.get_json()["data"]["id"]

        status = self.client.get(f"/api/exports/{job_id}", headers=stu).get_json()["data"]
        self.assertEqual(status["status"], "done")  # eager mode completes inline
        self.assertEqual(status["row_count"], 1)

        download = self.client.get(f"/api/exports/{job_id}/download", headers=stu)
        self.assertEqual(download.status_code, 200)
        self.assertIn(b"Drive Title", download.data)

    def test_export_ownership_enforced(self):
        co, stu = self._seed()
        job_id = self.client.post("/api/exports", headers=stu).get_json()["data"]["id"]
        self.assertEqual(self.client.get(f"/api/exports/{job_id}", headers=co).status_code, 404)

    def test_reminders_and_reports_run(self):
        self._seed()
        with self.app.app_context():
            reminders = run_daily_reminders()
            reports = run_monthly_reports()
        self.assertIn("deadlines", reminders)
        self.assertGreaterEqual(reports["company_reports"], 1)
