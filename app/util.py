from flask_jwt_extended import  verify_jwt_in_request, get_jwt_claims
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {'status': 'FORBIDDEN'}, 403, {'Content-Type': 'application/json'}
        else:
            return fn(*args, **kwargs)
    return wrapper