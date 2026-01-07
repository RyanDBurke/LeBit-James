import os

from dependency_injector.wiring import Provide, inject

from Infrastructure.Configuration.Container import Container
from Modules.User.UserFactory.UserFactory import UserFactory


# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


@inject
def run(username: str, user_factory: UserFactory = Provide[Container.user_factory]) -> None:
    user = user_factory.get_user(username)


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    # run UI

    # get username from input or from the last session
    test_username = os.getenv('TEST_USERNAME')
    run(test_username)
