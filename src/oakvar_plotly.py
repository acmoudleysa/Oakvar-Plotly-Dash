from dash import Dash, html, Input, Output, callback
import oakvar as ov
import json
import components



# Importing the sqlite data as pandas dataframe
df = ov.get_df_from_db('../test.txt.sqlite').to_pandas()

#df.drop(labels=['base__all_mappings','clinvar__disease_refs'],inplace= True,axis = 1)

# Dropping some null columns
df.dropna(axis = 1, how = 'all', inplace = True)


# Initialize
app = Dash(__name__)

app.title = "OakVar"


app.layout = html.Div(children=[
    components.logo(),
    html.Div(children=[components.description_oakvar(), components.dropdown_basechrom(df)
    ],style={'width': '30%', 'display': 'inline-block','vertical-align':'top','background-color': 'rgb(250, 250, 250)','text-align': 'center', 'height': '100vh'}),
    html.Div(children=[*components.make_break(2),components.annotation_table(df),*components.make_break(2),components.table_select_data()
    ],style={'width': '70%', 'display': 'inline-block','background-color': 'rgb(240, 240, 240)', 'height': '100vh'})
],style={'width':'100%'})


@callback(Output(component_id='annotation_table', component_property='data'),
          Input(component_id='dropdown_base_chrom', component_property='value'))
def update_table(value):
    if value is None:
        return df.to_dict('records')
    else: 
        dff = df.copy(deep = True)
        dff = dff.loc[df.base__chrom == value]
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