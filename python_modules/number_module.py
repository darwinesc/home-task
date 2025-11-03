import uuid


# Validate uuid column
def validateId(x):
    try:
        # Intenta convertir a UUID (versión 4 por defecto, pero puede ser flexible)
        uuid_obj = uuid.UUID(str(x))
        return True
    except (ValueError, TypeError):
        return False
    
# Validate a number value     
def validateNumber(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False