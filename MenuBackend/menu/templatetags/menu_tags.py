from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using a key.
    
    Args:
        dictionary: The dictionary to get the item from
        key: The key to look up
        
    Returns:
        The value from the dictionary if the key exists
    """
    return dictionary.get(str(key)) 