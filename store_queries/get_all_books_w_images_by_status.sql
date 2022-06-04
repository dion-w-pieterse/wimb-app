-- :name get_all_books_w_images_by_status :many
select * from book
inner join image_uploads
on book.image_id = image_uploads.id
where book.book_status_id
in (select book_status_id
    from book_status
    where status_desc = :status)
