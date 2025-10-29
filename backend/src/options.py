import os

def get_model_dir():
    work_dir = os.getcwd()
    model_dir = os.path.join(work_dir, "training", "models", "selected")
    return model_dir

def get_card_model_dir(card_count : int) -> str:
    model_dir = get_model_dir()
    card_model_dir = os.path.join(model_dir, str(card_count))
    return card_model_dir

def list_card_counts() -> list[int]:
    model_dir = get_model_dir()
    card_options = os.listdir(model_dir)
    return [int(card_count) for card_count in card_options]

def list_model_options(card_count : int) -> list[str]:
    card_model_dir = get_card_model_dir(card_count)
    model_options = os.listdir(card_model_dir)
    return [model.split("-")[0] for model in model_options]

def get_model_path(card_count : int, model_name : str) -> str:
    card_model_dir = get_card_model_dir(card_count)
    files = os.listdir(card_model_dir)
    for file in files:
        if file.startswith(model_name):
            return os.path.join(card_model_dir, file)
    raise FileNotFoundError(f"Model {model_name} not found for card count {card_count}")