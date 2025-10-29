import os

def get_model_dir():
    return os.path.join("training", "models", "selected")

def get_model_card_dir(card_count: int) -> str:
    model_dir = get_model_dir()
    model_card_dir = os.path.join(model_dir, str(card_count))
    return model_card_dir

def get_model_card_adversarial_dir(card_count: int, adversarial : str) -> str:
    model_card_dir = get_model_card_dir(card_count)
    model_card_adversarial_dir = os.path.join(model_card_dir, adversarial)
    return model_card_adversarial_dir

def list_card_counts() -> list[int]:
    model_dir = get_model_dir()
    card_options = os.listdir(model_dir)
    return [int(card_count) for card_count in card_options]

def list_adversarial_options(card_count: int) -> list[str]:
    model_card_dir = get_model_card_dir(card_count)
    adversarial_options = os.listdir(model_card_dir)
    return adversarial_options

def list_model_options(card_count: int, adversarial: str) -> list[str]:
    model_card_adversarial_dir = get_model_card_adversarial_dir(card_count, adversarial)
    model_options = os.listdir(model_card_adversarial_dir)
    return [model.split("_")[0] for model in model_options]

def get_model_path(card_count: int, adversarial: str, model_name: str) -> str:
    model_card_adversarial_dir = get_model_card_adversarial_dir(card_count, adversarial)
    files = os.listdir(model_card_adversarial_dir)
    for file in files:
        if file.startswith(model_name):
            return os.path.join(model_card_adversarial_dir, file)
    raise FileNotFoundError(f"Model {model_name} not found for card count {card_count}")