import pandas as pd
import subprocess
import os

def convert_to_latex(df: pd.DataFrame, output_file_path: str):

    all_tables_content = []

    column_groups = ["adversarial_strategy_test", "k"]
    index_groups = ["model", "adversarial_strategy_train"]

    for attribute in ["win_rate", "tie_rate", "loss_rate"]:

        # preprocess dataframes
        grouped = df.groupby(index_groups + column_groups)[attribute].mean().reset_index()
        pivoted = grouped.pivot(index=index_groups, columns=column_groups, values=attribute)
        pivoted_formatted = pivoted.map(lambda x: f"{x:.3f}")
        
        # define column specs
        test_strategies = pivoted.columns.get_level_values(0).unique().tolist()
        k_values = pivoted.columns.get_level_values(1).unique().tolist()
        num_k = len(k_values)
        num_test_strategies = len(test_strategies)
        num_data_cols = num_test_strategies * num_k
        column_spec = "ll|" + "c" * num_data_cols
        
        # construct header rows
        header_1_parts = ["\\multicolumn{2}{c|}{}"]
        for strategy in test_strategies:
            header_1_parts.append(f"\\multicolumn{{{num_k}}}{{c}}{{\\textbf{{{strategy}}}}}\n")

        header_1_base = " & ".join(header_1_parts).strip() + " \\\\"
        cmidrule_parts = []
        current_col = 3
        for _ in test_strategies:
            end_col = current_col + num_k - 1
            cmidrule_parts.append(f"\\cmidrule(lr){{{current_col}-{end_col}}}")
            current_col = end_col + 1
        header_1 = header_1_base + " " + "".join(cmidrule_parts)
        header_2_parts = ["\\textbf{Model}", "\\textbf{Training}"] # The two index columns
        for _ in test_strategies:
            header_2_parts.extend([f"{{$k={k}$}}" for k in k_values])
        header_2 = " & ".join(header_2_parts) + " \\\\ \\midrule"
        
        # construct table content
        latex_output = []
        col_order = [(c, k) for c in test_strategies for k in k_values]
        prev_model = None
        for (model, train_strategy) in pivoted_formatted.index:
            is_new_model = (model != prev_model)
            if is_new_model and prev_model is not None:
                latex_output.append("\\midrule")
            row_parts = []
            if is_new_model:
                row_parts.append(f"\\textbf{{{model}}}")
            else:
                row_parts.append("") 
            row_parts.append(f"\\multicolumn{{{1}}}{{{'|l|'}}}{{\\textit{{{train_strategy}}}}}")
            flat_row = [pivoted_formatted.loc[(model, train_strategy), (c, k)] for c, k in col_order]
            row_parts.extend(flat_row)
            latex_output.append(" & ".join(row_parts) + " \\\\")
            
            prev_model = model

        table_content = "\n".join(latex_output)

        # assemble Single Table
        single_table = f"""
\\subsection*{{{attribute.replace('_', '\\_')}}}
\\begin{{table}}[ht]
    \\centering
    \\begin{{tabular}}{{{column_spec}}}
        \\toprule
        {header_1}
        {header_2}
{table_content}
        \\bottomrule
    \\end{{tabular}}
\\end{{table}}
"""
        all_tables_content.append(single_table)
        
    # assemble Full Document
    full_latex = f"""\\documentclass{{article}}
\\usepackage{{booktabs}}
\\usepackage{{amsmath}}
\\usepackage[a4paper, margin=1in]{{geometry}}
\\usepackage{{times}}

\\begin{{document}}
\\section*{{Combined Experimental Results}}
{chr(10).join(all_tables_content)}

\\end{{document}}"""

    # write to File
    with open(output_file_path, 'w') as f:
        f.write(full_latex)

def render_latex_table(input_file_path: str, output_file_path: str):
    
    input_dir = os.path.dirname(input_file_path) or '.'
    input_filename = os.path.basename(input_file_path)
    command = [
        'pdflatex',
        '-interaction=nonstopmode',
        '-output-directory', input_dir,
        input_file_path
    ]

    subprocess.run(
        command,
        cwd=input_dir,
        check=True,
        capture_output=True,
        text=True
    )

    generated_pdf_name = os.path.splitext(input_filename)[0] + '.pdf'
    generated_pdf_path = os.path.join(input_dir, generated_pdf_name)
    os.replace(generated_pdf_path, output_file_path)
        
    aux_files = [f for f in os.listdir(input_dir) if f.startswith(os.path.splitext(input_filename)[0]) and f != os.path.basename(output_file_path)]
    extensions_to_remove = ['.aux', '.log', '.toc', '.out', '.nav', '.snm', '.dvi', '.gz']
    for filename in aux_files:
        if any(filename.endswith(ext) for ext in extensions_to_remove):
            os.remove(os.path.join(input_dir, filename))