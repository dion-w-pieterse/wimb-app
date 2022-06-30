# wimb-app (Where Is My Book?)

## Application Setup
Note: All usernames, passwords and database names and instances have been removed. You will need to set these up yourself. All images have been removed, and replaced with placeholder images.

### Dropping/Creating The Database Manually via Console and Python shell:

- Create the sqlite3 database:
    - Navigate to the project directory.
        - ```sqlite3 <database name>.db```
        - ```.tables```
        - ```.exit```
- Use dbsetup.py python script:
    - ```python dbsetup.py -u <username> -p <password>```
    - Note: The username and password that you use in the command above will be granted the admin user role.

- Now you can run the app, and login under the admin account you just setup.
- You can create and manage regular users via the admin account.


### Setup The Application (No repo clone process)

- create a project directory
- create a virtual environment (MacOS):
    - ```virtualenv \<environment name\>```
- activate your environment (MacOS):
    - ```source <environment name>/bin/activate```
- install all libraries using the requirements.txt file provided:
    - ```pip install -r requirements.txt```
- Your environment is setup and now you can run your app.
    - ```python app.py```


### Database User Created (if you use the database provided in the repo, these users are already rows in the DB):

  (Note: Only regular non-admin users can be created via the registration page).
- Admin:
    - ```username: admin```
    - ```password: <password>```

- Regular user 1:
    - ```username: test_person```
    - ```password: <password>```

### How To Delete / Rebuild SQLAlchemy Database, and Run a Fresh Database (via console if not using the dbsetup.py script):

- ```rm <database name>.db```
- ```sqlite3 <database name>.db```
- check the database is empty
    - ```sqlite3 <database name>.db```
    - ```.tables```
    - ```.exit```
- Enter Python shell in console:
    - ```python```
    - ```from app import db```
    - ```db.create_all()```     Note: If you need to drop the tables: db.drop_all()
    - ```exit()```
- Check all the tables are present via console:
    - ```sqlite3 <database name>.db```
    - ```.tables```
    - (You should see all the tables created)
    - ```.exit```
- Restart the app via console:
    - ```python app.py```

## Summarized Software Requirements Specification

## 1. INTRODUCTION

## 1.1 Purpose
This SRS document offers a description of the software requirements. The document will explain the purpose of the website, its functionalities, including the software requirements and overall goals to be accomplished.

## 1.2 Scope of the Problem
As the world has transitioned from physical stores to digital market an Online Bookstore is a boon to readers to buy a book online delivered to their doors on a few clicks. As the other online bookstores are available in the market, we will be having our own online bookstore website hosted on the internet for users to order books online. The users can browse through various categories of books and select and order desired books online. There will be some additional features added to the bookstore to the user side as well as the admin side of the website.

## 1.3 Intended Audience
The Intended Audience of this document includes Professor Lidia Morrison, and the members of our group to verify the functionality of the software. Other users include all students enrolled in CPSC 462 for (Spring 2021) at California State University, Fullerton. The application is intended for individuals in need of buying books online.

## 2. OVERALL DESCRIPTION
## 2.1 User Objective
Where’s My Book? Is a web application that focuses on providing a medium by which a user can buy a book online. This application will help users save time by physically going to store and find the desired book. Our web application will save the users time as users can just enter the name of the book desired or search for it in different categories made available on the web store. Figure 6.1 shows the Where’s My Book interface.

## 2.2 Product Functions
Where’s My Book is an online web store to purchase books. It allows users to view books in different genres, varieties, categories, etc. Users can select books over a wide range of categories and browse through them with brief details of each book mentioned on the individual book page. This web application facilitates users to search a book individually by typing the credentials related to that book in the search bar and also can filter the search according to their will. Users can add to cart as many books they want and can adjust the quantity of books they want to order. Users have the option to pay with credit card or debit card and get their books delivered to their doorsteps. Where’s My Book gives a detailed order summary of each order of the user to them before placing the order.
Below are the basic functions of Where’s My Book?:
- The website allows the non-registered users to browse through the homepage and take a look at the books.
- The website allows users to filter their search with different options.
- Authenticated users can order books from the online web store Where’s My Book.
- The website allows users to select books from a wide range of categories.
- Order Summary will be available to users after adding all the items to cart.
- Website allows users to add/edit the delivery information and credit card details at checkout.

