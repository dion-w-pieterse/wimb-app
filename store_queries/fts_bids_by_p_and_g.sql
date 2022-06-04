-- :name fts_bids_by_p_and_g :many
select book_id
from book
where price >= :minBound and price <= :maxBound and genre_id in :genre_ids
