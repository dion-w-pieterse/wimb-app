-- :name populate_vbook_table :affected
insert into vbook
select book_id, title, author, publisher, publish_date, description, isbn, book.genre_id, genre_desc, price, language, book.book_status_id, status_desc, path 
from book
inner join genre
on book.genre_id = genre.genre_id
inner join book_status
on book.book_status_id = book_status.book_status_id
inner join image_uploads
on book.image_id = image_uploads.id
