-- :name get_all_books_w_images :many
select * 
from book
inner join image_uploads
on book.image_id = image_uploads.id 
