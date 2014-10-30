Oxidizr
=======

Take the hassle out of online communications; build better audience, engage, and grow your brand.


What is this trying to achieve
-----------------------------

- Kewyord tracking across different Social Media (SM) channels
- Content tracking across websites, blogs, feeds
- Conversation tracking across SM, Yahoo/Google/other groups / forums, public mailing lists


Why Open Source
---------------

- I am building this from suggestions from friends who work on online marketing
- I want others to contribute and grow this software
- I want a community built solutions to many well-know issues in this domain


Who can benefit from this
-------------------------
- If you are an online marketer, or just want to track the above mentioned points
- If you are a marketing agency
- If you want to get leads from online channels


Setup Guide (Ubuntu 14.04 LTS)
-----------
* Install Virtualenv for Python
```
$ sudo apt-get install libpq-dev python-dev
$ sudo pip install virtualenv
```

* Setup workspace
```
$ mkdir -p ~/workspace
$ cd ~/workspace
$ virtualenv oxidizrenv
$ cd oxidizrenv
$ source bin/activate
```

* Install project based requirements
```
$ git clone https://github.com/pixlie/oxidizr.git
$ pip install -r oxidizr/requirements.txt
```

Who is behind this
------------------
For now this is being developed by Sumit Datta ([brainless](https://github.com/brainless)). Feel free to contribute. This project is in very early stages and I have not had to time to write a guide to easily setup an environment. So if you are familiar with Python, then you can easily go ahead. If not, kindly search for `virtualenv`, `pip`, `django`. You will easily find instructions to setup projects. I will write a guide soon. You are welcome to follow (Watch/Star) the project. Thanks.
