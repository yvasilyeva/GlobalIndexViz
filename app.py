import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
from fsi import fsi_index_name
from hdi import hdi_index_name
from db_util import get_index_value,get_percent_of_change, get_available_indexes_names,\
get_all_countries,get_index_years,get_index_countries_info,get_index_values,\
get_best_worst_index_value,get_country_info_for_value,get_index_id,get_country_id

import plotly.graph_objs as go

external_stylesheets = [{
	'rel':"stylesheet",
	'href':"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
	'integrity':"sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
	'crossorigin':"anonymous",
}]

app=dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True
colors = {
    'background': '#111111',
    'text': '#000519' #'#7FDBFF'
}
#id : index_name
index_names=get_available_indexes_names()
index_dropdown=html.Div(
	dcc.Dropdown(
	id='index-dropdown',
	options=[
		{'label': "{}".format(name.lower().capitalize(),name), 'value' : name}\
		 for name in index_names.values()
	],
	placeholder="Select an index...",
	searchable=True,
	multi=False
	),
	className='col-3'
)
country_dropdown=html.Div(
	dcc.Dropdown(
	id='country-dropdown',
	#option property will be added by callback function index_countries_values
    # options=[
    #    {'label': country_name, 'value' : info[1]} for country_name, info in index_countries_info.items()
    # ],
    #default values from the list
    value=[],
    multi=True,
    searchable=True,
    clearable=True,
    placeholder="Select a country...",
    #to disable dropdown set an option
    #dsabled=True
	),
	className='col-3'
)
year_dropdown=html.Div(
	dcc.Dropdown(
	id='year-dropdown',
	placeholder="Select a year...",
	#options will be added by call back function 
	#options=[
	#	{'label': year, 'value' : year} for year in years
	#],
	),
	className= 'col-3'
)
show_button=html.Div(
	[
	html.Button(
	id='show-button', 
	children='Show',
	n_clicks=0,
	className='btn btn-block btn-outline-primary'
	),
	],
	className='col-3'
	)
index_barchart=html.Div(
	dcc.Graph(
	id='index-barchart',
	#will be returned by callback function
	# figure={
	# 	'data' : data,
	# 	'layout' : layout
	# },
	),
	className='col-6'
)
line_chart=html.Div(
	dcc.Graph(
	id='line-chart',
	#will be returned by callback function
	 # figure={
	 # 	'data' : data,
	 # 	'layout' : layout
	 # },
	),
	className='col-6'
)             
index_map=html.Div(
	dcc.Graph(
	id='map-box',
	# figure={
	# 	'data' : [map_data],
	# 	'layout' : map_layout
	# },
	),
	className='col-6'
)
diff_year_dropdown=html.Div(
	dcc.Dropdown(
	id='diff-year-dropdown',
	placeholder="Select a year...",
	#options will be added by call back function 
	),
	id='diff-dropdown',
	className= 'col-7'
)
diff_year_text=html.Div(
	html.P('Select a year for comparison: ',style={'fontSize':18}),
	className= 'col-5',
	id='diff-year-text'
	)

diff_chart=html.Div(
	dcc.Graph(
	id='diff-chart',
	# figure={

	# }	
	),
	className='col'
	)

diff=html.Div(
	[html.Div(
		[diff_year_text,
		diff_year_dropdown
		],
		className= 'row',
		id='diff-div'
	),
	diff_chart,
	],
	className='col-6'
	)



app.layout=html.Div(children=[
	 html.H2(children='Global Indices Visualization',
	 	style={
	     'textAlign': 'center',
	     'color': colors['text']
         }
         ),

	 html.Div(children='''
	 	Visualization of global indeces related to GCERF.
	 	''',
	 	style={
         'textAlign': 'center',
         'color': colors['text']
     	}
	 	),
	 html.Div(
	 	[html.Div(
	 		[index_dropdown,
	 		country_dropdown,
	 		year_dropdown,
	 		show_button,
	 		],
 			className ='row'	
	 	),
	 	html.Div(
	 		[index_barchart,
	 		line_chart,
	 		],
	 		id='charts-div',
	 		className='row',
			style={'visibility':'hidden'}
		)
	 	],
	 	style={
	 	'padding': 30,
	 	}
	 ),
	 html.Div(
	 		[index_map,
	 		diff,
	 		],
	 		id='map-div',
	 		className='row',
			style={'visibility':'hidden'}
	 	)
 ],
 className='container-fluid'
 )
