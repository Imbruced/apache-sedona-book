{% macro test_within_boundary(model, column_name, boundary) %}
SELECT *
FROM {{ model }}
WHERE NOT ST_Intersects({{ column_name }}, ST_GeomFromText('{{ boundary }}'))
{% endmacro %}

{% macro test_is_point(model, column_name) %}
SELECT *
FROM {{ model }}
WHERE NOT ST_GeometryType({{ column_name }}) = 'ST_Point'
{% endmacro %}