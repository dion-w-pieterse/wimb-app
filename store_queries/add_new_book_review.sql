-- :name add_new_book_review :insert
insert into reviews (review_desc, user_id, book_id)
values (:review, :user_id, :book_id)
