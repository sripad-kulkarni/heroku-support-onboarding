# An app for Onboarding Heroku Support Engineers - `heroku-support-onboarding`

URL: https://heroku-support-onboarding.herokuapp.com/

The app is designed to make the onboarding process easier allowing new hires, onboarding buddies and managers/leads to follow and track the progress at one stop bringing all of them together. This eliminates the tedious effort of creating and managing various documents that in longer term can be a real pain to deal with.

Drilling down to the functionalities of the app, we have three different roles for login at the moment, the **'Manager/Lead', 'Onboarding Buddy/Trail Guide' and the 'New Hire'** themselves.

**Managers/Leads** hold the highest level of access where they can register users, create and modify the onboarding plan, add and remove the access requests, assign trail guides, onboarding buddies and onboarding managers to the new hires along with the plan, and have a audit trail logs to track down the activity inside the app. They enjoy with a dashboard which makes their job super easy to track progress with just one click after their login. We'll read through these features in more detail later. 

**Trail Guides**, after being assigned to their respective new hires, would also get a similar dashboard as of the managers/leads but as fine graining access is relevant, the app allows them to see the new hires only assigned to them. This would allow them to track the progress and keep in sync with the new hires.

The most important and the center of the app are our **New Hires** for whom the app is mainly designed. New Hires get an onboarding plan assigned to them, this would allow them to have a weekly list of tasks they would need to complete. They also get a necessary access requests list where that they can follow to start requesting accesses and update the status for visibility of their respective trail guides, onboarding buddies, and managers/leads.

## Role Based Available Functionailties:

### Managers/Leads:

1. Login
2. NH Cards
    1. View Details
    2. Basic Details
    3. Overall Weeks Progress
    4. Week-wise progress
    5. Access Requests
    6. Resources

**The Navigation Bar:**

3. Home
4. Access Request page
    1. Access Request tab
    2. The **`+`** option
        1. Add Access Request Section
        2. Remove Access Request Section
        3. Add Access Request Item
        4. Remove Access Request Item
5. Weekly Plan
    1 Week-wise content
6. Users
    1. Register New Users
    2. Manage Existing Users
7. Audit Log
8. My Profile
9. Logout
 
### Trail Guides/Onboarding Buddies:

1. Login
2. NH Cards
    1. View Details
    2. Basic Details
    3. Overall Weeks Progress
    4. Week-wise progress
    2.5. Access Requests
    2.6. Resources

**The Navigation Bar:**

3. Home
4. My Profile
5. Logout

### New Hires:

1. Login
2. NH Cards
    1. View Details
    2. Basic Details
    3. Overall Weeks Progress
    4. Week-wise progress
    5. Access Requests
    6. Resources

**The Navigation Bar:**

3. Home
4. Access Request page
    1. Access Request tab
5. Weekly Plan
    1 Week-wise content
6. My Profile
7. Logout
 
## A Guide to all of the Functionalities

