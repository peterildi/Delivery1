#imports
import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

#reading the excel and the 4 sheets
githubpath = './data/'
df_customers = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="customers")
df_order = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="order")
df_employee = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="employee")
df_products = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="products")

#function for combining tables and calcualting sales
def get_data():
    df_employee['Employee_Names'] = df_employee['firstname'] + ' ' + df_employee['lastname']
    df_order['Sales'] = df_order['unitprice'] * df_order['quantity']

    order = pd.merge(df_order, df_products, on='product_id')
    order = pd.merge(order, df_employee, on='employee_id')
    order = pd.merge(order, df_customers, on='customer_id')

    return order

#Creating graphs
order = get_data()
fig_product=px.bar(order,
    x='productname', y='Sales',
    color='type', title='Sales by product',
    labels={'Sales':'Total Sales', 'productname':'Products', 'type':'Product Type'})

fig_employee = px.bar(order,
    x='Employee_Names', y='Sales',
    color='type', title='Sales by Employee',
    labels={'Sales':'Total Sales', 'Employee_Names':'Employee', 'type':'Product Type'})

#staring dash
app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Sales per Product'),

        dcc.Graph(
            id='graph1',
            figure=fig_product),]),
    html.Div([
        html.H1(children='Sales per Employee'),

        dcc.Graph(
            id='graph2',
            figure=fig_employee),])])

#running dash 
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
