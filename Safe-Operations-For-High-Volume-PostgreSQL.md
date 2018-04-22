### The good

**Here\'s what we can safely do in a migration without downtime:**

| Can do this |
| ----------- |
| Add a new column |
| Drop a column |
| Add an index concurrently |
| Drop a constraint (for example, non-nullable) |
| Add a default value to an existing column |

---
---

### The bad

**Here's the stuff we cannot do, and our current workarounds:**

| Cannot do this on big tables          |  Our workaround |
| ------------------------------------- | :-------------: |
| Add an index                          |  Add the index using the CONCURRENTLY keyword |
| Change the type of a column           |  Add a new column, change the code to write to both columns, and backfill the new column |
| Add a column with a default           |  Add column, add default as a separate command, and backfill the column with the default value |
| Add a column that is non-nullable     |  Create a new table with the addition of the non-nullable column, write to both tables, backfill, and then switch to the new table [1 ] |
| Add a column with a unique constraint |  Add column, add unique index concurrently, and then add the constraint onto the table [2] |
| VACUUM FULL[3]                        |  We use pg̲repack instead |

