# Bite Me - Restaurant Booking System

A modern, full-featured restaurant booking and management system built with Django. This application allows customers to make table reservations, view menus, and contact the restaurant while providing staff with comprehensive management tools.

## Features

### Customer Features

- **User Authentication**

  - Register/Login functionality 
    
    For registration you need to click the register button on the top right corner of the screen, sending user the to the registration form and the user needs to fill in all empty fields. Fail to do so will error show with red written instruction 
    what and how need to register.
    
    ![registration](/staticfiles/img/readme.MD%20images/register.png)

  - Password reset via email
    
    Every account user on the biteMe website can retrieve his account if they forget their password for a user account. Simply click on forgot password and the website will let you type in the email address connected to your account and send the email with instructions on how to reset your password. 
    
    ![forgot password](/staticfiles/img/readme.MD%20images/password%20reset.png)

  - Profile management

    When you register or log in to the bite-me website you can see the welcome message and ge, then you can see your account dashboard. Give the user full control of his account he can do everything, check the history of user reservations make new reservations edit his profile and much more.

    ![user](/staticfiles/img/readme.MD%20images/user.png)

  

- **Reservations**

  To reserve a table user must register on the website. On the user dashboard when you click Make a Reservation or Book Table, tuserhe is sent to the booking page with simple navigation. 

  ![book table](/staticfiles/img/readme.MD%20images/book%20table.png)

  - Book tables with specific date and time

    Users can book the table on the left side of the website in the booking table tab there is a form where users can pick the date up, and fill time and number of guests. On the right is the table availability pick the table Which is highlighted in green colour. The tables with red colour mean they are already booked or there is not enough room for your guests. 

    ![user input](/staticfiles/img/readme.MD%20images/booking%20info.png)

  - View and manage bookings

    Users can view details of their reservations they are information as when is next booking for how many people, and what time and day. Booking could be cancelled or changed if the user needs to change anything. There are action buttons on the site for cancellation reservations and modifications. 

    ![booking manager](/staticfiles/img/readme.MD%20images/booking%20manager.png)

  - Real-time table availability check

    Every account holder can check booking real live table availability if the user would like to change something like the different date or number of guests. Users can manage their reservations anytime.

    ![table availability](/staticfiles/img/readme.MD%20images/table%20availability.png)

    - If the user clicks on the modify reservation, the website redirects it user to the form to change the reservation details. 

    ![modify reservation](/staticfiles/img/readme.MD%20images/modify%20reservation.png)

  - Modify or cancel reservations

    - If the user wanted to cancel the reservation he needed to click on the highlighted red Cancel Reservation button above Modyfi Reservation. Then the information shows up about reservation info and if a user is sure to cancel a reservation. 
    Click Yes, Cancel Reservation for a late reservation or No, Keep the reservation.

    ![cancel reservation](/staticfiles/img/readme.MD%20images/cancel%20reservation.png)

- **Menu**
  Any person who visits the page can check our menu, simply go to the menu on the right corner of the web click it, and you can see what is on the menu.

  - View menu items by category
    There are four categories you can navigate to, starters, main course, desserts and sides. 
    Additionally you cold navigate by meal type just above the menu.

    ![menu](/staticfiles/img/readme.MD%20images/menu.png)

  - Filter by meal type (Breakfast, Lunch, Dinner)
    Switch in between the time of the day, morning afternoon or evening. 

    ![menu options](/staticfiles/img/readme.MD%20images/menu%20options.png)

  - Detailed item descriptions and prices
    All menu items have description and price. have descriptions and prices. 

    ![menu item](/staticfiles/img/readme.MD%20images/menu%20item.png)


- **Contact**

  - Contact form for inquiries
  - Automated email responses

  On the website, you see the contact information at the bottom or if the user would like to contact Restauration by email, can use the user would like to contact Restauration by email, can use the contact page. Click on Contact in the navigation bar in the top right corner, and then at the bottom if the user would like to contact Restauration by email, if the user would like to contact Restauration by email, can use the contact page. Click on Contact in the navigation bar in the top right corner, and then the website form will open up. 

  ![contact](/staticfiles/img/readme.MD%20images/contact.png)

    To contact the restaurant all form fields need to be filled correctly and she sends a message. 
    On the right side, you can see the address, opening hours and phone number, you can find a map with a tag where Users can find restaurants.

