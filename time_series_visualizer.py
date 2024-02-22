import matplotlib.pyplot as plt
import pandas as pd
import calendar
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df.set_index('date', inplace = True)

# Clean data
low = df['value'].quantile(0.025)
hi = df['value'].quantile(0.975)
df = df[(df['value'] > low) & (df['value'] < hi)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Trazar el gráfico de líneas
    ax.plot(df.index, df['value'], color='g')

    # Establecer el título y las etiquetas de los ejes
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Ajustar el diseño
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    plt.close(fig)
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # Calcular el promedio diario de vistas de página para cada mes y año
    df_avg = df.groupby(['year', 'month'], observed=False)['value'].mean().unstack()

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw bar plot
    df_avg.plot(kind='bar', ax=ax)

    # Establecer el título y las etiquetas de los ejes
    ax.set_title('Average Daily Page Views by Month and Year')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Establecer la leyenda
    ax.legend(title='Months', loc='upper left', labels=calendar.month_name[1:])

    # Ajustar el diseño
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    plt.close(fig)
    return fig

def draw_box_plot():
    # Convertir el índice en una columna
    df.reset_index(inplace=True)

    # Convertir la columna de fecha a tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Extraer el año y el mes de la fecha
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()

    # Ordenar el DataFrame por el orden de los meses
    month_order = list(calendar.month_name)[1:]
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    df.sort_values('month', inplace=True)

    # Crear la figura y los ejes
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Diagrama de caja por año
    sns.boxplot(x='year', y='value', data=df, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Value')

    # Diagrama de caja por mes
    sns.boxplot(x='month', y='value', data=df, ax=axes[1], order=month_order, showfliers=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Value')

    # Rotar las etiquetas del eje x para el diagrama de caja por mes
    axes[1].tick_params(axis='x', rotation=45)

    # Ajustar el diseño
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    plt.close(fig)
    return fig
