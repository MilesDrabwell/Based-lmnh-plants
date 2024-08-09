
# Welcome to the LMNH Plants Data Pipeline!




### Folders Overview


`archive` -> Archive folder containing unused scripts that may be useful at a later time.

`dashboard` -> Dashboard folder containing a dockerfile and terraform file for the dashboard created in this project. It also contains the script used to run the StreamLit dashboard where the visualisation is hosted. 

`images` -> Images Folder containing images used in README.md

`long_term_storage` -> Long_term_storage folder containing a dockerfile and terraform file for an AWS lambda script that reads data from an AWS RDS, deletes data older than 24 hours and uploads it to an AWS S3 bucket as a parquet file. 

`pipeline` -> Pipeline folder containing a dockerfile and terraform file for the ETL pipeline that reads from an API instance and uploads it to an AWS RDS.

## Architecture Diagram

The Architect Diagram represents the AWS cloud Infrastructure used in the project.

![Architect_diagram](images/Architect_diagram.png)

## ERD Diagram

The schema diagram showing the entity relationships between the tables in the database is shown below where the data retrieved from the plants API is normalised using 3NF.

![ERD_DIAGRAM](images/ERD_diagram.png)



## Contributors 

This project was developed by the following contributors:

[Anna Camplani](https://github.com/annac02)

[Miles Drabwell](https://github.com/MilesDrabwell)

[Linfan Siddiqi](https://github.com/LinfanS)

[Jonathan Spence](https://github.com/HighestAuto)

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
