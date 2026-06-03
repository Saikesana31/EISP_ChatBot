"""

app/api/employee_endpoints.py — all API routes related to employee management (CRUD, listing, etc)

 websocket ha
* GET  /employees                                  List (role-filtered)
* GET  /employees/{id}                             Single profile
* GET  /employees/me/profile                       Own profile shortcut
* GET  /employees/{id}/direct-reports
* GET  /employees/analytics/headcount
* GET  /employees/analytics/new-joiners
* GET  /employees/search/query
* PATCH /employees/{id}/status
* GET  /employees/me/alerts
* GET  /employees/chat/{sid}/history
* WS   /employees/chat/{sid}   ←                  THE STREAMING CHAT (all 7 agents)

"""