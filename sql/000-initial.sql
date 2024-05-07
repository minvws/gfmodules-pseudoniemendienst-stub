--- Create web user pseudonym
CREATE ROLE pseudonym;
ALTER ROLE pseudonym WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

--- Create DBA role
CREATE ROLE pseudonym_dba;
ALTER ROLE pseudonym_dba WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

CREATE TABLE deploy_releases
(
        version varchar(255),
        deployed_at timestamp default now()
);

ALTER TABLE deploy_releases OWNER TO pseudonym_dba;

GRANT SELECT ON deploy_releases TO pseudonym;

