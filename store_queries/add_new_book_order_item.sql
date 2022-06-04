-- :name add_new_book_order_item :insert
insert into book_order_item (qty, order_id, book_id)
values (:qty, :order_id, :book_id)
