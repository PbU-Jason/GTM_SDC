from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime

import plotly.graph_objects as go
from mission_timeline_utc import *
from fermi_gbm_first_1000 import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

card_utc_now = dbc.Card(
    [
        dbc.CardHeader(html.H2('Current UTC', className='mb-0 mt-3')),
        dbc.CardBody(
            [
                html.Div(id='card-utc-text'),
                dcc.Interval(
                    id='card-utc-interval',
                    interval=1*1000, # ms
                    n_intervals=0,
                ),
            ],
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'5vh', 'alignItems':'center'},
    className='h-50 flex-grow-1',
)

card_last_fetch = dbc.Card(
    [
        dbc.CardHeader(html.H3('Last Fetching UTC+8', className='mb-0 mt-3')),
        dbc.CardBody(
            html.Div([
                html.H2('2023-09-26', className='text-center mb-0'),
                html.H2('19:17', className='text-center mb-0'),
            ]),
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'5vh', 'alignItems':'center'},
    className='h-100 flex-grow-1',
)

card_next_fetch = dbc.Card(
    [
        dbc.CardHeader(html.H3('Next Fetching UTC+8', className='mb-0 mt-3')),
        dbc.CardBody(
            html.Div([
                html.H2('2023-09-29', className='text-center mb-0'),
                html.H2('14:00', className='text-center mb-0'),
            ]),
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'5vh', 'alignItems':'center'},
    className='h-100 flex-grow-1',
)

future_time_fetch = html.Div(
    [
        card_last_fetch,
        card_next_fetch,
    ],
    className='h-50 d-flex flex-row flex-grow-1',
)

future_time = html.Div(
    [
        card_utc_now,
        future_time_fetch,
        
    ],
    className='h-100 w-50 d-flex flex-column flex-grow-1',
)

card_position_now = dbc.Card(
    [
        dbc.CardHeader(html.H2('Current Atittude', className='mb-0 mt-3')),
        dbc.CardBody(
            html.Div([
                html.Div(id='card-alt-text'),
                html.Div(id='card-lon-text'),
                html.Div(id='card-lat-text'),
                dcc.Interval(
                    id='card-position-interval',
                    interval=10*1000, # ms
                    n_intervals=0,
                ),
            ]),
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'5vh', 'alignItems':'center'},
    className='h-100 w-50 d-flex flex-column flex-grow-1',
)

future_time_position = html.Div(
    [
        future_time,
        card_position_now,
    ],
    className='h-25 d-flex flex-row flex-grow-1',
)

card_12hour_orbit = dbc.Card(
    [
        dbc.CardHeader(html.H2('Further 12 Hours Orbit', className='mb-0 mt-3')),
        dbc.CardBody(
            html.Div(
                [
                    html.Div(id='3d-orbit-plot', className='flex-grow-1'),
                    html.Div(id='2d-orbit-plot', className='flex-grow-1'),
                ],
                className='d-flex flex-column flex-grow-1',
            ),
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'5vh', 'alignItems':'center'},
    className='h-75 d-flex flex-column flex-grow-1',
)

future = html.Div(
    [
        future_time_position,
        card_12hour_orbit,
    ],
    className='h-100 d-flex flex-column',
)

card_lastest_grb = dbc.Card(
    [
        dbc.CardHeader(html.H2('The Lastest GRB', className='mb-0 mt-3')),
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Img(src='assets/LightCurve.png', style={'width':'25vw'}),
                        html.Img(src='assets/SykMap.png', style={'width':'20vw'}),
                    ],
                    style={'height':'23vh'},
                    className='d-flex flex-row',
                )
            ],
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'30vh', 'alignItems':'center'},
    className='flex-grow-1',
)

df_grb, df_grb_all_date = all_grb_statistic()
fig_sky = go.Figure()
fig_sky.add_trace(
    go.Scattergeo(
        mode="markers",
        lon = df_grb.ra,
        lat = df_grb.dec,
        marker = {
            'size': 8,
            'color':'#ff6666',
            },
        customdata=np.column_stack((df_grb.name, df_grb.trigger_time)),
        hovertemplate=
        "Name: %{customdata[0]}<br>" +
        "RA: %{lon:.3f} deg<br>" +
        "DEC: %{lat:.3f} deg<br>" +
        "Date: %{customdata[1]}" +
        "<extra></extra>",
        hoverlabel=dict(font_size=20),
        )
    )
fig_sky.update_layout(
    geo=dict(
        visible=False,
        projection=dict(
            type='aitoff',
        ),
        lonaxis=dict(
            showgrid=True,
            dtick=15,
            gridcolor='black',
            gridwidth=0.5
        ),
        lataxis=dict(
            showgrid=True,
            dtick=15,
            gridcolor='black',
            gridwidth=0.5
        )
        ),
    height=550, margin=dict(t=15, b=25)
    )
fig_rate = go.Figure(
        [
        go.Scatter(x=df_grb_all_date.index, 
                    y=df_grb_all_date['Count'],
                    line=dict(color='#6699ff'),
                    hovertemplate=
                    "Date: %{x}<br>" +
                    "Number of GRB: %{y}"
                    "<extra></extra>",
                    hoverlabel=dict(font_size=20),)
        ]
        )
fig_rate.update_layout(template='simple_white',
                    xaxis = dict(tickfont = dict(size=20)),
                    yaxis = dict(tickfont = dict(size=20)),
                    height=550, margin=dict(t=25, b=15))

card_past_statistic = dbc.Card(
    [
        dbc.CardHeader(html.H2('All GRB Statistic', className='mb-0 mt-3')),
        dbc.CardBody(
            html.Div(
                [
                    html.Div(dcc.Graph(figure=fig_sky), className='flex-grow-1'),
                    html.Div(dcc.Graph(figure=fig_rate), className='flex-grow-1'),
                ],
                className='d-flex flex-column flex-grow-1',
            ),
            style={'width':'100%', 'display':'flex', 'alignItems':'center', 'justifyContent':'center'},
        ),
    ],
    style={'height':'70vh', 'alignItems':'center'},
    className='flex-grow-1',
)

past = html.Div(
    [
        card_lastest_grb,
        card_past_statistic,
    ],
    className='h-100 d-flex flex-column',
)

future_and_past = [
    dbc.Row(
        [
            dbc.Col(
                future,
                style={'backgroundColor': 'black', 'height': '100vh'},
            ),
            dbc.Col(
                past,
                style={'backgroundColor': 'black', 'height': '100vh'},
            ),
        ],
        className='g-0',
    ),
]

app.layout = dbc.Container(
    id='root',
    children=future_and_past,
    fluid=True,
    className='g-0',
)

@app.callback(Output('card-utc-text', 'children'), Input('card-utc-interval', 'n_intervals'))
def update_utc(n):
    utc_now = datetime.utcnow()
    utc_now_str = utc_now.strftime('%Y-%m-%d %H:%M:%S')
    return [
        html.H1(f'{utc_now_str}', className='text-center mb-0'),
    ]

@app.callback([
    Output('card-alt-text', 'children'),
    Output('card-lon-text', 'children'),
    Output('card-lat-text', 'children'),
    Output('3d-orbit-plot', 'children'),
    Output('2d-orbit-plot', 'children'),
], Input('card-position-interval', 'n_intervals'))
def update_position(n):
    tle = load_tle('FS8B_20230521_0100.nor')
    now_utc = datetime.utcnow()
    times, orbit, is_sunlight, minutes, orbit_alt = \
    calculate_orbit_eclipse(tle, 
                            (now_utc.year, 
                            now_utc.month, 
                            now_utc.day, 
                            now_utc.hour, 
                            now_utc.minute, 
                            now_utc.second), 
                            720)
    saa, df = circle_saa('df_for_contour.pkl', 200000)
    is_saa, intersection_x, intersection_y = in_saa(times, saa, orbit)

    color_list = []
    for time_idx, time in enumerate(minutes):
        if is_sunlight[time_idx] == 1:
            color_list.append('gray')
        else:
            if is_saa[time_idx] == 0:
                color_list.append('green')
            else:
                color_list.append('red')

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=saa[:, 0],
            lat=saa[:, 1],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'
            )
        )
    fig.add_trace(
        go.Scattergeo(
            lon=orbit[:, 0],
            lat=orbit[:, 1],
            mode='markers',
            marker=dict(color=color_list, size=5),
            showlegend=False,
            customdata=np.column_stack((np.array(times.utc_strftime()), orbit_alt)),
            hovertemplate=
            'Time: %{customdata[0]}<br>' +
            'Lon: %{lon:.3f} deg<br>' +
            'Lat: %{lat:.3f} deg<br>' +
            'Height: %{customdata[1]:.3f} km' +
            '<extra></extra>',
            hoverlabel=dict(font_size=20),
            )
        )
    fig.add_trace(
        go.Scattergeo(
            lon=[orbit[0, 0]],
            lat=[orbit[0, 1]],
            mode='markers',
            marker=dict(size=10, symbol='cross-thin', line=dict(width=3, color='blue')),
            showlegend=False,
            hoverinfo='none'
            )
        )

    fig.update_layout(margin=dict(t=25, b=15), height=580)
    fig_2d = go.Figure(fig)
        
    fig.update_geos(projection_rotation_lon=orbit[0, 0], 
                    projection_rotation_lat=orbit[0, 1],
                    projection_type='orthographic')
    fig_3d = fig.update_layout(margin=dict(t=15, b=25), height=580)
    
    return [html.H1(f'Altitude: {np.round(orbit_alt[0], 3)} km', className='text-center my-5')], \
        [html.H1(f'Longitude: {np.round(orbit[0, 0], 3)} deg', className='text-center my-5')], \
        [html.H1(f'Latitude: {np.round(orbit[0, 1], 3)} deg', className='text-center my-5')], \
        [dcc.Graph(figure=fig_3d)], \
        [dcc.Graph(figure=fig_2d)]

if __name__ == '__main__':
    app.run_server()
    # app.run(debug=True)

