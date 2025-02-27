import IPython
import io
import ipywidgets
from contextlib import redirect_stdout
from .cell_parser import CellParser


class CellContext:
    """This context cell contains cell executions:
    - Two are defined by default: 'student' or 'teacher'
    When using the correction code, the stdout and answer are filled
    """

    @property
    def stdout(self):
        return False

    @property
    def answer(self):
        return False

    @property
    def data(self):
        return 3

    @property
    def stdout2(self):
        return True


def run_cell(code, stdout=True):
    if (ipp := IPython.get_ipython()) is None:
        print(f"No IPython instance found:\n{code}")
        return

    if not stdout:
        with redirect_stdout(f := io.StringIO()):
            run_cell(code)
            return f.getvalue().split()

    ipp.run_cell(code)


def generate_empty_context(context):
    run_cell(
        f"""class CellContext:
    @property
    def stdout2(self):
        return False
                                   
{context} = CellContext()
"""
    )


def add_variables_in_contexts(cell_id, configs):
    for context in ["student", "teacher"]:
        run_cell(f"from argparse import Namespace\n{context}.{cell_id} = Namespace(**{configs})")


def generate_context_code(code, context):
    code = CellParser.remove_meta_functions_execution(code)
    ncode = f"\n\nclass C{context}:\n"
    for l in code.splitlines():
        ncode += f"    {l}\n"

    ncode += f"{context.lower()} = C{context}\n"
    return ncode


def generate_context_code(code, context):
    code = CellParser.remove_meta_functions_execution(code)
    ncode = f"\n\nclass C{context}:\n"
    for l in code.splitlines():
        ncode += f"    {l}\n"

    ncode += f"{context.lower()} = C{context}\n"
    return ncode


def build_context(data, code_label, context, do_evaluate, do_debug=False, use_context=True):
    output = ipywidgets.Output()
    if code_label not in data.minfo:
        return output

    code = CellParser.remove_meta_functions_execution(data.get_code(code_label))

    generate_empty_context(context)
    if not (code is None or len(code.replace("\n", "").replace(" ", "")) == 0):
        fcode = code if not use_context or "compile_and_exec" in code else generate_context_code(code, context)

        output_return = "None"
        if do_debug:
            print(f"Execute context {context}/{code_label}/{data.minfo['source']}")
            run_cell(fcode)
        else:
            with output:
                if do_evaluate:
                    with redirect_stdout(f := io.StringIO()):
                        run_cell(fcode)
                        output_return = f.getvalue()

    run_cell(f'{context}.stdout="""{output_return}"""')

    if data.is_cell_type():
        run_cell(f'{context}.answer={data["answer"]}')
    return output
