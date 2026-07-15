# Standards

This layer is where the platform's shared vocabulary is defined and
explained for humans, independent of any one schema's exact field list. It
answers "what is this concept and why does it exist" (`concepts/`) and
"what does each field mean, and what are its constraints" (`data_dictionary/`).

## Structure

- `concepts/*.yaml` — one file per core domain concept (`identity`,
  `entity`, `relationship`, `evidence`, `source`, `finding`, `investigation`,
  `case`, `report`, `workflow`, `event`). Each file states the concept's
  description, purpose, concrete examples, related concepts, and — critically
  — `forbidden_confusions`: concepts it is commonly mistaken for, and why
  they are distinct. This is the layer new contributors (human or agent)
  should read before touching a schema or domain module.
- `data_dictionary/*.md` — one file per object with a full field table
  (type, required, unique, mutable, description, example), always pointing
  back to the canonical schema in `contracts/` and the canonical
  implementation in `domain/` as the source of truth for exact shape.

## Why both exist

`concepts/` and `data_dictionary/` intentionally overlap in subject but not
in content: concepts explain *meaning and boundaries*, the data dictionary
explains *exact shape and constraints*. When the two appear to disagree, the
schema in `contracts/` is authoritative for shape and `domain/` is
authoritative for behavior; `standards/` should be corrected to match, never
the reverse.
