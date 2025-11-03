import re

# Validate a sku value
def validateSku(value):
    try:
        pattern = r'^[A-Za-z0-9]{3}-\d{8}$' # Regex for sku
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False
    
# Validate a Product title value
def validateProductTitle(value):
    try:
        pattern = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$'
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False
    
# Validate a currency value
def validateCurrency(value):
    try:
        pattern = r'^[A-Za-z0-9]{3}$' # Regex for sku
        return bool(re.fullmatch(pattern, str(value)))
    except (ValueError, TypeError):
        return False