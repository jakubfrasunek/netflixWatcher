# Netflix watcher

Update Netflix Household without interaction.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)

## Project Description

This is made for all the Netflix users that switches between TV's and have to update Netflix Household everytime they want to watch by confirming either via SMS or E-mail. This code checks for incoming e-mail from Netflix when you click on validate via e-mail on your TV, reads the mail, click the button, opens the page in Selenium, logs into your Netflix account and confirm your new TV. So everything you need to do is just click on check via e-mail on your TV and the rest is done here within seconds.

## Installation

1. Clone this repository: `git clone https://github.com/jakubfrasunek/netflixWatcher`
2. Navigate to the project directory: `cd netflixWatcher`.
3. Create your own `.env` file from `.example.env` file. `EMAIL_LOGIN` is the email that you have associated with Netflix account. `NETFLIX_EMAIL_SENDER` is the e-mail address that sends the confirmation button. Default is `info@account.netflix.com`, you may want to change it if you want to forward that e-mail from your Netflix associated e-mail address to another one.
4. Run the containers: `make up`.
5. Enjoy.