@app.callback(
     Output(component_id='country-dropdown', component_property='options'),
     [Input(component_id='index-dropdown', component_property='value')]
 )
def index_countries_values(index_name):
	if not index_name:
		return []	
	index_id=get_index_id(index_name)
	index_countries_info=get_index_countries_info(index_id)	
	return [
	{'label': country_name, 'value' : country_name}\
	for country_name, info in index_countries_info.items()
    ]
 	
@app.callback(
     Output(component_id='year-dropdown', component_property='options'),
     [Input(component_id='index-dropdown', component_property='value')]
)
def index_years_values(index_name):
	if not index_name:
			return []
	index_id=get_index_id(index_name)
	years=get_index_years(index_id)
	return [
	{'label': year, 'value' : year} for year in years
	]

@app.callback(Output('index-barchart', 'figure'),
  [Input('show-button', 'n_clicks')],
  [State('index-dropdown', 'value'),
   State('country-dropdown', 'value'),
   State('year-dropdown','value')])
def draw_best_score_ref_line(n_clicks, index_name,countries_list,year):
# draw a barchart
#country_name:[index_value,country_code]
	if not index_name:
		return {}
	index_id=get_index_id(index_name)
	countries_ids=[get_country_id(name) for name in countries_list]
	index_values_dic=get_index_values(index_id, year, countries_ids)
	y=list(index_values_dic.keys())
	x=[value[0] for value in index_values_dic.values()]
	best_score, worst_score=get_best_worst_index_value(index_name,index_id, year)
	best_score_countries_info_list=get_country_info_for_value(index_id, best_score, year)
	worst_score_countries_info_list=get_country_info_for_value(index_id, worst_score, year)
	#numeric values for y axis
	y_enum = list(range(len(y)))
	#define the width of a bar and and for how long to overhang it
	overhang = 0.5
	bar_width=0.5
	best_score_ref= go.Scatter(
		mode='lines',
		#possible to start from 0 also
		#one bar takes width=0.5 plus 0.5 for space in between 
        y =[-overhang, len(y) - 1 + overhang],
        #only two values are necessary to build a line
        x = [best_score]*2,
        name = 'Best score',
        line = dict(
            color = "green",
            width = 1,
         dash = 'dash'
         ),
        hoverinfo='x'
    )
	worst_score_ref= go.Scatter(
		mode='lines',
        y = [-overhang, len(y) - 1 + overhang],
        x = [worst_score]*2,
        name = 'Worst score',
        line = dict(
            color = "red",
            width = 1,
            dash = 'dash',
            ),
        hoverinfo='x'
   )

	bar=go.Bar(x=x,
		   y=y_enum,
		   width = 0.4,
		   name=False,
		   showlegend=False,
		   orientation='h',
		   opacity = 0.8,
		   text = [(c, v) for c,v in zip(x,y)],
           hoverinfo='text',
           marker=dict(
    		color='#2d46ad',
    		line=dict(
        	color='#2d46ad',
        	width=1.5),
    	),
		   )

	data=[bar,
		best_score_ref,
		worst_score_ref
	]

	layout=go.Layout({'title': "{} {}".format(index_name.lower().capitalize(), year),
		'yaxis':{
			'zeroline': False,
			'tickmode': 'array', 
			'ticktext': y, 
			'tickvals': y_enum,
			'tickwidth': 0,
			'showline' : True,
			'linecolor' : '#b5afaf',
			'linewidth': 0.1,
			'showgrid' :True,
			'automargin' :True,
			 },

		'xaxis':{
			'zeroline': False,
			 'linecolor' : '#b5afaf',
			 'linewidth': 0.1, 
	}		 
	})
	figure={
			'data' : data,
			'layout' : layout
		}
	return figure
