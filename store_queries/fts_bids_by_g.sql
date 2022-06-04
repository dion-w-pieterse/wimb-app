-- :name fts_bids_by_g :many
select book_id
from book
where genre_id in :genre_ids
