# Bite Me - Restaurant Booking System

A modern, full-featured restaurant booking and management system built with Django. This application allows customers to make table reservations, view menus, and contact the restaurant, while providing staff with comprehensive management tools.

## Features

### Customer Features

- **User Authentication**

  - Register/Login functionality 
    
    For registration you need to click register butto on top right corner of the screen, sending user to registration form and user need to fill all empty fileds. Fail to do will error show with red writen instruction 
    what and how need to register.
    
    ![registration](/staticfiles/img/readme.MD%20images/register.png)

  - Password reset via email
    
    Every account user in biteMe website is able to retrive his account if they forggot theyr passwork for user account. Simply click on forgot passwork and the website will let you typ in emial address connected to your accont and send the emial with instruction how to reset passowrd. 
    
    ![forgot password](/staticfiles/img/readme.MD%20images/password%20reset.png)

  - Profile management

    When you register or log in to bite-me website you can see welcome message, then you can see your account dashboard. Give user full control of his acount he coud do everything, check history of user reservation make new reservation edit his profile and much more.

    ![user](/staticfiles/img/readme.MD%20images/user.png)

  

- **Reservations**

  To reserv table user must be register on the website. On the user dashboard when you click Make a Reservation or Book Table, user is send to booking page with sipmle navigation. 

  ![book table](/staticfiles/img/readme.MD%20images/book%20table.png)

  - Book tables with specific date and time

    User can book the tbale on the left side of the website in booking table tab there is form that user can pick the date up, fill time and number of guests. On the right is table availability pick the table witch is highlited green color. the tbales with red color mean they are allready booked or there is not enough room for your guests. 

    ![user input](/staticfiles/img/readme.MD%20images/booking%20info.png)

  - View and manage bookings

    User can view detalis of his reservation they are information like when is next booking and for how many people, what time and day. Booking could be cancel or change if the user needs to change anythng. They are to action buttons on left hand site for cancelation reservation and for modify. 

    ![booking manager](/staticfiles/img/readme.MD%20images/booking%20manager.png)

  - Real-time table availability check

    Evry account holder can chcek booking real live table availability if the user would like to change somethink like the diffrent date or nummber of the guests. User can manage his reservation anytime.

    ![table availability](/staticfiles/img/readme.MD%20images/table%20availability.png)

    - If user will click on the modify reservation, the websita redirect it user to form for change the reservation detali. 

    ![modify reservation](/staticfiles/img/readme.MD%20images/modify%20reservation.png)

  - Modify or cancel reservations

    - If user wanted to cancel reservation he need to clik on highlited red Cancel Resrevation button above Modyfi Reservation. Then the information showin up about reservation info and if user is sure to cancel reservation. 
    Click Yes, Canlel Reseration for delate reservation or No, Keep the reservation.

    ![cancel reservation](/staticfiles/img/readme.MD%20images/cancel%20reservation.png)

- **Menu**
  Any person who visite page can chack our menu, simply go to menu on top rigt corner of the web clik it, and you can see whtas on the menu.

  - View menu items by category
    They are four categories you can to navigate to, starters, main course, desserts and sides. 
    additionaly you cold navigate by meal type just above menu.

    

  - Filter by meal type (Breakfast, Lunch, Dinner)
    Switch in between the time of the day, mornig afternoon or evening. 

    

  - Detailed item descriptions and prices
    All menu iteam have secription and price 




- **Contact**
  - Contact form for inquiries
  - Automated email responses

### Admin Features
- **Reservation Management**
  - View all reservations
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
- **Database**: PostgresSQL
- **Additional Packages**:
  - django-crispy-forms
  - django-widget-tweaks
  - django-environ

## Tests 
