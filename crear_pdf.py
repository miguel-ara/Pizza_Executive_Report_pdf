from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import signal
import sys

def handler_signal(signal, frame):
    print("\n\n Interrupción! Saliendo del programa de manera ordenada")
    sys.exit(1)

# Señal de control por si el usuario introduce Ctrl + C para parar el programa
signal.signal(signal.SIGINT, handler_signal)

class PDF(FPDF):

    # Esta clase servirá para manejar el pdf 

    def colour_rect(self): # Crea bordes de página y los colorea
        self.set_fill_color(300, 0, 0)
        self.rect(5.0, 5.0, 200.0,287.0,'DF')
        self.set_fill_color(255, 255, 255)
        self.rect(8.0, 8.0, 194.0,282.0,'FD')

    def portada(self): # Crea la página de la portada con el título y dos imágenes
        self.add_page()
        self.colour_rect()
        self.set_xy(0, 60)
        self.set_font('Times', 'B', 35)
        self.cell(w=210.0, h=20.0, align='C', txt="MAVEN PIZZAS", border= False, ln = True)
        self.cell(w=195.0, h=20.0, align='C', txt="EXECUTIVE REPORT", border= False, ln = True)
        self.image('maven_logo.png', 32, 100, 150)
        self.image('pizza_cocinada.jpeg', 47, 150, 120)

    def ingredientes(self): # Crea la página del análisis de los ingredientes con 3 gráficas
        self.add_page()
        self.colour_rect()
        self.set_xy(0, 10)
        self.set_font('Times', 'BU', 30)
        self.cell(w=210.0, h=15.0, align='C', txt="INGREDIENT ANALYSIS", border= False, ln = True)
        self.image('Full_ingredients.png', 25, 28, 155, 93)
        self.image('Top_5_used_ingredients.png', 43, 123, 120)
        self.image('Top_5_less_used_ingredients.png', 43, 205, 120)

    def pizzas_precios(self): # Crea la página del análisis de los precios de las pizzas con 3 gráficas
        self.add_page()
        self.colour_rect()
        self.set_xy(0, 10)
        self.set_font('Times', 'BU', 30)
        self.cell(w=210.0, h=15.0, align='C', txt="PIZZAS PRICES ANALYSIS", border= False, ln = True)
        self.image('Pizzas_prices.png', 15, 28, 175, 93) # Posicionx, posiciony, tamañox, tamañoy (si solo pongo tamañox, tamañoy lo hace proporcional)
        self.image('Top_5_expensive_pizzas.png', 43, 122, 120)
        self.image('Top_5_cheap_pizzas.png', 43, 205, 119) # Posicionx, posiciony, tamañox, tamañoy (si solo pongo tamañox, tamañoy lo hace proporcional)

    def pizzas_vendidas(self): # Crea la página del análisis de la cantidad de pizzas pedidas con 3 gráficas
        self.add_page()
        self.colour_rect()
        self.set_xy(0, 10)
        self.set_font('Times', 'BU', 30)
        self.cell(w=210.0, h=15.0, align='C', txt="PIZZAS SOLD ANALYSIS", border= False, ln = True)
        self.image('Pizzas_sold.png', 15, 28, 175, 93) # Posicionx, posiciony, tamañox, tamañoy (si solo pongo tamañox, tamañoy lo hace proporcional)
        self.image('Top_5_popular_pizzas.png', 43, 122, 120)
        self.image('Top_5_less_popular_pizzas.png', 43, 205, 120) # Posicionx, posiciony, tamañox, tamañoy (si solo pongo tamañox, tamañoy lo hace proporcional)

def procesar_pedidos(pedidos):

    pedidos = pedidos[pedidos['pizza_id'].isnull() == False]
    pedidos = pedidos[pedidos['quantity'].isnull() == False]
    pizza_id = []
    quantity = []

    # Ahora procesaremos estas dos columnas del dataframe, remplazando ciertos caracteres por otros
    # para así tener estas dos columnas de manera que se correspondan los nombres de las pizzas
    # con los nombres de las pizzas en los dataframe pizzas e ingredientes. Con ello tratamos de
    # tener los nombres de las pizzas en el formato <nombre_separado_por_guiones_bajos_tamaño_pizza>
    # y las cantidades en números enteros positivos.

    for pizza_sin_procesar in pedidos['pizza_id']:
        pizza = pizza_sin_procesar.replace('@', 'a').replace('3', 'e').replace('0', 'o').replace('-', '_').replace(' ', '_')
        pizza_id.append(pizza)

    for cantidad in pedidos['quantity']:    
        cantidad = cantidad.replace('One', '1').replace('one', '1').replace('two', '2')
        cantidad = abs(int(cantidad))
        quantity.append(cantidad)

    pedidos['pizza_id'] = pizza_id  # Reescribimos las dos columnas del dataframe que acabamos de procesar
    pedidos['quantity'] = quantity

    return pedidos


