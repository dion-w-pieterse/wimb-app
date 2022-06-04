-- :name get_user_details :one
select * 
from user_details
where user_id = :user_id
