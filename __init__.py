from dependency_injector.wiring import Provide, inject

from Infrastructure.Configuration.Container import Container
from Modules.League.LeagueService.LeagueService import LeagueService
from Modules.User.UserService.UserService import UserService
from UI.App import App

@inject
def run(username: str, user_service: UserService = Provide[Container.user_service]):
    return user_service.get_user(username)


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, 'Infrastructure.UserCache', 'UI.Pages.Login'])

    league_service: LeagueService = container.league_service()

    # run UI, passing username callback
    App().start(on_username=lambda username: run(username), league_service=league_service)

