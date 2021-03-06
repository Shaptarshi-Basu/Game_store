**Generic requirements**

**Valid CSS and HTML**
How does your code reflect this aspect? How did you validate?

The HTML and CSS used are valid and have been tested extensively.Thus they are for surely properly valid.

**The service should work on modern browsers**
It is, manually tested.Tested on Chrome, mozilla and safari.

**Code should be commented well**
Comment have been added as and when required.The names of the functions , variables and modules have been named appropriately for better understanding.

**Write your own code**

The codes can be checked from the following locations
Play2win/{models.py,views.py,forms.py}, Play2win/templates etc


**Signs of quality**

**Reusability**
There is very loose coupling in the modules.The normal MTV structure has been adhered to. This will allow the same structure to be used for different web applications.

**Modularity**
The application modules performing adequately and independently. Modules and their subcomponents represent more real world objects.Files **smaller and easier** to navigate

**Versatile use of Django&#39;s features**
For login I used Django&#39;s implementation.Check settings.py and the login files in Template for more details.

**Sensible URL scheme**
The wsd2018project/urls.py is indicative of this criterion

**Security**
Use of CSRF middleware token have been done which demonstrates this quality.

**Crash &amp; idiot proof**
Proper error handling has been done to ensure that

**Testing your game store**
Tested and review submitted.


Mandatory requirements
Minimum functional requirements (mandatory)

**Register as a player and developer**
Try it over the heroku deployment or look at Play2Win/views.py - class UserFormView.


**Authentication (mandatory, 100-200 points)**

I should get 200 points for this part. Play2Win/views.py, wsd2018project/settings.py
Login, logout and register, both as player or developer
Play2Win/views.py, wsd2018project/settings.py

**Email validation (max. +100 points)**

I should get 70 points.
AUTH\_PASSWORD\_VALIDATORS in wsd2018project/settings.py,etc. The email can be authenticated if you try to register.


**Basic player functionalities (mandatory, 100-300 points)**

I should get 250

There are games listed on the dashboard page
The game models is defined in models.py.

**As a player: buy games (communication with Simple Payments, payment process verification)**

The payment Simple Payments is used. Once add game is clicked in dashboard. If player is authenticated and score object for the particular game and the particular user is there then redirected to /payment\_successful.

**As a player: play games**
The code is done in views.py

As a player: see game high scores and record their score
Game should have submit score. The entire game is added in iframe through game.html.

Also get high score button fetches all the high score for the game and the code is added in views.py /highscores



**As a player: Security restrictions, e.g. player is only allowed to play the games they&#39;ve purchased**

Implemented. Check to see is score object for the game and the user exists. Score object created when game is paid for.The code is added in views.py

**Basic developer functionalities (mandatory 100-200 points)**

I should get 100
As a developer: Add a game (URL) and set price for that game and manage that game (remove, modify)
The views.py is where the code has been added.the method add\_game will add the game.It will

Check if user is authenticated and the user is a developer before letting the user to add.The user fills three fields. Game name , url and price.

As a developer: Basic game inventory and sales statistics (how many of the developers&#39; games have been bought and when)
This has not been implemented.

As a developer: Security restrictions, e.g. developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory, etc.There is check placed in add\_game in views.py which enures this criterion.
This is done and in views.py.add:game

**Game/service interaction (mandatory 100-200 points)**

Should get 150 points, 50 less as the highscores are not automatically added.

Submitting high score from the game using PostMessage
This works if game has a submit score button. The score can be view also from het highscores button in game page.

The code is there in views.py in method save, load and highscores.Also to catch these

Jquery code has been added in game.html


**Quality of Work (mandatory 100-200 points**

I should get 150
The code is modular , reusable and simple to understand and properly follows Django MTV and has proper comments.there has been purposeful use of framework





**User experience (styling, interaction)**

The styles used are simple and not distracting. Also the website is responsive

**Meaningful testing**
Tests for two games were done using the gamstore.And extensive testing of the game store has been done by both the members.

**Non-functional requirements (mandatory 100-200 points)**

150 points should be given.The project plan is precise and neat. The code contains meaningful comments. Also one thing can be added is the project development was mostly done by a single member which an added constraint which was overcome during the project.


Own JavaScript game(s) (mandatory 100-300  points)

Worth 200 points
Two appropriate games were added. The games were quite nice and exciting fighter plane game and the evergreen 2048 game also they were interactive to some extent.

**Technical quality of the game (code, comments, communication with the game store)**
Game is simple and properly commented. Submit score is added to the game.Game is pretty interesting also.



**Functionality that earns your group extra points:** None

**Save/load and resolution feature (0-100 points)**

I should get 100.

Jquery code added to game.html to catch the save and load features.Also the method for save and load were added in views.py to handle the game score and state and add them to the models.

**3rd party login (0-100 points)**

Should get 20 points.Added with google, but some bug remains which I can&#39;t figure out. All details added in settings.py and code changes also added in base.html.

**RESTful API (0-100 points)**
I should get 100 points

Can get highscores.  Method GET highscores added in views.py  100 points

**Mobile Friendly (0-50 points)**
I should get 50 points

Bootstrap and similar responsive styles used. Check the templates.

**Social media sharing (0-50 points)**

I should get 30 points
Facebook sharing added in game.html but not much fancy sharing.

**Some extra special feature your group has implemented (200 points max.)**
None.