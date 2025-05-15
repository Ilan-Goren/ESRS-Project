-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 15, 2025 at 02:07 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant_inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$jEZmjbIM8ZLczrj2D4ytaT$JK9iW2Q5RQEnxV9oY59ZE6JruC3wtBGyv9jiaIMAUdU=', '2025-05-15 12:03:28.828854', 1, 'admin', 'admin', '', 'admin@example.com', 1, 1, '2025-05-02 17:25:53.152269'),
(22, 'pbkdf2_sha256$600000$OVfbRRKf0ZBJJzmcqKRSoY$w0ajHwNlImYa5Ksb/ifUIlNDwAlG1YLRJOhNe/N4dug=', NULL, 0, 'manager@example.com', 'manager', '', 'manager@example.com', 0, 1, '2025-05-15 12:04:19.627150'),
(23, 'pbkdf2_sha256$600000$vWQDJsNWgCz0RP5TQKlZ0l$wBvgjQ8x/mi+XWLW1KrysgPj9FG3lISN+3KwCRqapQk=', NULL, 0, 'staff@example.com', 'staff', '', 'staff@example.com', 0, 1, '2025-05-15 12:04:33.042910'),
(24, 'pbkdf2_sha256$600000$crLgJJebzeMdikqFb42E1Q$qoHcHa46Z2s04afVu3Is9cYEmZaBgdVzxQsuJMd/oyM=', NULL, 0, 'supplier@example.com', 'supplier', '', 'supplier@example.com', 0, 1, '2025-05-15 12:04:51.692476');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-05-02 17:25:14.666474'),
(2, 'auth', '0001_initial', '2025-05-02 17:25:14.806138'),
(3, 'admin', '0001_initial', '2025-05-02 17:25:14.848798'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-05-02 17:25:14.856466'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-02 17:25:14.861636'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-05-02 17:25:14.886075'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-05-02 17:25:14.902953'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-05-02 17:25:14.912346'),
(9, 'auth', '0004_alter_user_username_opts', '2025-05-02 17:25:14.916940'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-05-02 17:25:14.929474'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-05-02 17:25:14.930340'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-05-02 17:25:14.934219'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-05-02 17:25:14.943917'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-05-02 17:25:14.952229'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-05-02 17:25:14.959148'),
(16, 'auth', '0011_update_proxy_permissions', '2025-05-02 17:25:14.963318'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-05-02 17:25:14.971554'),
(18, 'sessions', '0001_initial', '2025-05-02 17:25:14.987596'),
(19, 'store', '0001_initial', '2025-05-02 17:25:15.014650');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('07yg2579e4ywq835c606ijwqjkzi04d3', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFFB:z4hP9a762jwP4GnS1ycTaXB-IFu67wAfclUK-49Ir34', '2025-05-20 10:09:45.320964'),
('0l0ramu65iesvvplsewt9v5umsa17p35', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuPu:7ZGxgLIagpitqm7ncuILzP3H9HvTvCEW_RXK3c3ugJc', '2025-05-16 17:43:18.914608'),
('0wqxtblh6giyaz8csvq6pq5vhu4psovr', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuFQ:H-4j-YbBo-1GM-UcLg4Mqq4o79wr5c_zg4lSobXv4lc', '2025-05-16 17:32:28.761412'),
('0z2qe8wn7pm467na8uk1zm0nhkrbml7m', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBGlT:nAwpgqEMrMVn2Z0ka0JhhsXt_dYR8k4G1j6xBGHmg58', '2025-05-17 17:35:03.077028'),
('194i8fhqmdijf5s3n6wb4sgg0qj2kojg', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEwI:9B-dIkveWnEO0t3g9Xkd6KkE66h7QkpYX2lHpzqGy_4', '2025-05-20 09:50:14.150532'),
('1pqh8fv34igork0cxbzd8gm80wxssqte', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFAN:9yGFMR5paFvLdHxfdoDBSzuamYftnznd2mH7s9Ud5iQ', '2025-05-20 10:04:47.384981'),
('1qrb2jcd0lorbvdx548rmbayn4x5p5tc', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uFWPJ:yOqJ-6ktmtTbD0J8pORigvnC1mwtqy8Tg-ge0-ZwrpY', '2025-05-29 11:05:45.292087'),
('1uazz7x99nlzz3uvtrtv3szsdjjcp09a', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuIK:JTX05lW8QD8UrWijZ9VMQ748TOWKg99rqGGYSPpiBZ4', '2025-05-16 17:35:28.723648'),
('244q7coxn5pscsuyxjhgqoq30nhliypy', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAvLX:1yfV9vVDcj8NLLmiMHyFWytIRx2L1DOIvZcBwpgJitQ', '2025-05-16 18:42:51.039270'),
('28wc05i8olvy2vgznp1tax0km2sszaz6', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuz9:0YQSkrwf7bOaAYxorosp-W9TTwMwx-bh6UmSr7GL--8', '2025-05-16 18:19:43.632088'),
('3m0uq8c8z8kryos022fd3xhimxad43tr', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEtV:hrlrzu2UYgz_9lTWVmba4RO5ZzEpMNuMXjKgKtZLPTg', '2025-05-20 09:47:21.173026'),
('3msl5jy2rmghdp1wgjkysnyqprvygglj', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBGuG:FYKIgkQN4uNi_VoBDbHEBDAI5AjjZk07sibvo7CJ-vo', '2025-05-17 17:44:08.386780'),
('4puembpsajfkz3r12cju6zh5yy8e2dlf', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxki:VTBLLn3FsPqrRc7TBJInLUBJ4-0Ygz9Om_tRRQGZGwc', '2025-05-16 21:17:00.013235'),
('4zpjgy8d2dtkec1lg56dmlputdpwyebr', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAvMr:pOyfejBVa7KzN5-RwwzyZVwjlLJLG9UJhbhceDe-8e0', '2025-05-16 18:44:13.199147'),
('5w266ochd5gb4bgidxcezpa53z2i7c51', '.eJxVjMEOwiAQRP-FsyHQLS169O43kN1lkaopSWlPxn-XJj3ocWbevLcKuK05bFWWMEV1UZ1Vp9-SkJ8y70t84Hwvmsu8LhPpHdHHWvWtRHldD_ZPkLHm9hZg9Gl0AwGzEJ_JSy8mJp8GY4mbaZQBout6aAi1BBbQJEtjB86ozxdKHDk9:1uFWo8:B72HGcPy2gYCkw3r3dTcTVcBmRWw4le-uCcIPq08IV0', '2025-05-29 11:31:24.221974'),
('6b26aq74uktoq25ntxwdtjxrp26beebg', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuws:k9EqzypyMS50tqLA6n536aszTc8OdFsR48f3OFkJFkk', '2025-05-16 18:17:22.073742'),
('6z1v957wgf24hea1pma33o4m9d06ne5e', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uFRQs:XBeQRhabgB8QQ1I2B91sT3WIIUA30r7fN-hD3DbZYSI', '2025-05-29 05:47:02.710170'),
('724gomttsu5q6eyv6hkdx8mnrquekl9u', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuGu:BsX7xxcQCD0XS0gNOGkobImB4FgOG8kQSp9S-7d4N5g', '2025-05-16 17:34:00.564280'),
('7bn3pc0t3ldhev3ys6fbf6yxbs1ujipe', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFvM:L32ynyi0NoPNkLotDqxszxuUkKtG9-9Kk1NXw2XJ5kg', '2025-05-20 10:53:20.808702'),
('7d24c322vx7li5b0vlh7pfuxocje32z2', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv7r:081_VtA-6NbYk3fLUUAi4kLhWKpQhhylxMwIVVR8emQ', '2025-05-16 18:28:43.477091'),
('7dhd66692frs1nr1f3a7l9qe3tx9grqh', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuOq:m5-NEW0f02mroIJnLTguCyHez14PEmAtCo5hOuz4WnI', '2025-05-16 17:42:12.493673'),
('7g08i4hva509nh2bknko14puon9tn5a3', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEo7:ukGrT4DSlYOLUjEiyrPOuSxS7iqQ0hQtq64_WyeEYkM', '2025-05-20 09:41:47.373746'),
('7qw1kb3p34kagk2i6vjbqemdb27c4d29', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuts:F7KbkwdXZ3RVxyKNmG_JMiOusrSrTBL1aKwKAXwKd48', '2025-05-16 18:14:16.651645'),
('7qyx3j4ggp4qnityo8nl582xerfhidt8', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFzJ:Sq1x79ePum_8RgBUwrUfP7CLsinjWj0Dc-0h4Gr10No', '2025-05-20 10:57:25.506264'),
('7rwd1nd2ocj9ge6dhhij4vzqc9yeovpo', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFvB:HBisa2O5cybeBGjd96EG6vAB5Skb7DngD35q2k75Muc', '2025-05-20 10:53:09.585368'),
('876kta2jq1n1ceopaurucii8o2647eqq', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv2q:K4YPHMJ3Sl6E1q-T0U7aifhLBh7ZtASKu7GOR9TT_c0', '2025-05-16 18:23:32.483533'),
('8dx5yfjvzsvd4lck6u2uux5c6w91ivdo', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuU4:IcgQSyq8me9JxFuu87Eg73K0udmbjhCnEX37ZRkzRKI', '2025-05-16 17:47:36.109891'),
('8mmj940yk6cb25b6g6z83fsp7i5jyb2r', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBHXV:VrrpwhcG5BNMfFSsj1SlcyseGzsxXnuu4olIlK-YbJw', '2025-05-17 18:24:41.714451'),
('9c1g0f5w3st9zu6864a4efras8i6s1js', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAvBv:iT0tvy2vimypyA3s2NM7VoPNcLRerGbfwJ6oXDJMujw', '2025-05-16 18:32:55.690801'),
('9p7voq3y6zp5pn8dmzbqixnfotrwvb3q', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv8H:L1heHiAPt5yyGCuO21uqav7N7A8K9RetzjoARPm8FXg', '2025-05-16 18:29:09.754844'),
('9phnuy0b2ivkfudtmvu8qhjqiaaf57i6', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRyi:1zzmz6tpcnD_Z7V8AYjh3Iko3xeN5gjgnMPVGJFKmUA', '2025-05-29 06:22:00.429390'),
('9xa6cii1akj6daak7cy18hd1icpuogmp', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFiF:x-oyDG43FwaN5RuI72pJlVgXOSpOcIT2d-rCGaSFJJc', '2025-05-20 10:39:47.553277'),
('aai07c1k3rykmdy6zl6oeo54fkzjfe8u', '.eJxVjMEOwiAQRP-FsyHQLS169O43kN1lkaopSWlPxn-XJj3ocWbevLcKuK05bFWWMEV1UZ1Vp9-SkJ8y70t84Hwvmsu8LhPpHdHHWvWtRHldD_ZPkLHm9hZg9Gl0AwGzEJ_JSy8mJp8GY4mbaZQBout6aAi1BBbQJEtjB86ozxdKHDk9:1uFXIX:3jAbkI2WTeM6nClzW6YTnXHg6KMIBVmJvQX7Cz9BbmE', '2025-05-29 12:02:49.496369'),
('au6asjeiggj115rd2hisnu02f0kwezyo', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxLl:G0zzakUeLfKjxMPkJnsKzpV8E88EiX4zaRf_SRIuJ7g', '2025-05-16 20:51:13.435463'),
('ave8yh5jeejg5jfgd8rase7dpq562008', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuH3:ySi1Yu1Bqeawh3OM_pNJQ0_nMtyNZsOSl7Z_3n0Lx68', '2025-05-16 17:34:09.077211'),
('b7mkq199dgd6hbvmi49r2hbx1q3m5934', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxpU:KhVL0_hUnO9fx_PIKkAJoRp32QGyIEiqMaZU7yhR-k4', '2025-05-16 21:21:56.734543'),
('beyd7wmx7gbrec7tvrr78m4yd8augy2g', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuEK:Y3R02rNKnxC5iLbimpLLn8SdRAY5fPNXkc2Mkc4kB-0', '2025-05-16 17:31:20.202200'),
('bi29wnfs2gfvhmy8y42hlvszq6kdakrd', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFH8:WZ0IyDo2tqTlGn0QvukwEUTGC0_9nLwQM3wmU5kVDuc', '2025-05-20 10:11:46.386644'),
('bxcadfqz9vosmub7zh3w3c1m8dxro9n7', '.eJxVjDsOwjAQBe_iGln-4E8o6XMGy-vdxQHkSHFSIe4OkVJA-2bmvUTK21rT1mlJE4qLMEqcfkfI5UFtJ3jP7TbLMrd1mUDuijxol-OM9Lwe7t9Bzb1-a-s8WKLg0AFh1AzBRBe0IcXM2iEPRMr4qMEMrOHsKbuSLUNUaGMQ7w8asDif:1uFWf1:Kk7MT0ffTzY-gn04sFy0T1dI6klQJ-5l9cMB-mWTqHI', '2025-05-29 11:21:59.146374'),
('c75pt0ll7k7abrucxa14e3p5f0jrdkii', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFuE:OBO_N9cwmMaO8AwDhU_T5n_tAnx4wBy8DfxWdABdisw', '2025-05-20 10:52:10.974693'),
('cmlvvsohnlq1qux54wfbjbwct3qqoi65', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuBp:34kIfUmf_89ODSKEBHjZ47yIyE4Tpd-tt-3DUIpMTCA', '2025-05-16 17:28:45.364874'),
('cr4nfwkpn08p4pk488v9o9ksbxm3bnmm', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRTF:Io_4N5FFwP9uhwEQR0vz3a1sFC8R14bUJRa8aTxmuB8', '2025-05-29 05:49:29.558120'),
('d0j6dzu5n4opuacebzuijen1f4ic43bb', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuNe:o-v4Ae1oq-FIEBnwfeXEsOo_bL6mWKbWXW5I1lxMWuU', '2025-05-16 17:40:58.966629'),
('dsc9tx5kk6s0nhy0yzb1hm0vw0hgi78t', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uFWgI:cB-Af9z9BbjASJ0S1_i9EAAk_g0cV1vBugIFsS3MMhI', '2025-05-29 11:23:18.390102'),
('e3389age1qyex9m5oilt7udvatipx8kg', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuav:GWdWCk9zi2k_nXcACtUTVP_y2w3CUMTzeVyyj-bsL7A', '2025-05-16 17:54:41.364822'),
('e5c8n84zu0hwb1pbuhgzu69jyw8sjh6w', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxhj:tC4n8n1iKFPU9dlG3NI2rFtB_VOhxCP-3TeYCd51h9U', '2025-05-16 21:13:55.353615'),
('ex93s6tdlvij4501q4huedbb81bptubd', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uFXJA:6G9rByIE0IZJq_iZ7mQWvmvZ_RktkB9Z-V3_gBQnwfA', '2025-05-29 12:03:28.831886'),
('f9ceki8mkywic03ae3inz0yca85738ls', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxjd:WV4XKZCxOTiHA3qwCGZ9E4e_a1kB6w1emjcnniFGZ4U', '2025-05-16 21:15:53.057993'),
('fac9l6fe2xl2d8aegguemiu9h1a7alpd', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEwg:fWsFObisJPO6zD8FwCpaDqLgH2Jk2ATiyt_MSl6m2ok', '2025-05-20 09:50:38.646187'),
('fcegk3rz8j2m24lkpxt61y2qqnf3fcpa', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEzb:Mr-mIJT53UNDcsltCedbPNkUpGaD5ZXVaI6FYesHrkQ', '2025-05-20 09:53:39.311799'),
('fe9gcep50i8yojadqij7j2l7f7xxhr01', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uFRSB:KGOnEIwyLtEcR84DE74ESHHhFZv3lNEQFHnykmJl_bI', '2025-05-29 05:48:23.627968'),
('fhq62tw0f1qaw0uixwsrb1rdld1tj9m7', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFi7:Dnh1CqiixS0wIq7v2CZ2kz4f5qX1waiBNmen9j7sceo', '2025-05-20 10:39:39.380887'),
('g7u0fulk3dtja07vlsd5ehw3elcq5w1f', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFzZ:kkdQlKraG_1_stY6hayb07yZGpwJbetgS1fybPc0riQ', '2025-05-20 10:57:41.688992'),
('g9a31p0p4b9dg6vm710gzgwgjtwho7q7', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv93:NV2SP5Ltdd4bt0Nr9iuzSNt5TpONFz9a49Hx7W3OC90', '2025-05-16 18:29:57.636105'),
('hhlnql7cfncymbyxfu01n2c3pim9fueh', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFcq:sQd_-b2EeK_-sKsUq8BNWtg38REBE60iJafKyXMMd8A', '2025-05-20 10:34:12.940201'),
('hw487c2tu5nlb1gy5dfptilpzytsuh7t', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAu9P:fnIz6XlnnaKqGQa8vpA8LtSuC8euG3JdJmXRk1bGSdc', '2025-05-16 17:26:15.227966'),
('i96k7eod83fuoljurwygg9qzurf2o4v4', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRTO:kCz9gT3SeaCaunm7oeoXkwSom5HBXw61Q5exqImjjKE', '2025-05-29 05:49:38.992801'),
('j366pnerpv9qtn6z4gzvarh8ud58lz6t', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuSZ:WRQDoMRK7mDL8GOjS03gcHnRgAUNQC1-FgX5RgXXRfc', '2025-05-16 17:46:03.725248'),
('jz2dxf25kiawiehlfzt3qlogpq36056f', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFnp:WFmeoqXqstBt_JuybbeGQefriFhYthp4Hu67V4kN3ZM', '2025-05-20 10:45:33.386245'),
('kepu4e5s6vda8wa1ouwhgvo1v0l7jaam', '.eJxVjMEOwiAQRP-FsyHQLS169O43kN1lkaopSWlPxn-XJj3ocWbevLcKuK05bFWWMEV1UZ1Vp9-SkJ8y70t84Hwvmsu8LhPpHdHHWvWtRHldD_ZPkLHm9hZg9Gl0AwGzEJ_JSy8mJp8GY4mbaZQBout6aAi1BBbQJEtjB86ozxdKHDk9:1uFWjV:SE3VeMUmwn3fHm1nI76sWtyGQYvrX1bYzV0QAt0xWd0', '2025-05-29 11:26:37.429045'),
('kpel2etmhm6xy5bacm54mulv2f14j6zn', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxcd:eQf23br3i3fW58Ev-GgCtqSwVhOGICSY8Jnt852iWag', '2025-05-16 21:08:39.372319'),
('kxg3zi5xyxae4g6z9bvchjxv8k0aa272', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEfO:f1nPeDUEDeUsxJ6IsPa0XWIFhSVt1adYbFZvHt67nsE', '2025-05-20 09:32:46.868694'),
('lopgxdc5exbwh1vomplitwx679m2cwyw', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFpK:rkGft-ft3X-97RDokBC4mFr_AGyXmXXg-bhZq5CJvyA', '2025-05-20 10:47:06.489314'),
('mz6zw7s7b032q8h2u8g4js0ai3graytn', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxO7:oYQYC9zChNv9S3LqgupXskdwuYgdt_HeFHP2NZsKfjo', '2025-05-16 20:53:39.219834'),
('n9moil54s44wli6fq31gbvs6jdui48pq', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEcS:9pluM1hw9289eIMosLgNpN5vbfH5LBK7C89TU4pHn4c', '2025-05-20 09:29:44.870511'),
('ndwf9fqyscn44c74reg25v96dn36jqj8', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxm8:XLDpTa_W82JqUlqTPwWdD_cETmHvKZZgOk-KtOZIgjc', '2025-05-16 21:18:28.654526'),
('nejrhao40mk3cz1wl75ifv71pe1p6s9y', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAu9Z:CufbFmr4lkC4aycfLsMqfAKgIKmfT1PLxUJAseyUs-U', '2025-05-16 17:26:25.124317'),
('nf81d3namrxloplh9fnjhvhx9tlnp177', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBGt4:1YZuVAmpFminwkkLprCdPRxRVLIc5SCf6TQnURISbL0', '2025-05-17 17:42:54.559878'),
('ohsijjf9z0c4bmdjqpyh0qj1ekjdb2b1', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFcP:4nvnG0jAJWRmlTbWSh1Gi9ePLAE28sHK99gBXKYbMkE', '2025-05-20 10:33:45.464223'),
('oq1k3q6hfcc7vjfx64nklevwj41jh8ya', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAu9W:F6tt8Myhx6yGg-MIlq8tpKFeDKCumyqwVSYzpjdY7v0', '2025-05-16 17:26:22.642327'),
('osogw0ymvi01vvewr3eeqlfb8ql4l3q4', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxhd:O9d9Hp0ShN_TOp1qbd3AL-SQMOQpK1XNLqCYmPuOQ-Y', '2025-05-16 21:13:49.622509'),
('otpuu271dgu9zlhq0c7c4qvb4clvgllq', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEcd:ggcdpCLiQsVK2eD7EEoFrev2lPJ6g7rd9pchP4VCUHM', '2025-05-20 09:29:55.851038'),
('plokudp27ftn8wg8xumctxphg10mk8rz', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv1U:0vn-rJInPx7NzyXUbl0tMcJIS9J4W3P98pesJn7gD44', '2025-05-16 18:22:08.083640'),
('q2qu6za0q9x50wt5mht82186k72adgtz', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuBt:b66Pt68iTShmyOdEjzk5dVXuvmRNxiwt202KMMI7WDI', '2025-05-16 17:28:49.633072'),
('qdqz80cmbkj3mwk3ak9o71q1usgifkj8', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuvT:5iBWpV3UPEsN7yTJZe-LGWXK2L0C09DNDFs3uuU8tE8', '2025-05-16 18:15:55.207222'),
('qe38sutstvebl5jha2zkyr3wizc8cmea', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxbp:OrqZMCzx3wvfaGqTit27tuhpJGy01pDwjG64ehlJvRs', '2025-05-16 21:07:49.591291'),
('qga6ew3l73bpxsmwv2ethxw6iypf6hyf', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAv9u:kYKWGSvqrLqbzE7F5xlTLFm5CjtqszeljdRCQtmJ8as', '2025-05-16 18:30:50.442061'),
('qjow8l4gypsjwbjdjc3m1tr64ap2ynrd', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRTM:YxPNKjSbN5pi_8iPNn5Cwgn5R4EWWDLvVtZARYhfjHs', '2025-05-29 05:49:36.012135'),
('qqd1y064m7020xy1pgdq03u20okibu62', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuQA:vODJMLPMeJ6NnjIormF3KAXJlncHHJ6Q2s5iI1foFhM', '2025-05-16 17:43:34.726576'),
('qt4isqoy04fjmrkx410x82oz7g7rpgrm', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxv4:KnzIFZ3kzWLMoquRTmawGxsDNYrc7e5XOr1dPfKes2M', '2025-05-16 21:27:42.162744'),
('rgtdyqzmzwecuc153ky2gbnb1kjz1uh2', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuEl:vKZhQImrl_CtWuHXtY5EN2xjKhAIprqtSzuFH6HNOnQ', '2025-05-16 17:31:47.476616'),
('rhjigx6or347ze5b0r8avw8h320mw6bh', '.eJxVjDsOwjAQBe_iGln-4E8o6XMGy-vdxQHkSHFSIe4OkVJA-2bmvUTK21rT1mlJE4qLMEqcfkfI5UFtJ3jP7TbLMrd1mUDuijxol-OM9Lwe7t9Bzb1-a-s8WKLg0AFh1AzBRBe0IcXM2iEPRMr4qMEMrOHsKbuSLUNUaGMQ7w8asDif:1uFWWE:na8gQ4QLDsq1tiDY58b66nRZkDcCvnjt3TFL8RoIAsA', '2025-05-29 11:12:54.531532'),
('rjouyxif2dvbetvbcb2xhavaiv9hd8lr', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuHA:65-Jj5YUgmsuhOcWG2esBq2f7t7sP6QEQboh5ZwXGFo', '2025-05-16 17:34:16.824314'),
('rw0bdchhptrqevpu8b77uhvkjjc8zc7w', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuSh:JCH0ax35OMFL_TyoTGmFjmN39pKDlCwEqM0IroNdLGw', '2025-05-16 17:46:11.814147'),
('rwzfakej1ziu4qxm74hgwref2aphksj0', '.eJxVjMEOwiAQRP-FsyHQLS169O43kN1lkaopSWlPxn-XJj3ocWbevLcKuK05bFWWMEV1UZ1Vp9-SkJ8y70t84Hwvmsu8LhPpHdHHWvWtRHldD_ZPkLHm9hZg9Gl0AwGzEJ_JSy8mJp8GY4mbaZQBout6aAi1BBbQJEtjB86ozxdKHDk9:1uFWgm:1puO1bQ_BAjcu_Je9UVZ9mAVOjVD2ThdRpX6vHc9Eho', '2025-05-29 11:23:48.558938'),
('rzxkwvpjzrqayy1zy1ubvspqvgzr3lpz', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRYX:GY4rqE67K0MVVOasSHGUepeOFZBmDKf_zXa-IUCy6lQ', '2025-05-29 05:54:57.909507'),
('ssdkpm300mnc3xagej6nsrqmkbkep8nv', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAxWL:olUWwb6fc9SSaLhAXrGO4v7iYpPk2u6MyFx8sFqvido', '2025-05-16 21:02:09.368140'),
('sxhg18ertg25zslh2zmpau5z5armod6h', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAvSG:x8It8JyVyMEkOBfLGgXM2EsRUpXjRCO4nqHjWVdEb6o', '2025-05-16 18:49:48.506103'),
('t5c5yvsqgvylpbwkqgxhezdkljsinsm4', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBHHj:UR8f4MaI2KCpjB2z2z-xeowR62yi_gdM1Y62oGZ0vL4', '2025-05-17 18:08:23.831672'),
('tab00ngers6u1i67jhjc2vm0emcm2v6j', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFyW:VI2Lfkl_oDEHQoYU8VzAhCzzsd5sNpfPoQW-zQQ5ZG8', '2025-05-20 10:56:36.968828'),
('tth0t1awiuomkl97erkdd6p1wpn4cab5', '.eJxVjDsOwjAQBe_iGln-4E8o6XMGy-vdxQHkSHFSIe4OkVJA-2bmvUTK21rT1mlJE4qLMEqcfkfI5UFtJ3jP7TbLMrd1mUDuijxol-OM9Lwe7t9Bzb1-a-s8WKLg0AFh1AzBRBe0IcXM2iEPRMr4qMEMrOHsKbuSLUNUaGMQ7w8asDif:1uFWTk:ndnlsjn-UzpTw-8CxTNu3dwA8YVQzqtyo5xfU0-ht1A', '2025-05-29 11:10:20.506015'),
('ubourglhbdabd07he386wotffdwjtbbg', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEz3:-Kt8zEkYGCHA9NnJXKG2WEtYRoqeyNVkII6rYZCoey4', '2025-05-20 09:53:05.009003'),
('ucdhgxjwqxnbfo4nxkonl8rt57g8dvnl', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRYM:hlTsBxbpEJBWbr1u-enRGU1-IS6nSBj8dizCWuYmxWk', '2025-05-29 05:54:46.196935'),
('ue2mc1x4gkfzx6qt7nm370t6d7wqwy16', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBHFf:0Ti09baf4_E7vACGyBmCDkBz94oH5Y3txVzYhYPq8as', '2025-05-17 18:06:15.977349'),
('uf1qdb4e1kmqctfla77ysda5u7yz7e4y', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFrH:jt3WlkIrspMfaH84H0DiWqrfWliEHLR1l_Skg4FmD0k', '2025-05-20 10:49:07.154394'),
('ukv2kte6p11mcbkk58gzgp84w8ovvro0', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRp9:_LfB3_ZRUbRdHmDdlIGyLsioILB5tG8qnqNJYJe6tuc', '2025-05-29 06:12:07.551064'),
('wx8p8rtd1y8p7r4ykaxr3btz9ad4kt82', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBGwG:p-Rxd0SwO-bXR5ZVpeDDP-3iel1hwxVrfiD-7AvkryM', '2025-05-17 17:46:12.317748'),
('x0j408te6f6f5i3h39knq9e2liyxhzbv', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCFNM:MpBKF_XEd6ulp2ZFT3crtnHkdEvhxgSOeTkUd2oNBbo', '2025-05-20 10:18:12.245544'),
('x39qwy3wg6rv5qfpt3s1kiwfu45s8vb8', '.eJxVjEEOwiAQRe_C2hAoDIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSNqnD71iQHtI2wndst0nT1JZ5LHpT9E67vkwsz_Pu_h1U7PVbFxJwnMhQCZ4jRHsVwJCGGMzgI5noDaAUE8BKRAFI7L2zUgKn5I7q_QENvze6:1uFRSa:LSLM8PG5sJdvLop5InAD4zBqAo8vsx3og17lW-hXZQM', '2025-05-29 05:48:48.152841'),
('xjbm6b4bbb9cn8ryeo47u7pf5273tdaf', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAusr:GWBIH5LoR9dKsroJ09gw8sr_U7yIvsnVnA5lx79y4cc', '2025-05-16 18:13:13.141811'),
('y8a6xuf6buobqx15ghtph6beue41v1q5', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uBH8m:PSPSsKs6t38IV8xFbXSpDuTkGJGoDp1Qh5gJAZPCZG4', '2025-05-17 17:59:08.331120'),
('yfy6i4z6z8prjr5kdhj9kqktoltirj55', '.eJxVjEEOwiAQRe_C2hAGKjAu3XsGMjAgVUOT0q6Md7dNutDtf-_9twi0LjWsPc9hZHERYMXpd4yUnrnthB_U7pNMU1vmMcpdkQft8jZxfl0P9--gUq9bncvZGocRkJ1OxmtNPgIVRlakCPMALpbMCpxLCBg3mAAMGuv8oL34fAEQ_jfa:1uCFcI:XmGizh-c7Ej9uUfhTJDAGfpIMW3DLLScrfYhaw-IDDY', '2025-05-20 10:33:38.415461'),
('ypoof2xcypz4pijipo01qqh95hcjuu32', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuBg:2U1Mv1i2Wv1LKhq8leqmkeYjOklxPmypM2vEhwpiquM', '2025-05-16 17:28:36.213338'),
('yubye8lcy29fmag6r2pt67or2zhl7d3e', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAvOS:sloBZk0fRCm0keC4cD-BfIybkfdh9HiBQVQWRJOhnKE', '2025-05-16 18:45:52.829142'),
('z55irbci1c3ecvr1xiq6n1s2xic2snt4', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uAuGp:nE9A4BvUXuJYAXRlVLN_oZbgCsWQz0-PDFSL9kUegZw', '2025-05-16 17:33:55.227867'),
('zsxma98b01ps6oryfp7xzoq9n68os74k', '.eJxVizEOAiEQRe9CbTbAwA5Y6hmsyTDMBmPUZFkq493FZAst__vvvVSivtXUm6zpWtRRGXX4ZZn4Jo_v0bbnKtO-23TuA9wvwzntyl9XqdUREQbIRVC8YYs-UkZiDeyQrYnWOMyzLD6As1AYIs2MC4NoR9kFTer9AddXNNw:1uCEja:w773cRaiaVfQIICYEqkArVCFZ0jKUpFxcVxVF-COSoQ', '2025-05-20 09:37:06.226291'),
('zvn39mdzimgdqfj3u4k5dpofitsxrytz', '.eJxVjEEOwiAQAP_C2RBYLFs8eu8byMKCVA1NSnsy_l1JetDrzGRewtO-Fb-3tPqZxUVoFKdfGCg-Uu2G71Rvi4xL3dY5yJ7IwzY5LZye16P9GxRqpX-1UYEzZLaQ8ZwVqpiNtqO2qAYcrYvKBHIDG0DIGpEgsE0ArN0XiPcH7l43Rg:1uCFgw:G5DAwOk4lFZHqipqcJkLjZfsjHYmxXBgwNusWE9eMOc', '2025-05-20 10:38:26.517043');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `sku` varchar(50) DEFAULT NULL,
  `item_name` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `reorder_level` int(11) NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `last_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`id`, `sku`, `item_name`, `category`, `quantity`, `reorder_level`, `expiry_date`, `supplier_id`, `last_updated`) VALUES
(1, NULL, 'Test Item', 'Test Category', 50, 10, '2025-12-31', 1, '2025-02-25 10:22:24'),
(7, NULL, 'Tomatoes', 'Vegetables', 60, 10, '2025-03-15', 1, '2025-02-25 10:16:12'),
(8, NULL, 'Lettuce', 'Vegetables', 30, 5, '2025-02-25', 1, '2025-02-25 10:13:39'),
(9, NULL, 'Milk', 'Dairy', 20, 8, '2025-03-01', 2, '2025-02-25 10:13:39'),
(10, NULL, 'Cheese', 'Dairy', 20, 5, '2025-04-10', 2, '2025-02-25 10:21:28'),
(11, NULL, 'Chicken Breast', 'Meat', 25, 7, '2025-02-28', 3, '2025-02-25 10:13:39'),
(12, NULL, 'Ground Beef', 'Meat', 40, 12, '2025-03-05', 3, '2025-02-25 10:13:39');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `status` enum('pending','shipped','delivered','cancelled') DEFAULT 'pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `expected_delivery` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `supplier_id`, `status`, `order_date`, `expected_delivery`) VALUES
(1, 1, 'delivered', '2025-02-10 00:00:00', '2025-02-12'),
(2, 2, 'pending', '2025-02-15 00:00:00', '2025-02-20'),
(3, 3, 'shipped', '2025-02-14 00:00:00', '2025-02-18');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `inventory_id` int(11) NOT NULL,
  `quantity_ordered` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `order_items`
--
DELIMITER $$
CREATE TRIGGER `reduce_stock_after_order` AFTER INSERT ON `order_items` FOR EACH ROW UPDATE inventory
SET quantity = quantity - NEW.quantity_ordered
WHERE id = NEW.inventory_id
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `store_userprofile`
--

CREATE TABLE `store_userprofile` (
  `id` bigint(20) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `store_userprofile`
--

INSERT INTO `store_userprofile` (`id`, `role`, `created_at`, `user_id`) VALUES
(1, 'admin', '2025-05-02 17:25:53.322512', 1),
(33, 'manager', '2025-05-15 12:04:19.836285', 22),
(34, 'staff', '2025-05-15 12:04:33.210035', 23),
(35, 'supplier', '2025-05-15 12:04:51.852472', 24);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`, `contact_info`, `email`, `phone`, `created_at`) VALUES
(1, 'Fresh Veggies Ltd.', '123 Green St.', 'contact@freshveggies.com', '0123456789', '2025-02-25 10:11:25'),
(2, 'Dairy Co.', '45 Milk Road', 'sales@dairyco.com', '0987654321', '2025-02-25 10:11:25'),
(3, 'Meat Distributors Inc.', '78 Steak Ave.', 'info@meatdistributors.com', '0156789456', '2025-02-25 10:11:25');

-- --------------------------------------------------------

--
-- Table structure for table `supplier_deliverynotification`
--

CREATE TABLE `supplier_deliverynotification` (
  `id` bigint(20) NOT NULL,
  `message` longtext DEFAULT NULL,
  `delivery_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `supplier_supplierperformance`
--

CREATE TABLE `supplier_supplierperformance` (
  `id` bigint(20) NOT NULL,
  `total_orders` int(11) NOT NULL,
  `on_time_deliveries` int(11) NOT NULL,
  `late_deliveries` int(11) NOT NULL,
  `quality_rating` decimal(3,2) NOT NULL,
  `period_start` date NOT NULL,
  `period_end` date NOT NULL,
  `supplier_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `supplier_supplierprofile`
--

CREATE TABLE `supplier_supplierprofile` (
  `id` bigint(20) NOT NULL,
  `supplier_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `inventory_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `quantity_used` int(11) NOT NULL,
  `transaction_type` enum('added','removed','adjusted') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `inventory_id`, `user_id`, `quantity_used`, `transaction_type`, `created_at`) VALUES
(6, 1, 2, 5, 'removed', '2025-02-25 10:22:31');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','manager','staff','supplier') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'Admin User', 'admin@example.com', 'hashedpassword1', 'admin', '2025-02-25 10:11:25'),
(2, 'Manager User', 'manager@example.com', 'hashedpassword2', 'manager', '2025-02-25 10:11:25'),
(3, 'Staff User', 'staff@example.com', 'hashedpassword3', 'staff', '2025-02-25 10:11:25'),
(4, 'Supplier User', 'supplier@example.com', 'hashedpassword4', 'supplier', '2025-02-25 10:11:25');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `idx_item_name` (`item_name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `inventory_id` (`inventory_id`);

--
-- Indexes for table `store_userprofile`
--
ALTER TABLE `store_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `supplier_deliverynotification`
--
ALTER TABLE `supplier_deliverynotification`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_id` (`order_id`);

--
-- Indexes for table `supplier_supplierperformance`
--
ALTER TABLE `supplier_supplierperformance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `supplier_supplierprofile`
--
ALTER TABLE `supplier_supplierprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventory_id` (`inventory_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `store_userprofile`
--
ALTER TABLE `store_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `supplier_deliverynotification`
--
ALTER TABLE `supplier_deliverynotification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `supplier_supplierperformance`
--
ALTER TABLE `supplier_supplierperformance`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `supplier_supplierprofile`
--
ALTER TABLE `supplier_supplierprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `store_userprofile`
--
ALTER TABLE `store_userprofile`
  ADD CONSTRAINT `store_userprofile_user_id_6db609dc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