## Testing

This project includes comprehensive automated tests to ensure reliability and maintainability. Tests are written using Django’s built-in `unittest` framework.

### What’s Covered

#### Booking App
- **Model Tests**: `Table`, `Reservation`, `Contact`, and `EmailLog` models are tested for:
  - String representations
  - Relationship integrity (e.g. reservation ↔ tables)
  - Default field values

- **Form Tests**:
  - `ReservationForm`: Validates guest limits, date ranges (0–30 days), and time ranges (11:00–22:00)
  - `UserProfileForm`: Validates password change logic and email/username updates
  - `RegistrationForm`: Validates email uniqueness and user creation

- **View Tests**:
  - Added auth protection for views like `create_reservation_view` and `my_bookings_view`
  - Proper template rendering
  - Access control (403 or redirect for unauthorised access)

#### Menu App
- **Model Tests**: `Category` and `MenuItem` models are tested for:
  - String representations
  - Reverse relationship (`category.items.all()`)

- **Form Tests**:
  - `MenuItemForm`: Validates required fields, price formats, and meal type choices

- **View Tests** *(optional)*:
  - Test separately if implemented (admin panel, menu editing, etc.)

---

### How to Run Tests Locally

  Python manage.py test
  python manage.py test booking.test_models
  python manage.py test menu.test_forms
  

### Admin Features
  
  As an Admin, you are in charge of the website: 

- **Reservation Management**
  - View all reservations ( History and upcoming reservations)
  - Filter and search reservations
  - Cancel/modify bookings
  - Table allocation

- **Table Management**
  - Add/edit/delete tables
  - Set table capacities
  - Monitor table availability

- **Menu Management**
  - Add/edit/delete menu items
  - Organize items by category
  - Set meal types

- **Communication**
  - View and respond to contact messages
  - Email logs tracking
  - Message status management

  

## Technology Stack

- **Backend**: Django 5.0+
- **Frontend**: Bootstrap 5
- **Database**: PostgreSQL
- **Additional Packages**:
  - Django-crispy-forms
  - Django-widget-tweaks
  - Django-environ
  - Grammarly for typo mistakes
  - Personal Tower PC 
  - Windows 10

## Deployment 

  This website was deployed to the GitHub page as my repository the steps are below.
    Type in the new repository name and click "Create Repository." I chose my repository name and directory in the beginning.

The dev environment was Gitpod workspace, where the code was written. The steps to was:
  Sign up to GitHub click on the repository and open up by GitPod from the green icon on the left side.
  Workspace is opening up with all the environments to write the code. 

Heroku cloud application platform, steps i did:
    
Click Create New Application, choose a unique name for the app, choose a region, and create an app.
Go to settings and open config vars fill up all keys and values (database names and values)
Choose deployment methods, from the 3 options select Github, type in the repository name, and click search. 
chose your repository from Github by name and click connect to link your Heroku account with the GitHub repository
At the bottom of the page are automatic and manual deploy, I use the manual deploy. To test the app click open app from the top right. a region, and create an app.
Go to settings and open config vars fill up all keys and values (database names and values)
Choose deployment methods, from the 3 options select Github, type in the repository name, and click search. 
chose your repository from Github by name and click connect to link your Heroku account with the GitHub repository
At the bottom of the page are automatic and manual deploy, I use the manual deploy.
To test the app click open app from the top right corner.

## Credits

The information about website was taken from Code Institute from idea example 1.
I gathered the information for a better understanding of the restaurant booking system website.

Special thanks to:

 Support Tutor Assistance for helping me with my project at every step.
 My Mentor Rory Patrick Sheridan for advising me on my project.
 My Student care (Helped with my deadlines)
 Code Institute tutor team for helping me sort out some issues. 
Thank you
