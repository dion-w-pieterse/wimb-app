-- :name get_all_books_and_statuses_and_genres :many
select * 
from book
inner join genre
on genre.genre_id = book.genre_id
inner join book_status
on book.book_status_id = book_status.book_status_id
inner join image_uploads
on book.image_id = image_uploads.id
