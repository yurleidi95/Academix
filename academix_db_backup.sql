-- ============================================================================
-- ACADEMIX - RESPALDO Y COPIA COMPLETA DE BASE DE DATOS (MYSQL / MARIADB)
-- Generado: 2026-09-16 16:15:27
-- Motor de almacenamiento: InnoDB | Juego de caracteres: utf8mb4_unicode_ci
-- Cumple con especificaciones técnicas del informe y protocolos de empresa
-- ============================================================================

CREATE DATABASE IF NOT EXISTS `academix_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `academix_db`;

SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET NAMES utf8mb4;

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `accounts_customuser`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `accounts_customuser`;
CREATE TABLE `accounts_customuser` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME DEFAULT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME NOT NULL,
  `role` VARCHAR(20) NOT NULL,
  `document_type` VARCHAR(10) NOT NULL,
  `document_number` VARCHAR(30) DEFAULT NULL,
  `phone` VARCHAR(25) DEFAULT NULL,
  `address` VARCHAR(255) DEFAULT NULL,
  `avatar` VARCHAR(100) DEFAULT NULL,
  `must_change_password` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `accounts_customuser` (17 registros)
INSERT INTO `accounts_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `document_type`, `document_number`, `phone`, `address`, `avatar`, `must_change_password`, `created_at`, `updated_at`) VALUES
  (1, 'pbkdf2_sha256$870000$Tr5gVnG7myCUQalTOk9sgd$P5642czYYAN//6Djk/uoe3Mvku/T4Tinb1EBPkone+c=', '2026-09-15 02:15:14.660254', 1, 'admin', 'Administrador', 'Principal', 'admin@academix.edu.co', 1, 1, '2026-09-15 01:36:44.568904', 'ADMIN', 'CC', '1000000001', '3001234567', 'Sede Principal ACADEMIX', '', 0, '2026-09-15 01:36:44.873864', '2026-09-15 01:36:44.873864'),
  (2, 'pbkdf2_sha256$870000$l9l4mk6cNDgnxVclt8OVW3$sOuMJOiN5/oJkhv24fXt1rHt5UO4lL/0kMYELpf2NnE=', '2026-09-15 02:58:55.532901', 0, 'rector', 'Ramiro', 'Rectoría', 'rector@academix.edu.co', 1, 1, '2026-09-15 01:36:44.891411', 'RECTOR', 'CC', '1000000002', '3100000000', 'Ciudad Escolar', '', 0, '2026-09-15 01:36:45.208956', '2026-09-15 01:36:45.208956'),
  (3, 'pbkdf2_sha256$870000$vnjzoyRDnTCdWVc8Y1OeLC$SJi21Rg3RsLiNKWA9MeZxCYxlEP0TZVDo7XHFs1jkSw=', NULL, 0, 'secretaria', 'Sonia', 'Secretaría', 'secretaria@academix.edu.co', 0, 1, '2026-09-15 01:36:45.221365', 'SECRETARIA', 'CC', '1000000003', '3100000000', 'Ciudad Escolar', '', 0, '2026-09-15 01:36:45.539291', '2026-09-15 01:36:45.539291'),
  (4, 'pbkdf2_sha256$870000$KY4PlstJzA4B4eD2Wju3q8$OY8XcIijfk465Pbd4EO9ewN11msxq5nv1xhqc6VhyoI=', '2026-09-15 02:59:08.389055', 0, 'docente', 'Diego', 'Docente', 'docente@academix.edu.co', 0, 1, '2026-09-15 01:36:45.556742', 'TEACHER', 'CC', '1000000004', '3100000000', 'Ciudad Escolar', '', 0, '2026-09-15 01:36:45.866757', '2026-09-15 01:36:45.866757'),
  (5, 'pbkdf2_sha256$870000$LN16pr7FIQbGQVHym0hgXm$nEbAjTWL9jHgjSmSf2RQzyLtvqYmCYlgKzgrGLMYJXU=', '2026-09-15 02:59:09.619669', 0, 'estudiante', 'Esteban', 'Estudiante', 'estudiante@academix.edu.co', 0, 1, '2026-09-15 01:36:45.879857', 'STUDENT', 'CC', '1000000005', '3100000000', 'Ciudad Escolar', '', 0, '2026-09-15 01:36:46.185529', '2026-09-15 01:36:46.185529'),
  (6, 'pbkdf2_sha256$870000$zIKwEDUbl3RdFYu8lnn0qu$iqEqBR7vRqneUFR2iFHGQrkBG6aWsC479xpHwcrlLmA=', NULL, 0, 'acudiente', 'Patricia', 'Padre de Familia', 'acudiente@academix.edu.co', 0, 1, '2026-09-15 01:36:46.193143', 'PARENT', 'CC', '1000000006', '3100000000', 'Ciudad Escolar', '', 0, '2026-09-15 01:36:46.506262', '2026-09-15 01:36:46.506262'),
  (8, 'pbkdf2_sha256$870000$FxVNw2gXHxriauk9r4X2hw$lRULUOyEcSg2O3fJIRNaFdUghBsJ1yCKVhdHcy7Uy2Y=', '2026-09-16 15:55:50.478656', 0, 'dulce', 'Dulce', 'Docente', 'dulce@academix.edu.co', 0, 1, '2026-09-15 13:55:21.541776', 'TEACHER', 'CC', '1000000007', '3110000001', 'Sede Principal', '', 0, '2026-09-15 13:55:22.367120', '2026-09-15 14:00:48.889575'),
  (9, 'pbkdf2_sha256$870000$IzdokndLW4EGCgiK4CaTDE$bNu1v6zbLnVfF2dGXzCeQbL3pDLu4DQrAEuX2CcHHgE=', '2026-09-16 15:54:53.276716', 0, 'yesi', 'Yesi', 'Cabrera', 'yesi@academix.edu.co', 0, 1, '2026-09-15 13:55:22.406274', 'STUDENT', 'CC', '1000000008', '3001372139', 'Sede Principal', '', 0, '2026-09-15 13:55:23.291750', '2026-09-15 14:27:24.333161'),
  (10, 'pbkdf2_sha256$870000$ndhvJzpHZwlBYDRaaakT7W$w42qfsoyTNaA3wHCLVFBIrFkjFLvDJPLph951Xszy5g=', '2026-09-16 15:48:06.850754', 0, 'nurys', 'Nurys', 'Secretaria', 'nurys@academix.edu.co', 0, 1, '2026-09-15 13:55:23.321736', 'SECRETARIA', 'CC', '1000000009', '3110000003', 'Sede Principal', '', 0, '2026-09-15 13:55:24.208523', '2026-09-15 15:23:24.639957'),
  (11, 'pbkdf2_sha256$870000$evgcnJo89A7Hpj5ue96u4H$bMuYFfgvm8sznCU4bblFDckoocz2rNTxqhQrKyHvFo4=', NULL, 0, 'est_1221467456', 'Elizareth', 'Cabrera', 'eli@gmail.com', 0, 1, '2026-09-16 11:27:43.949022', 'STUDENT', 'TI', '1221467456', '3001372139', NULL, '', 1, '2026-09-16 11:27:45.069390', '2026-09-16 11:27:45.069420'),
  (12, 'pbkdf2_sha256$870000$gfKlPVFG0gzsaHsgY6tbZi$VhrIPQEUO015QIiCh8z3gQYf7+zSsxoen6U42tBwtok=', '2026-09-16 16:02:29.553818', 1, 'admini', '', '', 'admini@gmail.com', 1, 1, '2026-09-16 12:07:12.355032', 'STUDENT', 'CC', NULL, NULL, NULL, '', 0, '2026-09-16 12:07:13.098967', '2026-09-16 12:07:13.098983'),
  (13, 'pbkdf2_sha256$870000$lQd4nfzWKQL8jRHPFj67j7$d7ZkBAFoliVR5ANnAMn1t905ZNOQOv8H5nOm2F41t3c=', '2026-09-16 14:47:17.961666', 0, 'yurleidilondono@gmail.com', 'Yurleidi', 'Londoño', 'yurleidilondono@gmail.com', 0, 1, '2027-09-16 12:11:21', 'RECTOR', 'CC', '123456789', '300154896', 'Calle 22 carrera23', '', 0, '2026-09-16 12:11:22.613011', '2026-09-16 12:14:04.189534'),
  (14, 'pbkdf2_sha256$870000$tH5aIgzlEIZjq536pVTyEF$1vRSuA1W6yyYJcRfpu1BpmYZ504hEKdzV1F+yKMBkHs=', NULL, 0, 'est_1245678980', 'Camilo', 'Mendoza', 'camilo@gmail.com', 0, 1, '2026-09-16 12:16:50.169495', 'STUDENT', 'TI', '1245678980', '3124567843', NULL, '', 1, '2026-09-16 12:16:51.424143', '2026-09-16 12:16:51.424162'),
  (15, 'pbkdf2_sha256$870000$OPff12PI8ibKrIE32mlkZq$+9e0iXCcTQgDrsf+lixHVeNxF0VyYd0v5ZosmGJmzoo=', '2026-09-16 12:23:30.480886', 0, 'Ana@gmail.com', 'Ana', 'Retamozo', 'ana@gmail.com', 0, 1, '2027-09-16 12:20:24', 'PARENT', 'CC', '111245623', '3001245889', 'Calle 22 carrera23', '', 0, '2026-09-16 12:20:25.493870', '2026-09-16 12:22:55.211448'),
  (16, 'pbkdf2_sha256$870000$dPGnadmo0zPpwzCMTFk8MU$OAeZ/pbeC4i9waYMtePxFWvkP4/XpDoDth99a5S0+IE=', NULL, 0, 'est_12214537245', 'Alanna', 'Acosta', 'Alanna@gmail.com', 0, 1, '2026-09-16 12:23:36.727656', 'STUDENT', 'TI', '12214537245', '3209786543', NULL, '', 1, '2026-09-16 12:23:37.872305', '2026-09-16 12:23:37.872328'),
  (17, 'pbkdf2_sha256$870000$6HpYlPSBJFiljolZjspDY1$Rpx5LxHe4KMnpD2AW8I42nnMJnm5gx8NVh6y0NG0kms=', NULL, 0, 'doc_1234534234', 'Claudia', 'gomez', 'claudia@gmail.com', 0, 1, '2026-09-16 15:49:57.124372', 'TEACHER', 'CC', '1234534234', '3001245889', NULL, '', 1, '2026-09-16 15:49:58.331657', '2026-09-16 15:49:58.331720'),
  (18, 'pbkdf2_sha256$870000$yQKla7r6ctO6cpAlel9SSK$Su6xsyGid5NrbrjZbqgjpc6HGbMUA8Ei1dm0aET4hYo=', NULL, 0, 'est_1223454323', 'Andres', 'Cantillo', 'andres@gmail.com', 0, 1, '2026-09-16 15:52:51.124952', 'STUDENT', 'TI', '1223454323', '3245678907', NULL, '', 1, '2026-09-16 15:52:52.387441', '2026-09-16 15:52:52.387478');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `accounts_customuser_groups`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `accounts_customuser_groups`;
