-- :name create_audio_entry :insert
insert into audio_samples(name, path)
values (:name, :path)
