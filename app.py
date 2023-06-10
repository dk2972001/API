from flask import Flask, jsonify, request
from waitress import serve
import pandas as pd

df = pd.read_csv('C:/Users/2001d/Downloads/data.csv')
app = Flask(__name__)


@app.route('/api/total_items', methods=['GET'])
def total_items():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    department = request.args.get('department')

    # Filter the dataset based on the specified criteria
    filtered_df = df[(df['department'] == department) & (df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate the total items sold
    total_items_sold = filtered_df['quantity'].sum()

    return jsonify(total_items=total_items_sold)


@app.route('/api/nth_most_total_item', methods=['GET'])
def nth_most_total_item():
    item_by = request.args.get('item_by')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    n = int(request.args.get('n'))

    # Filter the dataset based on the specified criteria
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate the nth most sold item based on quantity or price
    if item_by == 'quantity':
        nth_item = filtered_df.groupby('item_name')['quantity'].sum().nlargest(n).index[n - 1]
    elif item_by == 'price':
        filtered_df['total_price'] = filtered_df['quantity'] * filtered_df['unit_price']
        nth_item = filtered_df.groupby('item_name')['total_price'].sum().nlargest(n).index[n - 1]
    return jsonify(item_name=nth_item)


@app.route('/api/percentage_of_department_wise_sold_items', methods=['GET'])
def percentage_of_department_wise_sold_items():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Filter the dataset based on the specified criteria
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate the percentage of sold items department-wise
    department_percentages = filtered_df.groupby('department')['quantity'].sum() / filtered_df['quantity'].sum() * 100

    return jsonify(department_percentages.to_dict())


@app.route('/api/monthly_sales', methods=['GET'])
def monthly_sales():
    product = request.args.get('product')
    year = int(request.args.get('year'))

    # Filter the dataset based on the specified product and year
    filtered_df = df[(df['product'] == product) & (df['year'] == year)]

    # Calculate the monthly sales
    monthly_sales_list = filtered_df.groupby('month')['total_price'].sum().tolist()

    return jsonify(monthly_sales=monthly_sales_list)


if __name__ == '__main__':

    serve(app, port=5000, host='127.0.0.1')