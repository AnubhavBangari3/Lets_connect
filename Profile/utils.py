import uuid

def get_unicode():
    code=str(uuid.uuid4())[:8].replace("-","")
    
    return code