-- :name fts_bids_by_p :many
select book_id
from book
where price >= :minBound and price <= :maxBound
