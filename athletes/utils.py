from datetime import date


def calculate_age(birth_date: date, on_date: date) -> int:
    """
    Calculate athletes current age based on his birth data.
    """
    return (
        on_date.year
        - birth_date.year
        - ((on_date.month, on_date.day) < (birth_date.month, birth_date.day))
    )
