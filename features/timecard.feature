Feature: Timecard Interactions

Scenario: Create a timecard event
    Create a timecard event and verify it looks good
    Given I start with an empty database
    When I post a timecard entry
    Then I can get all data back

Scenario: I try my current month
    Create a timecard event and verify it looks good
    Given I start with an empty database
    When I post June timecard entries
    Then I can get June charge code data

