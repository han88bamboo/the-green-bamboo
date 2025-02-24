# The Green Bamboo
# “Happy Hour!” UGC Product Review Application

<a>
    <img src="Images/Logo/88 Bamboo.png" title="The Green Bamboo" alt="The Green Bamboo" style="height: 150px">
</a>

## Team

| Member | Picture | Email
| :---:  | :----: | :---: |
| Leong Jun Wei | <img src="Images/Team Pictures/Jun Wei.png" width="100" height="100"> | jwleong.2020@scis.smu.edu.sg |
| Shannie Kwok | <img src="Images/Team Pictures/Shannie.png" width="100" height="100"> | shanniekwok.2021@scis.smu.edu.sg |
| Poh Li Ying | <img src="Images/Team Pictures/Li Ying.png" width="100" height="100"> |  liying.poh.2021@scis.smu.edu.sg |
| Matthew Foo | <img src="Images/Team Pictures/Matthew.png" width="100" height="100"> | matthew.foo.2021@scis.smu.edu.sg |
| Kai Lin Choo | <img src="Images/Team Pictures/Kai Lin.jpeg" width="100" height="100"> | Product Owner | kailin@88bamboo.co |
| Wesley Chia | <img src="Images/Team Pictures/Wesley.jpeg" width="100" height="100"> | Product Owner | wesley@88bamboo.co |

## Project Background

88 Bamboo is an online store focused on educating consumers about different types of spirits and beverages through a drinks-focused editorial that currently caters to over 70,000 readers every month. They aspire to connect and empower drink lovers across Asia and their mission is to make spirits appreciation fun and accessible for their users, with a focus on their target audience of Gen Zs and millennials in Asia. Some of their current initiatives include having an editorial that provides no-jargon, approachable content to promote spirits and drinks and a marketplace to connect users to 88 Bamboo’s vendors, allowing them to purchase and discover new drinks. 

## Project Goals

The goal of the project is to build out a program that allows users to search, bookmark, rate and review different bottle expressions, as well as to engage with other reviewers through upvotes/downvotes and comment replies. These features will be integrated within the broader 88Bamboo.co site, where the same user account can be used to access the already existing editorial and marketplace features on the site. The purpose of this feature would be to help deepen user engagement and retention, and make the process of drinks discovery more fun and interactive!

## Key Features

<!-- TODO: to be filled -->
- Browse drinks catalogue (listings table in database)
- Search, sort and filter drinks listing
- Find out where to try (venues like bars etc., based on proximity if location enabled) and where to buy (producers like distilleries) listings/drinks
- Profile dashboards (Users, Venues, Producers)
- Venue Menu
- Profile Q & A and updates (Venues, Producers)
- Administrator controls

## Getting Started

### Clone

- Clone our github repository to your local machine using `https://github.com/shanniekwok/the-green-bamboo`

### Setup

- Install WAMP/MAMP from \
**For Windows**: `http://www.wamp.org` \
**For Macbook**: `https://www.mamp.info/en/downloads/`

- Move cloned repository into \
**For Windows**: `c:\wamp\www` \
**For Macbook**: `Applications/MAMP/htdocs`

- Switch on WAMP/MAMP

- Navigate to `http://localhost/phpMyAdmin` and import the database from \
**For Windows**: `c:\wamp\www\the-green-bamboo\Dataset\` <!-- TODO: to be changed --> \
**For Macbook**: `Applications/MAMP/htdocs/the-green-bamboo/Dataset/` <!-- TODO: to be changed -->
- Open your browser and navigate to `http://localhost/the-green-bamboo/` <!-- TODO: to be filled -->

### Logging In

Navigate to `http://localhost:8080/Login` 

These are the login credentials for test accounts:

| Account Type | Username | Password |
| :---:  | :----: | :---: |
| User (admin) | `111hotpot` | `westlife123` |
| User (non-admin) | `charsiucharlie` | `westlife123` |
| Producer | `ardbegdistillery` | `ardbegdistillery123` |
| Venue | `orhgaotaproom` | `orhgaotaproom123` |

### Installation

> For `Jest` unit test cases
````
npm install
````
> For `PHPUnit` and  `SQLite3` test cases

1. Download [Composer](https://getcomposer.org/doc/00-intro.md#:~:text=Before%20using%20Composer%2C%20ensure%20that,on%20Windows%2C%20Linux%20and%20macOS)
2.	During installation when prompted for install mode, click **install for me only** and do not click developer mode
3. In VS code, open a new terminal and copy this code in to download `PHPUnit`
````
composer require phpunit/phpunit --dev
````
4. To get path to access ini file under **Loaded Configuration File**, enter in terminal
```
php -ini
```
5. Hover over the path and click open file in editor to access the ini file
6. Once in the ini file, enter this extension code
```
extension=sqlite3
```
7. Restart your server once you have done so

### Testing
> For `Jest` unit test cases

Open new terminal and executed the following code
````
npm test
````
> For `PHPUnit` and  `SQLite3` test cases

Open new terminal and executed the following code
```
./vendor/bin/phpunit ./unit_testing/DatabaseTest.php
