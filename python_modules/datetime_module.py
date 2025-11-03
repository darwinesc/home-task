from datetime import datetime

# Validate datetime %Y-%m-%d column
def validateDate(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
    
# Validate datetime format %Y-%m-%dT%H:%M:%S.%f column
def validateDatetime(valor):
    try:
        datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S.%f")
        return True
    except (ValueError, TypeError):
        return False