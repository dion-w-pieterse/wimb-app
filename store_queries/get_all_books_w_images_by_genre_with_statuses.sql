-- :name get_all_books_w_images_by_genre_with_statuses :many
select * 
from book
inner join image_uploads
on book.image_id = image_uploads.id
inner join book_status
on book.book_status_id = book_status.book_status_id
where book.genre_id 
in (select genre_id
    from genre
    where genre_desc = :genre)
