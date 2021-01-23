# Understinding Proxy Models by Example

- It's a normal issue to want to create an app with differnt types of users.
- This repo shows an example where I create a spy, and driver user
- the examples/models.py file is carefully laced with comments to guide you through recreating this work by yourself.


##### How to use:
        
        - create virtual environment:
            virtualenv venv

        - activate virtual env(windows)
            .\venv\scripts\activate

        - activate virtualenv (linux)
            source venv/bin/activate

        - cd into project root folder

        - install requirements
            pip install -r requirements.txt
        
        -Create a super user
            python manage.py creaatesuperuser
        
        - run server:
            python manage.py runserver #python3 might be what works for you instead of python
        
        - you can log into the admin console and play around with the project!

Reference: [link](https://www.youtube.com/watch?v=f0hdXr2MOEA&list=PL_qGav8csvacp5ylXC3xrREd4stG90qNK)