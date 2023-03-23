import jwt
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_id = ""
        role = ""
        if "sub" in decoded_token:
            user_id = decoded_token["sub"]
        if "https://example.com/app_metadata" in decoded_token:
            role = decoded_token["https://example.com/app_metadata"]["roles"][0]
        return {"user_id": user_id,"role":role}
    except jwt.exceptions.DecodeError:
        return None
