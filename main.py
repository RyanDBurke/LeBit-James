# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dependency_injector.wiring import Provide, inject

from Infrastructure.Container import Container
from Modules.User.UserFactory.UserFactory import UserFactory

@inject
def main(username: str, user_factory: UserFactory = Provide[Container.user_factory]) -> None:
    user = user_factory.get_user(username)

if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    # run UI

    # get username from input or from last session
    main("ConsolationWnrAgain")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
