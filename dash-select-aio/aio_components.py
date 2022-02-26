# Modified from https://dash.plotly.com/all-in-one-components

from dash import Dash, Output, Input, State, html, dcc, callback, clientside_callback, MATCH
import uuid

# All-in-One Components should be suffixed with 'AIO'
class SelectWithMemoryAIO(html.Div):  # html.Div will be the "parent" component

    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        label = lambda aio_id: {
            'component': 'SelectWithMemoryAIO',
            'subcomponent': 'label',
            'aio_id': aio_id
        }
        select = lambda aio_id: {
            'component': 'SelectWithMemoryAIO',
            'subcomponent': 'select',
            'aio_id': aio_id
        }
        storage = lambda aio_id: {
            'component': 'SelectWithMemoryAIO',
            'subcomponent': 'storage',
            'aio_id': aio_id
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        header,
        select_props={},
        storage_props={},
        aio_id=None,
        storage_visible=False
    ):
        # Allow developers to pass in their own `aio_id` if they're
        # binding their own callback to a particular component.
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Merge user-supplied properties into default properties
        select_props = select_props.copy()  # copy the dict so as to not mutate the user's dict
        #if 'options' not in dropdown_props:
        #    dropdown_props['options'] = [{'label': i, 'value': i} for i in colors]
        #dropdown_props['value'] = dropdown_props['options'][0]['value']

        # Merge user-supplied properties into default properties
        storage_props = storage_props.copy()  # copy the dict so as to not mutate the user's dict
        #if 'style' not in markdown_props:
        #    markdown_props['style'] = {'color': dropdown_props['value']}
        #if 'children' not in markdown_props:
        #    markdown_props['children'] = text

        if 'options' in select_props:
            opts = [html.Option(c) for c in select_props['options'] if c]
            del select_props['options']
        else:
            opts = []

        if storage_visible:
            storage_style=dict(display="block")
        else:
            storage_style=dict(display="none")
        print(storage_visible, storage_style, storage_props)
        # Define the component's layout
        super().__init__([  # Equivalent to `html.Div([...])`
            html.Label(header, id=self.ids.label(aio_id)),
            html.Select(opts, id=self.ids.select(aio_id), **select_props),
            dcc.Input(id=self.ids.storage(aio_id), style=storage_style, **storage_props)
        ])

    clientside_callback(
        """
        function(n, id) {
            var id = JSON.stringify(id);
            var items = document.getElementById(id).selectedOptions;
            var out = [];
            for (let i=0; i<items.length; i++) {
                out.push(items[i].value);
            };
            return out.join()
        }
        """,
        Output(ids.storage(MATCH), 'value'),
        [Input(ids.select(MATCH), 'n_clicks'),
        Input(ids.select(MATCH), 'id')]
    )

if __name__ == "__main__":
    pass