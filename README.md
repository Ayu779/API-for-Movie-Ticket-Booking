# API-for-Movie-Ticket-Booking
ZOMENTUM HIRING ASSIGNMENT
BACK-END STREAM
# Problem Statement :
1. You have to design a REST interface for a movie theatre ticket booking system. It should support the following business cases:
2. An endpoint to book a ticket using a user’s name, phone number, and timings.
3. An endpoint to update a ticket timing.
4. An endpoint to view all the tickets for a particular time.
5. An endpoint to delete a particular ticket.
6. An endpoint to view the user’s details based on the ticket id.
7. Mark a ticket as expired if there is a diff of 8 hours between the ticket timing and current time.
8.  Note: For a particular timing, a maximum of 20 tickets can be booked.
9.  You should follow the REST paradigm while building your application.
10.  You can use any database you like.
11.  Create a proper readme for your project.
12.  Plus point if you could delete all the tickets which are expired automatically.
13.  Plus point if you could write the tests for all the endpoints.
14.  Please attach a screenshot of your postman while testing your application.
15.  Please avoid plagiarism. 

# Getting Started:
    Install Python 3.x
    Get pip
    Download Postman for testing.
    Install flask and pymongo.
    After setting up, download the zip file or get it cloned. We are good to go.
    Open cmd and run the command: python root.py

# Routes of the API:'
    http://127.0.0.1:5000/
    Method: GET
    Input: No input
    Output: List of all the time slots available

    http://127.0.0.1:5000/booktickets
    Method: POST
    Input: {‘name’ : *username*,
          ‘phone’ : *phoneno*
          ‘timing’ : *timing slots in format HH:MM* }
    Output: Booked ticket and Updated Databases.
    
    http://127.0.0.1:5000/update
    Method: POST
    Input: {‘ticket_id’ : *Ticket ID*,
          ‘phone’ : *phoneno*
          ‘timing_alter’ : *timing slots in format HH:MM* }
    Output: Updated time in database.
    
    http://127.0.0.1:5000/delete
    Method : POST
    Input: {‘ticket_id’ : *Ticket ID*,
          ‘phone’ : *Phone number associated with the ticket*}
    Output: Deleted from Database
   
    http://127.0.0.1/viewontime
    Method : POST
    Input: {‘timing’ : *TIME*}
    Output: All the tickets on the given time.

    http://127.0.0.1/viewuser
    Method: POST
    Input: {“ticket_id” : *Ticket ID*}
    Output: User's Detail
  
# Other Specifications:
    Missing Input Error Handling
    Invalid Input Error Handling
    Deletion of the Ticket after 8 Hrs Using TTL
    
 # Please See the Screenshots.