def añadir_pizzas_totales(pizzas, pedidos):

    # Al dataframe de pizzas añade una columna que cuente las veces que se ha pedido cada pizza en el año

    lista = []
    for pizza in pizzas['pizza_id']:
        lista.append(pedidos[pedidos['pizza_id'] == pizza]['quantity'].sum())
    pizzas['totales'] = lista

    return pizzas


def cargar_ficheros():

    # Carga y procesa los ficheros csv necesarios para generar las gráfias a modo de análisis

    compra_semanal_ingredientes = pd.read_csv("compra_semanal_ingredientes.csv", sep = ",", encoding = "UTF-8")
    pedidos = pd.read_csv("order_details.csv", sep = ";", encoding = "UTF-8")
    pedidos = procesar_pedidos(pedidos)
    pizzas = pd.read_csv("pizzas.csv", sep = ",", encoding = "UTF-8")
    pizzas = añadir_pizzas_totales(pizzas, pedidos)

    return compra_semanal_ingredientes, pizzas


def graficos_ingredients_cantidad(compra_semanal_ingredientes):

    # Pone el fondo en Blanco con líneas negras
    # Ingredientes totales por semana (grande)
    sns.set_style('whitegrid')
    plt.figure(figsize=(20, 10))
    plt.title("Ingredients Per Week", fontsize = 48, fontweight = 'bold')
    ax = sns.barplot(x='Ingredient', y='Amount (units)', data=compra_semanal_ingredientes, palette='magma')
    plt.xlabel('Ingredients', fontsize = 32)
    plt.ylabel('Units', fontsize = 32)
    plt.xticks(rotation=90, fontsize = 16)
    plt.savefig('Full_Ingredients.png', dpi=300, bbox_inches='tight')

    # Cambia el fondo a ligeramente oscurito con líneas blancas
    # 5 ingredientes más usados por semana (pequeño)
    ingredientes_mas_usados = compra_semanal_ingredientes.sort_values('Amount (units)', ascending=False).head(5)
    sns.set_style('darkgrid')
    sns.set_palette('Set2')
    plt.figure(figsize=(8, 5))
    plt.title("5 Most Used Ingredients (per week)", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='Ingredient', y='Amount (units)', data=ingredientes_mas_usados, palette='magma')
    plt.xlabel('Ingredients', fontsize = 16)
    plt.ylabel('Units', fontsize = 16)
    plt.savefig('Top_5_used_ingredients.png', dpi=300, bbox_inches='tight')

    # 5 ingredientes menos usados por semana (pequeño)
    ingredientes_menos_usados = compra_semanal_ingredientes.sort_values('Amount (units)', ascending=True).head(5)
    plt.figure(figsize=(8, 5))
    plt.title("5 Least Used Ingredients (per week)", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='Ingredient', y='Amount (units)', data=ingredientes_menos_usados, palette='magma')
    plt.xlabel('Ingredients', fontsize = 16)
    plt.ylabel('Units', fontsize = 16)
    plt.savefig('Top_5_less_used_ingredients.png', dpi=300, bbox_inches='tight')

