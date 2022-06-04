-- :name get_all_books_w_images_by_genre :many
select * 
from book
inner join image_uploads
on book.image_id = image_uploads.id
where book.genre_id 
in (select genre_id
    from genre
    where genre_desc = :genre)
