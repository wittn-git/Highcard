import pandas as pd
import subprocess
import os

def convert_to_latex(df: pd.DataFrame, output_file_path: str):
    attributes = ["W", "T", "L"]
    all_tables_content = []

    for attribute in attributes:

        # process dataframes
        grouped = df.groupby(["model", "adversarial_strategy", "k"])[attribute].mean().reset_index()
        pivoted = grouped.pivot(index="model", columns=["adversarial_strategy", "k"], values=attribute)
        pivoted_formatted = pivoted.map(lambda x: f"{x:.3f}")
        
        # get column specifications
        adversarial_strategies = pivoted.columns.get_level_values(0).unique().tolist()
        k_values = pivoted.columns.get_level_values(1).unique().tolist()
        num_k = len(k_values)
        num_cols = 1 + len(adversarial_strategies) * num_k
        column_spec = "l" + "c" * (num_cols - 1)
        
        # construct headers
        header_1_parts = ["\\multicolumn{1}{c}{\\textbf{Model}}"]
        for strategy in adversarial_strategies:
            header_1_parts.append(f"\\multicolumn{{{num_k}}}{{c}}{{\\textbf{{{strategy}}}}}\n")
        header_1_base = " & ".join(header_1_parts) + " \\\\" 
        cmidrule_parts = []
        current_col = 2 
        for _ in adversarial_strategies:
            end_col = current_col + num_k - 1
            cmidrule_parts.append(f"\\cmidrule(lr){{{current_col}-{end_col}}}")
            current_col = end_col + 1
        header_1 = header_1_base + " " + "".join(cmidrule_parts)
        header_2_parts = [""]
        for _ in adversarial_strategies:
            header_2_parts.extend([f"{{$k={k}$}}" for k in k_values])
        header_2 = " & ".join(header_2_parts) + " \\\\ \\midrule\n"

        # construct table content
        latex_output = []
        col_order = [(c, k) for c in adversarial_strategies for k in k_values]
        for model in pivoted_formatted.index:
            row_parts = [model]
            flat_row = [pivoted_formatted.loc[model, (c, k)] for c, k in col_order]
            row_parts.extend(flat_row)
            latex_output.append(" & ".join(row_parts) + " \\\\")
        table_content = "\n".join(latex_output)

        # assemble full table
        single_table = f"""
\\subsection*{{{attribute}}}
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
    
    # assemble full document
    full_latex = f"""\\documentclass{{article}}
\\usepackage{{booktabs}}
\\usepackage{{amsmath}}

\\begin{{document}}

\\section*{{Combined Experimental Results}}
{chr(10).join(all_tables_content)}

\\end{{document}}"""

    # write to file
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