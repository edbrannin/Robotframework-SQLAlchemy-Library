import os

from invoke import task

@task
def docs(ctx, version=None):
    targets = ["latest"]
    if version:
        targets.append(version)
    for target in targets:
        try:
            os.makedirs("docs/{}".format(target))
        except:
            pass
        ctx.run("python -m robot.libdoc -f html src/SQLAlchemyLibrary docs/{}/SQLAlchemyLibrary.html".format(target))

@task
def dist(ctx):
    ctx.run("python setup.py sdist bdist_wheel")


@task
def publish(ctx):
    ctx.run("python setup.py sdist bdist_wheel upload")


@task
def clean(ctx):
    ctx.run("rm -rf build dist")


