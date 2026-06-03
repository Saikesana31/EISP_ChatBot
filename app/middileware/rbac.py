"""

app/middileware/rbac.py — Role-Based Access Control middleware for FastAPI WebSocket endpoints.

* get_current_user dependency decodes JWT, checks Redis blacklist, and returns user info. (raise 401)
* requires_role decorator checks if the user has the required role for the endpoint.( raise 403)
* require_min_role decorator checks if the user has at least the required role level 
                                    (admin > hr > manager > employee).( raise 403)
* Rolefilter defines the role hierarchy and levels.


"""