## 2.3 Operating Environment
Where’s My Book is an online web store developed using front-end technology like Bootstrap CSS Framework, JQuery. Back-end technology like Python Flask and DBMS, Object-Relational-Mapping (ORM), and Other DB Tools: SQLite3, SQLAlchemy, PugSQL. Group-Code-Development Plugin: Git Live. DVCS: Git. Graphical Tools: Adobe Photoshop, Adobe Illustrator. User-Experience Design Tool: Adobe XD. Hosting Service: AWS Lightsail – Amazon. Email Service: Gmail SMTP Server. Text-to-Speech Service: AWS Polly – Amazon. This web application can work on all the Operating Systems and can be opened on Google Chrome, Microsoft Edge and Mozilla Firefox.

## 2.4 Similar System Information
There are more than hundreds of web applications for selling books online. Topping the list are: Amazon Books, Barnes and Noble, Powell’s Book, AbeBooks, Book Depository, etc (Source: https://booksliced.com)

## 2.5 User Characteristics
This app is for users interested in buying books online in a hard copy format or online version. The app can be used by all age groups. Users should only have skills to add the details correctly in the web application as needed. The user friendly interface and easy to understand features will facilitate users to order books from the web application smoothly.

## 2.6 Design and Implementation Constraints
This web application is a simple online bookstore to buy books online and not an entertainment site. This website will be able to work on all the Operating systems which have access to browsers such as Google Chrome, Mozilla Firefox and Microsoft Edge. This website needs the user to be authenticated so as to order books through the website. Unauthorized users will only be able to view the home page and search for books.

## 2.7 Assumptions
This SRS assumes that:
- Users understands English Language
- User has a device with accessibility to a browser
- User has connectivity to internet
- User can access and use a browser
- User can access to link and access the website
- User has a valid Email address
- User can create a account
- Users know how to search and apply filters to search
- Users have a valid credit card or debit card to purchase the book

## FUNCTIONAL REQUIREMENTS

## USER VIEW

## 3.1 The app shall display the home page
**Description**:
After entering the link in the browser/ clicking the link to open in the browser, a home page will be displayed.
**Pre-condition**: – User has the link to the website.
**Post-condition**: – The home page is displayed.

## 3.2 The app shall display the login page
**Description**:
The user will be directed to the login page. If the user is registered with the web application user can enter the correct credentials in the spaces provided for email and password.

**Pre-condition**: User has valid credentials like the email and password registered with the web application.

**Post-condition**: The user is directed to the homepage if the credentials are authorized correctly and will be signed in, else the user is prompted that the entered credentials are incorrect.

## 3.3 The app shall allow the user Register as a new user
**Description**:
The app shall let the user register with the web application by creating a new account by entering credentials like First name, Last name, email and password. This action takes place if the new user clicks on the “Create Account” link on the Login Page.

**Pre-condition**: User clicks the “Create account” link on the login page.

**Post-condition**: The user has to enter the credentials like First name, last name, email and password to create a new account. The data is stored in the database and the user is directed to the login page to log in as an authenticated user.

## 3.4 The app shall display the home screen for authorised user
**Description**:
The Where’s My Book home screen is displayed. The home screen contains a wide range of categories of books under which individual book information is displayed. On the Home page users can view the individual book, quick add to cart the individual book, search and filter the book search, go to cart page, go to login page, browse through different categories of books. Users can use a “Top Arrow ^” Button to go to the top of the homepage. Users can also Update or Add their User details by clicking the “Account” button on the Navigation bar.

**Pre-condition**: User enters correct login credentials like the email and password and was authorised to go to the home page.

**Post-condition**: Users can browse through different categories of books, view each book individually, read the individual book descriptions under the book cover image, View price of each book under the book cover of each book, Add to cart the individual book, view the product individually. Users can also search for a particular book and apply filters for the search results. Users can go to the login page from the home page. Users can view the cart page by clicking the cart link from the home page.

## 3.5 The app shall allow the user to Add/Update the User Details Information
**Description**:
The app shall allow the Authorized user to Add/Update the User Details Information on the User Details Update Form Page. Users can access this page by clicking on the “Account” button on the Navigation bar. Here the user can enter or update the information in the text
fields provided like, First Name, Last Name, Email, Phone, Address, City, State, Zip-Code, Country, Credit Card type. When the user is done entering the information, the user can click “Update Your Information” so the information is saved into the database. When this information is saved in the database the data will be pre populated for the user in the checkout page.

**Pre-condition**: User clicks the “Account” Button on the Navigation Bar.

**Post-condition**: The user enters information in the text fields provided like, First Name, Last Name, Email, Phone, Address, City, State, Zip-Code, Country, Credit Card type. Updates the Information and saves it for future use.

## 3.6 The app shall allow the user to view individual product
**Description**:
The user can click on the button “View Item” under the cover page of any individual book displayed, and can go to an individual product page to get brief information of a book. On the Individual product page the user can see the cover photo of the book. Read a detailed description of the book, check the price of the book. View different information related to the book. Users can go back to the home page by clicking the back button or home link. The user can search for books and add filters to the search on the search bar. Users can add book to the cart. Users can go to the cart page by clicking the cart link. Authorised Users can enter a review of the individual book in the provided text field for review and submit the review by clicking the submit review button. Users can also view the reviews by other users on this page.

**Pre-condition**: User clicks the “View Button” on the individual item displayed on the home page.

**Post-condition**: Users can see the individual product page, read the detailed description of the book, read the information related to the book, add book to cart, go to cart page, search a book and add filters to the search result, add reviews, go to home page.

## 3.7 The app shall allow the user to Add book to cart from the Individual Product Page
**Description**:
Users can click on the “Add to Cart” button to add the book to the cart for delivery on the Individual Product Page. Users can adjust the quantity of the books by the “+” and “-” quantity buttons provided to increment and decrement the book quantity respectively. The user can manually input the quantity of books in the text area provided between “+” and “-” buttons. The quantity of the book as well as the price according to the quantity is adjusted in the cart. A confirmation of the book and items added to cart page is displayed to ensure that the book is added to cart.

**Pre-condition**: User is on the Individual Book Page and clicks on the “Add to Cart” Button.

**Post-condition**: The books are added to cart and cart quantity and price is adjusted according to the user selection.

## 3.8 The app shall allow the Authorised user to add and view Reviews for the book on Individual Product Page
**Description**:
Authorised Users(Users who have an account registered with Where’s My Book?) can enter the Review for the particular book in the text area provided under the book cover page and click on the “Add Review '' button to add the Review for the book on the Individual Product Page. Unregistered as well as registered users can view the reviews for the book on the individual book page.

**Pre-condition**: User is on the Individual Book Page, enters review in the text area and clicks on the “Add Review” Button to add reviews for a book.

**Post-condition**: The Review is posted in the review section. Users view reviews in the review section.

## 3.9 The app shall allow the user to Play an audio Sample
**Description**:
When the user is on the individual book page the user can play a sample audio of that book which is below the Book Title on the Individual Book Page. When the user clicks on the Play button of the Audio, a sample chapter will be played for that book in English Language.

**Pre-condition**: User is on the Individual Book Page and clicks on the play audio button.

**Post-condition**: The user will be able to listen to the audio sample provided for the book.

## 3.10 The app shall allow the user to quick add a book to cart on Home Page.
**Description**:
The user can click on the “Quick Add Cart” button below the individual book description on the homepage to add the book to cart. A confirmation of the book and items added to cart page is displayed to ensure that the book is added to cart. The cart items and price is updated in the database according to the items added to cart.

**Pre-condition**: User clicks on the quick add to cart button.

**Post-condition**: The user is directed to the confirmation page where the user can see the number of items added to cart. Items in cart are updates and price also updates. Book is successfully added to the cart.

## 3.11 The app shall allow the users to search a book
**Description**:
On the navigation bar of each page is the search bar. Users can enter text related to books to search for books and then can add filters like price filters, genre filters, category filters to make their search easier. In the search results the user can view the book description and details related to the book besides the cover picture of the book.

**Pre-condition**: The user enters a search text in the search bar present on the navigation bar.

**Post-condition**: Users can see displayed results of their search. Users can apply filters to the search results and view individual books description and details beside the cover page. Users can click on a book to visit its individual book page.

## 3.12 The app shall allow the user to view the cart page
**Description**:
The user can click on the cart link on the navigation bar to get to the cart page. The users can view the detailed order summary on this page. Users can adjust the quantity of books by clicking on the + and - buttons to increment and decrement the book quantity respectively. When the user clicks on the Update cart button the cart is updated with the correct amount of books and rate of the books according to the adjustments done by the user. After clicking the proceed to checkout button user will be directed to the checkout page.

**Pre-condition**: User clicks on the cart link on the navigation bar.

**Post-condition**: User views the cart summary on cart page. Adjusts the quantity of books. Users can go to the checkout page on the button click of the checkout page.

## 3.13 The app shall allow the user to view the checkout page
**Description**:
After clicking on the checkout button on the cart page, the user will be directed to the checkout page. Users can see the detailed order summary on the checkout page. The user can see the shipping details on this checkout page. Users can see the customer details form which gives delivery information for the book, this field will be pre populated if the user information is present in the database. User needs to enter the credit card details on this page so as to make the payment for the order to be delivered. After clicking the “Place Order” button the order will be placed for the books after verification of the credit card details. The user will receive a confirmation Email containing the order details in it.

**Pre-condition**: The user clicks on the proceed to checkout page on the cart page.

**Post-condition**: Order for books will be placed and users will be directed to the confirmation page. Users will receive an Confirmation email of their order.

## 3.14 The app shall display the confirmation page
**Description**:
After successfully placing the order for books the user will be directed to the confirmation page. An order confirmation message is displayed on this page. Users can click the home button to be redirected to the home page.

**Pre-condition**: The user successfully makes the payment for the order and successfully places the order.

**Post-condition**: An order successful message will be displayed and the user can go to the home page.

## 3.15 The app shall allow the user to logout of the web application
**Description**:
The user can log out of the web app by selecting the “Logout” button from the navigation bar.

**Pre-condition**: User clicks on the “Logout” button from the navigation bar.

**Post-condition**: User is logged out of the application and taken back to the home page.

## 3.16 The app shall allow the users to set a new password
**Description**:
The user can request a new password to enter the website if the user forgets the password. When the user clicks on the “Forgot Password” link on the login page the user will get an email with the temporary password so the user can access their accounts. When the user clicks the “Forgot Password” link, the user will be directed to the Forgot Password Form. Here on the Forgot Password From user will have to enter the email address entered while registration to get the email for temporary password. After logging in with the temporary password, the user will see a confirmation message and users can reset a new password by clicking the “Rest” option on the Navigation bar.

**Pre-condition**: User clicks the forgot password link on login page.

**Post-condition**: User receives an email with temporary login details to access their account and reset a new password.

## 3.17 The app shall allow the users to read the about us page with Animation.
**Description**:
The user can read the About us information i.e the developers of the website information, The qualities of the company, Interesting facts about the website; on About us page, by clicking on the “About button” on the navigation bar or below in the footer.

**Pre-condition**: User clicks the About us button on the navigation bar or the footer.

**Post-condition**: User is directed to the About Us page, can see an Animation on the page and can read the details of the website and developers on About Us page.

## 3.18 The app shall allow the users to update their Information
**Description**:
The authorised user can click on the “Account” button on the navigation bar. The user will be directed to the update details update form. Here the user information available in the database will be pre populated. Users can update or add any new information in this form and click on the “Update Information” button to confirm the changes to be saved in the database.

**Pre-condition**: User clicks the “Account” button on the navigation bar.

**Post-condition**: Users directed to the update details update form. Users can update the information and that will be saved in the database after clicking the “Update Information” button.

## ADMIN VIEW
## 3.19 The app shall allow the admin to login
**Description**:
The authorised admin will already have their login credentials, the username and password saved in the database. Admin shall enter the correct credentials on the login page of the web application, like the username and password to get access to the admin view side of the application. After clicking the “Login” button admin will be directed to the Homepage of Where’s My Book?

**Pre-condition**: Admin opens the login page, enters the correct credentials to login.

**Post-condition**: Admin credentials verified with database and Admin directed to authorized admin homepage.

## 3.20 The app shall allow the admin to reset password
**Description**:
The admin can request a new password to enter the website if the admin forgets the password. When the admin clicks on the forgot password link on the login page the admin will get an email with the username, temporary password so the admin can access their accounts. After logging in with the temporary password admin can reset a new password.

**Pre-condition**: Admin clicks the forgot password link on the login page.

**Post-condition**: Admin receives an email with temporary login details to access their account and reset a new password.

## 3.21 The app shall have access to the Admin Dashboard
**Description**:
The admin can click on the Admin Dashboard button on the navigation bar for admin and have access to the different controls admin can control and manage.

**Pre-condition**: Admin clicks the Admin Dashboard button.

**Post-condition**: Admin directed to Admin Dashboard.

## 3.22 The app shall allow the admin to view the homepage
**Description**:
The admin can also be a regular user and browse through different categories of books and place an order for books like the regular user following the same steps. The admin will have all the access to the website as a regular user. Admin homepage will have the similar features like the user view mentioned above.

**Pre-condition**: Admin clicks on the Home button on the navigation bar.

**Post-condition**: Admin is directed to the homepage.

## 3.23 The app shall allow the admin to manage the admin and users records
**Description**:
Admin has access to the admin dashboard under which there is a User link on the navigation bar. On this page Admin can edit/delete admin/user records, create new admin/user records, export the record in any file format, filter the user table according to username, password or role, delete the current selection and search admin/user.

**Pre-condition**: Admin clicks on the User button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the admin/user records.

## 3.24 The app shall allow the admin to manage the users details
**Description**:
Admin has access to the admin dashboard under which there is a User Details link on the navigation bar. On this page Admin can edit/delete user records, create new user records, export the record in any file format, filter the user table according to username, password or
role, delete the current selection and search user.

**Pre-condition**: Admin clicks on the User Details button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the user details records.

## 3.25 The app shall allow the admin to manage the book records
**Description**:
Admin has access to the admin dashboard under which there is a Book on the navigation bar. On this page Admin can edit/delete book records, create new book records, export the book record in any file format, filter the book table according to filters given, delete the current selection of book records and search book records.

**Pre-condition**: Admin clicks on the Book button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the book records.

## 3.26 The app shall allow the admin to Book Status
**Description**:
Admin has access to the admin dashboard under which there is a Book Status link on the navigation bar. On this page Admin can view the book id and the status of books. Admin can edit/delete a record, create a new book status record, export the record in any file format, filter the table according to Status Desc, delete the current selection and search a record.

**Pre-condition**: Admin clicks on the Book Status button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Book Status records.

## 3.27 The app shall allow the admin to manage the reviews
**Description**:
Admin has access to the admin dashboard under which there is a Reviews link on the navigation bar. On this page Admin can edit/delete a review, create a new review, export the record in any file format, filter the reviews table according to Review Desc, delete the current selection and search reviews.

**Pre-condition**: Admin clicks on the Reviews button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Reviews records.

## 3.28 The app shall allow the admin to manage the Book Order
**Description**:
Admin has access to the admin dashboard under which there is a Book Order link on the navigation bar On this page Admin can edit/delete book order records, create new book order record, export the record in any file format, filter the book orders table according to filters available, delete the current selection and search a book order record.

**Pre-condition**: Admin clicks on the Book Order button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Book Order records.

## 3.29 The app shall allow the admin to manage the Book Order Item Records
**Description**:
Admin has access to the admin dashboard under which there is a Book Order Item link on the navigation bar On this page Admin can edit/delete book order item records, create new book order item record, export the record in any file format, filter the book orders item table according to filters available, delete the current selection and search a book order item record.

**Pre-condition**: Admin clicks on the Book Order Item button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Book Order Item records.

## 3.30 The app shall allow the admin to manage the Genre
**Description**:
Admin has access to the admin dashboard under which there is a Genre link on the navigation bar. On this page Admin can edit/delete any Genre records, create new Genre records, export the record in any file format, filter the Genre table according to filters available, delete the current selection and search for a Genre record.

**Pre-condition**: Admin clicks on the Genre button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Genre records.

## 3.31 The app shall allow the admin to manage the Images uploaded for the books
**Description**:
Admin has access to the admin dashboard under which there is a Image Uploads link on the navigation bar. On this page Admin can edit/delete a Book Image, create a new book image record, and delete the current selection.

**Pre-condition**: Admin clicks on the Image Upload button on the navigation bar under the Admin Dashboard.

**Post-condition**: Admin can manage the Image Upload records.

## 3.32 The app shall allow the admin to logout of the web application
**Description**:
The Admin can log out of the web app by selecting the “Logout” button from the navigation bar.

**Pre-condition**: Admin clicks on the “Logout” button from the navigation bar.

**Post-condition**: Admin is logged out of the application and taken back to the home page.

## Summarized Software Design Description Documentation

### General Overview
In the modern world where anything and everything can be bought online from multiple separate sites, the website Where’s My Book? dares to offer a selection of books so varied any book can be found and purchased easily. This site not only tries to compete with other online bookstores but with physical bookstores as well by offering convenient book searching, audiobook capability, and short shipping times.

### Application Overview
Where’s My Book? Is a web application that focuses on providing a medium by which a user can buy a book online saving time wasted by physically going to a store and searching for their desired book. Our web application will save time by making it simple to find a book as users can just enter the name of the book or search for it within the different categories available on the web store.
  On initial entry into the site the user is greeted by the homescreen. On the homescreen the user is able to see a small sample of books from different categories. Additionally from this page the user is able to register an account or login to their existing account by clicking on the Register or Login buttons respectively. The user is also able to search for a book from the search bar and see what books they are going to purchase if they click on the cart button. On the login page the user will enter their username and password to login. On the registration page the user will enter their email and create a username and password to create an account. Having an account is not required to use the website but it does allow the user to save their shipping information so that it does not need to be entered every time an order is placed.
  Using the search bar will send the user to the search results page where books that pertain to the search query will be displayed and can be selected to add to the user’s cart. Selecting a book will open that book’s product page where the user can see more information about the book, add multiples of the book to their cart, and write a review about the book. When the user visits their cart page they are able to see all the books they are about to purchase and the total cost of the books. From this page the user can edit their cart through removing books or adding more quantities of a book and also they can proceed to place their order. After proceeding to checkout a first time or not logged in user will enter their shipping details and payment method while a logged in user will be able to check if their information is correct before placing their order.

## APPENDIX A: USER OPERATIONS MANUAL

## 1. Home Page
On clicking or entering the web app URL from the device’s browser, the Where’s My Book? Home Page is displayed. On top of each page is the Navigation Bar. You can Click “Home” to return to the home page from any other page. You can click “ Register” to register as a new user with the website. You can click “Login” to Log into the website. You can click “About” to get Information about the website and developers. You can click “Cart” to view the cart page. You Can use a “Top Arrow ^” Button to go to the top of the homepage.

## 2. Login Page
Enter Username and Password to sign in and start using the app.

## 3. Forgot Password
When you Forget your Password you can click on the “Recover Password” link on the Login Page. You will then be directed to the Forgot Password Form page where you will have to enter the registered email address to receive the temporary password. When you click the “Recover Password” button you will receive the email to retrieve your password. After successfully entering the correct temporary password you will see a confirmation page.

## 4. Create New Account
If you are a first time user, you are required to create an user account with Where’s My Book?.
This can be done by selecting the “Create Account” Link from the login page. To create an account you need to enter your valid email, username and password. Also you need to confirm your password entered. After clicking the “Register” button you will be directed to the Login.

## 5. Account Information Page
When the user Logs in with the correct credentials, the user can update their Account Information by clicking on the “Account” button on the Navigation bar. Here the user can fill the User Details Update Form by adding in the information in the text fields provided like, First Name, Last Name, Email, Phone, Address, City, State, Zip-Code, Country, Credit Card type. When the user is done entering the information, the user can click “Update Your Information” so the information is saved into the database. When this information is saved in the database the data will be pre populated for the user in the checkout page.

## 6. Search Books
On the Navigation Bar on each page of Where’s My Book? Website you can type in the search area provided and search for books of your choice by hitting “Search” Button. You can also apply filters to the search results like, Genre filter, price filter. For advanced Filtered search you can also type in your book name in the text field provided below Advanced Filtered Search and when you hit the “Search” button you will see the search results below.
  In the Search results you can also View Individual Book Page for more information on the individual book by clicking the “View” Button and you will be directed to the Individual Product Page. You can also add a book to cart from this search results page by clicking the “Quick Add Cart” button. The book will be added to cart and cart will be updated.
  
## 7. View Individual Book Page
On the Individual Book Page, you can Listen to the sample book audio by clicking on the play button. You can see the Cover Picture of the book, title, price, description, book author, language, ISBN number on this page related to that book you opened. You can also add a review for the book on this page. To add Review, you must be a registered user and logged in to review a book. You can click on the “Add Review” button to add review and type in the text area provided.
  You can Add a book to cart by clicking the “Add to Cart” button. You can adjust the quantity of the books by clicking “+” to increment the quantity and “-” to decrement the quantity. And all the updates will be updated in the cart according to your selection.
  
## 8. Add Book to Cart
You can either add a book to cart from Homepage, Search results page or Individual Book Page. When you add a book to cart you will get this screen displayed to confirm that the book is added to cart. On clicking “Return” you will return to the Individual book page of that book added to cart.

## 9. Cart Page
When you click the Cart option on the Navigation Bar of any page you will be directed to the Cart Page. Here you will see your Order Summary Which contains the details like Number of Items in cart, Grand total mpf your order, Tax, The Item Information, Details of the book also you can adjust the book quantity by clicking '+' to increment the quantity of books and '_' to decrement the quantity of books. When you adjust the order quantity the price will be updated accordingly. Once you are done adding books to cart you can either click “Update Cart” Button so as to update the recent changes you made to cart or you can click “Proceed to Checkout” button to go to the checkout page.

## 10. Checkout Page
On the Checkout page you will see the book details you have added to the cart. You will have to either update your Customer information if we do not have that in our database, or else it will be pre populated. You can view the order summary, Shipping details on this page. Once you are done and satisfied with your cart you can make a payment for the book you want to purchase and successfully place an order by clicking on the “Place Order” button.

## 11. Confirmation Page
Once you place an order on the checkout page you will be directed to a Confirmation page. Here you will view a message something like below, confirming your order placement. You can go back to Homepage by clicking on the “Return Home” button. You can also “Logout” using the “Logout” option on the Navigation Bar.


## Documentation is pending. Please check back soon.
