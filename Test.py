import streamlit as st
import numpy as np

#from bokeh.models.annotations.labels import Label
from bokeh.plotting import figure, show
from bokeh.models import SingleIntervalTicker, LinearAxis, Range1d, Label

remove_ticks = False

st.header("test")

a = st.slider("amp", 0.1, 3.0, 1.0, 0.1)

x = np.linspace(-6, 6, 500)
y = a*8*np.sin(x)*np.sinc(x)
y2 = a*1/3*x**2-4

p = figure(title="", tools="",
           toolbar_location=None, match_aspect=True, aspect_scale = 1)

p.line(x, y, color="red", alpha=0.9, line_width=2)
p.line(x, y2, color="navy", alpha=0.9, line_width=2)
p.background_fill_color = "#ffffff"
p.x_range = Range1d(-6, 6.4)
p.y_range = Range1d(-4.5, 5.5)

p.xaxis.fixed_location = 0
p.yaxis.fixed_location = 0
p.grid.visible = True
p.xaxis.axis_label = 'x'
p.yaxis.axis_label = 'y'

labelx = Label(x=6, y=0, x_offset=10, y_offset=-30, text="x")
labely = Label(x=0, y=5.5, x_offset=-15, y_offset=-20, text="y")

p.add_layout(labelx)
p.add_layout(labely)


if remove_ticks:
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
    p.xaxis.major_label_text_color = None  # preferred method for removing tick labels
    p.yaxis.major_label_text_color = None  # preferred method for removing tick labels
    
else:
    p.xaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=2)
    p.yaxis.ticker = SingleIntervalTicker(interval=1, num_minor_ticks=2)
    p.ygrid.minor_grid_line_color = 'black'
    p.ygrid.minor_grid_line_alpha = 0.1
    p.xgrid.minor_grid_line_color = 'black'
    p.xgrid.minor_grid_line_alpha = 0.1



st.bokeh_chart(p, use_container_width=True)