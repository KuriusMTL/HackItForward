# Contributing

You **always** want to look at this file *before* contributing. In here you should find
steps that you need to take to set up your development environment as well as instructions
for coding standards and contributing guidelines.


## Set up instructions

You're going to have to do those things to contribute to this project.

1. Fork the repo
2. Clone your fork
3. Create upstream by running `git remote add upstream https://github.com/KuriusMTL/HackItForward.git`. You will then be able to run `git pull upstream master`to pull any changes from the the original repository since you last forked it).
4. Create a branch by running `git checkout -b <branch-name>`
5. Run these commands
```
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tags
python manage.py loaddata social_links
python manage.py loaddata challenges
python manage.py loaddata projects
```
6. To start the Django server, run `python manage.py runserver`
7. Contribute!
8. If you get things working, add your changed files with `git add .` and run `git commit -m "insert message here"` to commit your messages
9. Push your changes to your fork with `git push origin <branch-name>`
10. Create a pull request
11. Iterate on the solution
12. Get merged! 🎉 🎊
