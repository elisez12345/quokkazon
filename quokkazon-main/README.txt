Team: Query Quokkas

Team members:
- Phillip Ding (User Guru) --> Main designer of user and purchases tables. For milestone 3, Phillip wrote app/allpurchases.py and app/templates/allpurchases.html which allows someone to enter a uid and receive a table of all purchases by that user. Phillip also updated app/__init__.py to include this additional page as well as app/templates/index.html to include a button widget to access the allpurchases page. Features that have been added since the last milestone: Users now have a dedicatde profile page, users can now check their profile information, users can now register as sellers and gain access to all seller functionalities.

- Jonathan Shi (Seller Guru) --> Main designer of seller and inventory tables. For milestone 4, Jonathan wrote app/templates/editInventory.html, app/templates/orders.html and modified app/allpurchases.py, app/inventory.py, app/models/inventory.py, app/models/purchase.py. The inventory display has been updated to exclude product ID, sellers can now add, edit, and remove items from their inventory, as well as view and fulfill their orders plus add existing products to their inventory from the products page. Also updated some miscellaneous html template files to allow sellers to add existing products and improve flow between pages.

- Amy Weng (Social Guru) --> Main designer of feedback and messages tables. For milestone 4, Amy created myfeedback_edited.html and myfeedback_add.html, and she expanded the my_feedback.html, app/feedback.py and model/feedback.py files that she had created for the third milestone. She also wrote db/data/feedback.py to generate the two feedback CSV files, wrote the functions to generate users and purchases (gen_users and gen_purchases) in db/generated/gen.py, and modified the app/products.py and productDetail.html files to incorporate feedback details into individual product pages. Moreover, she updated index.html to place buttons to add or edit feedback next to each purchased product. 

- Lyndrinn Yao (Carts Guru) --> Main designer of carts table. For Milestone 3, Lyndrinn updated app/cart.py, app/models/cart.py, app/templates/cart.html, index.html, app/purchases.py, and wrote app/templates/sellerselection.html and app/templates/buyerorder.html. Features that have been added since the last milestone are the ability to view all sellers selling a product, add a product to the cart from a seller, update the quantity of an item in the cart, removing an item from the cart, displaying a calculated total price of items in the cart, and being able to submit the cart as an order, emptying the cart, updating the Purchases table and updating user balances accordingly.

- Elise Zhang (Products Guru) --> 
    - Main designer of products, tags, and categories table. For milestone 3, Elise wrote the app/products.py, app/models/stock.py, app/templates/products.html, app/templates/topProducts.html files, and put corresponding links into index.html.
    - For milestone 4 Elise has:
        - Created or updated: app/models/category.py, app/categories.py, app/products.py, app/carts.py, app/models/purchase.py, app/models/stock.py, app/static/css/main.css, app/templates/index.html, app/templates/productDetail.html, app/templates/products2.html, app/templates/searchResults2.html
        - Added a top products display on the home page,
        - Added a search bar to the header that searches through product names and description
        - Added a "add product" button on the inventory page that will allow users to add new products
        - Allowed pagination on the products pages
        - Allowed users to view certain categories
        - Allowed users to sort products by price
        - Made a product details page that displays product and seller information
        - Users can choose a seller to buy from and add the product to their cart

Everyone worked together to customize the website. 
https://gitlab.oit.duke.edu/query-quokkas/quokkazon 

We populate the database through the gen.py script: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/db/generated/gen.py?ref_type=heads
NOTE: We also used ChatGPT to create quokka themed products

Link to Milestone 4 Video Demo: https://gitlab.oit.duke.edu/query-quokkas/quokkazon/-/blob/main/Milestone_4_Demo_final.mp4?ref_type=heads
Or use this link: https://www.youtube.com/watch?v=ZExKCehaD2w
