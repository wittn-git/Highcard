import time
import os

def get_filepath_result() -> str:
    return f"experiments/results/results_{str(time.time()).replace('.', '-')}.csv"

def get_filepath_rendered(filepath_result : str, file_extension : str) -> str:
    filename_result = os.path.basename(filepath_result)
    filename_base, _ = os.path.splitext(filename_result)
    return f"experiments/renders/{filename_base}_rendered.{file_extension}"
