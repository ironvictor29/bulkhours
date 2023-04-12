import IPython
import ipywidgets
import time




class SwitchButton:
    def __init__(
        self,
        label,
        on_description,
        on_description_fr,
        tmp_description,
        tmp_description_fr,
        off_description,
        off_description_fr,
        sleep_on=None,
    ) -> None:
        self.label = label
        self.en = dict(on=on_description, warning=tmp_description, off=off_description)
        self.fr = dict(on=on_description_fr, warning=tmp_description_fr, off=off_description_fr)
        self.show_answer, self.in_french = True, False
        self.d = self.fr if self.in_french else self.en
        self.sleep_on = sleep_on

    def update_style(self, button, style=None):
        if style in ["warning", "on", "off"]:
            button.description, button.button_style = self.d[style]["description"], self.d[style]["button_style"]
        elif style == "danger":
            button.description, button.button_style = "Erreur" if self.in_french else "Error", "danger"
        button.disabled = style in ["warning", "danger"]
        button.icon = "fa-spinner fa-pulse fa-1x fa-fw" if style in ["warning"] else ""

    def g(self, in_french):
        self.in_french = in_french
        self.d = self.fr if self.in_french else self.en
        args = self.d["on"]
        args.update(
            dict(
                flex_flow="column",
                align_items="stretch",
                tooltip=args["description"],
                layout=ipywidgets.Layout(width="max-content"),
            )
        )
        return ipywidgets.Button(**args)

    def wait(self, show_answer, button, style="off", sleep=None):
        sleep = self.sleep_on if sleep is None else sleep
        if not sleep:
            return show_answer

        self.update_style(button, style=style)
        description = button.description
        for u in range(int(sleep)):
            d = sleep - u
            button.description = f"{d} " + description
            time.sleep(1)
        return True


sbuttons = [
    SwitchButton(
        "submit",
        dict(description="Send answer to corrector", button_style="primary"),
        dict(description="Envoyer au correcteur", button_style="primary"),
        dict(description="Operation in progress", button_style="warning"),
        dict(description="Operation en cours   ", button_style="warning"),
        dict(description="Answer sent to corrector", button_style="success"),
        dict(description="Correction envoyée", button_style="success"),
        sleep_on=4,
    ),
    SwitchButton(
        "correct",
        dict(description="Show correction", button_style="primary"),
        dict(description="Voir la correction", button_style="primary"),
        dict(description="Operation in progress", button_style="warning"),
        dict(description="Operation en cours   ", button_style="warning"),
        dict(description="Hide correction", button_style="danger"),
        dict(description="Cacher la correction", button_style="danger"),
    ),
    SwitchButton(
        "message",
        dict(description="Message from corrector", button_style="info"),
        dict(description="Message au correcteur", button_style="info"),
        dict(description="Operation in progress", button_style="warning"),
        dict(description="Operation en cours   ", button_style="warning"),
        dict(description="Hide message from corrector", button_style="warning"),
        dict(description="Cacher le message du correcteur", button_style="warning"),
    ),
    SwitchButton(
        "evaluate",
        dict(description="Save the grade", button_style="info"),
        dict(description="Sauvegarder la note", button_style="info"),
        dict(description="Operation in progress", button_style="warning"),
        dict(description="Operation en cours   ", button_style="warning"),
        dict(description="Grade saved", button_style="warning"),
        dict(description="Note sauvegardée", button_style="warning"),
    ),
    SwitchButton(
        "test",
        dict(description="Save And test", button_style="info"),
        dict(description="Sauver et tester", button_style="info"),
        dict(description="Operation in progress", button_style="warning"),
        dict(description="Operation en cours   ", button_style="warning"),
        dict(description="Saved and tested", button_style="success"),
        dict(description="Sauver et tester", button_style="success"),
        sleep_on=1,
    ),
]


def get_buttons_label():
    return [s.label for s in sbuttons]


def get_button(label):
    return [s for s in sbuttons if s.label == label][0]


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    if header:
        IPython.display.display(
            IPython.display.Markdown(
                f"<b><font face='FiraCode Nerd Font' size=4 color='{hc}'>{header} {icon}:<font></b>"
            )
        )

    if mdbody and len(mdbody) > 1:
        IPython.display.display(
            IPython.display.Markdown(f"<font face='FiraCode Nerd Font' size=4 color='{bc}'>{mdbody}<font>")
        )
    if 0 and mdbody and len(mdbody) > 1:
        IPython.display.display(IPython.display.Markdown(mdbody))
    if rawbody and len(rawbody) > 1:
        print(rawbody)
    if codebody and len(codebody) > 1:
        IPython.display.display(IPython.display.Code(codebody))
