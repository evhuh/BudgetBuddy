-> helpers.py
	Python code with helpful, pre-written functions to use in the main app.py code.
The ‘apology’ function is used to display a simple apology with the apology.html page, also taking an argument ‘message’ to customize the error message with respect to each circumstance.
The ‘login_required’ decorator function is used at every route in which the user must be logged in to access, this ensures users are logged in before gaining the ability to use the functions of the site.
The ‘usd’ function converts integers to USD format.

-> app.py
	Imports SQL from CS50 to make/user tables, flask to run the website, Session from flask_session to store session data, werkzeug.security to hash and check the hash when users set a password, and the helper functions.
The register route takes the actions to display the registration page, and post to register the user after checking they have filled the form, and their selected username has not been taken. Then, the password is hashed and necessary information is stored in the SQLite table ‘users’.
The LOGIN route’s get action displays the page, and the action post logs the user in by matching their username and hashes their inputted password to check against the stored hash in the database. Apologies are returned if passwords/usernames don’t match. If they successfully log in, they will be directed to the dashboard.
The LOGOUT route clears the user's session and redirects them to the login page.
The DASHBOARD route greets the user by their username and displays the budget, the status of their progress in staying below their budget goal, a chart that displays the category and their respective spendings, as well as a percentage bar that displays the percentage of their budget the user has spent thus far.
The INFO route, user inputted budget is inserted into the SQL chart to be displayed in index.html (the main dashboard), and the user is redirected to the dashboard upon inserting a budget. In the get method, a table is looped through in Jinja on info.html to display the categories available for the drop-down selection. An expense input section takes the category the user selected from the drop-down, the expense amount, and the expense name and inserts it into the input SQLite table. The information is used in index.html, info.html, and history.html as table displays. The expense removal section takes the user inputted id and matches it with the id of the column in the ‘input’ table to drop the row.
The HISTORY route gets the list of dictionaries from the ‘input’ table and ‘categories’ table to create a cohesive table to be displayed to users in the history tab of the web-application.
The SETTINGS is a tab that clears all expense inputs that correlate to the user’s id from the ‘input’ table and resets the budget to 0 in the ‘users’ table.

-> budgetbuddy.db
	SQLite database that includes three tables: ‘categories’, ‘input’, and ‘users’.
The table, ‘categories’ is framed by fields: id, user_id (foreign key that relates to the table user its respective field, id), and category. The table comes pre-filled with categories that appear in the info.html in a jinja loop that displays the category options for users to select in a drop-down when they input their expense. The table allows for ease of future expansion in the future, where the app may feature a customizable category-adding functionality for users to manually input unique categories of their choosing.
	The ‘input’ table has the fields: id, user_id, amount, expense_name, category_id, and date_time. This is to track the users expense inputs, and to display them in a table format for their viewing convenience.
	The ‘users’ table includes the fields: id, username, hash, and budget. This table stores the information of user-registered username and password (after hashing) used to reference when performing actions such as logging in, and outputting data to the users. Additionally, the budget field directly displays the budget users set for themselves, and is overridden each time they set a budget.

-> styles.css
	Sets the brand name to a large, bold, green color. Tone for application, seen site-wide.

-> layout.html
	Importing bootstrap functionalities, the layout.html page acts as the integral structure for the basic formatting of our site. Creates the navigation bar featured on every page of the web-application.

-> apology.html
	Simple html page that displays a message in case of an error that html functions cannot prevent, and displays a unique message to each error situation.

-> history.html
	A page on the application that displays the user’s expense tracking history by Jinja-looping through a table made in python.

-> index.html
	The main dashboard to the web-application. Users are greeted here and displayed a quick financial overview including: their set budget, status, a table with the amount they have spent within each category, and a visualization of the amount of their budget they have spent with a percentage bar.

-> info.html
	Contains three main sections; setting their budget goal, inserting expenses, and removing expenses, which is followed by a brief history chart to display their recent inputs.

-> login.html
	The login page features a field for username, a field for password, and a button to submit the form.

-> register.html
The register page features a field for username, a field for password, a field for password confirmation, and a button to submit the form.

-> settings.html
	A brief page that offers a single button for the user to reset their application, essentially clearing all preexisting data.
