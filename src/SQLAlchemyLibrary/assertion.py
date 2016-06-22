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
            raise AssertionError("Expected to have have at least one row from '{0}' "
                                 "but got 0 rows.".format(selectStatement))

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
            raise AssertionError("Expected to have have no rows from '{0}' "
                                 "but got some rows : {1}.".format(selectStatement, queryResults))

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
            raise AssertionError("Expected zero rows to be returned from '{0}' "
                                 "but got rows back. Number of rows returned was {1}".format(selectStatement, num_rows))

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
            raise AssertionError("Expected same number of rows to be returned from '{0}' "
                                 "than the returned rows of {1}".format(selectStatement, num_rows))

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
            raise AssertionError("Expected more rows to be returned from '{0}' "
                                 "than the returned rows of {1}".format(selectStatement, num_rows))

    def row_count_is_less_than_x(self,selectStatement,numRows):
        """Check if the number of rows returned from `selectStatement` is less
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
            raise AssertionError("Expected less rows to be returned from '{0}' "
                                 "than the returned rows of {1}".format(selectStatement, num_rows))

    def table_must_exist(self, table_name, schema_name=None):
        """*DEPRECATED* Use keyword `Table Should Exist` instead."""
        self.table_should_exist(table_name, schema_name)

    def table_should_exist(self, table_name, schema_name=None, message=None):
        """Check if the table given exists in the database.

        For example, given we have a table `person` in a database

        When you do the following:
        | Table Should Exist | person |

        Then you will get the following:
        | Table Should Exist | person | # PASS |
        | Table Should Exist | first_name | # FAIL |
        """
        md = sqlalchemy.schema.MetaData(bind=self._engine)
        table = sqlalchemy.schema.Table(table_name, md, schema=schema_name)
        if not table.exists():
            if schema_name is not None:
                table_name = "{0}.{1}".format(table_name, schema_name)
            if message:
                message = ": {0}".format(message)
            else:
                message = ""
            raise AssertionError("Table '{0}' should exist but does not {1}".format(table_name, message))

    def query_for_single_column(self, selectStatement, *expected_values, **params):
        """
        Execute the given query (which should return one column, but could be multiple rows).

        The first argument is the SQL Query to run.

        If more than one argument is provided, assert that the result-set contains each of the non-first arguments and nothing else.

        Examples:

        Suppose we have a "stuff" table with these columns and values:

        | A | B | C |
        | 1 | 2 | 3 |
        | 4 | 5 | 6 |
        | 7 | 8 | 9 |

        ---

        | ${values}= | Query for Single Column | select A from stuff |
        Result: A list containing [1, 4, 7]. \ No "Should" assertions happen.

        ---

        | ${values}= | Query for Single Column | select A from stuff | 1 | 4 | 7 |

        Result: PASS. \ Also, A list containing [1, 4, 7].

        ---

        | ${values}= | Query for Single Column | select A from stuff | 12345 |

        Result: FAIL because 12345 is not in [1, 4, 7].

        ---

        | ${values}= | Query for Single Column | select A from stuff | 1 | 4 |

        Result: FAIL because we got [1, 4, 7] but were only expecting [1, 4].

        """
        raw_rows = self.query(selectStatement, **named_args)
        rows = [row[0] for row in raw_rows]
        if len(expected_values) > 0:
            builtin = BuiltIn()
            for expected_value in expected_values:
                builtin.should_contain(rows, expected_value)
            builtin.log_many("Expecting values:", *expected_values)
            builtin.length_should_be(rows, len(expected_values),
                    "There are more or fewer rows than expected!")
        return rows



    def query_for_single_value(self, selectStatement, expected_value=None, message=None, **named_args):
        """Return the result of this query IF it returns only 1 row with 1 column.

        Fails via `Length Should Be` if the query returns
        multiple rows or multiple columns.

        Optionally check the resulting value with `Should Be Equal`.

        NOTE: Keyword-argument Bind-parameters are supported,
        but the arguments `expected_value` and `message` are reserved
        for optionally passing to `Should Be Equal`
        if `expected_value` is not None.

        This keyword will NOT try to check if your single value is null.

        Example:
        | ${count}= | Query for Single Value | select count(*) from my_table; |

        Examples with assertions:
        | ${count}= | Query for Single Value | select count(*) from my_table; | ${5} |
        | ${count}= | Query for Single Value | select count(*) from my_table; | ${5} | Should have 5 rows in my_table |

        Use a seperate assertaion if you want to ensure a null value:
        | ${value}= | Query for Single Value | select foo from my_table where id=:id; | id=5 |
        | Should Be Equal | ${value} | ${None} | Should be null! |

        """
        values = self.query(selectStatement, **named_args)
        BuiltIn().length_should_be(values, 1,
                "There should be exactly one row returned by the query {0}".format(selectStatement))
        row = values[0]
        BuiltIn().length_should_be(row, 1,
                "There should be exactly one column in the results of {0}".format(selectStatement))
        answer = row[0]
        if expected_value is not None:
            BuiltIn().should_be_equal(answer, expected_value, message)
        return answer

    def query_for_single_number(self, selectStatement, expected_value=None, message=None, **named_args):
        answer = self.query_for_single_value(selectStatement, **named_args)
        if expected_value is not None:
            BuiltIn().should_be_equal_as_numbers(answer, expected_value, message)

    def query_for_count(self, selectStatement, expected_value=None, message=None, **named_args):
        """Alias for `Query for Single Number`."""
        return self.query_for_single_number(selectStatement, expected_value=expected_value, message=message, **named_args)
