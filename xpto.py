origin = '13560-049'
middle = '01313-020'
destination = '11040-050'

# (p_arrival > departure AND p_arrival < arrival)
# OR (p_departure < arrival and p_departure > departure)

# CREATE FUNCTION get_travel(
#     p_id INTEGER
# ) RETURNS TABLE (
#     travel_id INTEGER,
#     status BOOLEAN,
#     user_id INTEGER,
#     renavam VARCHAR,
#     departure TIMESTAMP WITH TIME ZONE,
#     origin_space INTEGER,
#     origin_cep VARCHAR,
#     origin_street VARCHAR,
#     origin_city VARCHAR,
#     origin_state VARCHAR,
#     origin_district VARCHAR,
#     origin_house_number VARCHAR,
#     middle_space INTEGER,
#     middle_duration INTEGER,
#     middle_distance VARCHAR,
#     middle_price FLOAT,
#     middle_cep VARCHAR,
#     middle_street VARCHAR,
#     middle_city VARCHAR,
#     middle_state VARCHAR,
#     middle_district VARCHAR,
#     middle_house_number VARCHAR,
#     destination_duration INTEGER,
#     destination_distance VARCHAR,
#     destination_price FLOAT,
#     destination_cep VARCHAR,
#     destination_street VARCHAR,
#     destination_city VARCHAR,
#     destination_state VARCHAR,
#     destination_district VARCHAR,
#     destination_house_number VARCHAR,
#     arrival TIMESTAMP WITH TIME ZONE,
#     involved INTEGER[]
# )
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     RETURN QUERY
#     SELECT
#         t.id,
#         t.status,
#         t.user_id,
#         t.renavam,
#         t.departure,
#         o.space,
#         ao.cep,
#         ao.street,
#         ao.city,
#         ao.state,
#         ao.district,
#         ao.house_number,
#         am.cep,
#         am.street,
#         am.city,
#         am.state,
#         am.district,
#         am.house_number,
#         m.space,
#         m.duration,
#         m.distance,
#         m.price,
#         ad.cep,
#         ad.street,
#         ad.city,
#         ad.state,
#         ad.district,
#         ad.house_number,
#         d.duration,
#         d.distance,
#         d.price,
#         t.arrival,
#         t.involved
#     FROM travels t
#     LEFT JOIN origins o ON t.origin_id = o.id
#     LEFT JOIN address ao ON o.address_id = ao.id
#     LEFT JOIN middles m ON t.middle_id = m.id
#     LEFT JOIN address am ON m.address_id = am.id
#     LEFT JOIN destinations d ON t.destination_id = d.id
#     LEFT JOIN address ad ON d.address_id = ad.id;
# END;
# $$;
