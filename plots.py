import pandas as pd
from bokeh.models import BoxAnnotation, LinearAxis, Range1d, Scatter, Band
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.palettes import Paired

def get_overall_plot(df: pd.DataFrame):

    #define available tools in plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save, hover"

    # Define tooltip info
    TOOLTIPS = [
        ("Puntaje promedio", "@promedio"),
        ("Puntaje total", "@puntaje"),
        
    ]

    source = ColumnDataSource(df)

    #reduce data size

    p = figure(x_axis_type="datetime", tools=TOOLS, y_range=(0,10), tooltips=TOOLTIPS)
    p.yaxis.axis_label = "Puntaje Promedio"

    # Setting the second y axis range name and range
    p.extra_y_ranges = {"puntaje": Range1d(start=0, end=720)}

    # Adding the second axis to the plot.  
    p.add_layout(LinearAxis(y_range_name="puntaje", axis_label="Puntaje Total"), 'right')

    # Plot main line
    p.line("date", "promedio", source=source, color="#DD1C77", line_width=2)

    # Plot markers
    glyph = Scatter(x="date", y="promedio", size=12, fill_color="#DD1C77", marker="circle_x")
    p.add_glyph(source, glyph)

    # Define color bars
    yellow = BoxAnnotation(bottom=9, top=10, fill_alpha=0.2, fill_color='#FFE552')
    red = BoxAnnotation(bottom=7, top=9, fill_alpha=0.2, fill_color='#F65058')
    blue = BoxAnnotation(bottom=5, top=7, fill_alpha=0.2, fill_color='#00B4E4')
    black = BoxAnnotation(bottom=3, top=5, fill_alpha=0.2, fill_color='#1b1b1b')

    # Plot color bars
    p.add_layout(black)
    p.add_layout(blue)
    p.add_layout(red)
    p.add_layout(yellow)
    
    return p

def get_round_scores(df: pd.DataFrame, round_type: int = 1, rondas = None):
    
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save, hover"


    TOOLTIPS = [
        ("Puntaje promedio", "@promedio"),
        ("Puntaje total", "@puntaje"),
        
    ]

    #promedio == 1
    if round_type == 1:
        round_scores_to_plot = df[['ronda', 'promedio']].groupby(['ronda']).agg(['mean', 'std']).reset_index()
        round_scores_to_plot.columns = ['ronda', 'promedio', 'std']
        round_scores_to_plot['puntaje'] = round_scores_to_plot['promedio'] * 6
        round_scores_to_plot['lower'] = round_scores_to_plot['promedio'] - round_scores_to_plot['std']
        round_scores_to_plot['upper'] = round_scores_to_plot['promedio'] + round_scores_to_plot['std']

        source = ColumnDataSource(round_scores_to_plot)

        p = figure(tools=TOOLS, y_range=(0,10), tooltips=TOOLTIPS)
        p.yaxis.axis_label = "Puntaje Promedio"

        # Setting the second y axis range name and range
        p.extra_y_ranges = {"puntaje": Range1d(start=0, end=60)}

        # Adding the second axis to the plot.  
        p.add_layout(LinearAxis(y_range_name="puntaje", axis_label="Puntaje Total"), 'right')

        p.line("ronda", "promedio", source=source, color="#DD1C77", line_width=2)
        band = Band(base="ronda", lower="lower", upper="upper", source=source,
                    fill_alpha=0.3, fill_color="gray", line_color="black")
        p.add_layout(band)

        glyph = Scatter(x="ronda", y="promedio", size=12, fill_color="#DD1C77", marker="circle_x")
        p.add_glyph(source, glyph)
    
    #TODO: do we want a chart with all rounds? cluttered?
    else:
        round_scores_to_plot = df.set_index(['date', 'ronda'])['promedio'].unstack().reset_index()
        round_scores_to_plot.columns = ['date'] + [str(c) for c in round_scores_to_plot.columns[1:]]
        source = ColumnDataSource(round_scores_to_plot)

        p = figure(width=1200, height=600, x_axis_type="datetime", tools=TOOLS, y_range=(0,10), tooltips=TOOLTIPS)
        p.yaxis.axis_label = "Puntaje Promedio"

        # Setting the second y axis range name and range
        p.extra_y_ranges = {"puntaje": Range1d(start=0, end=60)}

        # Adding the second axis to the plot.  
        p.add_layout(LinearAxis(y_range_name="puntaje", axis_label="Puntaje Total"), 'right')

        for r, c in zip(rondas, Paired[12]):
            p.line("date", r, source=source, color=c, line_width=2)

            glyph = Scatter(x="date", y=r, size=12, fill_color=c, marker="circle_x")
            p.add_glyph(source, glyph)

    yellow = BoxAnnotation(bottom=9, top=10, fill_alpha=0.2, fill_color='#FFE552')
    red = BoxAnnotation(bottom=7, top=9, fill_alpha=0.2, fill_color='#F65058')
    blue = BoxAnnotation(bottom=5, top=7, fill_alpha=0.2, fill_color='#00B4E4')
    black = BoxAnnotation(bottom=3, top=5, fill_alpha=0.2, fill_color='#1b1b1b')

    p.add_layout(black)
    p.add_layout(blue)
    p.add_layout(red)
    p.add_layout(yellow)

    return p

def get_x_m_counts(df: pd.DataFrame):
    
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save, hover"


    TOOLTIPS = [
        ("Conteo X", "@x"),
        ("Conteo M", "@m"),
        
    ]

    source = ColumnDataSource(df)

    p = figure(width=1200, height=600, x_axis_type="datetime", tools=TOOLS, y_range=(0,10), tooltips=TOOLTIPS)
    p.yaxis.axis_label = "Conteo"

    p.line("date", "x", source=source, color="#3CB043", line_width=2)
    glyph = Scatter(x="date", y="x", size=12, fill_color="#03AC13", marker="circle_x")
    p.add_glyph(source, glyph)

    p.line("date", "m", source=source, color="#DD1C77", line_width=2)
    glyph = Scatter(x="date", y="m", size=12, fill_color="#DD1C77", marker="circle_x")
    p.add_glyph(source, glyph)

    return p