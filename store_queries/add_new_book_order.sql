-- :name add_new_book_order :insert
insert into book_order (first_name, last_name, email, phone, addr, city, state, country, zip, cc_type, cc_num, sec_num, order_status)
values (:first_name, :last_name, :email, :phone, :addr, :city, :state, :country, :zip, :cc_type, :cc_num, :sec_num, :order_status)
