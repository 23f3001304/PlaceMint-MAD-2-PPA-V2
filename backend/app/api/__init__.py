"""Register every API blueprint under /api.

Blueprints are added here as each feature phase lands; keeping registration in
one place makes the app's surface easy to scan.
"""


def register_api(app):
    _register_core(app)
    _register_admin(app)
    _register_company(app)
    _register_student(app)
    _register_directory(app)


def _register_directory(app):
    from app.api.directory import directory_bp

    app.register_blueprint(directory_bp, url_prefix="/api/directory")


def _register_core(app):
    from app.api.auth.routes import auth_bp
    from app.api.documents import documents_bp
    from app.api.exports import exports_bp
    from app.api.health import health_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    app.register_blueprint(exports_bp, url_prefix="/api/exports")


def _register_admin(app):
    from app.api.admin.applications import admin_apps_bp
    from app.api.admin.dashboard import admin_dash_bp
    from app.api.admin.drives import admin_drives_bp
    from app.api.admin.moderation.companies import admin_companies_bp
    from app.api.admin.moderation.students import admin_students_bp
    from app.api.admin.moderation.users import admin_users_bp

    app.register_blueprint(admin_dash_bp, url_prefix="/api/admin")
    app.register_blueprint(admin_companies_bp, url_prefix="/api/admin/companies")
    app.register_blueprint(admin_students_bp, url_prefix="/api/admin/students")
    app.register_blueprint(admin_users_bp, url_prefix="/api/admin/users")
    app.register_blueprint(admin_drives_bp, url_prefix="/api/admin/drives")
    app.register_blueprint(admin_apps_bp, url_prefix="/api/admin/applications")


def _register_company(app):
    from app.api.company.applications import company_apps_bp
    from app.api.company.drives import company_drives_bp
    from app.api.company.overview import company_overview_bp

    app.register_blueprint(company_overview_bp, url_prefix="/api/company")
    app.register_blueprint(company_drives_bp, url_prefix="/api/company/drives")
    app.register_blueprint(company_apps_bp, url_prefix="/api/company/applications")


def _register_student(app):
    from app.api.student.applications import student_apps_bp
    from app.api.student.drives import student_drives_bp
    from app.api.student.profile import student_profile_bp

    app.register_blueprint(student_profile_bp, url_prefix="/api/student/profile")
    app.register_blueprint(student_drives_bp, url_prefix="/api/student/drives")
    app.register_blueprint(student_apps_bp, url_prefix="/api/student/applications")
