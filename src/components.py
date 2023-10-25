from dash import dcc, html, dash_table


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


def description_oakvar():
    """Create a description of OakVar
    
    Returns
    -------
    A div containing dashboard title and information
    """
    return html.Div(id = 'description_init',
                    children=[
                        html.H3('A Genomic Variant Analysis Platform'),
                    ])


def dropdown_basechrom(dataframe):
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

def annotation_table(dataframe):
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
