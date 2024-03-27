# Trackedly

Trackedly is an application to track time you worked or studied. The goal is to keep things simple and to focus on individual, rather than on teams. The app allows to organize your customers, projects and time entries in an easy and straightforward manner.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Bulma](https://img.shields.io/badge/bulma-00D0B1?style=for-the-badge&logo=bulma&logoColor=white)

## Installation

The application can be deployed on your cloud server/PaaS or run locally on localhost. This is Django application, so usual installation instructions apply.

System requirements:

- Python 3.11 +
- Poetry 1.8 +
- PostgreSQL

## Usage

The application has 3 core domains: time entries, projects and customers. Each time entry has start/finish date/time and can be assigned to a project. Each customer can have multiple associated projects. Projects can be set up as billable. By clicking on the project name it is possible to show only time entries that belong to the particular project.

## Roadmap

The Trackedly application was written for internal usage (to keep track of my working/study time). Although, there is always a room for improvement. In particular, following features are planned to be implemented:

- Export data to files (~~CSV~~, Excel)
- Add a frontend timer like in Timecamp to track time
- ~~Add weekly goals to projects~~ [Done]
- Add rates to projects and generate invoices
- Add project detail view with breakdown
- Add customer detail view with breakdown
- Add dashboard
- Add more flexible sorting and filtering in list views

## Authors

(c) 2024 [Iurii Mednikov](https://github.com/mdnkv)

## License

The project is released under terms of the MIT license. Please see the ```LICENSE.txt``` file for more information.