def graficos_pizzas_cantidad(pizzas):

    # Pone el fondo en Blanco con líneas negras
    # Pizzas vendidas totales (grande)
    sns.set_style('whitegrid')
    plt.figure(figsize=(25, 10))
    plt.title("Pizzas Sold", fontsize = 50, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='totales', data=pizzas, palette='magma')
    plt.xlabel('Pizzas', fontsize = 28)
    plt.ylabel('Amount', fontsize = 28)
    plt.xticks(rotation=90, fontsize = 12)
    plt.savefig('Pizzas_sold.png', dpi=300, bbox_inches='tight')

    # Cambia el fondo a ligeramente oscurito con líneas blancas
    # 5 pizzas más vendidas (pequeño)
    pizzas_mas_vendidas = pizzas.sort_values('totales', ascending=False).head(5)
    sns.set_style('darkgrid')
    sns.set_palette('Set2')
    plt.figure(figsize=(8, 5))
    plt.title("Top 5 Popular Pizzas", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='totales', data=pizzas_mas_vendidas, palette='magma')
    plt.xlabel('Pizzas', fontsize = 16)
    plt.ylabel('Amount', fontsize = 16)
    plt.savefig('Top_5_popular_pizzas.png', dpi=300, bbox_inches='tight')

    # 5 pizzas menos vendidas (pequeño)
    pizzas_menos_vendidas = pizzas.sort_values('totales', ascending=True).head(10).tail(5) # Para quitarme las 5 menos vendidas que se han vendido 0 veces
    plt.figure(figsize=(8, 5))
    plt.title("Top 5 Less Popular pizzas", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='totales', data=pizzas_menos_vendidas, palette='magma')
    plt.xlabel('Pizzas', fontsize = 16)
    plt.ylabel('Amount', fontsize = 16)
    plt.savefig('Top_5_less_popular_pizzas.png', dpi=300, bbox_inches='tight')


def graficos_pizzas_precio(pizzas):

    # Pone el fondo en Blanco con líneas negras
    # Precio de pizzas (grande)
    sns.set_style('whitegrid')
    plt.figure(figsize=(25, 10))
    plt.title("Pizzas Prices ($)", fontsize = 50, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='price', data=pizzas, palette='magma')
    plt.xlabel('Pizzas', fontsize = 28)
    plt.ylabel('Price ($)', fontsize = 28)
    plt.xticks(rotation=90, fontsize = 12)
    plt.savefig('Pizzas_prices.png', dpi=300, bbox_inches='tight')

    # Cambia el fondo a ligeramente oscurito con líneas blancas
    # 5 pizzas más caras (pequeño)
    pizzas_caras = pizzas.sort_values('price', ascending=False).head(5)
    sns.set_style('darkgrid')
    sns.set_palette('Set2')
    plt.figure(figsize=(8, 5))
    plt.title("Top 5 Expensive Pizzas", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='price', data=pizzas_caras, palette='magma')
    plt.xlabel('Pizzas', fontsize = 16)
    plt.ylabel('Price ($)', fontsize = 16)
    plt.savefig('Top_5_expensive_pizzas.png', dpi=300, bbox_inches='tight')

    # 5 pizzas más baratas (pequeño)
    pizzas_baratas = pizzas.sort_values('price', ascending=True).head(5)
    plt.figure(figsize=(8, 5))
    plt.title("Top 5 Cheap Pizzas", fontsize = 28, fontweight = 'bold')
    ax = sns.barplot(x='pizza_id', y='price', data=pizzas_baratas, palette='magma')
    plt.xlabel('Pizzas', fontsize = 16)
    plt.ylabel('Price ($)', fontsize = 16)
    plt.savefig('Top_5_cheap_pizzas.png', dpi=300, bbox_inches='tight')


def generar_gráficos(compra_semanal_ingredientes, pizzas):

    # Llama a las funciones que acabo de crear para generar todos los gráficos

    graficos_ingredients_cantidad(compra_semanal_ingredientes)
    graficos_pizzas_cantidad(pizzas)
    graficos_pizzas_precio(pizzas)


def crear_reporte_ejecutivo():

    # Crea el reporte ejecutivo en pdf incluyendo portado y gráficos (4 páginas)

    executive_report = PDF(orientation='P', unit='mm', format='A4')#pdf object
    executive_report.set_author('Miguel Ara Adánez') # Autor del pdf
    executive_report.portada()
    executive_report.ingredientes()
    executive_report.pizzas_precios()
    executive_report.pizzas_vendidas()
    executive_report.output('Executive_Report.pdf', 'F') # Guardar el pdf


if __name__ == '__main__':

    compra_semanal_ingredientes, pizzas = cargar_ficheros()
    generar_gráficos(compra_semanal_ingredientes, pizzas)
    crear_reporte_ejecutivo()
