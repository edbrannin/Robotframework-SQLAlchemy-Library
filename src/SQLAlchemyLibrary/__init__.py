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

import os

from SQLAlchemyLibrary.connection_manager import ConnectionManager
from SQLAlchemyLibrary.query import Query
from SQLAlchemyLibrary.assertion import Assertion

__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()

class SQLAlchemyLibrary(ConnectionManager, Query, Assertion):
    """
    SQLAlchemy Library allows you to interact with your database in Robot Framework tests.

    This can allow you to query your database after an action has been made to verify the results.

    This can use any database supported by SQLAlchemy, including Oracle, MySQL, Postgres, SQLite.
    (Not yet tested on Oracle).

    This should be a drop-in replacement for DatabaseLibrary in most situations.

    Advantages over DatabaseLibrary

    - Ability to provide named-parameter BIND values

    == References: ==

     - SQLAlchemy documentation - http://docs.sqlalchemy.org/en/latest/index.html
     - List of SQLAlchemy Dialects -  http://docs.sqlalchemy.org/en/latest/dialects/
     - Python Database Programming - http://wiki.python.org/moin/DatabaseProgramming/

    == Notes: ==



    === Example Usage: ===

    | # Setup |
    | Connect to Database |
    | # Guard assertion (verify that test started in expected state). |
    | Check if not exists in database | select id from person where first_name = :first_name and last_name = :last_name | firat_name=Franz Allan | last_name=See |
    | # Drive UI to do some action |
    | Go To | http://localhost/person/form.html | | # From selenium library |
    | Input Text |  name=first_name | Franz Allan | # From selenium library |
    | Input Text |  name=last_name | See | # From selenium library |
    | Click Button | Save | | # From selenium library |
    | # Log results |
    | @{queryResults} | Query | select * from person |
    | Log Many | @{queryResults} |
    | # Verify if persisted in the database |
    | Check if exists in database | select id from person where first_name = 'Franz Allan' and last_name = 'See' |
    | # Teardown |
    | Disconnect from Database |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
