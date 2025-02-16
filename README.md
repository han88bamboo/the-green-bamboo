# BA Wizards

<a>
    <img src="Images/Logo/88 Bamboo.png" title="The Green Bamboo" alt="The Green Bamboo" style="height: 150px">
</a>

## Team

| Member | Picture | Email
| :---:  | :----: | :---: |
| Carissa Chia Shenru |  | carissachia.2022@scis.smu.edu.sg |
| Chin Hui Juan Dycia |  | dycia.chin.2022@scis.smu.edu.sg |
| Liew Wai Horng |  |  whliew.2022@scis.smu.edu.sg |
| Kenneth Lim Hu Gui |  | kenneth.lim.2021@scis.smu.edu.sg |
| Khoo Teck Xuan |  | txkhoo.2022@scis.smu.edu.sg |
| Lee Pei Wen Jovinne |  | jovinne.lee.2022@scis.smu.edu.sg |
| Kai Lin Choo | <img src="Images/Team Pictures/Kai Lin.jpeg" width="100" height="100"> | Product Owner | kailin@88bamboo.co |
| Wesley Chia | <img src="Images/Team Pictures/Wesley.jpeg" width="100" height="100"> | Product Owner | wesley@88bamboo.co |

## Project Background

88 Bamboo is an online store focused on educating consumers about different types of spirits and beverages through a drinks-focused editorial that currently caters to over 70,000 readers every month. They aspire to connect and empower drink lovers across Asia and their mission is to make spirits appreciation fun and accessible for their users, with a focus on their target audience of Gen Zs and millennials in Asia. Some of their current initiatives include having an editorial that provides no-jargon, approachable content to promote spirits and drinks and a marketplace to connect users to 88 Bamboo’s vendors, allowing them to purchase and discover new drinks. 

## Project Goals

The business objectives of this project are to enhance user engagement and retention on 88 Bamboo's DrinkX app by implementing two advanced features: personalised recommendation logic and a reverse image search tool. To achieve these goals, we will develop a recommendation engine using collaborative and content-based filtering to suggest bottle listings tailored to individual user preferences, and a reverse image search feature leveraging Convolutional Neural Networks (CNNs) for image-based identification and similarity matching. Expected outcomes are increased user interaction on the explore page, and a higher conversion rate from casual browsing to purchases. 

## Key Features

<!-- TODO: to be filled -->
- Onboarding
- Recommender System
- Reverse Image Search

## Getting Started

### Clone

- Clone our github repository to your local machine using `https://github.com/CarissaChia/the-green-bamboo/tree/Group-3`

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
