-- :name get_audio_sample :one
select * 
from audio_samples
where id = :audio_id
