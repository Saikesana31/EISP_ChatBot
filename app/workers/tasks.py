"""
app/workers/tasks.py — Celery background tasks for the Employee Agent module.

Celery tasks:visa_expiry_scan (nightly 06:00)
             lca_deadline_scan (06:15), document_expiry_scan (06:30)
             timesheet_missing_scan (Mon+Wed 08:00)
             payroll_anomaly_scan (1st of month), invoice_overdue_scan (Mon)



"""