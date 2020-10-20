import plotly.graph_objects as go
from plotly.subplots import make_subplots
from random import random
import numpy as np

# suppose we have a parameter m
m = 20
p = 1
y = (m/p)*random()

while y < 1:
    y = (m/p)*random()

y = 10

def f(x,y=y):
    return (x**.5)*(y**.5)

def inv_f(x):
    return (f(m-y))**2/x


def f_x(x,y=y):
    # I'll eventually implement a version which disregards differentiability
    return .5*(x**(-.5))*(y**.5)

def L(x,lbda):
    return f(x,y)+lbda*(m-x-p*y)


x,pnsh = np.meshgrid(np.arange(0,m,.04),np.arange(0,2,.01))
x_obs = np.size(np.arange(0,m,.04))
p_obs = np.size(np.arange(0,2,.01))

fig = make_subplots(
    rows=1,cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]]
)


# add the surface to the figure
fig.add_trace(
    go.Surface(
        name='L(x,y,lambda)',
        x=x,y=pnsh,z=L(x,pnsh),
        colorscale='Viridis',
        opacity=.8,
        hoverinfo='none'
    ),row=1,col=1
)

fig.add_trace(
    go.Scatter3d(
        name='optimal point',
        x=[m-y],y=[f_x(m-y)],z=[L(m-y,f_x(m-y))],
        mode='markers',
        marker=dict(color='black',size=5)
    ),row=1,col=1
)

fig.add_trace(
    go.Scatter3d(
        x=np.arange(0,m,.04),
        y=np.repeat(f_x(m-y),x_obs),
        z=L(np.arange(0,m,.04),np.repeat(f_x(m-y),x_obs)),
        mode='lines',
        line=dict(color='blue',width=3),
        hoverinfo='none'
    ),row=1,col=1
)

fig.add_trace(
    go.Scatter3d(
        x=np.repeat(m-y,p_obs),
        y=np.arange(0,2,.01),
        z=L(np.repeat(m-y,p_obs),np.arange(0,2,.01)),
        mode='lines',
        line=dict(color='red',width=3),
        hoverinfo='none'
    ),row=1,col=1
)

# now define the indifference curve and utility
x_i,y_i = np.meshgrid(np.arange(0,m,.04),np.arange(0,m,.04))

fig.add_trace(
    go.Scatter3d(
        name='indifference curve',
        x=np.arange(((f(m-y))**2)/m,m,.04),
        y=inv_f(np.arange(((f(m-y))**2)/m,m,.04)),
        z=np.repeat(f(m-y),x_obs),
        mode='lines',
        line=dict(color='black',width=5)
    ),row=1,col=2
)

fig.add_trace(
    go.Surface(
        name='utility surface',
        x=x_i,y=y_i,z=f(x_i,y_i),
        colorscale='Viridis',
        opacity=.8,
        hoverinfo='none',
        showscale=False
    ),row=1,col=2
)

fig.add_trace(
    go.Scatter3d(
        name='budget line',
        x=np.arange(0,m,.04),
        y=np.arange(m,0,-.04),
        z=f(np.arange(0,m,.04),np.arange(m,0,-.04)),
        mode='lines',
        line=dict(color='red',width=3),
        hoverinfo='none'
    ),row=1,col=2
)

fig.add_trace(
    go.Scatter3d(
        name='optimal x given y=%d' % y,
        x=[m-y],y=[y],z=[f(m-y,y)],
        mode='markers',
        marker=dict(color='black',size=5)
    ),row=1,col=2
)

fig.update_layout(
    scene1=dict(
        xaxis_title='(x,%.5f)' % y,
        yaxis_title='lambda',
        zaxis_title='L(x,lambda)'
    ),
    scene2=dict(
        xaxis_title='x',
        yaxis_title='y',
        zaxis_title='f(x,y)'
    ),
    showlegend=False
)

fig.show()