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
