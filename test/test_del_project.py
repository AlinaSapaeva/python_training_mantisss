import random
import string

from model.project import Project


def random_string(prefix , maxlen):
    simbols = string.ascii_letters + string.digits + " "*4 + string.digits
    return prefix + "".join([random.choice(simbols) for i in range(random.randrange(maxlen))])

def test_delete_project(app, db):
    config = app.config['webadmin']
    app.session.login(config["username"], config['password'])
    assert app.soap.can_login(config["username"], config['password'])
    if len(db.get_project_list())== 0:
        app.project.add_new(Project(name = random_string("name", 8), description=random_string("description", 10)))
    old_project= db.get_project_list()
    project = random.choice(old_project)
    app.project.delete_project_by_name(project.name)
    soap_project_list = app.soap.get_project_list()
    old_project.remove(project)
    assert sorted(soap_project_list, key=Project.id_or_max) == sorted(old_project, key=Project.id_or_max)

def clean(project):
    return Project(id=project.id, name=project.name.strip(), description=project.description.strip())
