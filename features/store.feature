Feature: Create a Store
  I want to create a store for interacting with representatiopn of a given resource.
  I want to power the store with a selection of drivers.


    Scenario Outline: A metadata record can be accessed
        Given I'm using a store of type <Store Type>
        And I get a metadata record identified by "11111"
        Then there are "1" records with fields that match
            | key               | value                       |
            | date_created      | 01/19/2022, 12:56:25        |
            | last_modified     | 01/19/2022, 12:56:25        |
            | graph_identifier  | graph-identifier-for-11111  |
        
        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: A metadata record can be updated
        Given I'm using a store of type <Store Type>
        And I update a metadata record identified by "11111" with
            | key             | value                   |
            | last_modified   | 01/19/2022, 14:00:200   |
        And I get a metadata record identified by "11111"
        Then there are "1" records with fields that match
            | key          | value                      |
            | last_modified   | 01/19/2022, 14:00:200   |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: A metadata record for a new graph resource can be created
        Given I'm using a store of type <Store Type>
        And I create a new resource for the graph identifier "my-new-magic-graph-url"
        Then there are "1" records with fields that match
            | key                 | value                      |
            | graph_identifier    | my-new-magic-graph-url     |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: An additional metadata record for an existing graph resource can be created
        Given I'm using a store of type <Store Type>
        And I create a new resource for the graph identifier "some-pre-existing-graph-identifier"
        Then there are "2" records with fields that match
            | key                 | value                                  |
            | graph_identifier    | some-pre-existing-graph-identifier     |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: Select latest where more than one metadata record for a graph resource exists
        Given I'm using a store of type <Store Type>
        And I create a new resource for the graph identifier "graph-id-that-has-three-fixtures"
        Then there are "2" records with fields that match
            | key                 | value                                  |
            | graph_identifier    | some-pre-existing-graph-identifier     |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |
