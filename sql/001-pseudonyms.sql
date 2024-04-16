create table public.pseudonyms
(
    id         varchar(36) not null primary key,
    hashed_bsn varchar(64) not null,
    provider   varchar(36) not null,
    pseudonym  varchar(36) not null
);

create index ix_pseudonyms_hashed_bsn
    on public.pseudonyms (hashed_bsn);