@app.callback(Output('diff-year-dropdown', 'value'),
	[Input('show-button', 'n_clicks')])
def clear_year_diff(n_clicks):
	if n_clicks:
		return None

@app.callback(Output('map-box', 'figure'),
  [Input('show-button', 'n_clicks')],
  [State('index-dropdown', 'value'),
   State('country-dropdown', 'value'),
   State('year-dropdown','value')])
def draw_index_map(n_clicks, index_name,countries_list,year):
	if not index_name:
		return {}
	index_id=get_index_id(index_name)
	best_score, worst_score=get_best_worst_index_value(index_name,index_id, year)
	best_score_countries_info_list=get_country_info_for_value(index_id, best_score, year)
	worst_score_countries_info_list=get_country_info_for_value(index_id, worst_score, year)

	
	countries_ids=[get_country_id(name) for name in countries_list]

	index_values_dic=get_index_values(index_id, year, countries_ids)

	all_countries_codes=[value[1] for value in get_all_countries().values()]
	all_countries_names=[key for key in get_all_countries().keys()]

	#merge chosen countries indexes and best/worst world scores 
	#[[106.62, 'AFG'], [75.79, 'DZA'], [29.65, 'BEL']]
	ch_country_info_value=[value for value in index_values_dic.values()]

	#[{'South Sudan': [113.36, 'SSD']}]
	for country_info in worst_score_countries_info_list:
		for ws_country_info_value in country_info.values():
			#print('country_info_value', ws_country_info_value)
			ch_country_info_value.append(ws_country_info_value)

	for country_info in best_score_countries_info_list:
		for ws_country_info_value in country_info.values():
			#print('country_info_value', ws_country_info_value)
			ch_country_info_value.append(ws_country_info_value)
	#[[106.62, 'AFG'], [75.79, 'DZA'], [29.65, 'BEL'], [113.36, 'SSD'], [17.93, 'FIN']]		
	ccode_ivalue_dic=dict()
	for value in ch_country_info_value:
		ccode_ivalue_dic[value[1]]=value[0]
		#ccode_ivalue_dic {'AFG': 106.62, 'DZA': 75.79, 'BEL': 29.65, 'SSD': 113.36, 'FIN': 17.93}
		#print('ccode_ivalue_dic.keys()',ccode_ivalue_dic.keys())
		all_ccode_ivalue_to_show=dict()
		for code in all_countries_codes:
			if code not in ccode_ivalue_dic.keys():
				all_ccode_ivalue_to_show[code]=0
			else:
				all_ccode_ivalue_to_show[code]=ccode_ivalue_dic.get(code)
	#antarctica='ATA'			
	#all_countries_codes.remove(antarctica)
	map_data = go.Choropleth(
	        locations = all_countries_codes,
	        #it is set by default
	        #locationmode="ISO-3",
	        z=[value for value in all_ccode_ivalue_to_show.values()],
	        text=all_countries_names,
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
	            #autotick = False,
	            ticks="outside",
	            title = 'Index Value'),
	    )

	map_layout = go.Layout(
	    title ='{} {}'.format(index_name.lower().capitalize(), 'country location'),
	    geo = dict(
	        showframe = False,
	        showcoastlines = False,
	        projection = dict(
	            type = 'mercator'
	        )
	    ),    
	    autosize=True,
	    #width =800,
	    #height=600   
	    
	)
	figure={
		 	'data' : [map_data],
		 	'layout' : map_layout
		 }
	return figure
	 

@app.callback(Output('map-div', 'style'),
	[Input('show-button', 'n_clicks')])
def show_map_div(n_clicks):
	if n_clicks:
		return {'visibility':'visible'}
	return 	{'visibility':'hidden'}

@app.callback(Output('line-chart', 'figure'),
	[Input('show-button', 'n_clicks')],
	[State('index-dropdown', 'value'),
	State('country-dropdown', 'value'),
	])
