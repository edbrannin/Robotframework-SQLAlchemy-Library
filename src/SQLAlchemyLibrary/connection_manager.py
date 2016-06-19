#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

try:
    import ConfigParser
except:
    import configparser as ConfigParser

from robot.api import logger
import sqlalchemy


class ConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._engine = None
        self._dbconnection = None

    def connect_to_database(self, url, echo=False, **kwargs):
        """
        Connect to the given database URL with SQLAlchemy.

        See also:

        - http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
        - http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine

        Example usage:
        | # Connect to an in-memory SQLite database |
        | Create Engine | sqlite:///:memory: |

        """
        self._engine = sqlalchemy.create_engine(url, echo=echo, **kwargs)
        self._dbconnection = self._engine.connect()

    @property
    def db_api_module_name(self):
        try:
            return self._engine.driver
        except:
            return None

    def disconnect_from_database(self):
        """
        Disconnects from the database.

        For example:
        | Disconnect From Database | # disconnects from current connection to the database |
        """
        self._dbconnection.close()
