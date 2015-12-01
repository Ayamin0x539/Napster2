# Napster2
Napster/iTunes/Bandcamp clone for CSE4701: Principles of Databases

# Installation instructions
This assumes Ubuntu 12.04 LTS or 14.04 LTS. Other platforms have not been
tested.

````
sudo apt-get install mysql
sudo apt-get install mysql-workbench
sudo apt-get install libmysqlclient-dev
````
Download the most recent version of mysqlclient from
https://pypi.python.org/pypi/mysqlclient

````
cd ~/Downloads
tar -xzvf mysqlclient-<version>.tar.gz
cd mysqlclient-<version>.tar.gz
python3 setup.py build
sudo python3 setup.py install
````

Delete any existing Chinook schemas in MySQL Workbench by right-clicking on the
schema and choosing

Click the cylinder with a + to create a new schema in the connected server.

Name the new schema "Chinook" and press Apply.

Click "Apply" and then "Close" in the prompt that appears.

Import our provided Chinook_startingstate.sql file my clicking the SQL logo with
a folder on it to Open a SQL script file in a new query tab. Run the query to 
fill the Chinook database with the relevant information.

Create the relevant django tables by executing the following:
````
python3 manage.py migrate
````

Create yourself a superuser account by executing the following:
````
python3 manage.py createsuperuser
````

Follow the prompts and create your new superuser.

Finally, run the server by executing the following:
````
python3 manage.py runserver <port>
````

If the port option is left out, it defaults to 8000.

# Requirements and TODO list

*High Level*
- Customer can register accounts
- Customer can manage their accounts
- Customer can set/manage payment types
- Customer can lookup by track name
- Customer can lookup by album name
- Customer can lookup by artist name
- Customer can lookup by composer name
- Customer can lookup by genre name
- Customer can lookup by media name
- Customer can create playlists (MyPlaylist, MyPlaylistTrack)
- Customer can review created playlists
- Customer can modify created playlists
- Customer can place order for one or more playlists or tracks
- Employee can enter new media (track name, album name, artist name, composer name, genre name,
millisecond, bytes, media-name)
- Employee can create new playlists
- Employee can modify existing playlists (Playlist, PlaylistTrack)
- Employee can review info on customers (demographics and playlists)
- Employee can approve client orders (generating invoice)
- Administrators can do all things Employees can do.
- Administrators can run reports on sales by month
- Administrators can run reports on sales by duration
- Administrators can run reports on sales by city/state/country
- Administrators can query employee productivity: number of customers per employee, sales per employee by month/duration period
- Administrators can run inventory reports by track name, album name, artist name composer name, genre name, media name

*Front End/Mock Ups*
- Registration Screen
- Login Screen
- "Edit your information" screen
- Customer dashboard
- Employee Dashboard
- (Customer) Set/edit payment types screen
- (Customer) Pending/completed orders screen
- (Customer) Create/manage myplaylists 
- (Customer) Order screen
- (Customer) Shopping cart screen
- (Employee) Active order screen
- (Employee) Enter/edit new media screen
- (Employee) Create/manage playlists screen
- (Employee) Review customer demographic screen
- (Administrator) Sales reporting screen
- (Administrator) Employee productivity reporting screen
- (Administrator) Inventory reporting screen
- (Administrator) Customer reporting screen

