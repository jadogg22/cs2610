#**What command do I use to install poetry?**

welp I tried running the curl command but it kept breaking, so I instaled pipx and installed it that way from the documentation

#**How do I initialize poetry in an existing project?**

'''poetry init'''

#***What is a lock file and should it be committed to my git repository?Why or why not?**

absolutly its how we know what packages are used

#**What are dev dependencies? The docs don't explicitly say this but do a quick google search and you will find a good answer :)**

claude spit this out for me.

Dev dependencies (or development dependencies) are package dependencies that are only required during development or testing of a project, but not at runtime in production environments.

Some examples of common dev dependencies:

Testing frameworks like pytest, nose, unittest
Code linters like pylint, flake8
Documentation generators like Sphinx
Build tools like setuptools, wheel
Code formatters like black, yapf
Version control systems like Git