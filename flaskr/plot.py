import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#for the plots:
import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required

sample_data = pd.read_csv("flaskr/static/sandbox_data.csv")
sns.set(font_scale=0.85)

bp = Blueprint('plot', __name__)

@bp.route('/plot1.png')
@login_required
def plot_png1():
    fig = create_figure1()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@bp.route('/plot2.png')
@login_required
def plot_png2():
    fig = create_figure2()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@bp.route('/plot3.png')
@login_required
def plot_png3():
    fig = create_figure3()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@bp.route('/plot4.png')
@login_required
def plot_png4():
    fig = create_figure4()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@bp.route('/plot5.png')
@login_required
def plot_png5():
    fig = create_figure5()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure1():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    countries = sample_data.country_long.unique().tolist()

    num_each_country = []
    for i in countries:
        num_each_country.append(len(sample_data[sample_data.country_long == i])/float(len(sample_data))*100)

    axis.barh(countries,num_each_country,0.7,alpha=0.9)
    axis.set_xlabel('Number of entries [%]')
    axis.set_ylabel('Country')
    axis.set_title('Distribution over countries')
    axis.set_autoscale_on(True)
    #fig.set_figheight(2)
    fig.set_figwidth(8)
    #axis.plot(xs, ys)
    return fig

def create_figure2():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    x = sample_data.odometer_km.tolist()


    _ = axis.hist(x,bins=30)
    _ = axis.set_xlabel('mileage [km]')
    _ = axis.set_ylabel('proportion of vehicles in data [%]')
    _ = axis.set_title('Histogramm vehicle mileage')
    return fig

def create_figure3():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x = sample_data.damage_count.tolist()

    _ = axis.hist(x,bins=30)
    _ = axis.set_xlabel('damage counter [FullRackTravel]')
    _ = axis.set_ylabel('proportion of steering systems [%]')
    _ = axis.set_title('Histogramm steering system damage counter')
    return fig

def create_figure4():
    #fig = Figure()
    #axis = fig.add_subplot(1, 1, 1)

    #Filter rows
    country_sublist = ['India','Norway','USA']
    subset_row = sample_data[sample_data.country_long.isin(country_sublist)]
    #Filter columns
    subset = subset_row.loc[:,['country_long','odometer_km', 'damage_count']]
    #Checking the correlation using seaborn pairplot
    pairgrid = sns.pairplot(subset, hue="country_long",palette="husl", aspect=1.2, size=1.8)

    pairgrid.fig.suptitle("Correlation between mileage, damage counter and countries",fontsize=8)

    return pairgrid.fig



def create_figure5():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    #Filter rows
    country_sublist_warm = ['India','Portugal','Spain']
    country_sublist_cold = ['Russia','Denmark','Norway']
    subset_row_cold = sample_data[sample_data.country_long.isin(country_sublist_cold)]
    subset_row_warm = sample_data[sample_data.country_long.isin(country_sublist_warm)]
    subset_row_ice = sample_data[sample_data.type.isin(['ICE'])]
    subset_row_em = sample_data[sample_data.type.isin(['EM'])]
    #Filter columns
    tempCat_sublist = ['17_lessThan-40degC','16_-40to-30degC','15_-30to-20degC',
                     '14_-20to-10degC','13_-10to0degC','12_0to10degC','11_10to20degC',
                     '10_20to30degC','09_30to40degC','08_40to50degC','07_50to60degC',
                     '06_60to70degC','05_70to80degC','04_80to90degC','03_90to100degC',
                     '02_100to110degC','01_110to120degC','00_abv_120']
    subset_column_cold = subset_row_cold.loc[:, tempCat_sublist]
    subset_column_warm = subset_row_warm.loc[:, tempCat_sublist]
    subset_column_ice = subset_row_ice.loc[:, tempCat_sublist]
    subset_column_em = subset_row_em.loc[:, tempCat_sublist]

    #Get the sum of each column and save it in sum_list
    sum_list_cold = []
    sum_list_warm = []
    sum_list_ice = []
    sum_list_em = []
    #sum_list = sum_list.append(subset_column[0].sum())
    for i in range(len(tempCat_sublist)):
        sum_list_cold.append(subset_column_cold.iloc[:,i].sum())
        sum_list_warm.append(subset_column_warm.iloc[:,i].sum())
        sum_list_ice.append(subset_column_ice.iloc[:,i].sum())
        sum_list_em.append(subset_column_em.iloc[:,i].sum())
    y_list_cold= sum_list_cold/max(sum_list_cold)*100
    y_list_warm= sum_list_warm/max(sum_list_warm)*100
    y_list_ice = sum_list_ice/max(sum_list_ice)*100
    y_list_em = sum_list_em/max(sum_list_em)*100
    x_list = ['<-40','-40..-30','-30..-20','-20..-10','-10..0','0..10','10..20','20..30',
              '30..40','40..50','50..60','60..70','70..80','80..90','90..100','100..110','110..120','>120']

    # plot with 4 subplots
    output_fig = plt.figure(figsize=[16, 10])

    # warm
    plt.subplot(221)
    plt.bar(x_list,y_list_warm,color='red')
    plt.xticks(rotation=50)
    plt.axis([3, 13, 0, 101])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    plt.grid(True)
    #plt.xlabel('temperature range [°C]')
    plt.ylabel('time [%]')
    plt.title('Warm climate')
    plt.grid(True)

    # cold
    plt.subplot(222)
    plt.bar(x_list,y_list_cold,color='blue')
    plt.xticks(rotation=50)
    plt.axis([3, 13, 0, 101])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    plt.grid(True)
    #plt.xlabel('temperature range [°C]')
    #plt.ylabel('time [%]')
    plt.title('Cold climate')
    plt.grid(True)

    # ice
    plt.subplot(223)
    plt.bar(x_list,y_list_ice,color='black')
    plt.xticks(rotation=50)
    plt.axis([3, 13, 0, 101])
    plt.grid(True)
    plt.xlabel('temperature range [°C]')
    plt.ylabel('time [%]')
    plt.title('Exp. to ICE')
    plt.grid(True)

    # em
    plt.subplot(224)
    plt.bar(x_list,y_list_em,color='green')
    plt.xticks(rotation=50)
    plt.axis([3, 13, 0, 101])
    plt.grid(True)
    plt.xlabel('temperature range [°C]')
    #plt.ylabel('time [%]')
    plt.title('Exp. to EM')
    plt.grid(True)

    plt.subplots_adjust(top=0.95, bottom=0.14, left=0.10, right=0.95, hspace=0.1,
                        wspace=0.1)

    

    return output_fig

