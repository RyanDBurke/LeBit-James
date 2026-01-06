from dependency_injector import containers, providers

from Modules.Fetch.Fetch import Fetch
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.User.UserFactory.UserFactory import UserFactory


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    # region Gateways
    fetch = providers.Singleton(
        Fetch,
        version=config.version.version
    )
    sleeper_api = providers.Singleton(
        SleeperApi,
        api=fetch,
        base_url=config.sleeper.base_url
    )
    # endregion

    # region Services / Factories
    user_factory = providers.Factory(
        UserFactory,
        api=sleeper_api
    )
    # endregion
