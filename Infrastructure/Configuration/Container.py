"""
Config mapping
Register database, services, and their dependencies
"""
import os

from dependency_injector import containers, providers
from dotenv import load_dotenv

from Infrastructure.Database.Database import Database
from Infrastructure.UserCache.UsernameCache import UsernameCache
from Modules.Fetch.Fetch import Fetch
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.League.LeagueService.LeagueService import LeagueService
from Modules.User.UserService.UserService import UserService


class Container(containers.DeclarativeContainer):
    load_dotenv()
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

    db = providers.Singleton(
        Database,
        db=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    # endregion

    # region Services / Factories
    username_cache = providers.Singleton(
        UsernameCache
    )

    user_service = providers.Factory(
        UserService,
        api=sleeper_api,
        db=db
    )

    league_service = providers.Factory(
        LeagueService,
        api=sleeper_api,
        db=db
    )
    # endregion
