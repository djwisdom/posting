from typing import Iterable
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from posting.collection import FormItem
from posting.widgets.datatable import PostingDataTable
from posting.widgets.key_value import KeyValueEditor, KeyValueInput
from posting.widgets.variable_input import VariableInput


class FormTable(PostingDataTable):
    BINDINGS = [
        Binding("backspace", action="remove_row", description="Remove row"),
        Binding("space", action="toggle_row", description="Enable/disable row"),
    ]

    def on_mount(self):
        self.fixed_columns = 2
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.row_disable = True
        self.add_columns("Key", "Value")

    def to_model(self) -> list[FormItem]:
        form_data: list[FormItem] = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            checkbox: PostingDataTable.Checkbox = row[0]
            form_data.append(FormItem(name=row[1], value=row[2], enabled=checkbox.checked))
        return form_data


class FormEditor(Vertical):
    """An editor for form body data."""

    def compose(self) -> ComposeResult:
        yield KeyValueEditor(
            FormTable(),
            KeyValueInput(
                VariableInput(placeholder="Key"),
                VariableInput(placeholder="Value"),
            ),
            empty_message="There is no form data.",
        )

    def to_model(self) -> list[FormItem]:
        return self.query_one(FormTable).to_model()

    def replace_all_rows(self, rows: Iterable[tuple[str, str]]) -> None:
        self.query_one(FormTable).replace_all_rows(rows)
