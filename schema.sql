create table if not exists species
(
    id         integer primary key,
    name       text not null unique,
    latin_name text not null unique
);

create table if not exists watercourse
(
    id   integer primary key,
    name text not null unique
);

create table if not exists site
(
    id             integer primary key,
    name           text    not null,
    latitude       real    not null check (latitude between -90 and 90),
    longitude      real    not null check (longitude between -180 and 180),
    watercourse_id integer not null references watercourse (id)
);

create table if not exists survey
(
    id             integer primary key,
    site_id        integer not null references site (id),
    event_date     text    not null,
    method         text,
    strategy       text,
    number_of_runs integer,
    zero_catch     integer not null default 0 check (zero_catch in (0, 1))
);

create table if not exists survey_species
(
    id                 integer primary key,
    survey_id          integer not null references survey (id),
    species_id         integer not null references species (id),
    all_runs           integer,
    observed_abundance text,
    unique (survey_id, species_id)
);

create table if not exists individual_fish_length
(
    id                integer primary key,
    survey_species_id integer not null references survey_species (id),
    length_mm         integer not null check (length_mm > 0)
);
