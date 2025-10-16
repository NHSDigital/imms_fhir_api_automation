import random

def get_text(text_str: str) -> str:
    match text_str:
        case "missing":
            return None
        case "empty":
            return ""
        case "number":
            return random.randint(0, 9)
        case "gender_code":
            return "1"
        case "random_text":
            return "random"
        case "white_space":
            return " "
        case _:
            raise ValueError(f"Unknown date type: {text_str}")