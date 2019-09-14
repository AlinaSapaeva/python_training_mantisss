# -*- coding: utf-8 -*-
from model.project import Project
import random
import string

def random_string(prefix , maxlen):
    simbols = string.ascii_letters + string.digits + " "*4 + string.digits
    return prefix + "".join([random.choice(simbols) for i in range(random.randrange(maxlen))])

def test_add_new_project(app, db):
    config = app.config['webadmin']
    app.session.login(config["username"], config['password'])
    assert app.soap.can_login(config["username"], config['password'])
    project = Project(name = random_string("name", 8), description=random_string("description", 10))
    old_projects =  db.get_project_list()
    app.project.add_new(project)
    # хеширование      == app.contact.count()
    old_projects.append(project)
 #   assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    soap_project_list = app.soap.get_project_list()
    old_projects = sorted(old_projects, key=Project.id_or_max)
    soap_project_list =  sorted(soap_project_list, key=Project.id_or_max)
    assert old_projects == soap_project_list




def clean(project):
    return Project(id=int(project.id), name=project.name.strip(), description=project.description.strip())



