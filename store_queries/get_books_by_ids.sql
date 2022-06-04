-- :name get_books_by_ids :many
select * 
from book
inner join image_uploads
on book.image_id = image_uploads.id
where book_id 
in :book_ids
