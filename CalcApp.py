import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ui
# input: number of stitches w and h
# checkboxes for aida count?
# table for width/height and aida counts
# slider for hoop size
# graph with moving hoop size

# calculations
# height + width, inch + cm
# draw rectangles
# circle draw

def calc_dimen(w_stitch, h_stitch, aida_ct):
    w_in = w_stitch/aida_ct
    h_in = h_stitch/aida_ct
    return w_in, h_in

def get_rect(w_in, h_in):
    w = w_in/2
    h = h_in/2
    x = [-w, w, w, -w, -w]
    y = [-h, -h, h, h, -h]
    return x, y

def get_circ(hoop):
    r = hoop/2
    return -r, r

st.title("Cross Stitch Size Calculator")

col_w, col_h = st.columns(2)
w_stitch = col_w.number_input("Number of Stitches Horizontal", step=1, format="%d")
h_stitch = col_h.number_input("Number of Stitches Vertical", step=1, format="%d")

aida_cts = [14, 16, 18]
dimens = [calc_dimen(w_stitch, h_stitch, ct) for ct in aida_cts]

dimen_df = pd.DataFrame()
dimen_df["Dimensions (Width x Height)"] = [f"{w_in:.2f} in x {h_in:.2f} in" for w_in, h_in in dimens]
dimen_df.index = pd.Index(aida_cts, name="Aida Count")
st.table(dimen_df)

hoop_d = st.slider("Hoop Size", min_value=1, max_value=20, step=1, format="%d")

fig = go.Figure()
for a_ct, (dx, dy) in zip(aida_cts, dimens):
    x, y = get_rect(dx, dy)
    fig.add_trace(
        go.Scatter(x=x, y=y, name=f"Aida {a_ct}")
    )

min_r, max_r = get_circ(hoop_d)
fig.add_shape(type="circle",
              xref="x", yref="y",
              x0=min_r, y0=min_r, x1=max_r, y1=max_r,
              line_color='red',
              name='Hoop'
)
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
    showgrid=True,
    fixedrange=True
)
fig.update_xaxes(
    showgrid=True,
    fixedrange=True
)
st.plotly_chart(fig, config={'displayModeBar':False})