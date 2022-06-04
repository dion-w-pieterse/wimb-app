-- :name get_book_by_id :one
select * 
from book 
inner join image_uploads
on book.image_id = image_uploads.id
where book_id = :book_id
