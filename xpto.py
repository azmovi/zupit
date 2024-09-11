origin = '13560-049'
middle = '01313-020'
destination = '11040-050'

# CREATE FUNCTION valid_travel(
#     p_user_id INTEGER,
#     p_departure TIMESTAMP,
#     p_dureation INTEGER,
# ) RETURNS BOOLEAN
# LANGUAGE plpgsql
# AS $$
# DECLARE
#     is_valid BOOLEAN := TRUE;
# BEGIN
#     IF EXISTS (
#         SELECT 1
#         FROM travels
#         WHERE user_id = p_user_id AND status = TRUE
#         AND (
#             (p_arrival > departure AND p_arrival < arrival)
#             OR (p_departure < arrival and p_departure > departure)
#         )
#     ) THEN
#         is_valid := FALSE;
#     END IF;
#
#     RETURN is_valid;
# END;
# $$;
