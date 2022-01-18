Feature: Create a Store
  I want to create a store for interacting with representatiopn of a given resource.
  I want to power the store with a selection of drivers.


    Scenario Outline: A metadata record can be accessed
        Given I'm using a store of type <Store Type>
        And I get metadata for a resource identified by "11111"
        Then "3" fields are returned
        And there are "1" records with fields that match
            | key          | value                   |
            | csv_url      | default-csv-url-1.csv   |
        
        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: A metadata record can be updated
        Given I'm using a store of type <Store Type>
        And I update a resource identified by "11111" with
            | key           | value                     |
            | csv_url       | some-updated-csv-url.csv  |
        And I get metadata for a resource identified by "11111"
        Then "3" fields are returned
        And there are "1" records with fields that match
            | key          | value                      |
            | csv_url      | some-updated-csv-url.csv   |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: A metadata record for a new graph resource can be created
        Given I'm using a store of type <Store Type>
        And I create a new resource for the graph identifier "my-new-magic-graph-url"
        Then "2" fields are returned
        And there are "1" records with fields that match
            | key                 | value                      |
            | graph_identifier    | my-new-magic-graph-url     |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |

    Scenario Outline: An additional metadata record for an existing graph resource can be created
        Given I'm using a store of type <Store Type>
        And I create a new resource for the graph identifier "some-pre-existing-graph-identifier"
        Then "2" fields are returned
        And there are "2" records with fields that match
            | key                 | value                                  |
            | graph_identifier    | some-pre-existing-graph-identifier     |

        Examples: Implemented Stores
            | Store Type           |
            | "StubStore"          |
