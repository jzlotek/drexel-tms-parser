from db import database
from db.schema.class_section import Section

print(dir(Section))
exit(0)

print(database.db)
print(dir(database.db))
print(database.create_table("test2"))
print(database.get_table("test"))
