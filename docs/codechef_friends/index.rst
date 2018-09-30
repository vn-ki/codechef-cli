Codechef Friends
================

Because, it’s always better with friends :)

**NOTE**: All endpoints can be tested using the nice interface provided
by DRF. Just open them in your browser.

OAuth2
------

Root endpoint: ``/oauth``

- ``GET /redirect`` : redirect to codechef
- ``GET /callback`` : handle response

API
---

Root endpoint: ``/api``

-  ``GET /users/?q=<query>`` : Search/List users registered on
   “Codechef_friends”
-  ``GET /users/<username>`` : fetch user info from codechef
-  ``GET /friends``\ \* : returns user’s list of friends
-  ``PUT /friends``\ \* : add friend, requires:

   -  Friends’ codechef id

-  ``DELETE /friends/<username>``\ \* : remove friend, requires:

   -  Friends’ codechef id

``*`` needs authentication header

Development
-----------

-  Rename ``.env.sample`` to ``.env`` and enter your own creds.

------
Server
------
     - ``pipenv install``
     - ``./manage.py runserver <port>`` to start server

--------
Frontend
--------

     - ``cd frontend && yarn && yarn serve`` to start frontend
-  Open ``/oauth/redirect`` to start flow, and recieve tokens
-  For production server, use the provided nginx config.

Demo
----

-  A demo version is hosted at `aliyun.mrigankkrishan.tk`_

.. _aliyun.mrigankkrishan.tk: https://aliyun.mrigankkrishan.tk
