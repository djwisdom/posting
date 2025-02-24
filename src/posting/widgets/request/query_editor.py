from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Input
from posting.collection import QueryParam

from posting.widgets.datatable import PostingDataTable
from posting.widgets.key_value import KeyValueEditor, KeyValueInput
from posting.widgets.variable_input import VariableInput


class ParamsTable(PostingDataTable):
    """
    The parameters table.
    """

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

    def watch_has_focus(self, value: bool) -> None:
        self._scroll_cursor_into_view()
        return super().watch_has_focus(value)

    def to_model(self) -> list[QueryParam]:
        params: list[QueryParam] = []
        # TODO - handle enabled/disabled...
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            checkbox: PostingDataTable.Checkbox = row[0]
            params.append(QueryParam(name=row[1], value=row[2], enabled=checkbox.checked))
        return params


class QueryStringEditor(Vertical):
    """
    The query string editor.
    """

    def compose(self) -> ComposeResult:
        yield KeyValueEditor(
            ParamsTable(),
            KeyValueInput(
                VariableInput(placeholder="Key", id="query-key-input"),
                VariableInput(placeholder="Value"),
                button_label="Add parameter",
            ),
            empty_message="There are no parameters.",
        )

    @property
    def query_key_input(self) -> Input:
        return self.query_one("#query-key-input", Input)
