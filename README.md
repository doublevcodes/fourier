# Fourier

Fourier is a non-relational, NoSQL and adaptive database

## How it works

Fourier uses JSON-like documents in order to increase flexibility and ease of use. At the top level we have a **database**. A database is composed of multiple **collections**. A collection is composed of multiple **documents** which are JSON-like structures. Each document has a unique `_id` field. An example document would look like this:

```json
{
    "_id": 1234567890,
    "foo": "bar",
    "xyz": "amazing",
    "this": [
        "is",
        "an",
        "array"
    ],
    "bar": null
}
```

## Non-relational

For those of you coming from databases such as MySQL and PostgreSQL, we provide this table:

| Relational | Non-relational |
|------------|----------------|
| Database   | Database       |
| Table      | Collection     |
| Row        | Document       |
| Column     | Key of document|

This, of course, does not demonstrate the flexibility of non-relational DBs and should only be used in order to understand the concept, not from an implementation viewpoint.

## Quick start

1. First you must clone the GitHub repository:

```bash
$ git clone https://github.com/doublevcodes/fourier/ && cd fourier
```

2. Install all the dependencies for Fourier

```bash
$ python3 -m pip install click fastapi uvicorn
```

3. You can now run Fourier

```bash
$ python3 -m fourierdb run --port 8000
```
