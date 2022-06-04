-- :name get_book_reviews :many
select * 
from reviews 
inner join user
on reviews.user_id = user.id
where book_id = :book_id
order by review_id desc
limit 25
