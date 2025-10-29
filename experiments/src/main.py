from experiments.src.latex import convert_to_latex, render_latex_table
from experiments.src.file_handling import get_filepath_result, get_filepath_rendered
from experiments.src.experimentation import run_wl_experiments

if __name__ == "__main__":

    # number of evaluation games per configuration
    n_eval_games, n_repeated_games = 10, 100
    
    # run experiments for win/loss data
    df = run_wl_experiments(n_eval_games, n_repeated_games)
    
    # save results
    file_path_result = get_filepath_result() 
    df.to_csv(file_path_result, index=False)

    # render latex table
    file_path_rendered_tex, file_path_rendered_pdf = get_filepath_rendered(file_path_result, "tex"), get_filepath_rendered(file_path_result, "pdf")
    convert_to_latex(df, file_path_rendered_tex)
    render_latex_table(file_path_rendered_tex, file_path_rendered_pdf)

    # run experiments for comparison to optimal strategies
    # TODO implement
