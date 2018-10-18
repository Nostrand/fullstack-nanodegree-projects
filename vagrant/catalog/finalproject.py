from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# -- Database connection --
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Using '?check_same_thread=False' to prevent sqlalchemy.exc.ProgrammingError
engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# API Endpoint (GET Request)
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants=[r.serialize for r in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)

# -- Routing --
# Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)

# Create a new restaurant
@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant( name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

# Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = editedRestaurant)

# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash("Restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	return render_template('deleteRestaurant.html', restaurant = deletedRestaurant)

# Show a restaurant's menu
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html', restaurant=restaurant, items = items)

# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem( name = request.form['name'], description = request.form['description'],
		price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id)
	return render_template('newMenuItem.html', restaurant=restaurant)

# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu Item edited!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Menu Item deleted!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = deletedItem)



# -- End of file --
if __name__ == '__main__':
	app.secret_key = 'super_secret_key' # Just a common password for development
	app.debug = True 					# Server reloads everytime it notices a change in the code
	app.run(host = '0.0.0.0', port = 5000)