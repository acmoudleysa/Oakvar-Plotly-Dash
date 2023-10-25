from dash import Dash, dcc, html, Input, Output, callback, dash_table
import oakvar as ov
import json



# Importing the sqlite data as pandas dataframe
df = ov.get_df_from_db('test.txt.sqlite').to_pandas()
print(df)
#df.drop(labels=['base__all_mappings','clinvar__disease_refs'],inplace= True,axis = 1)


# Dropping some null columns
#df.dropna(axis = 1, how = 'all', inplace = True)


# Initialize
app = Dash(__name__)

app.title = "OakVar"
def make_break(num_breaks):
    br_list = [html.Br()]*num_breaks
    return  br_list

def logo():
    """Create OakVar logo
    Returns
    -------
    A div containing OakVar logo 
    """
    return html.Div(
                id='logo',
                children = [html.Img(src = 'assets/OakVar.png',style={'width': '40px', 'height': 'auto','margin':'5px 0px 0px 170px' })],style={'background-color':'white'})

def logo():
    """Create OakVar logo
    Returns
    -------
    A div containing OakVar logo
    """
    return html.Div(
                id='logo',
                style={'margin-left': '130px'},
                children=[html.Img(src='assets/OakVar.png',
                                    style={'width': '100px', 'height': 'auto'})])


def description_oakvar():
    """Create a description of OakVar
    
    Returns
    -------
    A div containing dashboard title and information
    """
    return html.Div(id='description_init',
                    children=[
                        html.H3('A Genomic Variant Analysis Platform'),
                    ])


def dropdown_basechrom(dataframe=df):
    """Create a dropdown menu along with description
    Parameters
    ----------
    df: annotation dataframe
    Returns
    -------
    A div containing dashboard title and information
    """


    return html.Div([
        html.P(['OakVar is a genomic variant interpretation platform. \
                             Genomic variants can be annotated with diverse annotation sources, stored in databases, \
                             queried with filter sets, written to reports in diverse formats, and visualized with graphical user interfaces.']),
        html.B('Select a base chromosome'),
        html.Div(dcc.Dropdown(id = 'dropdown_base_chrom', options = [{'label': str(i).capitalize(), 'value': i} for i in dataframe.base__chrom.unique()], value = None, searchable=True)
    ,style={'width': '50%', 'margin':'auto'})])


def annotation_table(dataframe=df):
    """Create a annotation data table
    
    Parameters
    ----------
    df: annotation dataframe
    Returns
    -------
    A div containing dashboard table
    """
    return html.Div(
        dash_table.DataTable(id = 'annotation_table',
                             cell_selectable=True,
                             columns=[{'id': c, 'name': str(c)} for c in dataframe.columns],
                             page_size=10,
                             style_table={'overflowX': 'auto'},
                             style_cell={'fontSize': '12px'},
                             row_selectable='single',style_as_list_view=True
                             ),style={'padding':'40px', 'width': '85%','margin':'auto','background-color':'white'}
    )

def table_select_data():
    return html.Div(id='table_data')


app.layout = html.Div(children=[
    logo(),
    html.Div(children=[description_oakvar(), dropdown_basechrom()
    ],style={'width': '30%', 'display': 'inline-block','vertical-align':'top','background-color': 'rgb(250, 250, 250)','text-align': 'center', 'height': '100vh'}),
    html.Div(children=[*make_break(2),annotation_table(),*make_break(2),table_select_data()
    ],style={'width': '70%', 'display': 'inline-block','background-color': 'rgb(240, 240, 240)', 'height': '100vh'})
],style={'width':'100%'})

@callback(Output(component_id='annotation_table', component_property='data'),
          Input(component_id='dropdown_base_chrom', component_property='value'))
def update_table(value):
    """Updating the table based on value selected from dropdown
    Parameters
    ----------
    value : str or None
        The value selected from the dropdown. If None, the function returns all records in the table

    Returns
    -------
    list of dict
        A list of dictionaries representing the records in the updated table.
    """
    if value is None:
        return df.to_dict('records')
    else: 
        dff=df.copy(deep=True)
        dff=dff.loc[df.base__chrom==value]
        return dff.to_dict('records')

@app.callback(
    Output('table_data', 'children'),
    Input('annotation_table', 'data'),
    Input('annotation_table', 'active_cell')
)

def print_it(data, select_data):
    if not select_data:
        return f"No cells selected {select_data}"
    
    cell_data = select_data

    return f'The data is: {cell_data}'


if __name__ == "__main__":
    app.run(debug = True)
    

# def print_it(data, select_data):
#     if not select_data:
#         return f"No cells selected {select_data}"
    
#     cell_data = json.dumps(select_data, indent=2)
#     row_index = select_data[0]['row']
#     column_index = select_data[0]['column']
#     selected_text = data[row_index][column_index]
#     return f'The data is: {cell_data} with text: {selected_text}'
