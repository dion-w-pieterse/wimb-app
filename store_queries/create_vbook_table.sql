-- :name create_vbook_table :affected
create virtual table vbook
using fts5(book_id, title, author, publisher, publish_date, description, isbn, genre_id, genre_desc, price, language, book_status_id, status_desc, path)

