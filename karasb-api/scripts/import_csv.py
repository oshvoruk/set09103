import sqlite3
from pathlib import Path

import pandas as pd
from pyproj import Transformer

from config import Config

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "csv"


sites = pd.read_csv(SOURCE_DIR / "FW_Fish_Sites_2026-09-20.csv")
counts = pd.read_csv(SOURCE_DIR / "FW_Fish_Counts_2026-09-20.csv")
lengths = pd.read_csv(SOURCE_DIR / "FW_Fish_Individual_Lengths_2026-09-20.csv")


transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

sites["longitude"], sites["latitude"] = transformer.transform(
    sites["SITE_RANKED_EASTING"],
    sites["SITE_RANKED_NORTHING"],
)


watercourses = sites[["SITE_PARENT_ID", "SITE_PARENT_NAME"]].drop_duplicates()
watercourses = watercourses.rename(
    columns={
        "SITE_PARENT_ID": "id",
        "SITE_PARENT_NAME": "name",
    }
)


site_data = sites[
    ["SITE_ID", "SITE_NAME", "latitude", "longitude", "SITE_PARENT_ID"]
].rename(
    columns={
        "SITE_ID": "id",
        "SITE_NAME": "name",
        "SITE_PARENT_ID": "watercourse_id",
    }
)


surveys = counts.drop_duplicates("SURVEY_ID")[
    [
        "SURVEY_ID",
        "SITE_ID",
        "EVENT_DATE",
        "SURVEY_METHOD",
        "SURVEY_STRATEGY",
        "NO_OF_RUNS",
        "ZERO_CATCH",
    ]
].copy()

surveys["ZERO_CATCH"] = surveys["ZERO_CATCH"].map({"Yes": 1, "No": 0})

surveys = surveys.rename(
    columns={
        "SURVEY_ID": "id",
        "SITE_ID": "site_id",
        "EVENT_DATE": "event_date",
        "SURVEY_METHOD": "method",
        "SURVEY_STRATEGY": "strategy",
        "NO_OF_RUNS": "number_of_runs",
        "ZERO_CATCH": "zero_catch",
    }
)


species = counts.dropna(subset=["SPECIES_ID"])[
    ["SPECIES_ID", "SPECIES_NAME", "LATIN_NAME"]
].drop_duplicates("SPECIES_ID")

species = species.rename(
    columns={
        "SPECIES_ID": "id",
        "SPECIES_NAME": "name",
        "LATIN_NAME": "latin_name",
    }
)

species["id"] = species["id"].astype(int)


survey_species = counts.dropna(subset=["SURVEY_SPECIES_ID"])[
    [
        "SURVEY_SPECIES_ID",
        "SURVEY_ID",
        "SPECIES_ID",
        "ALL_RUNS",
        "OBSERVED_ABUNDANCE",
    ]
].rename(
    columns={
        "SURVEY_SPECIES_ID": "id",
        "SURVEY_ID": "survey_id",
        "SPECIES_ID": "species_id",
        "ALL_RUNS": "all_runs",
        "OBSERVED_ABUNDANCE": "observed_abundance",
    }
)

survey_species[["id", "survey_id", "species_id"]] = survey_species[
    ["id", "survey_id", "species_id"]
].astype(int)


fish_lengths = lengths[["LW_MEASURED_ID", "SURVEY_SPECIES_ID", "FISH_LENGTH"]].rename(
    columns={
        "LW_MEASURED_ID": "id",
        "SURVEY_SPECIES_ID": "survey_species_id",
        "FISH_LENGTH": "length_mm",
    }
)


tables = {
    "watercourse": watercourses,
    "site": site_data,
    "species": species,
    "survey": surveys,
    "survey_species": survey_species,
    "individual_fish_length": fish_lengths,
}

with sqlite3.connect(Config.DATABASE) as db:
    db.execute("PRAGMA foreign_keys = ON")

    for table, data in tables.items():
        data.to_sql(table, db, if_exists="append", index=False)

print("successfully imported data")
