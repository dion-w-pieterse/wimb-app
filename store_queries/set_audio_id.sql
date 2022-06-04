-- :name set_audio_id :affected
update book
set audio_id = :audio_id
where book_id = :book_id
