from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
session = sessionmaker(bind = engine)
session = session()

# Routes for displaying JSONified data


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        print(restaurant.name)
        print(restaurant.id)
    return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    for i in items:
        print(i.name)
        print(i.id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/menu/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(MenuItems=item.serialize)

# Routes to main pages

@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/addrestaurant', methods=['GET', 'POST'])
def addRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("Restaurant Successfully Added")

        return redirect(url_for('allRestaurants'))
    else:
        return render_template('addrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurantToDelete)


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
        restaurantToEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if request.method == 'POST':
            restaurantToEdit.name = request.form['name']
            session.add(restaurantToEdit)
            session.commit()
            flash("Restaurant Details Successfully Edited")
            return redirect(url_for('allRestaurants'))
        else:
            return render_template('editrestaurant.html', restaurant=restaurantToEdit)


@app.route('/restaurants/<int:restaurant_id>/menu')
# Method is called when above addresses are visited.
# Call with the ID of the restaurant as a variable so that variable becomes build into the path.
# The variable also enables us to call queries on specific restaurants, as below.
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    # Passing the kwargs allows us to use these variables, created within the method, from within the template
    if items:
        return render_template('menuitems.html', restaurant=restaurant, items=items)
    else:
        return render_template('nomenuitems.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Successfully Created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        editedItem.price = request.form['price']
        editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
            methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
