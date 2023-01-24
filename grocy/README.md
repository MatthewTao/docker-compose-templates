# Grocy

Grocy is a simple ERP system.

## Usage

1. Make a copy of the env example `cp env.example .env`
2. Modify the newly created `.env` file so that it contains the settings desired.
3. Ensure that the target directory for the volume does exist.
4. Run `docker-compose up -d`
5. The service should now be available on `localhost:9283`

The default username for the admin account is `admin`
The default password for the admin account is `admin`

After logging in, the password for the admin account can be changed, and new accounts can be made.
