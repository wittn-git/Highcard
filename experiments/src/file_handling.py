import time
import os

def get_filepath_result(suffix_str: StopIteration) -> str:
    # return f"experiments/results/results_{suffix_str}_{str(time.time()).replace('.', '-')}.csv"
    return f"experiments/results/results_{suffix_str}.csv"

def get_filepath_rendered(filepath_result: str, file_extension: str) -> str:
    filename_result = os.path.basename(filepath_result)
    filename_base, _ = os.path.splitext(filename_result)
    return f"experiments/renders/{filename_base}_rendered.{file_extension}"
