# coding: utf-8
from __future__ import unicode_literals

from fabric.api import local, task, quiet


def change_version(change):
    version_row = local("grep 'VERSION = ' setup.py", capture=True)
    version = version_row.split(' = ')[1].strip()
    version = map(int, version[1:-1].split('.'))
    new_version = '.'.join(map(str, change(*version)))
    local("sed -i -e 's/VERSION =.*/VERSION = \"{}\"/g' setup.py".format(new_version))
    return new_version


def release(new_version):
    with quiet():
        local('find . -name "*.pyc" -exec rm -f {} \;')
        local('rm -r dist')
        local('rm -r build')
        local('git commit -am "new version {}"'.format(new_version))
        local('git tag -a v{0} -m \'new version {0}\''.format(new_version))
        local('git push origin master --tags')
    local("python setup.py bdist_wheel")
    local("twine upload dist/*")


@task
def major():
    release(change_version(lambda x, y, z: [x + 1, 0, 0]))


@task
def minor():
    release(change_version(lambda x, y, z: [x, y + 1, 0]))


@task
def patch():
    release(change_version(lambda x, y, z: [x, y, z + 1]))
