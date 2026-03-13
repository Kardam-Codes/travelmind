# Travel Catalog Dataset

## Purpose

The system must use **verified catalog data** for recommendations.

This dataset will contain travel-related entities.

---

## Tables

### Places

| Field | Description |
|------|-------------|
id | unique id |
name | place name |
location | city/location |
category | type |
rating | rating |

---

### Hotels

| Field | Description |
|------|-------------|
id | unique id |
name | hotel name |
location | city |
price | price range |
rating | rating |

---

### Activities

| Field | Description |
|------|-------------|
id | unique id |
name | activity |
location | place |
category | adventure/culture |
price | cost |

---

## Data Sources

Possible sources:

- Kaggle tourism datasets
- Open travel APIs
- curated datasets