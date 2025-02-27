import sys
import IPython
import ipywidgets

from .. import core
from . import answers

DEFAULT_NOTE = -1


def get_alias_name(cuser):
    if "@" in cuser:
        auser = cuser.split("@")[0].split(".")
        return auser[0].capitalize() + "." + auser[1][0]
    return cuser


def show_answer(cuser, answer, style=None):
    hc = "green" if cuser == "solution" else "red"
    codebody = "google.colab" in sys.modules and style != "dark"
    cuser = get_alias_name(cuser)

    # Show code
    core.tools.md(header=f"Code ({cuser})", hc=hc)
    core.tools.md(**{"codebody" if codebody else "rawbody": answer["answer"]})

    # Execute code
    core.tools.md(header=f"Execution ({cuser})", hc=hc, icon="💻")
    core.tools.eval_code(answer["answer"])


def create_evaluation_buttonanswer(cell_id, cuser, answer):
    config = core.tools.get_config()

    language = config["global"]["language"]
    label = core.tools.html(get_alias_name(cuser), size="6", color="#4F4F4F")
    abuttons = core.buttons.get_buttons_list(label="", language=language, user="solution")
    output = ipywidgets.Output()

    default_note = answer["note"]

    widget = ipywidgets.FloatSlider(
        min=0,
        max=10,
        value=default_note,
        step=0.5,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format=".1f",
    )
    widget.style.handle_color = "lightblue"

    def sevaluate(data, output):
        with output:
            output.clear_output()
            answers.update_note(cell_id, cuser, widget.value)

    def sevaluate2(b):
        return core.buttons.update_button(b, abuttons["e"], output, None, sevaluate)

    abuttons["e"].b.on_click(sevaluate2)

    IPython.display.display(ipywidgets.HBox([label, widget, abuttons["e"].b]), output)


def evaluate(cell_id, user="NEXT", show_correction=False, style=None, **kwargs):
    cell_answers = answers.get_answers(cell_id, **kwargs)
    config = core.tools.get_config(is_new_format=True)

    nuser, did_find_answer = user, False
    for cuser, answer in cell_answers.items():
        if (user == "NEXT" and answer["note"] == DEFAULT_NOTE) or user == cuser:
            nuser, did_find_answer = cuser, True
            if show_correction and "solution" in cell_answers:
                out1 = ipywidgets.Output(layout={"width": "50%"})
                out2 = ipywidgets.Output(layout={"width": "50%"})
                tabs = ipywidgets.HBox([out1, out2])

                with out1:
                    show_answer(cuser, answer, style=style)
                with out2:
                    # bulkhours.c.set_style(out2, "sol_background")
                    show_answer("solution", cell_answers["solution"], style=style)

                out = ipywidgets.Output(layout={"border": "1px solid #CFCFCF", "width": "100%"})
                # bulkhours.c.set_style(out, "cell_background")
                with out:
                    create_evaluation_buttonanswer(cell_id, cuser, answer)

                IPython.display.display(ipywidgets.VBox([tabs, out]))

            else:
                show_answer(cuser, answer)
                create_evaluation_buttonanswer(cell_id, cuser, answer)

    if not did_find_answer:
        core.tools.md(
            mdbody=f"Pas de réponse disponible pour {nuser}"
            if config.language == "fr"
            else f"{nuser} answer is not available"
        )
