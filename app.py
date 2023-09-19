from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.db'  # SQLite database file
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    list_name = db.Column(db.String(100), nullable=False, default="Default")
    url = db.Column(db.String(100), nullable=False)
    recommended = db.Column(db.Boolean, default=False)
    ordered = db.Column(db.Boolean, default=False)



@app.route('/')
def index():
    return '''
    Welcome to the Trackshops<br>
    <a href="/add">Add Item</a><br>
    <a href="/lists">View Lists</a><br>
    <a href="/recommended">View Recommended Items</a><br>
    <a href="/order_history">Order History</a>
    '''


@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    list_name = request.form.get('list_name')
    url = request.form.get('url')
    recommended = request.form.get('recommended')

    if item_name:
        new_item = Item(name=item_name, list_name=list_name, url=url, recommended=bool(recommended))
        db.session.add(new_item)
        db.session.commit()
        return get_add_item()
    return "Invalid input."



@app.route('/add', methods=['GET'])
def get_add_item():
    return render_template('add.html')


@app.route('/recommended')
def recommended_items():
    # Retrieve recommended items from the database or any other data source
    # For example, you can query items with a "recommended" flag set to True
    recommended_items = Item.query.filter_by(recommended=True).all()
    return render_template('recommended.html', recommended_items=recommended_items)


@app.route('/order', methods=['POST'])
def order_items():
    # Get the list of item IDs from the form submission
    item_ids = request.form.getlist('item_ids')

    # Set the "Ordered" value to True for the selected items
    for item_id in item_ids:
        item = Item.query.get(int(item_id))
        if item:
            item.ordered = True

    # Commit the changes to the database
    db.session.commit()

    # Redirect back to the lists page or any other desired page
    return redirect('/lists')


@app.route('/list/<list_name>', methods=['GET'])
def get_list_items(list_name):
    # Retrieve all items with the specified list name
    items = Item.query.filter_by(list_name=list_name).all()
    return render_template('list.html', list_name=list_name, items=items)


@app.route('/lists')
def lists():
    # Retrieve all unique list names
    list_names = db.session.query(Item.list_name).distinct().all()
    list_names = [name[0] for name in list_names]  # Extract names from tuples

    return render_template('lists.html', list_names=list_names)

@app.route('/order_history')
def order_history():
    # Retrieve a list of items that have been ordered in the past
    ordered_items = Item.query.filter_by(ordered=True).all()
    return render_template('order_history.html', ordered_items=ordered_items)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)