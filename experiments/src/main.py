from experiments.src.latex import wl_to_tex, opt_to_tex, render_latex_table
from experiments.src.file_handling import get_filepath_result, get_filepath_rendered
from experiments.src.experimentation import run_wl_experiments, run_opt_experiments

if __name__ == "__main__":

    # number of evaluation games per configuration and number of repeated games per evaluation
    n_eval_games, n_repeated_games = 10, 100
    
    # run experiments for win/loss data
    df = run_wl_experiments(n_eval_games, n_repeated_games)
    filepath_wl_result = get_filepath_result("wl") 
    df.to_csv(filepath_wl_result, index=False)
    filepath_wl_rendered_tex, filepath_wl_rendered_pdf = get_filepath_rendered(filepath_wl_result, "tex"), get_filepath_rendered(filepath_wl_result, "pdf")
    wl_to_tex(df, filepath_wl_rendered_tex)
    # render_latex_table(file_path_rendered_tex, file_path_rendered_pdf)

    # max k value for optimal strategy experiments
    k_limit = 5

    # run experiments for comparison to optimal strategies
    df = run_opt_experiments(k_limit)
    filepath_opt_result = get_filepath_result("opt")
    df.to_csv(filepath_opt_result, index=False)
    filepath_opt_rendered_tex, filepath_opt_rendered_pdf = get_filepath_rendered(filepath_opt_result, "tex"), get_filepath_rendered(filepath_opt_result, "pdf")
    # opt_to_tex(df, filepath_opt_rendered_tex)
    # render_latex_table(filepath_opt_rendered_tex, filepath_opt_rendered_pdf)
