# Fourier

Fourier is a non-relational, NoSQL and adaptive database

## How it works

Fourier uses JSON-like documents in order to increase flexibility and ease of use. At the top level we have a **database**. A database is composed of multiple **collections**. A collection is composed of multiple **documents** which are JSON-like structures. Each document has a unqiue `_id` field. An example document would look like this:

```json
{
    "_id": 1234567890,
    "foo": "bar",
    "xyz": "amazing"
    "this": [
        "is",
        "an",
        "array"
    ],
    "bar": null
}
```

## Non-relational

From those of you coming from databases such as MySQL and PostgreSQL, we provide this table:

| Relational | Non-relational |
|------------|----------------|
| Database   | Database       |
| Table      | Collection     |
| Row        | Document       |