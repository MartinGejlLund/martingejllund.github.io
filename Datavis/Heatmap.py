import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dataframe = pd.read_csv('StudentsPerformance.csv')
fig = make_subplots(
    rows=2,
    cols=2,
    row_heights=[0.2, 0.8],
    column_widths=[0.8, 0.2],
    vertical_spacing=0.07,
    horizontal_spacing=0.07,
    shared_xaxes=True,
    shared_yaxes=True
)

math_score = [0, 0, 0, 0, 0]
reading_score = [0, 0, 0, 0, 0]
writing_score = [0, 0, 0, 0, 0]
data = [math_score, reading_score, writing_score]

dataframe['group A'] = [1 if i == 'group A' else None for i in dataframe['race/ethnicity']]
dataframe['group B'] = [1 if i == 'group B' else None for i in dataframe['race/ethnicity']]
dataframe['group C'] = [1 if i == 'group C' else None for i in dataframe['race/ethnicity']]
dataframe['group D'] = [1 if i == 'group D' else None for i in dataframe['race/ethnicity']]
dataframe['group E'] = [1 if i == 'group E' else None for i in dataframe['race/ethnicity']]

ethnicity = ['group A', 'group B', 'group C', 'group D', 'group E']

for i in range(len(math_score)):
    math_score[i] = dataframe['math score'].loc[dataframe[ethnicity[i]] == 1].mean()
    reading_score[i] = dataframe['reading score'].loc[dataframe[ethnicity[i]] == 1].mean()
    writing_score[i] = dataframe['writing score'].loc[dataframe[ethnicity[i]] == 1].mean()

fig.add_trace(
    go.Heatmap(
        x=dataframe.columns[-5:],
        y=dataframe.columns[-8:-5],
        z=data,
        colorscale='viridis',
        name='Mean Score',
        legendgroup='Mean Score',
        visible=True
    ),
    row=2,
    col=1
)
fig.add_trace(
    go.Histogram(
        x=dataframe['race/ethnicity'],
        showlegend=False,
        marker_color='blue',
        name='Total count',
        legendgroup='Total count',
        visible=True
    ),
    row=1,
    col=1
)
fig.add_trace(
    go.Histogram(
        x=dataframe['race/ethnicity'].loc[dataframe['gender'] == 'male'],
        showlegend=False,
        marker_color='red',
        name='Male count',
        legendgroup='Male count',
        visible=False
    ),
    row=1,
    col=1
)
fig.add_trace(
    go.Histogram(
        x=dataframe['race/ethnicity'].loc[dataframe['gender'] == 'female'],
        showlegend=False,
        marker_color='blue',
        name='Female count',
        legendgroup='Female count',
        visible=False
    ),
    row=1,
    col=1
)
fig.add_trace(
    go.Bar(
        x=[dataframe['math score'].mean(), dataframe['reading score'].mean(), dataframe['writing score'].mean()],
        y=dataframe.columns[-8:-5],
        orientation='h',
        showlegend=False,
        marker_color='red',
        name='Total mean',
        legendgroup='Total mean',
        visible=True
    ),
    row=2,
    col=2
)
fig.add_trace(
    go.Bar(
        x=[dataframe['math score'].loc[dataframe['gender'] == 'male'].mean(),
           dataframe['reading score'].loc[dataframe['gender'] == 'male'].mean(),
           dataframe['writing score'].loc[dataframe['gender'] == 'male'].mean()],
        y=dataframe.columns[-8:-5],
        orientation='h',
        showlegend=False,
        marker_color='red',
        name='Male mean',
        legendgroup='Male mean',
        visible=False
    ),
    row=2,
    col=2
)
fig.add_trace(
    go.Bar(
        x=[dataframe['math score'].loc[dataframe['gender'] == 'female'].mean(),
           dataframe['reading score'].loc[dataframe['gender'] == 'female'].mean(),
           dataframe['writing score'].loc[dataframe['gender'] == 'female'].mean()],
        y=dataframe.columns[-8:-5],
        orientation='h',
        showlegend=False,
        marker_color='blue',
        name='Female mean',
        legendgroup='Female mean',
        visible=False
    ),
    row=2,
    col=2
)
fig.update_layout(
    title='Heatmap of subject scores by ethnicity',
    yaxis_title_text='Count',
    xaxis4=dict(
        title='Score'
    ),
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, False, False, True, False, False]}],
                    label='Display total',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, True, True, False, True, True]}],
                    label='Display by Gender',
                    method='update'
                )
            ]),
            type='buttons',
            direction='right',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=.45,
            xanchor='left',
            y=1.05,
            yanchor='bottom'
        ),
    ]
)

fig.show()
fig.write_html('Heatmap.html')
fig.write_image('Heatmap.png', width=1200, height=720, scale=1)
