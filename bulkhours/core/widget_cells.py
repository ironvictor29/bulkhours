import IPython

from .tools import md
from .widget_base import WidgetBase
from .cell_parser import CellParser
from . import equals


class WidgetCode(WidgetBase):
    widget_id = "bkcode"
    widget_comp = "sc"

    def init_widget(self):
        return None

    def get_answer(self):
        return self.cell_source

    def execute_raw_cell(self, bbox, output):
        student_data = CellParser.crunch_data(cinfo=self.cinfo, user=self.cinfo.user, data=self.cell_source)

        if student_data.do_run_evaluation():
            teacher_data = student_data
            # teacher_data = CellParser.crunch_data(self.cinfo, user="solution", data=None)
            score = equals.evaluate_student(student_data, teacher_data, raw=False)
            print(f"Estimated score: {score}")
        else:
            with output:
                IPython.get_ipython().run_cell(student_data.get_code("main_execution"))
        WidgetBase.execute_raw_cell(self, bbox, output)


class WidgetScript(WidgetCode):
    widget_id = "bkscript"

    def fix_woptions(self, code):
        ncode = ""
        for l in code.splitlines():
            if "%evaluation_cell_id" in l:
                if "-w" not in l:
                    l += " -w lw"
            ncode += l + "\n"
        return ncode

    def execute_raw_cell(self, bbox, output):
        local_data = CellParser.crunch_data(self.cinfo, user=self.cinfo.user, data=self.cell_source)

        local_data.minfo["main_execution"]["code"] = self.fix_woptions(local_data.minfo["main_execution"]["code"])

        if local_data.do_run_evaluation():
            teacher_data, student_data = local_data, local_data
            # teacher_data = CellParser.crunch_data(self.cinfo, user="solution", data=None)
            # student_data = CellParser.crunch_data(self.cinfo, user=self.cinfo.user, data=self.cell_source)

            score = equals.evaluate_student(student_data, teacher_data, raw=False)
            print(f"Estimated score: {score}")
        else:
            with output:
                IPython.get_ipython().run_cell(local_data.get_code("main_execution"))
        WidgetBase.execute_raw_cell(self, bbox, output)


class WidgetMarkdown(WidgetCode):
    widget_id = "markdown"

    def display_correction(self, student_data, teacher_data, output=None):
        md(header=f"Correction ({self.cinfo.cell_id})", mdbody=teacher_data["answer"])

    def execute_raw_cell(self, bbox, output):
        IPython.display.display(IPython.display.Markdown(self.cell_source))
        WidgetBase.execute_raw_cell(self, bbox, output)


class WidgetFormula(WidgetCode):
    widget_id = "formula"

    def display_correction(self, student_data, teacher_data, output=None):
        with output:
            md(header=f"Correction ({self.cinfo.cell_id})")
        IPython.display.display(IPython.display.Markdown("$" + teacher_data["answer"] + "$"))

    def execute_raw_cell(self, bbox, output):
        with output:
            IPython.display.display(IPython.display.Markdown("$" + self.cell_source + "$"))
            print("$" + self.cell_source[:-1] + "$")
        WidgetBase.execute_raw_cell(self, bbox, output)
