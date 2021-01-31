from PyInquirer import prompt


def get_user_selected_item(message, choices):
    """Prompts the user for which item they would like to pick from a list."""
    question = {
        "type": "list",
        "name": "choice",
        "message": message,
        "choices": choices,
    }
    return prompt(question)["choice"]
