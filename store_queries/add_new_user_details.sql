-- :name add_new_user_details :affected
insert into user_details(first_name, last_name, email, phone, addr, city, state, country, zip, cc_type, cc_num, sec_num, user_id)
values (:first_name, :last_name, :email, :phone, :addr, :city, :state, :country, :zip, :cc_type, :cc_num, :sec_num, :user_id)
