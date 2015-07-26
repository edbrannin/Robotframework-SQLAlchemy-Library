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

from robot.libraries.BuiltIn import BuiltIn
import sqlalchemy

class Assertion(object):
    """
    Assertion handles all the assertions of Database Library.
    """

    def check_if_exists_in_database(self,selectStatement):
        """
        Check if any row would be returned by given the input
        `selectStatement`. If there are no results, then this will
        throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |

        When you have the following assertions in your robot
        | Check If Exists In Database | SELECT id FROM person WHERE first_name = 'Franz Allan' |
        | Check If Exists In Database | SELECT id FROM person WHERE first_name = 'John' |

        Then you will get the following:
        | Check If Exists In Database | SELECT id FROM person WHERE first_name = 'Franz Allan' | # PASS |
        | Check If Exists In Database | SELECT id FROM person WHERE first_name = 'John' | # FAIL |
        """
        if not self.query(selectStatement):
            raise AssertionError("Expected to have have at least one row from '%s' "
                                 "but got 0 rows." % selectStatement)

    def check_if_not_exists_in_database(self,selectStatement):
        """
        This is the negation of `check_if_exists_in_database`.

        Check if no rows would be returned by given the input
        `selectStatement`. If there are any results, then this will
        throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |

        When you have the following assertions in your robot
        | Check If Not Exists In Database | SELECT id FROM person WHERE first_name = 'John' |
        | Check If Not Exists In Database | SELECT id FROM person WHERE first_name = 'Franz Allan' |

        Then you will get the following:
        | Check If Not Exists In Database | SELECT id FROM person WHERE first_name = 'John' | # PASS |
        | Check If Not Exists In Database | SELECT id FROM person WHERE first_name = 'Franz Allan' | # FAIL |
        """
        queryResults = self.query(selectStatement)
        if queryResults:
            raise AssertionError("Expected to have have no rows from '%s' "
                                 "but got some rows : %s." % (selectStatement, queryResults))

    def row_count_is_0(self,selectStatement):
        """
        Check if any rows are returned from the submitted `selectStatement`.
        If there are, then this will throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |

        When you have the following assertions in your robot
        | Row Count is 0 | SELECT id FROM person WHERE first_name = 'Franz Allan' |
        | Row Count is 0 | SELECT id FROM person WHERE first_name = 'John' |

        Then you will get the following:
        | Row Count is 0 | SELECT id FROM person WHERE first_name = 'Franz Allan' | # FAIL |
        | Row Count is 0 | SELECT id FROM person WHERE first_name = 'John' | # PASS |
        """
        num_rows = self.row_count(selectStatement)
        if (num_rows > 0):
            raise AssertionError("Expected zero rows to be returned from '%s' "
                                 "but got rows back. Number of rows returned was %s" % (selectStatement, num_rows))

    def row_count_is_equal_to_x(self,selectStatement,numRows):
        """
        Check if the number of rows returned from `selectStatement` is equal to
        the value submitted. If not, then this will throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |
        |  2 | Jerry       | Schneider |

        When you have the following assertions in your robot
        | Row Count Is Equal To X | SELECT id FROM person | 1 |
        | Row Count Is Equal To X | SELECT id FROM person WHERE first_name = 'John' | 0 |

        Then you will get the following:
        | Row Count Is Equal To X | SELECT id FROM person | 1 | # FAIL |
        | Row Count Is Equal To X | SELECT id FROM person WHERE first_name = 'John' | 0 | # PASS |
        """
        num_rows = self.row_count(selectStatement)
        if (num_rows != int(numRows.encode('ascii'))):
            raise AssertionError("Expected same number of rows to be returned from '%s' "
                                 "than the returned rows of %s" % (selectStatement, num_rows))

    def row_count_is_greater_than_x(self,selectStatement,numRows):
        """
        Check if the number of rows returned from `selectStatement` is greater
        than the value submitted. If not, then this will throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |
        |  2 | Jerry       | Schneider |

        When you have the following assertions in your robot
        | Row Count Is Greater Than X | SELECT id FROM person | 1 |
        | Row Count Is Greater Than X | SELECT id FROM person WHERE first_name = 'John' | 0 |

        Then you will get the following:
        | Row Count Is Greater Than X | SELECT id FROM person | 1 | # PASS |
        | Row Count Is Greater Than X | SELECT id FROM person WHERE first_name = 'John' | 0 | # FAIL |
        """
        num_rows = self.row_count(selectStatement)
        if (num_rows <= int(numRows.encode('ascii'))):
            raise AssertionError("Expected more rows to be returned from '%s' "
                                 "than the returned rows of %s" % (selectStatement, num_rows))

    def row_count_is_less_than_x(self,selectStatement,numRows):
        """
        Check if the number of rows returned from `selectStatement` is less
        than the value submitted. If not, then this will throw an AssertionError.

        For example, given we have a table `person` with the following data:
        | id | first_name  | last_name |
        |  1 | Franz Allan | See       |
        |  2 | Jerry       | Schneider |

        When you have the following assertions in your robot
        | Row Count Is Less Than X | SELECT id FROM person | 3 |
        | Row Count Is Less Than X | SELECT id FROM person WHERE first_name = 'John' | 1 |

        Then you will get the following:
        | Row Count Is Less Than X | SELECT id FROM person | 3 | # PASS |
        | Row Count Is Less Than X | SELECT id FROM person WHERE first_name = 'John' | 1 | # FAIL |
        """
        num_rows = self.row_count(selectStatement)
        if (num_rows >= int(numRows.encode('ascii'))):
            raise AssertionError("Expected less rows to be returned from '%s' "
                                 "than the returned rows of %s" % (selectStatement, num_rows))

    def table_must_exist(self,tableName):
        """
        Check if the table given exists in the database.

        For example, given we have a table `person` in a database

        When you do the following:
        | Table Must Exist | person |

        Then you will get the following:
        | Table Must Exist | person | # PASS |
        | Table Must Exist | first_name | # FAIL |
        """
        md = sqlalchemy.schema.MetaData(bind=self._engine)
        table = sqlalchemy.schema.Table(table_name, md, schema=schema_name)
        if not table.exists():
            if schema_name is not None:
                table_name = "%s.%s" % (table_name, schema_name)
            raise AssertionError("Table '%s' does not exist in the db" % table_name)

    def query_for_single_value(self, selectStatement, expected_value=None, message=None, **named_args):
        """Return the result of this query IF it returns only 1 row with 1 column.

        Fails via `Length Should Be` if the query returns
        multiple rows or multiple columns.

        Optionally check the resulting value with `Should Be Equal`.

        NOTE: Keyword-argument Bind-parameters are supported,
        but the arguments `expected_value` and `message` are reserved
        for optionally passing to `Should Be Equal`
        if `expected_value` is not None.

        This keyword will not try to check if your single value is null.

        Example:
