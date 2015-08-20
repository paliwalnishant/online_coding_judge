-- phpMyAdmin SQL Dump
-- version 4.0.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 09, 2015 at 01:40 AM
-- Server version: 5.6.14
-- PHP Version: 5.5.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `minor`
--

-- --------------------------------------------------------

--
-- Table structure for table `accepted`
--

CREATE TABLE IF NOT EXISTS `accepted` (
  `username` varchar(10) DEFAULT NULL,
  `quesname` varchar(10) DEFAULT NULL,
  `subtime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `accepted`
--

INSERT INTO `accepted` (`username`, `quesname`, `subtime`) VALUES
('12103483', 'INC', '2015-05-08 22:38:00');

-- --------------------------------------------------------

--
-- Table structure for table `loggedin`
--

CREATE TABLE IF NOT EXISTS `loggedin` (
  `username` varchar(20) DEFAULT NULL,
  `status` varchar(5) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `loggedin`
--

INSERT INTO `loggedin` (`username`, `status`, `ip`) VALUES
('12103483', 'YES', '192.168.43.80'),
('12103459', 'YES', '192.168.43.2'),
('12103462', 'NO', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `priv` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `priv`) VALUES
('admin1', 'admin1', 'admin'),
('12103483', 'nishant', 'user'),
('12103459', 'navneet', 'user'),
('12103462', 'shubhi', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE IF NOT EXISTS `questions` (
  `name` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`name`) VALUES
('INC'),
('DEC'),
('FAC');

-- --------------------------------------------------------

--
-- Table structure for table `score`
--

CREATE TABLE IF NOT EXISTS `score` (
  `username` varchar(20) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `score`
--

INSERT INTO `score` (`username`, `score`, `time`) VALUES
('12103483', 75, '00:00:00'),
('12103459', 0, '00:00:00'),
('12103462', 0, '00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `submission`
--

CREATE TABLE IF NOT EXISTS `submission` (
  `id` int(11) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `question` varchar(30) DEFAULT NULL,
  `language` varchar(5) DEFAULT NULL,
  `result` varchar(10) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `submission`
--

INSERT INTO `submission` (`id`, `username`, `question`, `language`, `result`, `time`, `filename`) VALUES
(2, '12103483', 'INC', 'c', 'ACCEPTED', '2015-05-08 22:38:00', 'files/2inc.c'),
(4, '12103483', 'INC', 'cpp', 'COMPILATIO', '2015-05-08 22:38:55', 'files/4Client_1gui.py');

-- --------------------------------------------------------

--
-- Table structure for table `temp`
--

CREATE TABLE IF NOT EXISTS `temp` (
  `username` varchar(20) NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `temp`
--

INSERT INTO `temp` (`username`, `score`) VALUES
('12103483', 2147483647),
('12103483', 0),
('12103459', 100),
('12103462', 100);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