def draw_line_chart(n_clicks, index_name,countries_list):
	if  not index_name:
		return {}
	index_id=get_index_id(index_name)
	years=sorted(get_index_years(index_id))       
	country_year_index=dict()
	for cname in countries_list:
		country_year_index[cname]={}
		c_id=get_country_id(cname)
		for year in years:
			index_value=get_index_value(index_id, year, c_id)
			country_year_index[cname][year]=index_value
	#{'c1': {2011: 1, 2012: 1, 2013: 1, 2014: 1, 2017: 1}, 'c2': {2011: 1, 2012: 1, 2013: 1, 2014: 1, 2017: 1}, }
	data=[]
	for c_name, y_v_dict in country_year_index.items():
		trace = go.Scatter(
		x = [key for key in y_v_dict.keys()],
		dx=1,
		y = [value for value in y_v_dict.values()],
		mode = 'lines+markers',
		name = c_name
		)
		data.append(trace)

	layout=go.Layout(title='{} {}'.format(index_name.lower().capitalize(), 'dynamics'),
		xaxis= {'tickformat':'d',
		'nticks': max([len(value) for value in country_year_index.values()]),
		
		# 'autorange':True
		})                 
	figure={'data': data,
			'layout': layout
			}
	return figure

@app.callback(Output('charts-div', 'style'),
	[Input('show-button', 'n_clicks')])
def show_charts_div(n_clicks):
	if n_clicks:
		return {'visibility':'visible'}
	return 	{'visibility':'hidden'}

@app.callback(Output('diff-year-dropdown', 'options'),
	[Input('show-button', 'n_clicks')],
	[State('index-dropdown', 'value'),
	State('year-dropdown','value')])
def fill_year_to_compare_combo(n_clicks, index_name,ch_year):
	if not index_name:
		return {}
	index_id=get_index_id(index_name)
	years=get_index_years(index_id)
	return [
	{'label': year, 'value' : year} for year in years if year!=ch_year
	]

@app.callback(Output('diff-chart', 'figure'),
	[Input('show-button', 'n_clicks'),
	Input('diff-year-dropdown', 'value')],
	[State('index-dropdown', 'value'),
	State('country-dropdown', 'value'),
	State('year-dropdown','value')])
def show_diff_chart(n_clicks,diff_year,index_name,countries_list,year):
	if not index_name:
		return {}
	index_id=get_index_id(index_name)
	min_available_year=min(get_index_years(index_id))
	if diff_year:
		min_available_year=diff_year
	y_diff={}
	for c_name in countries_list:
		c_id=get_country_id(c_name)
		y_diff[c_name]=get_percent_of_change(index_name, c_id, min_available_year, year)

	bar_width=0.5
	y = [value for value in y_diff.keys()]
	y_enum = list(range(len(y_diff)))
	bar=go.Bar(
		x=[value for value in y_diff.values()],
		y=[value for value in y_diff.keys()],
		width = bar_width,
		name=False,
		showlegend=False,
		orientation='h',
		opacity = 0.8,
		text = [(c, "{:.2%}".format(v)) for c,v in y_diff.items()],
		hoverinfo='text',
		marker=dict(
		color=['#2d46ad' if val>=0 else '#bf0540' for val in y_diff.values()],
			line=dict(
			color=['#2d46ad' if val>=0 else '#bf0540' for val in y_diff.values()],
			width=1.5),
		),
		)

	data=[bar]
	layout=go.Layout({
		'title': "{}, percent of change since {}".format(index_name.lower().capitalize(), min_available_year),
		'yaxis':{
			'zeroline': False,
			'showline' : False,
			'linecolor' : '#b5afaf',
			'linewidth': 0.1,
			'showgrid' :True,
			'automargin' :True,
			'type':"category",
			 },

		'xaxis':{
			'zeroline': True,
			'showline' : False,
			'tickformat' : '0,.1%',
			#that is for showline
			'linecolor' : '#878484',
			#that is for showline
			'linewidth': 9, 
		}		 
		})
	figure={
				'data' : data,
				'layout' : layout
			}
	return figure

if __name__=='__main__':
	app.run_server(debug=True)


	



