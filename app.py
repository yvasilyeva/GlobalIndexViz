import dash
import dash_core_components as dcc 
import dash_html_components as html 
from fsi import fsi_index_name
from hdi import hdi_index_name
from db_util import get_available_indexes_names,get_all_countries,get_index_years,get_index_countries_info,get_index_values,get_best_worst_index_value,get_country_info_for_value

import plotly.graph_objs as go

app=dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#index_name:id
index_names=get_available_indexes_names()
index_dropdown=html.Div(
	dcc.Dropdown(
	id='index-dropdown',
	options=[
		{'label': name, 'value' : name} for name in index_names.values()
	],
	placeholder="Select an index...",
	searchable=True,
	multi=False
	),
	style={'width': '33%', 'display': 'inline-block'}
)

def get_chosen_index_id():
	# use variable index_names to define id 
	return 1

def get_chose_index_name(chosen_index_id):
	return index_names.get(chosen_index_id)

chosen_index_id=get_chosen_index_id()
chosen_index_name=get_chose_index_name(chosen_index_id)

index_countries_info=get_index_countries_info(chosen_index_id)

country_dropdown=html.Div(
	dcc.Dropdown(
	id='country-dropdown',
    options=[
        {'label': country_name, 'value' : info[1]} for country_name, info in index_countries_info.items()
    ],
    #default values from the list
    value=[],
    multi=True,
    searchable=True,
    clearable=False,
    placeholder="Select a country..."
    #to disable dropdown set an option
    #dsabled=True
	),
	style={'width': '33%', 'display': 'inline-block'}
)

def get_chosen_countries_ids():
	return [4,12,16,56]

chosen_countries_ids=get_chosen_countries_ids()	
	
#should depend on choosen index
#and amount of countries
years=get_index_years(chosen_index_id) 

year_dropdown=html.Div(
	dcc.Dropdown(
	id='year-dropdown',
	options=[
		{'label': year, 'value' : year} for year in years
	],
	),
	style={'width': '33%', 'display': 'inline-block'}
)
def get_chosen_year():
	return 2018

chosen_year=get_chosen_year()

# draw a barchart
#country_name:[index_value,country_code]
index_values_dic=get_index_values(chosen_index_id, chosen_year, chosen_countries_ids)
y=list(index_values_dic.keys())
x=[value[0] for value in index_values_dic.values()]

best_score, worst_score=get_best_worst_index_value(chosen_index_name,chosen_index_id, chosen_year)
best_score_countries_info_list=get_country_info_for_value(chosen_index_id, best_score, chosen_year)
worst_score_countries_info_list=get_country_info_for_value(chosen_index_id, worst_score, chosen_year)
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
		   text = [(c, v) for c,v in zip(x,y)],
           hoverinfo='text'
		   )

data=[bar,
	best_score_ref,
	worst_score_ref
	]

layout=go.Layout({'title': "Fragility Index",
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
			 },

	'xaxis':{
			'zeroline': False,
			 'linecolor' : '#b5afaf',
			 'linewidth': 0.1, 
	}		 
})

index_barchart=html.Div(
	dcc.Graph(
		id='index-barchart',
		figure={
			'data' : data,
			'layout' : layout
		},
	),
	style={'width': '40%', 'display': 'inline-block'}
)
all_countries_codes=[value[1] for value in get_all_countries().values()]
all_countries_names=[key for key in get_all_countries().keys()]

#merge chosen countries indexes and best/worst world scores 
#[[106.62, 'AFG'], [75.79, 'DZA'], [29.65, 'BEL']]
ch_country_info_value=[value for value in index_values_dic.values()]

#[{'South Sudan': [113.36, 'SSD']}]
for country_info in worst_score_countries_info_list:
	for ws_country_info_value in country_info.values():
		print('country_info_value', ws_country_info_value)
		ch_country_info_value.append(ws_country_info_value)

for country_info in best_score_countries_info_list:
	for ws_country_info_value in country_info.values():
		print('country_info_value', ws_country_info_value)
		ch_country_info_value.append(ws_country_info_value)
#[[106.62, 'AFG'], [75.79, 'DZA'], [29.65, 'BEL'], [113.36, 'SSD'], [17.93, 'FIN']]		
ccode_ivalue_dic=dict()
for value in ch_country_info_value:
	ccode_ivalue_dic[value[1]]=value[0]
	#ccode_ivalue_dic {'AFG': 106.62, 'DZA': 75.79, 'BEL': 29.65, 'SSD': 113.36, 'FIN': 17.93}
	print('ccode_ivalue_dic.keys()',ccode_ivalue_dic.keys())
	all_ccode_ivalue_to_show=dict()
	for code in all_countries_codes:
		if code not in ccode_ivalue_dic.keys():
			print('we are inside')
			all_ccode_ivalue_to_show[code]=0
		else:
			all_ccode_ivalue_to_show[code]=ccode_ivalue_dic.get(code)


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
            #ticks="outside",
            title = 'Index Value'),
    )

map_layout = go.Layout(
    title = chosen_index_name,
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'mercator'
        )
    ),    
    autosize=True   
    
)

index_map=html.Div(
	dcc.Graph(
		id='map-box',
		figure={
			'data' : [map_data],
			'layout' : map_layout
		},
	),
	style={'width': '60%', 'display': 'inline-block'}
)

app.layout=html.Div(children=[
	 html.H2(children='Global Indices Visualization',
	 	style={
             'textAlign': 'center',
             'color': colors['text']
         }
         ),

	 html.Div(children='''
	 	Visualization of relatad to GCERF global indices.
	 	''',
	 	style={
         'textAlign': 'center',
         'color': colors['text']
     	}
	 	),
	 html.Div(
	 	[index_dropdown,
	 	country_dropdown,
	 	year_dropdown
	 	],
	 	style={
	 	'padding': 30
	 	}
	 ),
	  html.Div(
	 	[index_barchart,
	 	index_map],
	 	style={
	 	}
	 ),
])

if __name__=='__main__':
	app.run_server(debug=True)
	
	

	



