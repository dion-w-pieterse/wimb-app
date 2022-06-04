-- :name fts5_search :many
select * 
from vbook
where vbook 
match :query_string
