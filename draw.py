from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go

def drawBachart(worst_score,best_score, my_countries_index_dict): 
# Make plotly work with Jupyter notebook
    init_notebook_mode()
    x= list(my_countries_index_dict.keys())
    y=list(my_countries_index_dict.values())
    best_score_ref= go.Scatter(
        x =x,
        y = [best_score for i in x],
        name = 'Best score',
        line = dict(
            color = "green",
            width = 1,
         dash = 'dash')
    )
    worst_score_ref= go.Scatter(
        x = x,
        y = [worst_score for i in x],
        name = 'Worst score',
        line = dict(
            color = "red",
            width = 1,
            dash = 'dash')
   )

    bar=go.Bar(x=x, y=y, width = 0.4, name=False, showlegend=False)
    data=[bar,best_score_ref,worst_score_ref]

    layout=go.Layout(title="Fragility Index")
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
       
def drawWorldMap(all_countries_codes_index_value):
    data = [
        dict(
            type = 'choropleth',
            locations = list(all_countries_codes_index_value.keys()),
            z=[value[0] for value in all_countries_codes_index_value.values()],
            text =[value[1] for value in all_countries_codes_index_value.values()],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.9
            ) ),
            colorbar = dict(
            autotick = False,
            title = 'Index Value'),
        )
    ] 

    layout = dict(
        title = 'Frigile State Index',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    iplot( fig, validate=False, filename='d3-world-map' )