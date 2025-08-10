WITH telefonos AS(
    SELECT
        id_cliente,
        telefono,
        'archivos' AS Fuente
    FROM slv_tel_cliente_archivos
    UNION ALL
    SELECT
        id_cliente,
        telefono,
        'bd' AS Fuente
    FROM slv_tel_cliente_bd
    UNION ALL
    SELECT
        id_cliente,
        telefono,
        'externos' AS Fuente
    FROM slv_tel_cliente_ext
)