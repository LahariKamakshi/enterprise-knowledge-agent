project_orion_data = """

PROJECT: ORION DATABASE MIGRATION

Project Overview:
Project Orion is an internal enterprise application used by the company's
finance and operations teams. The project is managed by Sarah Chen.
The engineering team decided to migrate the application's database from
an on-premises Microsoft SQL Server to Azure SQL Database.

TEAM:
Sarah Chen - Project Manager
David Miller - Senior Database Engineer
Priya Rao - Cloud Engineer
Michael Smith - Application Developer
Lisa Johnson - QA Lead

--------------------------------------------------

MEETING 1 - INITIAL MIGRATION DISCUSSION
Date: June 10, 2026

The Orion team discussed migrating the production database from the
on-premises SQL Server environment to Azure SQL Database.

David Miller raised concerns about possible production downtime during
the migration. He recommended performing a test migration before making
any production changes.

Priya Rao explained that Azure SQL Database would reduce infrastructure
maintenance and provide better scalability.

Decision:
The team agreed to perform a test migration before proceeding with the
production migration.

Sarah Chen asked David Miller and Priya Rao to prepare the migration
plan and test environment.

--------------------------------------------------

MEETING 2 - TEST MIGRATION
Date: June 17, 2026

The team completed the first test migration of the Orion database.

The test migration was successful.

The migration caused 18 minutes of application downtime.

David Miller confirmed that the database data was transferred correctly.

Lisa Johnson reported that the QA team found no critical application
issues after the test migration.

Sarah Chen approved moving forward with the production migration,
provided that the final migration plan included a rollback procedure.

Decision:
The team approved the production migration with a rollback plan.

--------------------------------------------------

MEETING 3 - PRODUCTION MIGRATION
Date: June 24, 2026

The Orion production database was migrated from the on-premises
SQL Server environment to Azure SQL Database.

The production migration was completed successfully.

The application experienced 12 minutes of downtime, which was lower
than the 18 minutes recorded during the test migration.

Lisa Johnson confirmed that the application passed the post-migration
QA checks.

Priya Rao verified that the Azure SQL Database environment was
operating normally.

Sarah Chen announced that the production migration was officially
completed.

Decision:
Project Orion officially moved to Azure SQL Database.

--------------------------------------------------

POST-MIGRATION ISSUE
Date: June 27, 2026

The application team reported that a small number of database queries
were slower than expected after the production migration.

Michael Smith investigated the issue and identified several queries
that required optimization.

David Miller reviewed the database indexes and recommended changes
to improve query performance.

--------------------------------------------------

ISSUE RESOLUTION
Date: June 29, 2026

Michael Smith deployed the optimized queries.

David Miller confirmed that the database indexes were updated.

Lisa Johnson performed regression testing and confirmed that the
application performance returned to the expected level.

The performance issue was considered resolved.

--------------------------------------------------

FINAL PROJECT STATUS
Date: July 1, 2026

Project Orion's database migration was successfully completed.

The production database is now hosted on Azure SQL Database.

The final production downtime was 12 minutes.

The post-migration performance issue was resolved through query
optimization and database index updates.

Sarah Chen marked the database migration project as completed.

The team documented the migration process and lessons learned for
future database migration projects.

--------------------------------------------------

IMPORTANT RELATIONSHIPS:

Sarah Chen manages Project Orion.

David Miller is responsible for database migration activities.

Priya Rao is responsible for the Azure SQL environment.

Michael Smith is responsible for application development and query
optimization.

Lisa Johnson is responsible for QA and post-migration testing.

David Miller raised the original downtime concern.

The team performed a test migration before the production migration.

The test migration caused 18 minutes of downtime.

The production migration caused 12 minutes of downtime.

Sarah Chen approved the production migration after the successful
test migration.

Project Orion's production database now runs on Azure SQL Database.

The post-migration performance issue was resolved through query
optimization and index updates.

"""