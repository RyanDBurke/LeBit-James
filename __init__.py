from dependency_injector.wiring import Provide, inject

from Infrastructure.Configuration.Container import Container
from Modules.User.UserFactory.UserFactory import UserFactory
from UI.App import App

@inject
def run(username: str, user_factory: UserFactory = Provide[Container.user_factory]):
    return user_factory.get_user(username)


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, 'Infrastructure.UserCache', 'UI.Pages.Login'])

    # run UI, passing username callback
    App().start(on_username=lambda username: run(username))

