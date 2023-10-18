import jwt ,datetime


def create_access_token(id,email,password):
    # return jwt.encode
    return jwt.encode({
        'user_id': id,
        'email': email,
        'password':password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days= 1),
        'iat': datetime.datetime.utcnow()
    },'access_token',algorithm = 'HS256')