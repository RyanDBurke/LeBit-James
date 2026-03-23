from dependency_injector.wiring import Provide, inject

from Infrastructure.Configuration.Container import Container
from Modules.User.UserFactory.UserFactory import UserFactory
from UI.App import App


# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


@inject
def run(username: str, user_factory: UserFactory = Provide[Container.user_factory]):
    user = user_factory.get_user(username)
    return user


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    # run UI, passing username callback
    App().start(on_username=lambda username: run(username))