CREATE TABLE `accounts_customuser_groups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customuser_id` BIGINT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_accounts_customuser_groups_group_id` (`group_id`),
  CONSTRAINT `fk_accounts_customuser_groups_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  KEY `idx_accounts_customuser_groups_customuser_id` (`customuser_id`),
  CONSTRAINT `fk_accounts_customuser_groups_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `accounts_customuser_groups` (16 registros)
INSERT INTO `accounts_customuser_groups` (`id`, `customuser_id`, `group_id`) VALUES
  (1, 1, 1),
  (2, 2, 2),
  (3, 3, 3),
  (4, 4, 4),
  (5, 5, 5),
  (6, 6, 6),
  (7, 8, 4),
  (8, 9, 5),
  (9, 10, 3),
  (10, 11, 5),
  (11, 13, 2),
  (12, 14, 5),
  (13, 15, 6),
  (14, 16, 5),
  (15, 17, 4),
  (16, 18, 5);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `accounts_customuser_user_permissions`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customuser_id` BIGINT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_accounts_customuser_user_permissions_permission_id` (`permission_id`),
  CONSTRAINT `fk_accounts_customuser_user_permissions_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  KEY `idx_accounts_customuser_user_permissions_customuser_id` (`customuser_id`),
  CONSTRAINT `fk_accounts_customuser_user_permissions_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `accounts_customuser_user_permissions` (124 registros)
INSERT INTO `accounts_customuser_user_permissions` (`id`, `customuser_id`, `permission_id`) VALUES
  (1, 13, 1),
  (2, 13, 2),
  (3, 13, 3),
  (4, 13, 4),
  (5, 13, 5),
  (6, 13, 6),
  (7, 13, 7),
  (8, 13, 8),
  (9, 13, 9),
  (10, 13, 10),
  (11, 13, 11),
  (12, 13, 12),
  (13, 13, 13),
  (14, 13, 14),
  (15, 13, 15),
  (16, 13, 16),
  (17, 13, 17),
  (18, 13, 18),
  (19, 13, 19),
  (20, 13, 20),
  (21, 13, 21),
  (22, 13, 22),
  (23, 13, 23),
  (24, 13, 24),
  (25, 13, 25),
  (26, 13, 26),
  (27, 13, 27),
  (28, 13, 28),
  (29, 13, 29),
  (30, 13, 30),
  (31, 13, 31),
  (32, 13, 32),
  (33, 13, 33),
  (34, 13, 34),
  (35, 13, 35),
  (36, 13, 36),
  (37, 13, 37),
  (38, 13, 38),
  (39, 13, 39),
  (40, 13, 40),
  (41, 13, 41),
  (42, 13, 42),
  (43, 13, 43),
  (44, 13, 44),
  (45, 13, 45),
  (46, 13, 46),
  (47, 13, 47),
  (48, 13, 48),
  (49, 13, 49),
  (50, 13, 50),
  (51, 13, 51),
  (52, 13, 52),
  (53, 13, 53),
  (54, 13, 54),
  (55, 13, 55),
  (56, 13, 56),
  (57, 13, 57),
  (58, 13, 58),
  (59, 13, 59),
  (60, 13, 60),
  (61, 13, 61),
  (62, 13, 62),
  (63, 13, 63),
  (64, 13, 64),
  (65, 13, 65),
  (66, 13, 66),
  (67, 13, 67),
  (68, 13, 68),
  (69, 13, 69),
  (70, 13, 70),
  (71, 13, 71),
  (72, 13, 72),
  (73, 13, 73),
  (74, 13, 74),
  (75, 13, 75),
  (76, 13, 76),
  (77, 13, 77),
  (78, 13, 78),
  (79, 13, 79),
  (80, 13, 80),
  (81, 13, 81),
  (82, 13, 82),
  (83, 13, 83),
  (84, 13, 84),
  (85, 13, 85),
  (86, 13, 86),
  (87, 13, 87),
  (88, 13, 88),
  (89, 13, 89),
  (90, 13, 90),
  (91, 13, 91),
  (92, 13, 92),
  (93, 13, 93),
  (94, 13, 94),
  (95, 13, 95),
  (96, 13, 96),
  (97, 13, 97),
  (98, 13, 98),
  (99, 13, 99),
  (100, 13, 100),
  (101, 13, 101),
  (102, 13, 102),
  (103, 13, 103),
  (104, 13, 104),
  (105, 13, 105),
  (106, 13, 106),
  (107, 13, 107),
  (108, 13, 108),
  (109, 13, 109),
  (110, 13, 110),
  (111, 13, 111),
  (112, 13, 112),
  (113, 13, 113),
  (114, 13, 114),
  (115, 13, 115),
  (116, 13, 116),
  (117, 13, 117),
  (118, 13, 118),
  (119, 13, 119),
  (120, 13, 120),
  (121, 15, 120),
  (122, 15, 117),
  (123, 15, 118),
  (124, 15, 119);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `alerts_institutionalactivity`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `alerts_institutionalactivity`;
CREATE TABLE `alerts_institutionalactivity` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(160) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `event_date` DATE NOT NULL,
  `event_time` TIME DEFAULT NULL,
  `location` VARCHAR(120) NOT NULL,
  `target_audience` VARCHAR(20) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `created_by_id` BIGINT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_alerts_institutionalactivity_created_by_id` (`created_by_id`),
  CONSTRAINT `fk_alerts_institutionalactivity_created_by_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `alerts_institutionalactivity` (2 registros)
INSERT INTO `alerts_institutionalactivity` (`id`, `title`, `description`, `event_date`, `event_time`, `location`, `target_audience`, `is_active`, `created_at`, `created_by_id`) VALUES
  (1, 'Entrega de informe', 'entrega de informe', '2026-09-17', '10:00:00', 'Instalaciones del Colegio', 'ALL', 1, '2026-09-16 11:57:34.674219', NULL),
  (2, 'Reunión de Docentes', 'Puntualidad por favor', '2026-09-18', '08:48:00', 'Instalaciones del Colegio', 'TEACHERS', 1, '2026-09-16 12:48:28.449344', 13);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `alerts_systemalert`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `alerts_systemalert`;
CREATE TABLE `alerts_systemalert` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(150) NOT NULL,
  `message` LONGTEXT NOT NULL,
  `level` VARCHAR(15) NOT NULL,
  `target_role` VARCHAR(20) DEFAULT NULL,
  `is_dismissible` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `recipient_user_id` BIGINT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_alerts_systemalert_recipient_user_id` (`recipient_user_id`),
  CONSTRAINT `fk_alerts_systemalert_recipient_user_id` FOREIGN KEY (`recipient_user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `alerts_systemalert` (14 registros)
INSERT INTO `alerts_systemalert` (`id`, `title`, `message`, `level`, `target_role`, `is_dismissible`, `is_active`, `created_at`, `recipient_user_id`) VALUES
  (1, 'Cierre de Calificaciones del Periodo', 'El periodo lectivo se encuentra próximo a su fecha límite de registro.', 'WARNING', NULL, 1, 0, '2026-09-15 01:46:54.447953', NULL),
  (2, 'Bienvenido a ACADEMIX', 'Plataforma institucional configurada y lista para el Sprint 1: Fundación.', 'INFO', NULL, 1, 0, '2026-09-15 01:46:54.456430', NULL),
  (3, '🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: Esteban Estudiante', 'El estudiante ha acumulado un 100.00% de inasistencias en Matemáticas Fundamentales (Periodo 1). Se encuentra en causal de reprobación.', 'BLOCK', NULL, 0, 1, '2026-09-15 02:28:48.305566', 6),
  (4, '🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: Esteban Estudiante', 'El estudiante ha acumulado un 50.00% de inasistencias en Matemáticas Fundamentales (Periodo 1). Se encuentra en causal de reprobación.', 'BLOCK', NULL, 0, 1, '2026-09-15 15:20:36.809920', 6),
  (5, '🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: Esteban Estudiante', 'El estudiante ha acumulado un 25.00% de inasistencias en Matemáticas Fundamentales (Periodo 1). Se encuentra en causal de reprobación.', 'BLOCK', NULL, 0, 1, '2026-09-15 15:20:38.309205', 6),
  (6, '🟡 AVISO DE AUSENTISMO: Esteban Estudiante', 'El estudiante registra un 16.50% de inasistencias en Matemáticas Fundamentales. Se recomienda contactar a acudiente.', 'WARNING', NULL, 1, 1, '2026-09-15 15:20:39.564490', 6),
  (7, '🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: Esteban Estudiante', 'El estudiante ha acumulado un 50.00% de inasistencias en Matemáticas Fundamentales (Periodo 1). Se encuentra en causal de reprobación.', 'BLOCK', NULL, 0, 1, '2026-09-15 15:20:44.744241', 6),
  (8, '🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: Esteban Estudiante', 'El estudiante ha acumulado un 25.00% de inasistencias en Matemáticas Fundamentales (Periodo 1). Se encuentra en causal de reprobación.', 'BLOCK', NULL, 0, 1, '2026-09-15 15:20:48.037517', 6),
  (9, '🟡 AVISO DE AUSENTISMO: Esteban Estudiante', 'El estudiante registra un 16.50% de inasistencias en Matemáticas Fundamentales. Se recomienda contactar a acudiente.', 'WARNING', NULL, 1, 1, '2026-09-15 15:20:49.760104', 6),
  (10, '📅 Actividad Institucional: Entrega de informe', 'Fecha: 2026-09-17 a las 10:00 | Lugar: Instalaciones del Colegio. entrega de informe', 'INFO', 'STUDENT', 1, 1, '2026-09-16 11:57:34.678087', NULL),
  (11, '📅 Actividad Institucional: Entrega de informe', 'Fecha: 2026-09-17 a las 10:00 | Lugar: Instalaciones del Colegio. entrega de informe', 'INFO', 'TEACHER', 1, 1, '2026-09-16 11:57:34.680658', NULL),
  (12, '📅 Actividad Institucional: Entrega de informe', 'Fecha: 2026-09-17 a las 10:00 | Lugar: Instalaciones del Colegio. entrega de informe', 'INFO', 'PARENT', 1, 1, '2026-09-16 11:57:34.681724', NULL),
  (13, '📅 Actividad Institucional: Entrega de informe', 'Fecha: 2026-09-17 a las 10:00 | Lugar: Instalaciones del Colegio. entrega de informe', 'INFO', 'SECRETARIA', 1, 1, '2026-09-16 11:57:34.682825', NULL),
  (14, '📅 Actividad Institucional: Reunión de Docentes', 'Fecha: 2026-09-18 a las 08:48 | Lugar: Instalaciones del Colegio. Puntualidad por favor', 'INFO', 'TEACHER', 1, 1, '2026-09-16 12:48:28.451443', NULL);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `attendance_attendancerecord`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `attendance_attendancerecord`;
CREATE TABLE `attendance_attendancerecord` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(20) NOT NULL,
  `justification` TEXT DEFAULT NULL,
  `justification_file` VARCHAR(100) DEFAULT NULL,
  `is_justified` TINYINT(1) NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `student_id` BIGINT NOT NULL,
  `session_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_attendance_attendancerecord_session_id` (`session_id`),
  CONSTRAINT `fk_attendance_attendancerecord_session_id` FOREIGN KEY (`session_id`) REFERENCES `attendance_attendancesession` (`id`),
  KEY `idx_attendance_attendancerecord_student_id` (`student_id`),
  CONSTRAINT `fk_attendance_attendancerecord_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `attendance_attendancerecord` (15 registros)
INSERT INTO `attendance_attendancerecord` (`id`, `status`, `justification`, `justification_file`, `is_justified`, `updated_at`, `student_id`, `session_id`) VALUES
  (1, 'PRESENT', NULL, '', 0, '2026-09-15 02:28:48.303986', 1, 1),
  (2, 'PRESENT', NULL, '', 0, '2026-09-15 15:20:49.751972', 1, 2),
  (3, 'PRESENT', NULL, '', 0, '2026-09-16 11:29:03.740257', 3, 4),
  (4, 'PRESENT', NULL, '', 0, '2026-09-16 11:29:03.744860', 2, 4),
  (5, 'PRESENT', NULL, '', 0, '2026-09-16 11:29:03.749192', 1, 4),
  (6, 'PRESENT', NULL, '', 0, '2026-09-16 12:29:27.899206', 5, 6),
  (7, 'PRESENT', NULL, '', 0, '2026-09-16 12:29:27.904028', 4, 6),
  (8, 'PRESENT', NULL, '', 0, '2026-09-16 12:57:55.339370', 5, 7),
  (9, 'PRESENT', NULL, '', 0, '2026-09-16 12:57:55.343448', 4, 7),
  (10, 'PRESENT', NULL, '', 0, '2026-09-16 13:01:05.483325', 3, 8),
  (11, 'PRESENT', NULL, '', 0, '2026-09-16 13:01:05.486348', 2, 8),
  (12, 'PRESENT', NULL, '', 0, '2026-09-16 13:01:05.490872', 1, 8),
  (13, 'PRESENT', NULL, '', 0, '2026-09-16 15:58:22.246456', 3, 9),
  (14, 'PRESENT', NULL, '', 0, '2026-09-16 15:58:22.252554', 2, 9),
  (15, 'PRESENT', NULL, '', 0, '2026-09-16 15:58:22.259538', 1, 9);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `attendance_attendancesession`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `attendance_attendancesession`;
CREATE TABLE `attendance_attendancesession` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `hours_count` INT NOT NULL,
  `observations` LONGTEXT DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `academic_period_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `recorded_by_id` BIGINT DEFAULT NULL,
  `subject_id` BIGINT NOT NULL,
  `teaching_assignment_id` BIGINT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_attendance_attendancesession_teaching_assignment_id` (`teaching_assignment_id`),
  CONSTRAINT `fk_attendance_attendancesession_teaching_assignment_id` FOREIGN KEY (`teaching_assignment_id`) REFERENCES `teachers_teachingassignment` (`id`),
  KEY `idx_attendance_attendancesession_subject_id` (`subject_id`),
  CONSTRAINT `fk_attendance_attendancesession_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_attendance_attendancesession_recorded_by_id` (`recorded_by_id`),
  CONSTRAINT `fk_attendance_attendancesession_recorded_by_id` FOREIGN KEY (`recorded_by_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_attendance_attendancesession_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_attendance_attendancesession_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_attendance_attendancesession_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_attendance_attendancesession_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `attendance_attendancesession` (9 registros)
INSERT INTO `attendance_attendancesession` (`id`, `date`, `hours_count`, `observations`, `created_at`, `updated_at`, `academic_period_id`, `course_section_id`, `recorded_by_id`, `subject_id`, `teaching_assignment_id`) VALUES
  (1, '2026-02-16', 1, NULL, '2026-09-15 02:25:02.453866', '2026-09-15 02:25:02.453866', 1, 1, 4, 1, NULL),
  (2, '2026-09-15', 1, NULL, '2026-09-15 12:08:43.936531', '2026-09-15 12:08:43.936579', 1, 1, NULL, 1, NULL),
  (3, '2026-09-15', 1, NULL, '2026-09-15 14:28:38.751527', '2026-09-15 14:28:38.751570', 1, 2, 10, 1, NULL),
  (4, '2026-09-16', 1, NULL, '2026-09-16 11:29:03.727564', '2026-09-16 11:29:03.727614', 1, 1, 10, 1, NULL),
  (5, '2026-09-16', 2, '', '2026-09-16 12:04:10.340266', '2026-09-16 12:04:10.340347', 1, 3, 8, 4, 1),
  (6, '2026-09-16', 1, NULL, '2026-09-16 12:29:27.889069', '2026-09-16 12:29:27.889131', 1, 3, 8, 5, NULL),
  (7, '2026-09-16', 1, NULL, '2026-09-16 12:57:55.329473', '2026-09-16 12:57:55.329510', 2, 3, 8, 5, NULL),
  (8, '2026-09-16', 1, NULL, '2026-09-16 13:01:05.476252', '2026-09-16 13:01:05.476297', 2, 1, 8, 2, NULL),
  (9, '2026-09-16', 1, NULL, '2026-09-16 15:58:22.228799', '2026-09-16 15:58:22.228898', 1, 1, 8, 2, NULL);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `audit_auditlog`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `audit_auditlog`;
CREATE TABLE `audit_auditlog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NOT NULL,
  `action` VARCHAR(25) NOT NULL,
  `table_name` VARCHAR(100) NOT NULL,
  `record_id` INT DEFAULT NULL,
  `old_values` TEXT DEFAULT NULL,
  `new_values` TEXT DEFAULT NULL,
  `ip_address` VARCHAR(39) DEFAULT NULL,
  `reason` TEXT DEFAULT NULL,
  `user_id` BIGINT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_audit_auditlog_user_id` (`user_id`),
  CONSTRAINT `fk_audit_auditlog_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `audit_auditlog` (232 registros)
INSERT INTO `audit_auditlog` (`id`, `timestamp`, `action`, `table_name`, `record_id`, `old_values`, `new_values`, `ip_address`, `reason`, `user_id`) VALUES
  (1, '2026-09-15 01:51:47.399351', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (2, '2026-09-15 02:03:45.336775', 'UPDATE', 'AcademicYear', '1', NULL, '{"year": 2026, "is_current": true, "status": "ACTIVE"}', NULL, 'Establecido año 2026 como año lectivo vigente', NULL),
  (3, '2026-09-15 02:03:45.432306', 'INSERT', 'GradeSubject', '1', NULL, '{"grade": "Sexto", "subject": "Matem\\u00e1ticas Fundamentales", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Matemáticas Fundamentales en grado Sexto (4h/sem)', NULL),
  (4, '2026-09-15 02:03:45.447180', 'INSERT', 'GradeSubject', '2', NULL, '{"grade": "Sexto", "subject": "Geometr\\u00eda y Estad\\u00edstica", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Geometría y Estadística en grado Sexto (4h/sem)', NULL),
  (5, '2026-09-15 02:03:45.475675', 'INSERT', 'GradeSubject', '3', NULL, '{"grade": "Sexto", "subject": "Biolog\\u00eda General", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Biología General en grado Sexto (4h/sem)', NULL),
  (6, '2026-09-15 02:03:45.487617', 'INSERT', 'GradeSubject', '4', NULL, '{"grade": "Sexto", "subject": "F\\u00edsica Elemental", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Física Elemental en grado Sexto (4h/sem)', NULL),
  (7, '2026-09-15 02:03:45.517066', 'INSERT', 'GradeSubject', '5', NULL, '{"grade": "Sexto", "subject": "Lengua Castellana", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Lengua Castellana en grado Sexto (4h/sem)', NULL),
  (8, '2026-09-15 02:03:45.542381', 'INSERT', 'GradeSubject', '6', NULL, '{"grade": "Sexto", "subject": "Ingl\\u00e9s Comunicativo", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Inglés Comunicativo en grado Sexto (4h/sem)', NULL),
  (9, '2026-09-15 02:03:45.565601', 'INSERT', 'GradeSubject', '7', NULL, '{"grade": "Sexto", "subject": "Tecnolog\\u00eda e Inform\\u00e1tica", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Tecnología e Informática en grado Sexto (4h/sem)', NULL),
  (10, '2026-09-15 02:03:45.591812', 'INSERT', 'GradeSubject', '8', NULL, '{"grade": "Sexto", "subject": "Historia y Geograf\\u00eda", "weekly_hours": 4, "weight_percentage": "100.00"}', NULL, 'Configuración curricular: Historia y Geografía en grado Sexto (4h/sem)', NULL),
  (11, '2026-09-15 02:03:45.630105', 'INSERT', 'TeachingAssignment', '1', NULL, '{"teacher": "Diego Docente", "section": "6-A", "subject": "Matem\\u00e1ticas Fundamentales", "year": 2026}', NULL, 'Asignación académica de Matemáticas Fundamentales en 6-A a docente', NULL),
  (12, '2026-09-15 02:03:45.640180', 'INSERT', 'TeachingAssignment', '2', NULL, '{"teacher": "Diego Docente", "section": "6-B", "subject": "Matem\\u00e1ticas Fundamentales", "year": 2026}', NULL, 'Asignación académica de Matemáticas Fundamentales en 6-B a docente', NULL),
  (13, '2026-09-15 02:03:45.659684', 'INSERT', 'Enrollment', '1', NULL, '{"student": "Esteban Estudiante", "code": "EST-2026-0001", "section": "6-A", "year": 2026, "status": "ACTIVE"}', NULL, 'Matrícula de estudiante estudiante en curso 6-A (2026)', NULL),
  (14, '2026-09-15 02:07:13.732420', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (15, '2026-09-15 02:11:15.760930', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (16, '2026-09-15 02:12:00.921221', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (17, '2026-09-15 02:12:10.639661', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (18, '2026-09-15 02:12:22.857783', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (19, '2026-09-15 02:14:15.631387', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (20, '2026-09-15 02:15:03.714118', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (21, '2026-09-15 02:15:03.752702', 'PERIOD_CLOSE', 'AcademicPeriod', '1', '{"status": "ACTIVE"}', '{"status": "CLOSED"}', '127.0.0.1', 'Cierre preventivo de prueba', 1),
  (22, '2026-09-15 02:15:14.661259', 'LOGIN', 'CustomUser', '1', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 1),
  (23, '2026-09-15 02:15:14.692515', 'UPDATE', 'AcademicPeriod', '1', '{"status": "CLOSED"}', '{"status": "ACTIVE"}', '127.0.0.1', 'Reapertura para operación normal', 1),
  (24, '2026-09-15 02:24:48.010242', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (25, '2026-09-15 02:28:48.134592', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (26, '2026-09-15 02:28:48.305566', 'UPDATE', 'AttendanceRecord', '1', '{"status": "PRESENT"}', '{"status": "UNJUSTIFIED", "justification": null}', '127.0.0.1', 'Asistencia actualizada para estudiante: UNJUSTIFIED', 4),
  (27, '2026-09-15 02:28:48.344478', 'UPDATE', 'AttendanceSession', '1', NULL, '{"bulk_action": "ALL_PRESENT"}', '127.0.0.1', 'Marcado masivo de presentes en grupo 6-A para Matemáticas Fundamentales', 4),
  (28, '2026-09-15 02:38:28.964720', 'INSERT', 'GradeRecord', '1', '{"score": null}', '{"score": "4.50", "criterion": "Evaluaciones y Quices"}', NULL, 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.50', NULL),
  (29, '2026-09-15 02:38:28.981286', 'INSERT', 'GradeRecord', '2', '{"score": null}', '{"score": "4.00", "criterion": "Talleres y Actividades"}', NULL, 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 4.00', NULL),
  (30, '2026-09-15 02:38:28.996709', 'INSERT', 'GradeRecord', '3', '{"score": null}', '{"score": "4.80", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', NULL, 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 4.80', NULL),
  (31, '2026-09-15 02:38:29.009956', 'INSERT', 'Homework', '1', NULL, '{"title": "Taller #1: Operaciones con Conjuntos", "section": "6-A", "subject": "MAT-01"}', NULL, 'Asignación de tarea: Taller #1: Operaciones con Conjuntos para grupo 6-A', NULL),
  (32, '2026-09-15 02:38:29.021226', 'INSERT', 'HomeworkSubmission', '1', NULL, '{"student": "estudiante", "homework": "Taller #1: Operaciones con Conjuntos", "status": "SUBMITTED"}', NULL, 'Entrega de tarea Taller #1: Operaciones con Conjuntos por estudiante', NULL),
  (33, '2026-09-15 02:38:29.034651', 'UPDATE', 'HomeworkSubmission', '1', NULL, '{"score": "4.50", "feedback": "Buen trabajo con las demostraciones.", "status": "GRADED"}', NULL, 'Calificación de tarea Taller #1: Operaciones con Conjuntos para estudiante: 4.50', NULL),
  (34, '2026-09-15 02:39:56.366080', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (35, '2026-09-15 02:40:07.744496', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (36, '2026-09-15 02:40:22.910980', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (37, '2026-09-15 02:40:32.839074', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (38, '2026-09-15 02:40:32.928074', 'UPDATE', 'GradeRecord', '1', '{"score": "4.50"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (39, '2026-09-15 02:40:38.970240', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (40, '2026-09-15 02:40:39.070125', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (41, '2026-09-15 02:40:45.618538', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (42, '2026-09-15 02:40:45.712104', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (43, '2026-09-15 02:41:09.047653', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (44, '2026-09-15 02:41:09.149920', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (45, '2026-09-15 02:41:27.044863', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (46, '2026-09-15 02:41:27.147539', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (47, '2026-09-15 02:41:27.720789', 'LOGIN', 'CustomUser', '5', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 5),
  (48, '2026-09-15 02:58:55.532901', 'LOGIN', 'CustomUser', '2', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 2),
  (49, '2026-09-15 02:58:56.694951', 'LOGIN', 'CustomUser', '5', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 5),
  (50, '2026-09-15 02:59:08.389055', 'LOGIN', 'CustomUser', '4', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 4),
  (51, '2026-09-15 02:59:08.815908', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "4.80", "criterion": "Evaluaciones y Quices"}', '127.0.0.1', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 4.80', 4),
  (52, '2026-09-15 02:59:09.619669', 'LOGIN', 'CustomUser', '5', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 5),
  (53, '2026-09-15 12:05:26.225672', 'LOGIN', 'CustomUser', '7', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', NULL),
  (54, '2026-09-15 13:09:29.037991', 'LOGOUT', 'CustomUser', '7', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', NULL),
  (55, '2026-09-15 13:50:39.210001', 'FAILED_LOGIN', 'CustomUser', NULL, NULL, '{"attempted_username": " Padre"}', '10.8.182.242', 'Intento fallido de autenticación para usuario:  Padre', NULL),
  (56, '2026-09-15 13:52:15.934755', 'FAILED_LOGIN', 'CustomUser', NULL, NULL, '{"attempted_username": "Admin"}', '10.8.182.242', 'Intento fallido de autenticación para usuario: Admin', NULL),
  (57, '2026-09-15 13:56:22.961560', 'LOGIN', 'CustomUser', '9', NULL, NULL, '10.8.182.242', 'Inicio de sesión exitoso en la plataforma', 9),
  (58, '2026-09-15 13:56:37.506453', 'LOGIN', 'CustomUser', '10', NULL, NULL, '10.8.182.202', 'Inicio de sesión exitoso en la plataforma', 10),
  (59, '2026-09-15 13:56:38.353113', 'LOGIN', 'CustomUser', '8', NULL, NULL, '10.8.182.41', 'Inicio de sesión exitoso en la plataforma', 8),
  (60, '2026-09-15 13:58:36.435881', 'LOGIN', 'CustomUser', '7', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', NULL),
  (61, '2026-09-15 13:59:51.488986', 'LOGIN', 'CustomUser', '9', NULL, NULL, '10.8.182.62', 'Inicio de sesión exitoso en la plataforma', 9),
  (62, '2026-09-15 14:00:24.831896', 'UPDATE', 'GradeRecord', '1', '{"score": "4.80"}', '{"score": "1.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.62', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 1.00', 9),
  (63, '2026-09-15 14:00:25.538993', 'UPDATE', 'GradeRecord', '1', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.62', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 1.00', 9),
  (64, '2026-09-15 14:00:27.888877', 'UPDATE', 'GradeRecord', '2', '{"score": "4.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.62', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 9),
  (65, '2026-09-15 14:00:28.344047', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.62', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 9),
  (66, '2026-09-15 14:00:31.173273', 'UPDATE', 'GradeRecord', '3', '{"score": "4.80"}', '{"score": "1.00", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.62', 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 1.00', 9),
  (67, '2026-09-15 14:00:31.591632', 'UPDATE', 'GradeRecord', '3', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.62', 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 1.00', 9),
  (68, '2026-09-15 14:00:46.688824', 'UPDATE', 'CustomUser', '8', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '10.8.182.41', 'Actualización de datos personales de perfil', 8),
  (69, '2026-09-15 14:00:47.896303', 'UPDATE', 'CustomUser', '8', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '10.8.182.41', 'Actualización de datos personales de perfil', 8),
  (70, '2026-09-15 14:00:48.891590', 'UPDATE', 'CustomUser', '8', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '{"phone": "3110000001", "address": "Sede Principal", "email": "dulce@academix.edu.co"}', '10.8.182.41', 'Actualización de datos personales de perfil', 8),
  (71, '2026-09-15 14:27:11.261773', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (72, '2026-09-15 14:27:13.798655', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (73, '2026-09-15 14:27:19.634248', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (74, '2026-09-15 14:27:20.022290', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (75, '2026-09-15 14:27:20.221577', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (76, '2026-09-15 14:27:20.459741', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (77, '2026-09-15 14:27:20.715206', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (78, '2026-09-15 14:27:21.094951', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (79, '2026-09-15 14:27:21.400354', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (80, '2026-09-15 14:27:21.685881', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (81, '2026-09-15 14:27:21.950721', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (82, '2026-09-15 14:27:22.231668', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (83, '2026-09-15 14:27:22.387721', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (84, '2026-09-15 14:27:22.540085', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (85, '2026-09-15 14:27:22.959258', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (86, '2026-09-15 14:27:23.542544', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (87, '2026-09-15 14:27:24.100777', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (88, '2026-09-15 14:27:24.335267', 'UPDATE', 'CustomUser', '9', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '{"phone": "3001372139", "address": "Sede Principal", "email": "yesi@academix.edu.co"}', '10.8.182.62', 'Actualización de datos personales de perfil', 9),
  (89, '2026-09-15 14:48:08.467008', 'UPDATE', 'GradeRecord', '1', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.202', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 1.00', 10),
  (90, '2026-09-15 14:48:09.334121', 'UPDATE', 'GradeRecord', '1', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.202', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 1.00', 10),
  (91, '2026-09-15 14:48:11.273562', 'UPDATE', 'GradeRecord', '1', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.202', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 1.00', 10),
  (92, '2026-09-15 14:48:16.762613', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 10),
  (93, '2026-09-15 14:48:17.311018', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 10),
  (94, '2026-09-15 14:48:17.840883', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 10),
  (95, '2026-09-15 14:48:18.370910', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 10),
  (96, '2026-09-15 14:48:18.939283', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "1.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 1.00', 10),
  (97, '2026-09-15 14:48:25.307849', 'UPDATE', 'GradeRecord', '2', '{"score": "1.00"}', '{"score": "2.17", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 2.17', 10),
  (98, '2026-09-15 14:48:35.242571', 'UPDATE', 'GradeRecord', '1', '{"score": "1.00"}', '{"score": "2.37", "criterion": "Evaluaciones y Quices"}', '10.8.182.202', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 2.37', 10),
  (99, '2026-09-15 14:48:53.044614', 'UPDATE', 'GradeRecord', '3', '{"score": "1.00"}', '{"score": "3.84", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.202', 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 3.84', 10),
  (100, '2026-09-15 14:49:16.816312', 'UPDATE', 'GradeRecord', '2', '{"score": "2.17"}', '{"score": "5.00", "criterion": "Talleres y Actividades"}', '10.8.182.202', 'Calificación registrada para estudiante en Talleres y Actividades (MAT-01): 5.00', 10),
  (101, '2026-09-15 14:49:35.245922', 'UPDATE', 'GradeRecord', '1', '{"score": "2.37"}', '{"score": "3.65", "criterion": "Evaluaciones y Quices"}', '10.8.182.202', 'Calificación registrada para estudiante en Evaluaciones y Quices (MAT-01): 3.65', 10),
  (102, '2026-09-15 14:49:39.739249', 'UPDATE', 'GradeRecord', '3', '{"score": "3.84"}', '{"score": "1.35", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.202', 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 1.35', 10),
  (103, '2026-09-15 14:49:59.039891', 'UPDATE', 'GradeRecord', '3', '{"score": "1.35"}', '{"score": "4.14", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.202', 'Calificación registrada para estudiante en Actitudinal y Autoevaluación (MAT-01): 4.14', 10),
  (104, '2026-09-15 15:18:27.349551', 'LOGOUT', 'CustomUser', '9', NULL, NULL, '10.8.182.62', 'Cierre de sesión manual voluntario', 9),
  (105, '2026-09-15 15:18:41.552700', 'LOGIN', 'CustomUser', '10', NULL, NULL, '10.8.182.62', 'Inicio de sesión exitoso en la plataforma', 10),
  (106, '2026-09-15 15:20:36.794201', 'UPDATE', 'AttendanceRecord', '2', '{"status": "PRESENT"}', '{"status": "UNJUSTIFIED", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: UNJUSTIFIED', 10),
  (107, '2026-09-15 15:20:38.301679', 'UPDATE', 'AttendanceRecord', '2', '{"status": "UNJUSTIFIED"}', '{"status": "JUSTIFIED", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: JUSTIFIED', 10),
  (108, '2026-09-15 15:20:39.555905', 'UPDATE', 'AttendanceRecord', '2', '{"status": "JUSTIFIED"}', '{"status": "LATE", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: LATE', 10),
  (109, '2026-09-15 15:20:44.739466', 'UPDATE', 'AttendanceRecord', '2', '{"status": "LATE"}', '{"status": "UNJUSTIFIED", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: UNJUSTIFIED', 10),
  (110, '2026-09-15 15:20:48.031155', 'UPDATE', 'AttendanceRecord', '2', '{"status": "UNJUSTIFIED"}', '{"status": "JUSTIFIED", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: JUSTIFIED', 10),
  (111, '2026-09-15 15:20:49.753457', 'UPDATE', 'AttendanceRecord', '2', '{"status": "JUSTIFIED"}', '{"status": "LATE", "justification": null}', '10.8.182.202', 'Asistencia actualizada para estudiante: LATE', 10),
  (112, '2026-09-15 15:20:59.229509', 'UPDATE', 'AttendanceSession', '2', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.202', 'Marcado masivo de presentes en grupo 6-A para Matemáticas Fundamentales', 10),
  (113, '2026-09-15 15:21:00.319285', 'UPDATE', 'AttendanceSession', '2', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.202', 'Marcado masivo de presentes en grupo 6-A para Matemáticas Fundamentales', 10),
  (114, '2026-09-15 15:23:22.522222', 'UPDATE', 'CustomUser', '10', '{"phone": "3110000003", "address": "Sede Principal", "email": "nurys@academix.edu.co"}', '{"phone": "3110000003", "address": "Sede Principal", "email": "nurys@academix.edu.co"}', '10.8.182.202', 'Actualización de datos personales de perfil', 10),
  (115, '2026-09-15 15:23:24.642271', 'UPDATE', 'CustomUser', '10', '{"phone": "3110000003", "address": "Sede Principal", "email": "nurys@academix.edu.co"}', '{"phone": "3110000003", "address": "Sede Principal", "email": "nurys@academix.edu.co"}', '10.8.182.202', 'Actualización de datos personales de perfil', 10),
  (116, '2026-09-16 00:55:31.954969', 'LOGIN', 'CustomUser', '7', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', NULL),
  (117, '2026-09-16 11:27:45.093163', 'INSERT', 'Enrollment', '2', NULL, '{"student": "Elizareth Cabrera", "code": "236654", "section": "6-A", "year": 2026, "status": "ACTIVE"}', '10.8.182.62', 'Matrícula de estudiante est_1221467456 en curso 6-A (2026)', 10),
  (118, '2026-09-16 11:27:45.096716', 'CREATE_STUDENT', 'StudentProfile', '3', NULL, '{"username": "est_1221467456", "student_code": "236654", "section": "6-A"}', '10.8.182.62', 'Registro de nuevo alumno por nurys', 10),
  (119, '2026-09-16 11:28:00.222009', 'INSERT', 'Enrollment', '3', NULL, '{"student": "Yesi Cabrera", "code": "EST-2026-0002", "section": "6-A", "year": 2026, "status": "ACTIVE"}', '10.8.182.62', 'Matrícula de estudiante yesi en curso 6-A (2026)', 10),
  (120, '2026-09-16 11:49:57.233098', 'LOGIN', 'CustomUser', '8', NULL, NULL, '10.8.182.41', 'Inicio de sesión exitoso en la plataforma', 8),
  (121, '2026-09-16 11:53:50.372166', 'LOGOUT', 'CustomUser', '10', NULL, NULL, '10.8.182.62', 'Cierre de sesión manual voluntario', 10),
  (122, '2026-09-16 11:54:16.908580', 'FAILED_LOGIN', 'CustomUser', NULL, NULL, '{"attempted_username": "docente"}', '10.8.182.62', 'Intento fallido de autenticación para usuario: docente', NULL),
  (123, '2026-09-16 11:54:44.444751', 'LOGIN', 'CustomUser', '10', NULL, NULL, '10.8.182.62', 'Inicio de sesión exitoso en la plataforma', 10),
  (124, '2026-09-16 11:55:12.383666', 'LOGIN', 'CustomUser', '9', NULL, NULL, '10.8.182.62', 'Inicio de sesión exitoso en la plataforma', 9),
  (125, '2026-09-16 12:06:38.448969', 'INSERT', 'Homework', '2', NULL, '{"title": "Evaluaci\\u00f3n escrita", "section": "6-A", "subject": "ESP-01"}', '10.8.182.41', 'Asignación de tarea: Evaluación escrita para grupo 6-A', 8),
  (126, '2026-09-16 12:08:34.385049', 'INSERT', 'TeachingAssignment', '3', NULL, '{"teacher": "Dulce Docente", "section": "7-A", "subject": "Lengua Castellana", "year": 2026}', '10.8.182.62', 'Asignación académica de Lengua Castellana en 7-A a dulce', 10),
  (127, '2026-09-16 12:11:31.005601', 'INSERT', 'Homework', '3', NULL, '{"title": "Evaluaci\\u00f3n escrita", "section": "7-A", "subject": "ESP-01"}', '10.8.182.41', 'Asignación de tarea: Evaluación escrita para grupo 7-A', 8),
  (128, '2026-09-16 12:14:22.707135', 'FAILED_LOGIN', 'CustomUser', NULL, NULL, '{"attempted_username": "yurledi"}', '127.0.0.1', 'Intento fallido de autenticación para usuario: yurledi', NULL),
  (129, '2026-09-16 12:14:35.328642', 'LOGIN', 'CustomUser', '13', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 13),
  (130, '2026-09-16 12:16:51.449028', 'INSERT', 'Enrollment', '4', NULL, '{"student": "Camilo Mendoza", "code": "452314", "section": "7-A", "year": 2026, "status": "ACTIVE"}', '10.8.182.62', 'Matrícula de estudiante est_1245678980 en curso 7-A (2026)', 10),
  (131, '2026-09-16 12:16:51.450498', 'CREATE_STUDENT', 'StudentProfile', '4', NULL, '{"username": "est_1245678980", "student_code": "452314", "section": "7-A"}', '10.8.182.62', 'Registro de nuevo alumno por nurys', 10),
  (132, '2026-09-16 12:17:19.795381', 'INSERT', 'GradeRecord', '4', '{"score": null}', '{"score": "0.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.00', 8),
  (133, '2026-09-16 12:17:20.287829', 'UPDATE', 'GradeRecord', '4', '{"score": null}', '{"score": "0.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.00', 8),
  (134, '2026-09-16 12:17:21.370797', 'UPDATE', 'GradeRecord', '4', '{"score": null}', '{"score": "0.08", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.08', 8),
  (135, '2026-09-16 12:17:24.178829', 'UPDATE', 'GradeRecord', '4', '{"score": "0.08"}', '{"score": "0.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.00', 8),
  (136, '2026-09-16 12:17:24.811447', 'UPDATE', 'GradeRecord', '4', '{"score": null}', '{"score": "0.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.00', 8),
  (137, '2026-09-16 12:17:25.319260', 'UPDATE', 'GradeRecord', '4', '{"score": null}', '{"score": "0.00", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.00', 8),
  (138, '2026-09-16 12:17:31.262721', 'UPDATE', 'GradeRecord', '4', '{"score": null}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (139, '2026-09-16 12:17:31.957785', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (140, '2026-09-16 12:17:32.614143', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (141, '2026-09-16 12:17:33.317272', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (142, '2026-09-16 12:17:33.622591', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (143, '2026-09-16 12:17:34.333848', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (144, '2026-09-16 12:17:35.155085', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (145, '2026-09-16 12:17:36.517305', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (146, '2026-09-16 12:17:37.089793', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (147, '2026-09-16 12:17:37.394172', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (148, '2026-09-16 12:17:37.857467', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (149, '2026-09-16 12:17:39.337074', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (150, '2026-09-16 12:17:42.204017', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (151, '2026-09-16 12:17:42.701662', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (152, '2026-09-16 12:17:43.352209', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (153, '2026-09-16 12:17:44.052478', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (154, '2026-09-16 12:17:44.781384', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (155, '2026-09-16 12:17:45.299248', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (156, '2026-09-16 12:17:45.788157', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (157, '2026-09-16 12:17:46.419647', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (158, '2026-09-16 12:17:47.705246', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.02", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.02', 8),
  (159, '2026-09-16 12:17:48.254545', 'UPDATE', 'GradeRecord', '4', '{"score": "0.02"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (160, '2026-09-16 12:17:50.310025', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (161, '2026-09-16 12:17:50.840638', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (162, '2026-09-16 12:17:51.576265', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (163, '2026-09-16 12:17:52.257230', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (164, '2026-09-16 12:17:52.758854', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (165, '2026-09-16 12:17:53.273325', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (166, '2026-09-16 12:18:06.988818', 'UPDATE', 'GradeRecord', '4', '{"score": "0.01"}', '{"score": "0.08", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.08', 8),
  (167, '2026-09-16 12:18:19.067184', 'UPDATE', 'GradeRecord', '4', '{"score": "0.08"}', '{"score": "0.40", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Evaluaciones y Quices (ESP-01): 0.40', 8),
  (168, '2026-09-16 12:18:32.052404', 'INSERT', 'GradeRecord', '5', '{"score": null}', '{"score": "0.01", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Talleres y Actividades (ESP-01): 0.01', 8),
  (169, '2026-09-16 12:18:33.814299', 'UPDATE', 'GradeRecord', '5', '{"score": "0.01"}', '{"score": "0.17", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Talleres y Actividades (ESP-01): 0.17', 8),
  (170, '2026-09-16 12:18:37.611767', 'UPDATE', 'GradeRecord', '5', '{"score": "0.17"}', '{"score": "0.45", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Talleres y Actividades (ESP-01): 0.45', 8),
  (171, '2026-09-16 12:18:46.294215', 'INSERT', 'GradeRecord', '6', '{"score": null}', '{"score": "0.51", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_1245678980 en Actitudinal y Autoevaluación (ESP-01): 0.51', 8),
  (172, '2026-09-16 12:23:19.529561', 'FAILED_LOGIN', 'CustomUser', NULL, NULL, '{"attempted_username": "Ana@gmail.com"}', '10.8.182.30', 'Intento fallido de autenticación para usuario: Ana@gmail.com', NULL),
  (173, '2026-09-16 12:23:30.481989', 'LOGIN', 'CustomUser', '15', NULL, NULL, '10.8.182.30', 'Inicio de sesión exitoso en la plataforma', 15),
  (174, '2026-09-16 12:23:37.887508', 'INSERT', 'Enrollment', '5', NULL, '{"student": "Alanna Acosta", "code": "236745", "section": "7-A", "year": 2026, "status": "ACTIVE"}', '10.8.182.62', 'Matrícula de estudiante est_12214537245 en curso 7-A (2026)', 10),
  (175, '2026-09-16 12:23:37.889558', 'CREATE_STUDENT', 'StudentProfile', '5', NULL, '{"username": "est_12214537245", "student_code": "236745", "section": "7-A"}', '10.8.182.62', 'Registro de nuevo alumno por nurys', 10),
  (176, '2026-09-16 12:25:43.693683', 'INSERT', 'GradeRecord', '7', '{"score": null}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Evaluaciones y Quices (ESP-01): 0.01', 8),
  (177, '2026-09-16 12:25:47.824158', 'UPDATE', 'GradeRecord', '7', '{"score": "0.01"}', '{"score": "0.60", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Evaluaciones y Quices (ESP-01): 0.60', 8),
  (178, '2026-09-16 12:25:50.480730', 'UPDATE', 'GradeRecord', '7', '{"score": "0.60"}', '{"score": "0.17", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Evaluaciones y Quices (ESP-01): 0.17', 8),
  (179, '2026-09-16 12:25:51.758239', 'UPDATE', 'GradeRecord', '7', '{"score": "0.17"}', '{"score": "0.15", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Evaluaciones y Quices (ESP-01): 0.15', 8),
  (180, '2026-09-16 12:25:54.972948', 'UPDATE', 'GradeRecord', '7', '{"score": "0.15"}', '{"score": "0.51", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Evaluaciones y Quices (ESP-01): 0.51', 8),
  (181, '2026-09-16 12:26:04.510176', 'INSERT', 'GradeRecord', '8', '{"score": null}', '{"score": "0.58", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Talleres y Actividades (ESP-01): 0.58', 8),
  (182, '2026-09-16 12:26:12.174703', 'INSERT', 'GradeRecord', '9', '{"score": null}', '{"score": "0.53", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Actitudinal y Autoevaluación (ESP-01): 0.53', 8),
  (183, '2026-09-16 12:26:37.277662', 'UPDATE', 'GradeRecord', '9', '{"score": "0.53"}', '{"score": "3.15", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_12214537245 en Actitudinal y Autoevaluación (ESP-01): 3.15', 8),
  (184, '2026-09-16 12:31:52.992292', 'UPDATE', 'AttendanceSession', '6', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.41', 'Marcado masivo de presentes en grupo 7-A para Lengua Castellana', 8),
  (185, '2026-09-16 12:31:54.454482', 'UPDATE', 'AttendanceSession', '6', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.41', 'Marcado masivo de presentes en grupo 7-A para Lengua Castellana', 8),
  (186, '2026-09-16 12:33:02.931429', 'INSERT', 'HomeworkSubmission', '2', NULL, '{"student": "yesi", "homework": "Taller #1: Operaciones con Conjuntos", "status": "SUBMITTED"}', '10.8.182.62', 'Entrega de tarea Taller #1: Operaciones con Conjuntos por yesi', 9),
  (187, '2026-09-16 12:34:58.117707', 'INSERT', 'TeachingAssignment', '4', NULL, '{"teacher": "Dulce Docente", "section": "6-A", "subject": "Geometr\\u00eda y Estad\\u00edstica", "year": 2026}', '10.8.182.62', 'Asignación académica de Geometría y Estadística en 6-A a dulce', 10),
  (188, '2026-09-16 12:37:09.484099', 'INSERT', 'HomeworkSubmission', '3', NULL, '{"student": "yesi", "homework": "Evaluaci\\u00f3n escrita", "status": "SUBMITTED"}', '10.8.182.62', 'Entrega de tarea Evaluación escrita por yesi', 9),
  (189, '2026-09-16 12:38:05.102258', 'UPDATE', 'HomeworkSubmission', '3', NULL, '{"score": "4.54", "feedback": "Bien", "status": "GRADED"}', '10.8.182.41', 'Calificación de tarea Evaluación escrita para yesi: 4.54', 8),
  (190, '2026-09-16 12:41:04.290281', 'INSERT', 'GradeRecord', '10', '{"score": null}', '{"score": "2.62", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Evaluaciones y Quices (GEO-01): 2.62', 8),
  (191, '2026-09-16 12:41:24.258884', 'INSERT', 'GradeRecord', '11', '{"score": null}', '{"score": "3.32", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Talleres y Actividades (GEO-01): 3.32', 8),
  (192, '2026-09-16 12:41:49.004357', 'INSERT', 'GradeRecord', '12', '{"score": null}', '{"score": "2.76", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Actitudinal y Autoevaluación (GEO-01): 2.76', 8),
  (193, '2026-09-16 12:41:54.699539', 'UPDATE', 'GradeRecord', '12', '{"score": "2.76"}', '{"score": "0.80", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Actitudinal y Autoevaluación (GEO-01): 0.80', 8),
  (194, '2026-09-16 12:42:03.209231', 'UPDATE', 'GradeRecord', '12', '{"score": "0.80"}', '{"score": "0.64", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Actitudinal y Autoevaluación (GEO-01): 0.64', 8),
  (195, '2026-09-16 12:42:25.440579', 'UPDATE', 'GradeRecord', '12', '{"score": "0.64"}', '{"score": "4.21", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para est_1221467456 en Actitudinal y Autoevaluación (GEO-01): 4.21', 8),
  (196, '2026-09-16 12:42:31.974780', 'INSERT', 'GradeRecord', '13', '{"score": null}', '{"score": "0.01", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para yesi en Evaluaciones y Quices (GEO-01): 0.01', 8),
  (197, '2026-09-16 12:42:42.821648', 'UPDATE', 'GradeRecord', '13', '{"score": "0.01"}', '{"score": "1.82", "criterion": "Evaluaciones y Quices"}', '10.8.182.41', 'Calificación registrada para yesi en Evaluaciones y Quices (GEO-01): 1.82', 8),
  (198, '2026-09-16 12:42:56.967063', 'INSERT', 'GradeRecord', '14', '{"score": null}', '{"score": "2.28", "criterion": "Talleres y Actividades"}', '10.8.182.41', 'Calificación registrada para yesi en Talleres y Actividades (GEO-01): 2.28', 8),
  (199, '2026-09-16 12:43:15.447215', 'INSERT', 'GradeRecord', '15', '{"score": null}', '{"score": "2.48", "criterion": "Actitudinal y Autoevaluaci\\u00f3n"}', '10.8.182.41', 'Calificación registrada para yesi en Actitudinal y Autoevaluación (GEO-01): 2.48', 8),
  (200, '2026-09-16 12:45:36.897069', 'UPDATE', 'AcademicPeriod', '1', '{"status": "ACTIVE"}', '{"status": "CLOSED"}', '127.0.0.1', 'Cierre formal del periodo Periodo 1 (2026): Cierre formal de periodo lectivo', 13),
  (201, '2026-09-16 12:46:02.767597', 'UPDATE', 'AcademicPeriod', '2', '{"status": "CLOSED"}', '{"status": "ACTIVE"}', '127.0.0.1', 'REAPERTURA EXTRAORDINARIA del periodo Periodo 2: Nuevo periodo', 13),
  (202, '2026-09-16 13:01:27.702690', 'UPDATE', 'AttendanceSession', '8', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.41', 'Marcado masivo de presentes en grupo 6-A para Geometría y Estadística', 8),
  (203, '2026-09-16 13:03:54.220656', 'UPDATE', 'AttendanceSession', '8', NULL, '{"bulk_action": "ALL_PRESENT"}', '10.8.182.41', 'Marcado masivo de presentes en grupo 6-A para Geometría y Estadística', 8),
  (204, '2026-09-16 13:50:16.384286', 'LOGOUT', 'CustomUser', '13', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 13),
  (205, '2026-09-16 14:42:05.713472', 'LOGOUT', 'CustomUser', '12', NULL, NULL, '10.8.182.62', 'Cierre de sesión manual voluntario', 12),
  (206, '2026-09-16 14:42:14.040272', 'LOGIN', 'CustomUser', '12', NULL, NULL, '10.8.182.62', 'Inicio de sesión exitoso en la plataforma', 12),
  (207, '2026-09-16 14:43:01.699016', 'LOGOUT', 'CustomUser', '15', NULL, NULL, '10.8.182.30', 'Cierre de sesión manual voluntario', 15),
  (208, '2026-09-16 14:43:09.884334', 'LOGIN', 'CustomUser', '12', NULL, NULL, '10.8.182.30', 'Inicio de sesión exitoso en la plataforma', 12),
  (209, '2026-09-16 14:44:08.666734', 'INSERT', 'CourseSection', '4', NULL, '{"name": "8-C", "year": 2026, "grade": "Octavo", "capacity": 35}', '10.8.182.30', 'Creación de sección académica 8-C', 12),
  (210, '2026-09-16 14:44:34.453275', 'UPDATE', 'AcademicPeriod', '1', '{"status": "CLOSED"}', '{"status": "ACTIVE"}', '10.8.182.30', 'Apertura operativa de periodo', 12),
  (211, '2026-09-16 14:44:38.254309', 'PERIOD_CLOSE', 'AcademicPeriod', '2', '{"status": "ACTIVE"}', '{"status": "CLOSED"}', '10.8.182.30', 'Cierre de periodo académico', 12),
  (212, '2026-09-16 14:44:57.223696', 'INSERT', 'TeachingAssignment', '5', NULL, '{"teacher": "Dulce Docente", "section": "8-C", "subject": "Ingl\\u00e9s Comunicativo", "year": 2026}', '10.8.182.30', 'Asignación académica de Inglés Comunicativo en 8-C a dulce', 12),
  (213, '2026-09-16 14:47:17.962479', 'LOGIN', 'CustomUser', '13', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 13),
  (214, '2026-09-16 15:46:35.276502', 'LOGOUT', 'CustomUser', '13', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 13),
  (215, '2026-09-16 15:46:54.154820', 'LOGIN', 'CustomUser', '8', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 8),
  (216, '2026-09-16 15:47:53.690409', 'LOGOUT', 'CustomUser', '8', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 8),
  (217, '2026-09-16 15:48:06.853262', 'LOGIN', 'CustomUser', '10', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 10),
  (218, '2026-09-16 15:49:58.351818', 'CREATE_TEACHER', 'TeacherProfile', '3', NULL, '{"username": "doc_1234534234", "specialty": "Fisica"}', '127.0.0.1', 'Registro de nuevo docente por nurys', 10),
  (219, '2026-09-16 15:50:24.188399', 'INSERT', 'TeachingAssignment', '6', NULL, '{"teacher": "Claudia gomez", "section": "6-A", "subject": "F\\u00edsica Elemental", "year": 2026}', '127.0.0.1', 'Asignación académica de Física Elemental en 6-A a doc_1234534234', 10),
  (220, '2026-09-16 15:51:14.507099', 'INSERT', 'TeachingAssignment', '7', NULL, '{"teacher": "Claudia gomez", "section": "6-B", "subject": "Lengua Castellana", "year": 2026}', '127.0.0.1', 'Asignación académica de Lengua Castellana en 6-B a doc_1234534234', 10),
  (221, '2026-09-16 15:52:52.416107', 'INSERT', 'Enrollment', '6', NULL, '{"student": "Andres Cantillo", "code": "234567", "section": "6-B", "year": 2026, "status": "ACTIVE"}', '127.0.0.1', 'Matrícula de estudiante est_1223454323 en curso 6-B (2026)', 10),
  (222, '2026-09-16 15:52:52.419709', 'CREATE_STUDENT', 'StudentProfile', '6', NULL, '{"username": "est_1223454323", "student_code": "234567", "section": "6-B"}', '127.0.0.1', 'Registro de nuevo alumno por nurys', 10),
  (223, '2026-09-16 15:53:14.442990', 'LOGOUT', 'CustomUser', '10', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 10),
  (224, '2026-09-16 15:53:25.619244', 'LOGIN', 'CustomUser', '8', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 8),
  (225, '2026-09-16 15:54:28.508461', 'INSERT', 'Homework', '4', NULL, '{"title": "trabajo de la oracion", "section": "6-A", "subject": "ESP-01"}', '127.0.0.1', 'Asignación de tarea: trabajo de la oracion para grupo 6-A', 8),
  (226, '2026-09-16 15:54:41.496615', 'LOGOUT', 'CustomUser', '8', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 8),
  (227, '2026-09-16 15:54:53.278723', 'LOGIN', 'CustomUser', '9', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 9),
  (228, '2026-09-16 15:55:22.688766', 'INSERT', 'HomeworkSubmission', '4', NULL, '{"student": "yesi", "homework": "trabajo de la oracion", "status": "SUBMITTED"}', '127.0.0.1', 'Entrega de tarea trabajo de la oracion por yesi', 9),
  (229, '2026-09-16 15:55:38.168833', 'LOGOUT', 'CustomUser', '9', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 9),
  (230, '2026-09-16 15:55:50.479685', 'LOGIN', 'CustomUser', '8', NULL, NULL, '127.0.0.1', 'Inicio de sesión exitoso en la plataforma', 8),
  (231, '2026-09-16 15:57:24.228869', 'UPDATE', 'HomeworkSubmission', '4', NULL, '{"score": "1.00", "feedback": "", "status": "GRADED"}', '127.0.0.1', 'Calificación de tarea trabajo de la oracion para yesi: 1.00', 8),
  (232, '2026-09-16 16:31:52.610439', 'LOGOUT', 'CustomUser', '12', NULL, NULL, '127.0.0.1', 'Cierre de sesión manual voluntario', 12);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `auth_group`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `auth_group` (6 registros)
INSERT INTO `auth_group` (`id`, `name`) VALUES
  (1, 'Administradores'),
  (2, 'Directivos Rectores'),
  (3, 'Secretaría Académica'),
  (4, 'Docentes'),
  (5, 'Estudiantes'),
  (6, 'Padres y Acudientes');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `auth_group_permissions`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `group_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_auth_group_permissions_permission_id` (`permission_id`),
  CONSTRAINT `fk_auth_group_permissions_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  KEY `idx_auth_group_permissions_group_id` (`group_id`),
  CONSTRAINT `fk_auth_group_permissions_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `auth_permission`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content_type_id` INT NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_auth_permission_content_type_id` (`content_type_id`),
  CONSTRAINT `fk_auth_permission_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `auth_permission` (120 registros)
INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
  (1, 1, 'add_logentry', 'Can add log entry'),
  (2, 1, 'change_logentry', 'Can change log entry'),
  (3, 1, 'delete_logentry', 'Can delete log entry'),
  (4, 1, 'view_logentry', 'Can view log entry'),
  (5, 2, 'add_permission', 'Can add permission'),
  (6, 2, 'change_permission', 'Can change permission'),
  (7, 2, 'delete_permission', 'Can delete permission'),
  (8, 2, 'view_permission', 'Can view permission'),
  (9, 3, 'add_group', 'Can add group'),
  (10, 3, 'change_group', 'Can change group'),
  (11, 3, 'delete_group', 'Can delete group'),
  (12, 3, 'view_group', 'Can view group'),
  (13, 4, 'add_contenttype', 'Can add content type'),
  (14, 4, 'change_contenttype', 'Can change content type'),
  (15, 4, 'delete_contenttype', 'Can delete content type'),
  (16, 4, 'view_contenttype', 'Can view content type'),
  (17, 5, 'add_session', 'Can add session'),
  (18, 5, 'change_session', 'Can change session'),
  (19, 5, 'delete_session', 'Can delete session'),
  (20, 5, 'view_session', 'Can view session'),
  (21, 6, 'add_customuser', 'Can add Usuario Institucional'),
  (22, 6, 'change_customuser', 'Can change Usuario Institucional'),
  (23, 6, 'delete_customuser', 'Can delete Usuario Institucional'),
  (24, 6, 'view_customuser', 'Can view Usuario Institucional'),
  (25, 7, 'add_auditlog', 'Can add Registro de Auditoría'),
  (26, 7, 'change_auditlog', 'Can change Registro de Auditoría'),
  (27, 7, 'delete_auditlog', 'Can delete Registro de Auditoría'),
  (28, 7, 'view_auditlog', 'Can view Registro de Auditoría'),
  (29, 8, 'add_systemalert', 'Can add Alerta del Sistema'),
  (30, 8, 'change_systemalert', 'Can change Alerta del Sistema'),
  (31, 8, 'delete_systemalert', 'Can delete Alerta del Sistema'),
  (32, 8, 'view_systemalert', 'Can view Alerta del Sistema'),
  (33, 9, 'add_coursesection', 'Can add Curso / Grupo'),
  (34, 9, 'change_coursesection', 'Can change Curso / Grupo'),
  (35, 9, 'delete_coursesection', 'Can delete Curso / Grupo'),
  (36, 9, 'view_coursesection', 'Can view Curso / Grupo'),
  (37, 10, 'add_academicyear', 'Can add Año Lectivo'),
  (38, 10, 'change_academicyear', 'Can change Año Lectivo'),
  (39, 10, 'delete_academicyear', 'Can delete Año Lectivo'),
  (40, 10, 'view_academicyear', 'Can view Año Lectivo'),
  (41, 11, 'add_gradelevel', 'Can add Grado Escolar'),
  (42, 11, 'change_gradelevel', 'Can change Grado Escolar'),
  (43, 11, 'delete_gradelevel', 'Can delete Grado Escolar'),
  (44, 11, 'view_gradelevel', 'Can view Grado Escolar'),
  (45, 12, 'add_gradesubject', 'Can add Asignatura en Malla Curricular'),
  (46, 12, 'change_gradesubject', 'Can change Asignatura en Malla Curricular'),
  (47, 12, 'delete_gradesubject', 'Can delete Asignatura en Malla Curricular'),
  (48, 12, 'view_gradesubject', 'Can view Asignatura en Malla Curricular'),
  (49, 13, 'add_subject', 'Can add Asignatura'),
  (50, 13, 'change_subject', 'Can change Asignatura'),
  (51, 13, 'delete_subject', 'Can delete Asignatura'),
  (52, 13, 'view_subject', 'Can view Asignatura'),
  (53, 14, 'add_knowledgearea', 'Can add Área de Conocimiento'),
  (54, 14, 'change_knowledgearea', 'Can change Área de Conocimiento'),
  (55, 14, 'delete_knowledgearea', 'Can delete Área de Conocimiento'),
  (56, 14, 'view_knowledgearea', 'Can view Área de Conocimiento'),
  (57, 15, 'add_academicperiod', 'Can add Periodo Académico'),
  (58, 15, 'change_academicperiod', 'Can change Periodo Académico'),
  (59, 15, 'delete_academicperiod', 'Can delete Periodo Académico'),
  (60, 15, 'view_academicperiod', 'Can view Periodo Académico'),
  (61, 16, 'add_teacherprofile', 'Can add Perfil Docente'),
  (62, 16, 'change_teacherprofile', 'Can change Perfil Docente'),
  (63, 16, 'delete_teacherprofile', 'Can delete Perfil Docente'),
  (64, 16, 'view_teacherprofile', 'Can view Perfil Docente'),
  (65, 17, 'add_teachingassignment', 'Can add Asignación Académica'),
  (66, 17, 'change_teachingassignment', 'Can change Asignación Académica'),
  (67, 17, 'delete_teachingassignment', 'Can delete Asignación Académica'),
  (68, 17, 'view_teachingassignment', 'Can view Asignación Académica'),
  (69, 18, 'add_enrollment', 'Can add Matrícula Escolar'),
  (70, 18, 'change_enrollment', 'Can change Matrícula Escolar'),
  (71, 18, 'delete_enrollment', 'Can delete Matrícula Escolar'),
  (72, 18, 'view_enrollment', 'Can view Matrícula Escolar'),
  (73, 19, 'add_studentprofile', 'Can add Expediente Estudiantil'),
  (74, 19, 'change_studentprofile', 'Can change Expediente Estudiantil'),
  (75, 19, 'delete_studentprofile', 'Can delete Expediente Estudiantil'),
  (76, 19, 'view_studentprofile', 'Can view Expediente Estudiantil'),
  (77, 20, 'add_attendancesession', 'Can add Sesión de Asistencia'),
  (78, 20, 'change_attendancesession', 'Can change Sesión de Asistencia'),
  (79, 20, 'delete_attendancesession', 'Can delete Sesión de Asistencia'),
  (80, 20, 'view_attendancesession', 'Can view Sesión de Asistencia'),
  (81, 21, 'add_attendancerecord', 'Can add Registro de Asistencia'),
  (82, 21, 'change_attendancerecord', 'Can change Registro de Asistencia'),
  (83, 21, 'delete_attendancerecord', 'Can delete Registro de Asistencia'),
  (84, 21, 'view_attendancerecord', 'Can view Registro de Asistencia'),
  (85, 22, 'add_graderecord', 'Can add Calificación'),
  (86, 22, 'change_graderecord', 'Can change Calificación'),
  (87, 22, 'delete_graderecord', 'Can delete Calificación'),
  (88, 22, 'view_graderecord', 'Can view Calificación'),
  (89, 23, 'add_periodfinalgrade', 'Can add Nota Definitiva de Periodo'),
  (90, 23, 'change_periodfinalgrade', 'Can change Nota Definitiva de Periodo'),
  (91, 23, 'delete_periodfinalgrade', 'Can delete Nota Definitiva de Periodo'),
  (92, 23, 'view_periodfinalgrade', 'Can view Nota Definitiva de Periodo'),
  (93, 24, 'add_evaluationcriterion', 'Can add Criterio de Evaluación'),
  (94, 24, 'change_evaluationcriterion', 'Can change Criterio de Evaluación'),
  (95, 24, 'delete_evaluationcriterion', 'Can delete Criterio de Evaluación'),
  (96, 24, 'view_evaluationcriterion', 'Can view Criterio de Evaluación'),
  (97, 25, 'add_homeworksubmission', 'Can add Entrega de Tarea'),
  (98, 25, 'change_homeworksubmission', 'Can change Entrega de Tarea'),
  (99, 25, 'delete_homeworksubmission', 'Can delete Entrega de Tarea'),
  (100, 25, 'view_homeworksubmission', 'Can view Entrega de Tarea'),
  (101, 26, 'add_homework', 'Can add Tarea Escolar'),
  (102, 26, 'change_homework', 'Can change Tarea Escolar'),
  (103, 26, 'delete_homework', 'Can delete Tarea Escolar'),
  (104, 26, 'view_homework', 'Can view Tarea Escolar'),
  (105, 27, 'add_academicclosinglog', 'Can add Bitácora de Cierre Académico'),
  (106, 27, 'change_academicclosinglog', 'Can change Bitácora de Cierre Académico'),
  (107, 27, 'delete_academicclosinglog', 'Can delete Bitácora de Cierre Académico'),
  (108, 27, 'view_academicclosinglog', 'Can view Bitácora de Cierre Académico'),
  (109, 28, 'add_annualfinalgrade', 'Can add Definitiva Anual'),
  (110, 28, 'change_annualfinalgrade', 'Can change Definitiva Anual'),
  (111, 28, 'delete_annualfinalgrade', 'Can delete Definitiva Anual'),
  (112, 28, 'view_annualfinalgrade', 'Can view Definitiva Anual'),
  (113, 29, 'add_promotionrule', 'Can add Regla de Promoción'),
  (114, 29, 'change_promotionrule', 'Can change Regla de Promoción'),
  (115, 29, 'delete_promotionrule', 'Can delete Regla de Promoción'),
  (116, 29, 'view_promotionrule', 'Can view Regla de Promoción'),
  (117, 30, 'add_institutionalactivity', 'Can add Actividad Institucional'),
  (118, 30, 'change_institutionalactivity', 'Can change Actividad Institucional'),
  (119, 30, 'delete_institutionalactivity', 'Can delete Actividad Institucional'),
  (120, 30, 'view_institutionalactivity', 'Can view Actividad Institucional');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `courses_academicyear`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `courses_academicyear`;
CREATE TABLE `courses_academicyear` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `year` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `status` VARCHAR(15) NOT NULL,
  `is_current` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `courses_academicyear` (1 registros)
INSERT INTO `courses_academicyear` (`id`, `year`, `name`, `start_date`, `end_date`, `status`, `is_current`, `created_at`) VALUES
  (1, 2026, 'Año Escolar 2026', '2026-01-15', '2026-11-28', 'ACTIVE', 1, '2026-09-15 02:03:45.321234');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `courses_coursesection`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `courses_coursesection`;
CREATE TABLE `courses_coursesection` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(25) NOT NULL,
  `classroom` VARCHAR(50) DEFAULT NULL,
  `capacity` INT NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  `homeroom_teacher_id` BIGINT DEFAULT NULL,
  `grade_level_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_courses_coursesection_grade_level_id` (`grade_level_id`),
  CONSTRAINT `fk_courses_coursesection_grade_level_id` FOREIGN KEY (`grade_level_id`) REFERENCES `courses_gradelevel` (`id`),
  KEY `idx_courses_coursesection_homeroom_teacher_id` (`homeroom_teacher_id`),
  CONSTRAINT `fk_courses_coursesection_homeroom_teacher_id` FOREIGN KEY (`homeroom_teacher_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_courses_coursesection_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_courses_coursesection_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `courses_coursesection` (4 registros)
INSERT INTO `courses_coursesection` (`id`, `name`, `classroom`, `capacity`, `is_active`, `academic_year_id`, `homeroom_teacher_id`, `grade_level_id`) VALUES
  (1, '6-A', 'Aula 101', 35, 1, 1, 4, 1),
  (2, '6-B', 'Aula 102', 35, 1, 1, NULL, 1),
  (3, '7-A', '2', 35, 1, 1, 4, 2),
  (4, '8-C', 'Aula 200', 35, 1, 1, 8, 3);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `courses_gradelevel`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `courses_gradelevel`;
CREATE TABLE `courses_gradelevel` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `code` VARCHAR(10) NOT NULL,
  `level_stage` VARCHAR(20) NOT NULL,
  `order` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `courses_gradelevel` (6 registros)
INSERT INTO `courses_gradelevel` (`id`, `name`, `code`, `level_stage`, `order`) VALUES
  (1, 'Sexto', '06', 'SECUNDARIA', 6),
  (2, 'Séptimo', '07', 'SECUNDARIA', 7),
  (3, 'Octavo', '08', 'SECUNDARIA', 8),
  (4, 'Noveno', '09', 'SECUNDARIA', 9),
  (5, 'Décimo', '10', 'MEDIA', 10),
  (6, 'Once', '11', 'MEDIA', 11);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `django_admin_log`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `object_id` INT DEFAULT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` INT NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT DEFAULT NULL,
  `user_id` BIGINT NOT NULL,
  `action_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_django_admin_log_user_id` (`user_id`),
  CONSTRAINT `fk_django_admin_log_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_django_admin_log_content_type_id` (`content_type_id`),
  CONSTRAINT `fk_django_admin_log_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `django_admin_log` (4 registros)
INSERT INTO `django_admin_log` (`id`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`, `action_time`) VALUES
  (4, '13', 'yurleidilondono@gmail.com (Directivo / Rector)', 1, '[{"added": {}}]', 6, 12, '2026-09-16 12:11:22.614756'),
  (5, '13', 'Yurleidi Londoño (Directivo / Rector)', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address", "Groups", "User permissions", "Last login", "Date joined"]}}]', 6, 12, '2026-09-16 12:14:04.211797'),
  (6, '15', 'Ana@gmail.com (Padre de Familia / Acudiente)', 1, '[{"added": {}}]', 6, 12, '2026-09-16 12:20:25.495973'),
  (7, '15', 'Ana Retamozo (Padre de Familia / Acudiente)', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address", "Groups", "User permissions", "Last login", "Date joined"]}}]', 6, 12, '2026-09-16 12:22:55.219185');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `django_content_type`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `django_content_type` (30 registros)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
  (1, 'admin', 'logentry'),
  (2, 'auth', 'permission'),
  (3, 'auth', 'group'),
  (4, 'contenttypes', 'contenttype'),
  (5, 'sessions', 'session'),
  (6, 'accounts', 'customuser'),
  (7, 'audit', 'auditlog'),
  (8, 'alerts', 'systemalert'),
  (9, 'courses', 'coursesection'),
  (10, 'courses', 'academicyear'),
  (11, 'courses', 'gradelevel'),
  (12, 'subjects', 'gradesubject'),
  (13, 'subjects', 'subject'),
  (14, 'subjects', 'knowledgearea'),
  (15, 'periods', 'academicperiod'),
  (16, 'teachers', 'teacherprofile'),
  (17, 'teachers', 'teachingassignment'),
  (18, 'students', 'enrollment'),
  (19, 'students', 'studentprofile'),
  (20, 'attendance', 'attendancesession'),
  (21, 'attendance', 'attendancerecord'),
  (22, 'grades', 'graderecord'),
  (23, 'grades', 'periodfinalgrade'),
  (24, 'grades', 'evaluationcriterion'),
  (25, 'homework', 'homeworksubmission'),
  (26, 'homework', 'homework'),
  (27, 'rules', 'academicclosinglog'),
  (28, 'rules', 'annualfinalgrade'),
  (29, 'rules', 'promotionrule'),
  (30, 'alerts', 'institutionalactivity');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `django_migrations`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `django_migrations` (33 registros)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
  (1, 'contenttypes', '0001_initial', '2026-09-15 01:36:35.064034'),
  (2, 'contenttypes', '0002_remove_content_type_name', '2026-09-15 01:36:35.071158'),
  (3, 'auth', '0001_initial', '2026-09-15 01:36:35.092773'),
  (4, 'auth', '0002_alter_permission_name_max_length', '2026-09-15 01:36:35.107599'),
  (5, 'auth', '0003_alter_user_email_max_length', '2026-09-15 01:36:35.115807'),
  (6, 'auth', '0004_alter_user_username_opts', '2026-09-15 01:36:35.125892'),
  (7, 'auth', '0005_alter_user_last_login_null', '2026-09-15 01:36:35.137065'),
  (8, 'auth', '0006_require_contenttypes_0002', '2026-09-15 01:36:35.145543'),
  (9, 'auth', '0007_alter_validators_add_error_messages', '2026-09-15 01:36:35.155073'),
  (10, 'auth', '0008_alter_user_username_max_length', '2026-09-15 01:36:35.163722'),
  (11, 'auth', '0009_alter_user_last_name_max_length', '2026-09-15 01:36:35.173461'),
  (12, 'auth', '0010_alter_group_name_max_length', '2026-09-15 01:36:35.185342'),
  (13, 'auth', '0011_update_proxy_permissions', '2026-09-15 01:36:35.194176'),
  (14, 'auth', '0012_alter_user_first_name_max_length', '2026-09-15 01:36:35.203979'),
  (15, 'accounts', '0001_initial', '2026-09-15 01:36:35.224848'),
  (16, 'admin', '0001_initial', '2026-09-15 01:36:35.242891'),
  (17, 'admin', '0002_logentry_remove_auto_add', '2026-09-15 01:36:35.260379'),
  (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-09-15 01:36:35.271811'),
  (19, 'alerts', '0001_initial', '2026-09-15 01:36:35.291935'),
  (20, 'audit', '0001_initial', '2026-09-15 01:36:35.311899'),
  (21, 'sessions', '0001_initial', '2026-09-15 01:36:35.329604'),
  (22, 'courses', '0001_initial', '2026-09-15 02:02:46.300829'),
  (23, 'periods', '0001_initial', '2026-09-15 02:02:46.322056'),
  (24, 'students', '0001_initial', '2026-09-15 02:02:46.340147'),
  (25, 'subjects', '0001_initial', '2026-09-15 02:02:46.372722'),
  (26, 'teachers', '0001_initial', '2026-09-15 02:02:46.406116'),
  (27, 'attendance', '0001_initial', '2026-09-15 02:18:39.076123'),
  (28, 'grades', '0001_initial', '2026-09-15 02:37:03.725017'),
  (29, 'homework', '0001_initial', '2026-09-15 02:37:03.776769'),
  (30, 'rules', '0001_initial', '2026-09-15 02:54:01.939197'),
  (31, 'alerts', '0002_institutionalactivity', '2026-09-16 00:54:47.190109'),
  (32, 'grades', '0002_alter_graderecord_score', '2026-09-16 00:57:08.506176'),
  (33, 'homework', '0002_alter_homeworksubmission_score', '2026-09-16 00:58:38.948416');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `django_session`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `django_session` (34 registros)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
  ('hd71cbcgyqu6kq8txo7h4i41gm0sv307', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IKp:wYKueBOcT0w0M3n49AWkPYlMPRGQCeYL-8rggnUJG_Q', '2026-09-29 01:51:47.404676'),
  ('yn8lcp59htqf58ffh69xpmleos0xf4ix', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IZl:mjZVXjurhvPP8PHYFdnsFW2x819Ec47RDiq3kCxG2rw', '2026-09-29 02:07:13.741636'),
  ('e6sljexlwr9hzyttm2nnymgp6nvs70zo', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6Idf:BHS1YocRir0wlGZs33gE0y9KwQPXOxOApDR8DrPcb6o', '2026-09-29 02:11:15.768938'),
  ('z95o59dkj1pxrvidxg5msflnx21afhid', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IeO:AAtdU7_Jil11zTLnlTmuf3vABfkocGESyxRq8mLRCTo', '2026-09-29 02:12:00.932477'),
  ('xmmk1ti51x6ub1sj61eoxtkev5cz6jeg', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IeY:xu7oNK0nTGzaxQq3KlQJr6zA5XNP3SRo-8r735jdkOs', '2026-09-29 02:12:10.646788'),
  ('n11ph2ppx04lv6shjikl1vhpsac8svgz', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6Iek:zNzlEcFCfp8WsYSZa2f2RvJlCIRQvL4-2zVIJ_X_dOw', '2026-09-29 02:12:22.865113'),
  ('9sfmfyves2rdwojrufp3w56lcq1tlh0r', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IgZ:ZD_hyncoj53oP5c9cfZyG-_dhD2cy9Qm4qYrUM1fWSE', '2026-09-29 02:14:15.636333'),
  ('ztdvc3wajbqrp9u7pz2xwp9dumedvx2u', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IhL:884HwYeqekPI2f3N2AyOhPp5Xoujs5jsqtJq96aFGcY', '2026-09-29 02:15:03.723499'),
  ('vhat8wjmszll6v2rxgq01dwdng1m38jl', '.eJxVjEEOwiAQRe_C2hAKTEGX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERgzj9bhHpkeoO-I711iS1ui5zlLsiD9rl1Dg9r4f7d1Cwl29tFXkFo8-ULBA77TMYtppH1NqZs8mGwfiBkSMplR2B1-AUeGK2EcT7A9WXN6U:1x6IhW:m8-fH-EInZ8Yo0wvLn0BJGsAsvHE7kqswTDj27kLuPY', '2026-09-29 02:15:14.669376'),
  ('rhj38w7ziryu7qbia8pf1ry3c4n446dk', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6Iqm:8BNSktXUJbTO0CRvxp-Ba7-o5hpSvzp9AE07w9Wtzf4', '2026-09-29 02:24:48.025993'),
  ('mi9w2ohoaaervcq77aywk48g6tabagjo', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6Iue:2zuOO0Scrys7gctGRjhdH5K5451nzGYNtVxLRdXAWEI', '2026-09-29 02:28:48.146706'),
  ('iszqcqf1477zu7ar17jfyywa051o67bs', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J5Q:_co0C9c0jvvYnxOLJxqRbDZyumiWnn1x0h9CiLeJUNw', '2026-09-29 02:39:56.371026'),
  ('9l6e47i5ooy6lduna1gj1o6wm635m7sh', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J5b:6opLDIwUNimDTrlUCsP6GT7XpazAgGSFaybsQwj2jiY', '2026-09-29 02:40:07.756104'),
  ('v85lj502cpqrvcsaae84qns22l8jt01t', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J5q:YKHc9BCJYcZeiYLG0qTM8qVcryutQSJEe8DwYQG18YM', '2026-09-29 02:40:22.910980'),
  ('rxog9i2bd538c1ov73qg3ghqua6k0j6z', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J60:yFfG8nqTz0wfq0drbxqrV3RdlER5rIBCcpCVHJmlcE8', '2026-09-29 02:40:32.844762'),
  ('see9x9tkzqeoxj41wgnomdg3rlefa0in', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J66:E9bmBaFc7aLS-qfUT2pz36L045j33dHSmknl-QxPLs4', '2026-09-29 02:40:38.979117'),
  ('dkl8dkiddkou9jni0w63lcwdtnbovr40', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J6D:BdpaYH-4Z0FECeeTOhHAyKEJzyZAyDQcxbsv-tBaW1c', '2026-09-29 02:40:45.628294'),
  ('ppd3sqs0j9nfk10brc1j4w4gadk3kibx', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J6b:kNU42yXkIvRbW7whQEgS7nOA9IpPlafoVSpw4QbuY7Q', '2026-09-29 02:41:09.053649'),
  ('g04bxra58c659mjqqddaa3qy6uk89szp', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6J6t:Sx1tcLoXxyWckethWJMBoT4U_WE4EyvYHnJ6XFnzVFE', '2026-09-29 02:41:27.048494'),
  ('b6cno7vi20gbo634afmej4k1yqilt2n6', '.eJxVjDsOwjAQBe_iGln-r01JnzNYtneNAyiR4qRC3J1ESgHtm5n3ZjFta4tbpyWOyK7MssvvllN50nQAfKTpPvMyT-syZn4o_KSdDzPS63a6fwct9bbXYHImX4lQoSropRUSjJDGO3CatK0aMsgdO1FC8AJBkCxKm2pNcMA-X-EENyQ:1x6J6t:5SRt5MUT0T9P4K3nfVb2LLlRuP9v8dwit8oz5nIZKWg', '2026-09-29 02:41:27.730592'),
  ('iiqy7ppmqb86ibf8ph58nwti6ezatc8q', '.eJxVjDsOwyAQBe9CHSH-CynT-wxoYXFwEmHJ2FWUu0dILpL2zcx7s4jHXuPRyxYXYlem2OV3S5ifpQ1AD2z3lee17duS-FD4STufViqv2-n-HVTsddTKZtTSegWUgwcTkvNWedSgZTGkQSQTrE7gZPZ6JmEcWDJBAGaaiX2-vNw3Jw:1x6JNn:0UhKzFM76bw-NgxzPGrmC6pl3tOA-jEu_-Fkt30emjg', '2026-09-29 02:58:55.547948'),
  ('pjxmaesvdcvf8euza99y5zubw9ryozbw', '.eJxVjDsOwjAQBe_iGln-r01JnzNYtneNAyiR4qRC3J1ESgHtm5n3ZjFta4tbpyWOyK7MssvvllN50nQAfKTpPvMyT-syZn4o_KSdDzPS63a6fwct9bbXYHImX4lQoSropRUSjJDGO3CatK0aMsgdO1FC8AJBkCxKm2pNcMA-X-EENyQ:1x6JNo:5mfeV3gsX8KyIxwFFVFO-_nE_u6x8REQqQxnKvAAalE', '2026-09-29 02:58:56.706888'),
  ('ho7gixqgnimn1avx2qwqrzdz1svkqmjy', '.eJxVjEEOwiAQRe_C2hBgoIBL956BDMNUqoYmpV0Z765NutDtf-_9l0i4rTVtnZc0FXEWVpx-t4z04LaDcsd2myXNbV2mLHdFHrTL61z4eTncv4OKvX5rb7k4xDFEZxwA-8ycGYKHMKgA3irM2o1FqxhCyXEgY0iRJm8sgfbi_QHiujd6:1x6JO0:5P52aqjN97eauBsCwQ1o0YYY65YhRdPJ1Jv6pingWTE', '2026-09-29 02:59:08.399105'),
  ('h8fuz6uwzxs8h22l7f3wwwh6uljyhu8h', '.eJxVjDsOwjAQBe_iGln-r01JnzNYtneNAyiR4qRC3J1ESgHtm5n3ZjFta4tbpyWOyK7MssvvllN50nQAfKTpPvMyT-syZn4o_KSdDzPS63a6fwct9bbXYHImX4lQoSropRUSjJDGO3CatK0aMsgdO1FC8AJBkCxKm2pNcMA-X-EENyQ:1x6JO1:ri3Np8nezTl5zC7804tDmt4jm5ngHXi7AKmexQO-AyE', '2026-09-29 02:59:09.632578'),
  ('7fc8onj9azvcaanyaup1rxr3gpngqzip', '.eJxVjDsOwjAQBe_iGlmWjWMvJT1niPZnHECJFCdVxN0hUgpo38y8zfS4LrVfm879IOZiwJx-N0J-6rgDeeB4nyxP4zIPZHfFHrTZ2yT6uh7u30HFVr-1Jpac2cfsUTuIUEJwzFo8InWskl3nYgheCBKj10RFCQo4dHIuYN4fCTk5Bg:1x6Te2:yADfNN8J4ZVUeCBJnoukbseAydZ498tRqpleHdDFU3g', '2026-09-29 13:56:22.976065'),
  ('zv8i1avnll2z03twluq441jblzwt04o3', '.eJxVjMEKwyAQRP_FcxE1umKPvfcbZN2VmrYoxOQU-u81kEPL3Oa9mV1E3NYSt56XOLO4Cq3E5bdMSK9cD8JPrI8mqdV1mZM8FHnSLu-N8_t2un8HBXsZ68QTWqBkmVUwI2BAk4HJJg8cgsLAKTAo6xiIVB6e984Bk0dtWXy-Aco4Bg:1x6TeH:rAE2scG9pAwGZakTs3uYNJiLPZx2IIEUhgXz9FDGcJQ', '2026-09-29 13:56:37.535824'),
  ('akwftiqdafsbx2x69z6lbh3fkfa79wen', '.eJxVjMsOwiAQRf-FtSE8WqAu3fsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mzCOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLayN-Xg7376BAL9-ajSejiY0N4PU0OiZATJ5ctoSDnSxogyoMTMGzUto7zmNOTiXWLnjx_gD5Pjg6:1x6TeI:5QqsHenRk8tdSgFmzkt9MzAQkM8ZTdcTBZhiNnqjKT8', '2026-09-29 13:56:38.380747'),
  ('gz9q356ovqdjp7osfd0c8f6cy9kdew6o', '.eJxVjM0OwiAQhN-FsyFQfpb16N1nICyLUjU0Ke3J-O62SQ-azGm-b-YtYlqXGtde5jiyOAsQp9-OUn6WtgN-pHafZJ7aMo8kd0UetMvrxOV1Ody_g5p63dbemGScUkYDIWtkpTRZZg9hUBDQaiiMnrMtW26EQ0CyLjNzcoFAfL7ANjez:1x6TgC:Oh4_Y3LNkDTi_dByOZVltkGc3T03wVYPWuKw6RrivyM', '2026-09-29 13:58:36.461724'),
  ('o3ypnb1cj607d7qzr8aahfpkjno5nhdj', '.eJxVjMsOwiAQRf-FtSE8WqAu3fsNZIYZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mzCOL0uyGkB9cd0B3qrcnU6rrMKHdFHrTLayN-Xg7376BAL9-ajSejiY0N4PU0OiZATJ5ctoSDnSxogyoMTMGzUto7zmNOTiXWLnjx_gD5Pjg6:1x6o9F:YJjC7Ud8vpf02a6C7qS2dzslQNhMeUABVtct0eZVFsE', '2026-09-30 11:49:57.244915'),
  ('ccc690443x3e8c3k6susmcyxfvpu9f88', '.eJxVjDsOwjAQBe_iGlmWjWMvJT1niPZnHECJFCdVxN0hUgpo38y8zfS4LrVfm879IOZiwJx-N0J-6rgDeeB4nyxP4zIPZHfFHrTZ2yT6uh7u30HFVr-1Jpac2cfsUTuIUEJwzFo8InWskl3nYgheCBKj10RFCQo4dHIuYN4fCTk5Bg:1x6oEK:pQSEegO3SznIl0S3T6cEwWkBB41f5xuDyEsAI8gvrm8', '2026-09-30 11:55:12.410361'),
  ('pqpfsn9ohj9cemixos2cf17elv35asqg', '.eJxVjDsOwjAQBe_iGlmb9Sc2JT1nsHbtDQkgR4qTCnF3iJQC2jcz76USbeuYtiZLmoo6qw7V6Xdkyg-pOyl3qrdZ57muy8R6V_RBm77ORZ6Xw_07GKmN3xp9jgF6MCLMiAUcWEYJPTjT9ZGRAtAQnSmesBvA5TAIIBhrDdvo1fsD5dk2_g:1x6olB:rX-l8q5WzHtOItn5iL6aCejkyK83xP5hxXLrTHLlLKQ', '2026-09-30 12:29:09.874840'),
  ('e8h149lxpkr9dnw98qdxh8zs2wdcrwn6', '.eJxVjDsOwjAQBe_iGlmb9Sc2JT1nsHbtDQkgR4qTCnF3iJQC2jcz76USbeuYtiZLmoo6qw7V6Xdkyg-pOyl3qrdZ57muy8R6V_RBm77ORZ6Xw_07GKmN3xp9jgF6MCLMiAUcWEYJPTjT9ZGRAtAQnSmesBvA5TAIIBhrDdvo1fsD5dk2_g:1x6qIi:T-g7BB9E4V4Gy6nGzV7qheSpTg0w0M4jOFINi4Nq4f8', '2026-09-30 14:07:52.898118'),
  ('pm8st5nmw79e6t8vodrh8xhhjh8piq1t', '.eJxVjDsOwjAQBe_iGlmb9Sc2JT1nsHbtDQkgR4qTCnF3iJQC2jcz76USbeuYtiZLmoo6qw7V6Xdkyg-pOyl3qrdZ57muy8R6V_RBm77ORZ6Xw_07GKmN3xp9jgF6MCLMiAUcWEYJPTjT9ZGRAtAQnSmesBvA5TAIIBhrDdvo1fsD5dk2_g:1x6qpy:aIR10O-U1sj_F4HqSxkSC9uZcjmvC-dpmQIULMoh_yk', '2026-09-30 14:42:14.054698'),
  ('xq9ahu5rgpusi4vaf798h49hufvxp7zk', '.eJxVjDsOwjAQBe_iGlmb9Sc2JT1nsHbtDQkgR4qTCnF3iJQC2jcz76USbeuYtiZLmoo6qw7V6Xdkyg-pOyl3qrdZ57muy8R6V_RBm77ORZ6Xw_07GKmN3xp9jgF6MCLMiAUcWEYJPTjT9ZGRAtAQnSmesBvA5TAIIBhrDdvo1fsD5dk2_g:1x6qqr:0URFHPEEcJllGbwidUTYHIDeV7CGXPpeFy6CuBfrDrw', '2026-09-30 14:43:09.892803');

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `grades_evaluationcriterion`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `grades_evaluationcriterion`;
CREATE TABLE `grades_evaluationcriterion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `percentage` DECIMAL(5,2) NOT NULL,
  `order` INT NOT NULL,
  `academic_period_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_grades_evaluationcriterion_subject_id` (`subject_id`),
  CONSTRAINT `fk_grades_evaluationcriterion_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_grades_evaluationcriterion_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_grades_evaluationcriterion_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_grades_evaluationcriterion_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_grades_evaluationcriterion_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `grades_evaluationcriterion` (21 registros)
INSERT INTO `grades_evaluationcriterion` (`id`, `name`, `percentage`, `order`, `academic_period_id`, `course_section_id`, `subject_id`) VALUES
  (1, 'Evaluaciones y Quices', 40, 1, 1, 1, 1),
  (2, 'Talleres y Actividades', 40, 2, 1, 1, 1),
  (3, 'Actitudinal y Autoevaluación', 20, 3, 1, 1, 1),
  (4, 'Evaluaciones y Quices', 40, 1, 2, 1, 1),
  (5, 'Talleres y Actividades', 40, 2, 2, 1, 1),
  (6, 'Actitudinal y Autoevaluación', 20, 3, 2, 1, 1),
  (7, 'Evaluaciones y Quices', 40, 1, 1, 3, 5),
  (8, 'Talleres y Actividades', 40, 2, 1, 3, 5),
  (9, 'Actitudinal y Autoevaluación', 20, 3, 1, 3, 5),
  (10, 'Evaluaciones y Quices', 40, 1, 1, 3, 2),
  (11, 'Talleres y Actividades', 40, 2, 1, 3, 2),
  (12, 'Actitudinal y Autoevaluación', 20, 3, 1, 3, 2),
  (13, 'Evaluaciones y Quices', 40, 1, 1, 1, 2),
  (14, 'Talleres y Actividades', 40, 2, 1, 1, 2),
  (15, 'Actitudinal y Autoevaluación', 20, 3, 1, 1, 2),
  (16, 'Evaluaciones y Quices', 40, 1, 1, 4, 6),
  (17, 'Talleres y Actividades', 40, 2, 1, 4, 6),
  (18, 'Actitudinal y Autoevaluación', 20, 3, 1, 4, 6),
  (19, 'Evaluaciones y Quices', 40, 1, 1, 1, 5),
  (20, 'Talleres y Actividades', 40, 2, 1, 1, 5),
  (21, 'Actitudinal y Autoevaluación', 20, 3, 1, 1, 5);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `grades_graderecord`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `grades_graderecord`;
CREATE TABLE `grades_graderecord` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `score` DECIMAL(5,2) NOT NULL,
  `feedback` LONGTEXT DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `academic_period_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `criterion_id` BIGINT NOT NULL,
  `graded_by_id` BIGINT DEFAULT NULL,
  `student_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_grades_graderecord_subject_id` (`subject_id`),
  CONSTRAINT `fk_grades_graderecord_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_grades_graderecord_student_id` (`student_id`),
  CONSTRAINT `fk_grades_graderecord_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`),
  KEY `idx_grades_graderecord_graded_by_id` (`graded_by_id`),
  CONSTRAINT `fk_grades_graderecord_graded_by_id` FOREIGN KEY (`graded_by_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_grades_graderecord_criterion_id` (`criterion_id`),
  CONSTRAINT `fk_grades_graderecord_criterion_id` FOREIGN KEY (`criterion_id`) REFERENCES `grades_evaluationcriterion` (`id`),
  KEY `idx_grades_graderecord_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_grades_graderecord_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_grades_graderecord_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_grades_graderecord_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `grades_graderecord` (15 registros)
INSERT INTO `grades_graderecord` (`id`, `score`, `feedback`, `created_at`, `updated_at`, `academic_period_id`, `course_section_id`, `criterion_id`, `graded_by_id`, `student_id`, `subject_id`) VALUES
  (1, 3.65, NULL, '2026-09-15 02:38:28.958939', '2026-09-15 14:49:35.243483', 1, 1, 1, 10, 1, 1),
  (2, 5, NULL, '2026-09-15 02:38:28.978565', '2026-09-15 14:49:16.813955', 1, 1, 2, 10, 1, 1),
  (3, 4.14, NULL, '2026-09-15 02:38:28.995203', '2026-09-15 14:49:59.036643', 1, 1, 3, 10, 1, 1),
  (4, 0.4, NULL, '2026-09-16 12:17:19.772506', '2026-09-16 12:18:19.064245', 1, 3, 7, 8, 4, 5),
  (5, 0.45, NULL, '2026-09-16 12:18:32.049104', '2026-09-16 12:18:37.609075', 1, 3, 8, 8, 4, 5),
  (6, 0.51, NULL, '2026-09-16 12:18:46.290775', '2026-09-16 12:18:46.290823', 1, 3, 9, 8, 4, 5),
  (7, 0.51, NULL, '2026-09-16 12:25:43.691037', '2026-09-16 12:25:54.969974', 1, 3, 7, 8, 5, 5),
  (8, 0.58, NULL, '2026-09-16 12:26:04.507412', '2026-09-16 12:26:04.507459', 1, 3, 8, 8, 5, 5),
  (9, 3.15, NULL, '2026-09-16 12:26:12.172033', '2026-09-16 12:26:37.274498', 1, 3, 9, 8, 5, 5),
  (10, 2.62, NULL, '2026-09-16 12:41:04.287732', '2026-09-16 12:41:04.287776', 1, 1, 13, 8, 3, 2),
  (11, 3.32, NULL, '2026-09-16 12:41:24.253053', '2026-09-16 12:41:24.253126', 1, 1, 14, 8, 3, 2),
  (12, 4.21, NULL, '2026-09-16 12:41:49.000542', '2026-09-16 12:42:25.436651', 1, 1, 15, 8, 3, 2),
  (13, 1.82, NULL, '2026-09-16 12:42:31.971246', '2026-09-16 12:42:42.818895', 1, 1, 13, 8, 2, 2),
  (14, 2.28, NULL, '2026-09-16 12:42:56.963866', '2026-09-16 12:42:56.963914', 1, 1, 14, 8, 2, 2),
  (15, 2.48, NULL, '2026-09-16 12:43:15.444158', '2026-09-16 12:43:15.444207', 1, 1, 15, 8, 2, 2);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `grades_periodfinalgrade`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `grades_periodfinalgrade`;
CREATE TABLE `grades_periodfinalgrade` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `final_score` DECIMAL(5,2) NOT NULL,
  `performance_level` VARCHAR(15) NOT NULL,
  `is_approved` TINYINT(1) NOT NULL,
  `recalculated_at` DATETIME NOT NULL,
  `academic_period_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `student_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_grades_periodfinalgrade_subject_id` (`subject_id`),
  CONSTRAINT `fk_grades_periodfinalgrade_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_grades_periodfinalgrade_student_id` (`student_id`),
  CONSTRAINT `fk_grades_periodfinalgrade_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`),
  KEY `idx_grades_periodfinalgrade_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_grades_periodfinalgrade_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_grades_periodfinalgrade_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_grades_periodfinalgrade_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `grades_periodfinalgrade` (16 registros)
INSERT INTO `grades_periodfinalgrade` (`id`, `final_score`, `performance_level`, `is_approved`, `recalculated_at`, `academic_period_id`, `course_section_id`, `student_id`, `subject_id`) VALUES
  (1, 4.29, 'ALTO', 1, '2026-09-16 12:44:46.954463', 1, 1, 1, 1),
  (2, 1, 'BAJO', 0, '2026-09-16 12:44:46.894831', 1, 1, 3, 1),
  (3, 1, 'BAJO', 0, '2026-09-16 12:44:46.925526', 1, 1, 2, 1),
  (4, 1, 'BAJO', 0, '2026-09-16 11:28:56.192036', 2, 1, 3, 1),
  (5, 1, 'BAJO', 0, '2026-09-16 11:28:56.212184', 2, 1, 2, 1),
  (6, 1, 'BAJO', 0, '2026-09-16 11:28:56.230339', 2, 1, 1, 1),
  (7, 0.44, 'BAJO', 0, '2026-09-16 12:25:34.746551', 1, 3, 4, 5),
  (8, 1.07, 'BAJO', 0, '2026-09-16 12:26:37.302282', 1, 3, 5, 5),
  (9, 1, 'BAJO', 0, '2026-09-16 12:39:41.922997', 1, 3, 5, 2),
  (10, 1, 'BAJO', 0, '2026-09-16 12:39:41.951800', 1, 3, 4, 2),
  (11, 3.22, 'BASICO', 1, '2026-09-16 12:48:40.855599', 1, 1, 3, 2),
  (12, 2.14, 'BAJO', 0, '2026-09-16 12:48:40.874494', 1, 1, 2, 2),
  (13, 1, 'BAJO', 0, '2026-09-16 12:48:40.891662', 1, 1, 1, 2),
  (14, 1, 'BAJO', 0, '2026-09-16 15:41:02.478102', 1, 1, 3, 5),
  (15, 1, 'BAJO', 0, '2026-09-16 15:41:02.498627', 1, 1, 2, 5),
  (16, 1, 'BAJO', 0, '2026-09-16 15:41:02.517438', 1, 1, 1, 5);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `homework_homework`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `homework_homework`;
CREATE TABLE `homework_homework` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(150) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `due_date` DATETIME NOT NULL,
  `attachment` VARCHAR(100) DEFAULT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `academic_period_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  `teacher_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_homework_homework_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_homework_homework_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teachers_teacherprofile` (`id`),
  KEY `idx_homework_homework_subject_id` (`subject_id`),
  CONSTRAINT `fk_homework_homework_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_homework_homework_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_homework_homework_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_homework_homework_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_homework_homework_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `homework_homework` (4 registros)
INSERT INTO `homework_homework` (`id`, `title`, `description`, `due_date`, `attachment`, `is_active`, `created_at`, `academic_period_id`, `course_section_id`, `subject_id`, `teacher_id`) VALUES
  (1, 'Taller #1: Operaciones con Conjuntos', 'Resolver los ejercicios del módulo 1 y subir el archivo PDF con el procedimiento completo.', '2026-09-22 02:38:29.005550', '', 1, '2026-09-15 02:38:29.009956', 1, 1, 1, 1),
  (2, 'Evaluación escrita', 'Estudiar el tema:  La oración', '2026-09-17 15:00:00', '', 1, '2026-09-16 12:06:38.445650', 1, 1, 5, 2),
  (3, 'Evaluación escrita', 'Estudiar el tema: La oración', '2026-09-17 15:00:00', '', 1, '2026-09-16 12:11:31.003987', 1, 3, 5, 2),
  (4, 'trabajo de la oracion', 'entregue a tiempo', '2026-09-17 15:54:00', '', 1, '2026-09-16 15:54:28.503883', 1, 1, 5, 2);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `homework_homeworksubmission`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `homework_homeworksubmission`;
CREATE TABLE `homework_homeworksubmission` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `submission_text` TEXT DEFAULT NULL,
  `attachment` VARCHAR(100) DEFAULT NULL,
  `submitted_at` DATETIME NOT NULL,
  `score` DECIMAL(5,2) DEFAULT NULL,
  `teacher_feedback` LONGTEXT DEFAULT NULL,
  `status` VARCHAR(20) NOT NULL,
  `homework_id` BIGINT NOT NULL,
  `student_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_homework_homeworksubmission_student_id` (`student_id`),
  CONSTRAINT `fk_homework_homeworksubmission_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`),
  KEY `idx_homework_homeworksubmission_homework_id` (`homework_id`),
  CONSTRAINT `fk_homework_homeworksubmission_homework_id` FOREIGN KEY (`homework_id`) REFERENCES `homework_homework` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `homework_homeworksubmission` (4 registros)
INSERT INTO `homework_homeworksubmission` (`id`, `submission_text`, `attachment`, `submitted_at`, `score`, `teacher_feedback`, `status`, `homework_id`, `student_id`) VALUES
  (1, 'Adjunto solución del taller.', '', '2026-09-15 02:38:29.019156', 4.5, 'Buen trabajo con las demostraciones.', 'GRADED', 1, 1),
  (2, 'promt', 'homework_submissions/PROMPT_MAESTRO.md.pdf', '2026-09-16 12:33:02.928737', NULL, NULL, 'SUBMITTED', 1, 2),
  (3, 'promt', 'homework_submissions/MY_FUTURE_PLANS.docx', '2026-09-16 12:37:09.480679', 4.54, 'Bien', 'GRADED', 2, 2),
  (4, '', 'homework_submissions/HUELLAS.sql', '2026-09-16 15:55:22.685256', 1, NULL, 'GRADED', 4, 2);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `periods_academicperiod`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `periods_academicperiod`;
CREATE TABLE `periods_academicperiod` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `number` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `percentage` DECIMAL(5,2) NOT NULL,
  `status` VARCHAR(15) NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_periods_academicperiod_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_periods_academicperiod_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `periods_academicperiod` (4 registros)
INSERT INTO `periods_academicperiod` (`id`, `number`, `name`, `start_date`, `end_date`, `percentage`, `status`, `academic_year_id`) VALUES
  (1, 1, 'Periodo 1', '2026-01-15', '2026-04-03', 25, 'ACTIVE', 1),
  (2, 2, 'Periodo 2', '2026-04-04', '2026-06-21', 25, 'CLOSED', 1),
  (3, 3, 'Periodo 3', '2026-06-22', '2026-09-08', 25, 'CLOSED', 1),
  (4, 4, 'Periodo 4', '2026-09-09', '2026-11-28', 25, 'CLOSED', 1);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `rules_academicclosinglog`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `rules_academicclosinglog`;
CREATE TABLE `rules_academicclosinglog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `closing_type` VARCHAR(10) NOT NULL,
  `closed_at` DATETIME NOT NULL,
  `total_students_evaluated` INT NOT NULL,
  `total_promoted` INT NOT NULL,
  `total_failed` INT NOT NULL,
  `observations` LONGTEXT NOT NULL,
  `academic_period_id` BIGINT DEFAULT NULL,
  `academic_year_id` BIGINT NOT NULL,
  `closed_by_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rules_academicclosinglog_closed_by_id` (`closed_by_id`),
  CONSTRAINT `fk_rules_academicclosinglog_closed_by_id` FOREIGN KEY (`closed_by_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_rules_academicclosinglog_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_rules_academicclosinglog_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`),
  KEY `idx_rules_academicclosinglog_academic_period_id` (`academic_period_id`),
  CONSTRAINT `fk_rules_academicclosinglog_academic_period_id` FOREIGN KEY (`academic_period_id`) REFERENCES `periods_academicperiod` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `rules_academicclosinglog` (1 registros)
INSERT INTO `rules_academicclosinglog` (`id`, `closing_type`, `closed_at`, `total_students_evaluated`, `total_promoted`, `total_failed`, `observations`, `academic_period_id`, `academic_year_id`, `closed_by_id`) VALUES
  (1, 'PERIOD', '2026-09-16 12:45:36.892631', 0, 0, 0, 'Cierre formal de periodo lectivo', 1, 1, 13);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `rules_annualfinalgrade`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `rules_annualfinalgrade`;
CREATE TABLE `rules_annualfinalgrade` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `final_score` DECIMAL(5,2) NOT NULL,
  `performance_level` VARCHAR(15) NOT NULL,
  `is_approved` TINYINT(1) NOT NULL,
  `recalculated_at` DATETIME NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `student_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rules_annualfinalgrade_subject_id` (`subject_id`),
  CONSTRAINT `fk_rules_annualfinalgrade_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_rules_annualfinalgrade_student_id` (`student_id`),
  CONSTRAINT `fk_rules_annualfinalgrade_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`),
  KEY `idx_rules_annualfinalgrade_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_rules_annualfinalgrade_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_rules_annualfinalgrade_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_rules_annualfinalgrade_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `rules_promotionrule`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `rules_promotionrule`;
CREATE TABLE `rules_promotionrule` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `min_passing_grade` DECIMAL(5,2) NOT NULL,
  `max_failed_subjects` INT NOT NULL,
  `max_absence_percentage` DECIMAL(5,2) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rules_promotionrule_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_rules_promotionrule_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `rules_promotionrule` (1 registros)
INSERT INTO `rules_promotionrule` (`id`, `min_passing_grade`, `max_failed_subjects`, `max_absence_percentage`, `is_active`, `updated_at`, `academic_year_id`) VALUES
  (1, 3, 2, 20, 1, '2026-09-15 02:58:56.096110', 1);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `students_enrollment`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `students_enrollment`;
CREATE TABLE `students_enrollment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `enrollment_date` DATE NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `student_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_students_enrollment_student_id` (`student_id`),
  CONSTRAINT `fk_students_enrollment_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_studentprofile` (`id`),
  KEY `idx_students_enrollment_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_students_enrollment_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_students_enrollment_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_students_enrollment_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `students_enrollment` (6 registros)
INSERT INTO `students_enrollment` (`id`, `enrollment_date`, `status`, `academic_year_id`, `course_section_id`, `student_id`) VALUES
  (1, '2026-09-14', 'ACTIVE', 1, 1, 1),
  (2, '2026-09-16', 'ACTIVE', 1, 1, 3),
  (3, '2026-09-16', 'ACTIVE', 1, 1, 2),
  (4, '2026-09-16', 'ACTIVE', 1, 3, 4),
  (5, '2026-09-16', 'ACTIVE', 1, 3, 5),
  (6, '2026-09-16', 'ACTIVE', 1, 2, 6);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `students_studentprofile`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `students_studentprofile`;
CREATE TABLE `students_studentprofile` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_code` VARCHAR(30) NOT NULL,
  `blood_type` VARCHAR(5) NOT NULL,
  `eps` VARCHAR(80) DEFAULT NULL,
  `medical_notes` TEXT DEFAULT NULL,
  `parent_id` BIGINT DEFAULT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_students_studentprofile_user_id` (`user_id`),
  CONSTRAINT `fk_students_studentprofile_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  KEY `idx_students_studentprofile_parent_id` (`parent_id`),
  CONSTRAINT `fk_students_studentprofile_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `students_studentprofile` (6 registros)
INSERT INTO `students_studentprofile` (`id`, `student_code`, `blood_type`, `eps`, `medical_notes`, `parent_id`, `user_id`) VALUES
  (1, 'EST-2026-0001', 'O+', NULL, NULL, 6, 5),
  (2, 'EST-2026-0002', 'O+', NULL, NULL, NULL, 9),
  (3, '236654', 'O+', NULL, NULL, NULL, 11),
  (4, '452314', 'O+', NULL, NULL, NULL, 14),
  (5, '236745', 'O+', NULL, NULL, NULL, 16),
  (6, '234567', 'O+', NULL, NULL, NULL, 18);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `subjects_gradesubject`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `subjects_gradesubject`;
CREATE TABLE `subjects_gradesubject` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `weekly_hours` INT NOT NULL,
  `weight_percentage` DECIMAL(5,2) NOT NULL,
  `grade_level_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_subjects_gradesubject_subject_id` (`subject_id`),
  CONSTRAINT `fk_subjects_gradesubject_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_subjects_gradesubject_grade_level_id` (`grade_level_id`),
  CONSTRAINT `fk_subjects_gradesubject_grade_level_id` FOREIGN KEY (`grade_level_id`) REFERENCES `courses_gradelevel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `subjects_gradesubject` (8 registros)
INSERT INTO `subjects_gradesubject` (`id`, `weekly_hours`, `weight_percentage`, `grade_level_id`, `subject_id`) VALUES
  (1, 4, 100, 1, 1),
  (2, 4, 100, 1, 2),
  (3, 4, 100, 1, 3),
  (4, 4, 100, 1, 4),
  (5, 4, 100, 1, 5),
  (6, 4, 100, 1, 6),
  (7, 4, 100, 1, 7),
  (8, 4, 100, 1, 8);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `subjects_knowledgearea`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `subjects_knowledgearea`;
CREATE TABLE `subjects_knowledgearea` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `order` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `subjects_knowledgearea` (6 registros)
INSERT INTO `subjects_knowledgearea` (`id`, `name`, `order`) VALUES
  (1, 'Matemáticas', 1),
  (2, 'Ciencias Naturales y Educación Ambiental', 2),
  (3, 'Humanidades y Lengua Castellana', 3),
  (4, 'Idioma Extranjero', 4),
  (5, 'Tecnología e Informática', 5),
  (6, 'Ciencias Sociales', 6);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `subjects_subject`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `subjects_subject`;
CREATE TABLE `subjects_subject` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `code` VARCHAR(20) NOT NULL,
  `description` LONGTEXT DEFAULT NULL,
  `area_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_subjects_subject_area_id` (`area_id`),
  CONSTRAINT `fk_subjects_subject_area_id` FOREIGN KEY (`area_id`) REFERENCES `subjects_knowledgearea` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `subjects_subject` (8 registros)
INSERT INTO `subjects_subject` (`id`, `name`, `code`, `description`, `area_id`) VALUES
  (1, 'Matemáticas Fundamentales', 'MAT-01', NULL, 1),
  (2, 'Geometría y Estadística', 'GEO-01', NULL, 1),
  (3, 'Biología General', 'BIO-01', NULL, 2),
  (4, 'Física Elemental', 'FIS-01', NULL, 2),
  (5, 'Lengua Castellana', 'ESP-01', NULL, 3),
  (6, 'Inglés Comunicativo', 'ING-01', NULL, 4),
  (7, 'Tecnología e Informática', 'TEC-01', NULL, 5),
  (8, 'Historia y Geografía', 'SOC-01', NULL, 6);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `teachers_teacherprofile`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `teachers_teacherprofile`;
CREATE TABLE `teachers_teacherprofile` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `specialty` VARCHAR(120) NOT NULL,
  `escalafon_grade` VARCHAR(30) DEFAULT NULL,
  `hire_date` DATE DEFAULT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_teachers_teacherprofile_user_id` (`user_id`),
  CONSTRAINT `fk_teachers_teacherprofile_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `teachers_teacherprofile` (3 registros)
INSERT INTO `teachers_teacherprofile` (`id`, `specialty`, `escalafon_grade`, `hire_date`, `user_id`) VALUES
  (1, 'Licenciatura en Ciencias y Matemáticas', NULL, NULL, 4),
  (2, 'Educación Básica y Humanidades', NULL, NULL, 8),
  (3, 'Fisica', NULL, NULL, 17);

-- ----------------------------------------------------------------------------
-- Estructura de tabla para `teachers_teachingassignment`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `teachers_teachingassignment`;
CREATE TABLE `teachers_teachingassignment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `is_active` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `academic_year_id` BIGINT NOT NULL,
  `course_section_id` BIGINT NOT NULL,
  `subject_id` BIGINT NOT NULL,
  `teacher_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_teachers_teachingassignment_teacher_id` (`teacher_id`),
  CONSTRAINT `fk_teachers_teachingassignment_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teachers_teacherprofile` (`id`),
  KEY `idx_teachers_teachingassignment_subject_id` (`subject_id`),
  CONSTRAINT `fk_teachers_teachingassignment_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`),
  KEY `idx_teachers_teachingassignment_course_section_id` (`course_section_id`),
  CONSTRAINT `fk_teachers_teachingassignment_course_section_id` FOREIGN KEY (`course_section_id`) REFERENCES `courses_coursesection` (`id`),
  KEY `idx_teachers_teachingassignment_academic_year_id` (`academic_year_id`),
  CONSTRAINT `fk_teachers_teachingassignment_academic_year_id` FOREIGN KEY (`academic_year_id`) REFERENCES `courses_academicyear` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcado de datos para la tabla `teachers_teachingassignment` (7 registros)
INSERT INTO `teachers_teachingassignment` (`id`, `is_active`, `created_at`, `academic_year_id`, `course_section_id`, `subject_id`, `teacher_id`) VALUES
  (1, 1, '2026-09-15 02:03:45.624240', 1, 1, 1, 1),
  (2, 1, '2026-09-15 02:03:45.638486', 1, 2, 1, 1),
  (3, 1, '2026-09-16 12:08:34.364618', 1, 3, 5, 2),
  (4, 1, '2026-09-16 12:34:58.113556', 1, 1, 2, 2),
  (5, 1, '2026-09-16 14:44:57.216729', 1, 4, 6, 2),
  (6, 1, '2026-09-16 15:50:24.180979', 1, 1, 4, 3),
  (7, 1, '2026-09-16 15:51:14.498200', 1, 2, 5, 3);

SET FOREIGN_KEY_CHECKS = 1;
-- ============================================================================
-- FIN DEL SCRIPT DE RESPALDO Y CREACIÓN DE BASE DE DATOS
-- ============================================================================