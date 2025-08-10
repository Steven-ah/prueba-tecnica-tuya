CREATE VIEW rch.rachas_cliente AS
WITH fechas_corte AS(
-- Inicialmente tomar las fechas de inicio y fin en que el cliente estuvo
	SELECT 
		identificacion, 
		MIN(corte_mes) AS min_corte_mes, 
		MAX(corte_mes) AS max_corte_mes
	FROM rch.historia
	GROUP BY identificacion
), intervalo_fechas AS(
	--Posteriormente generar el total de fechas de ese intervalo
	SELECT
		*
	FROM fechas_corte AS p
	LEFT JOIN rch.fechas AS m ON m.fecha BETWEEN min_corte_mes AND max_corte_mes
), clasificacion AS(
	-- Agregar ahora los datos completos, y clasificar los niveles
	SELECT
		p.identificacion,
		p.fecha,
		h.saldo,
		CASE 
			WHEN (h.saldo >= 0 AND h.saldo < 300000) THEN 'N0'
			WHEN h.saldo >= 300000 AND h.saldo < 1000000 THEN 'N1'
			WHEN h.saldo >= 1000000 AND h.saldo < 3000000 THEN 'N2'
			WHEN h.saldo >= 3000000 AND h.saldo < 5000000 THEN 'N3'
			WHEN h.saldo >= 5000000 THEN 'N4'
			WHEN h.identificacion IS NULL AND p.fecha > r.fecha_retiro THEN NULL
			ELSE 'N0'
		END AS "nivel"
	FROM intervalo_fechas AS p
	LEFT JOIN rch.historia AS h ON p.identificacion = h.identificacion AND p.fecha = corte_mes
	LEFT JOIN rch.retiros AS r ON p.identificacion = r.identificacion
), racha AS(
	-- Agregar un indicador de las rachas
	SELECT
		c.*,
		-- Para los casos en que haya 0, significa que hay racha, el 1 iundica que no hay racha.
		CASE WHEN nivel = LAG(c.nivel) OVER(PARTITION BY c.identificacion ORDER BY c.fecha) THEN 0 ELSE 1 END AS racha
	FROM clasificacion AS c
), grupos AS(
	-- Generar grupos de rachas, para así poder luego distinguirlas.
	SELECT
		r.*,
		SUM(r.racha) OVER(PARTITION BY r.identificacion ORDER BY r.fecha ROWS UNBOUNDED PRECEDING) AS grupo
	FROM racha AS r
), resumir_rachas AS(
	-- Realizar el resumen de las rachas por cliente
	SELECT
		r.identificacion,
		r.nivel,
		MAX(fecha) AS fecha_fin,
		COUNT(1) + 1 AS n_racha
	FROM grupos AS r
	WHERE racha = 0
	GROUP BY identificacion, nivel, grupo
), rachas_maximas AS(
	-- Obtener las rachas máximas por cliente y nivel
	SELECT
		identificacion,
		nivel,
		max(n_racha) AS racha
	FROM resumir_rachas
	GROUP BY identificacion, nivel
)
	-- Por ultimo, asegurarnos de traer solo la racha máxima por nivel y cliente
	SELECT
		rr.identificacion,
		rr.nivel,
		rr.fecha_fin,
		rm.racha
	FROM resumir_rachas AS rr
	INNER JOIN rachas_maximas AS rm ON rr.identificacion = rm.identificacion AND rr.nivel = rm.nivel AND rr.n_racha = rm.racha