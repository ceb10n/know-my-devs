def snake_to_pascal(v: str) -> str:
    """Converts a string in snake_case to PascalCase.

    Args:
        v (str): The snake case string

    Raises:
        ValueError: In case the value is not a valid string

    Returns:
        str: The converted string
    """
    if not v or not isinstance(v, str):
        raise ValueError("Value must be a valid string")
    
    return v.replace("_", " ").title().replace(" ", "")