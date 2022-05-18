# Software Engineering Challenge

Challenge for selecting Software engineers.

To complete this challenge you will need to:

- Fork this repository.
- Create a Django application.
- Implement CI pipeline Django.

## API development

### Description

They have been always here, but we have never seen them. This API will be used by the Human Air Forces to defend the world against the alian invasion.

The API needs to have three entities:

- Mothership {ship capacity: 9}
- Ship {crew member capacity: 5}
- CrewMember

Mothership has many ships.
Ships has Many CrewMembers.

### Requeriments

- Python ^3.9
- Poetry ^1.1.12
- Django ^3.2.12

### Acceptance criteria

- Given that the officer wants to add a mothership, when he adds a mothership, then the mothership will be created with three ships
- Given that the mothership was created, when the ship is created, then ship will create three crew members
- Given that the officer wants to add a ship to a mothership, when he sends which mother ship and how much ships he wants to add, then ships will be created with three crew members each one if the mothership contains less than 9 ships
- Given that the officer wants to remove a ship, when he tries he send which ship he wants to remove, then the ship will be removed along with all its crew members
- Given that the officer wants to add a crew member, when he sends the name of the member and the ship he wants to add, then the crew member is added if the ship contains less than 5 crew members
- When the officer tries to add more ships or crew members over the capacities, then an error is raised pointing out what is wrong
- Given that the officer wants to switch a crew member between the ships, when he sends the from_ship and the to_ship and the name of the crew member, then the action will be allowed only if the to_ship will not exceed the capacity

### Definition of Done

Complete the following checklist

1. Use the [Django Styleguide](https://github.com/HackSoftware/Django-Styleguide) as reference
2. Remove duplicated or unnecessary code
3. Avoid hardcoded values
4. No unnecessary comments
5. Unit test implemented checking custom behaviors and business rules
6. API Documentation
   1. Action | route
   2. Description
   3. URL Parameters
   4. Request Params
   5. Request body
   6. Response body
   7. Status code

### Api Docs

1. localhost:8000/docs/
2. localhost:8000/schema/ #downloadable yaml version

#### First Time Server Run

1. chmod a+rwx scripts/local/run_server.sh
2. ./scripts/local/run_server.sh

#### Consecutive Server Run

1. ./scripts/local/run_server.sh

#### First Time Test Run

1. chmod a+rwx scripts/local/run_server_test.sh
2. ./scripts/local/run_server_test.sh

#### Consecutive Test Run

1. ./scripts/local/run_server_test.sh
