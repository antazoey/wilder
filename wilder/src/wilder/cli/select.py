from PyInquirer import prompt


def get_user_selected_resource(item_type, choices):
    """Prompts the user for which item they would like to pick from a list."""
    message = f"Please select a {item_type}."
    return get_user_selected_item(message, choices)


def get_user_selected_item(message, choices):
    """Prompts the user for which item they would like to pick from a list."""
    question = {
        "type": "list",
        "name": "choice",
        "message": message,
        "choices": choices,
    }
    return prompt(question)["choice"]
