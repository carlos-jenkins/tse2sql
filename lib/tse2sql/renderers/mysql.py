# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Jenkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
MySQL SQL generator.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from logging import getLogger

from tqdm import tqdm


log = getLogger(__name__)


SCHEMA = """\
-- MySQL Script generated by MySQL Workbench
-- Thu 11 Feb 2016 08:09:35 PM CST
-- Model: TSE Voters MySQL Database    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema tsesql
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `tsesql` ;

-- -----------------------------------------------------
-- Schema tsesql
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tsesql` DEFAULT CHARACTER SET utf8 ;
USE `tsesql` ;

-- -----------------------------------------------------
-- Table `tsesql`.`province`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tsesql`.`province` (
  `id_province` TINYINT(1) UNSIGNED NOT NULL,
  `name` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id_province`))
ENGINE = InnoDB
COMMENT = 'Costa Rica has 7 provinces, plus one code for consulates.';


-- -----------------------------------------------------
-- Table `tsesql`.`canton`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tsesql`.`canton` (
  `id_canton` SMALLINT(3) UNSIGNED NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `province_id_province` TINYINT(1) UNSIGNED NOT NULL,
  PRIMARY KEY (`id_canton`, `province_id_province`),
  INDEX `fk_canton_province1_idx` (`province_id_province` ASC),
  CONSTRAINT `fk_canton_province1`
    FOREIGN KEY (`province_id_province`)
    REFERENCES `tsesql`.`province` (`id_province`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'As of 02/2016 Costa Rica has 81 cantons (124 if including consulates).\nThe largest name was \"REPUBLICA DOMINICANA\" (20 characters).';


-- -----------------------------------------------------
-- Table `tsesql`.`district`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tsesql`.`district` (
  `id_district` MEDIUMINT(6) UNSIGNED NOT NULL,
  `name` VARCHAR(34) NOT NULL,
  `canton_id_canton` SMALLINT(3) UNSIGNED NOT NULL,
  PRIMARY KEY (`id_district`, `canton_id_canton`),
  INDEX `fk_district_canton1_idx` (`canton_id_canton` ASC),
  CONSTRAINT `fk_district_canton1`
    FOREIGN KEY (`canton_id_canton`)
    REFERENCES `tsesql`.`canton` (`id_canton`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'As of 02/2016 Costa Rica has 2068 districts (2123 if including consulates).\nThe largest name was \"EMPALME ARRIBA GUARIA(PARTE OESTE)\" (34 characters).';


-- -----------------------------------------------------
-- Table `tsesql`.`voter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tsesql`.`voter` (
  `id_voter` INT UNSIGNED NOT NULL,
  `sex` TINYINT(1) UNSIGNED NOT NULL,
  `id_expiration` DATE NOT NULL,
  `site` MEDIUMINT(5) UNSIGNED NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `family_name_1` VARCHAR(26) NOT NULL,
  `family_name_2` VARCHAR(26) NOT NULL,
  `district_id_district` MEDIUMINT(6) UNSIGNED NOT NULL,
  PRIMARY KEY (`id_voter`, `district_id_district`),
  INDEX `fk_voter_district1_idx` (`district_id_district` ASC),
  CONSTRAINT `fk_voter_district1`
    FOREIGN KEY (`district_id_district`)
    REFERENCES `tsesql`.`district` (`id_district`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


"""  # noqa

SECTION_HEADER = """\
-- -----------------------------------------------------
-- Data for table `tsesql`.`{name}`
-- -----------------------------------------------------
"""


def write_provinces(fd, provinces):
    """
    Write provinces INSERT INTO statement.
    """
    fd.write(SECTION_HEADER.format(name='province'))

    with tqdm(
            total=len(provinces), unit='e', leave=True,
            desc='INSERT INTO province') as pbar:

        for province_code, name in provinces.items():
            fd.write('INSERT INTO province VALUES (')
            fd.write(str(province_code))
            fd.write(', \'')
            fd.write(name)
            fd.write('\');\n')
            pbar.update(1)

    fd.write('\n\n')


def write_cantons(fd, cantons):
    """
    Write cantons INSERT INTO statement.
    """
    fd.write(SECTION_HEADER.format(name='canton'))

    with tqdm(
            total=len(cantons), unit='e', leave=True,
            desc='INSERT INTO canton') as pbar:

        for (province_code, canton_code), name in cantons.items():
            fd.write('INSERT INTO canton VALUES (')
            fd.write(str(province_code))
            fd.write('{:02d}'.format(canton_code))
            fd.write(', \'')
            fd.write(name)
            fd.write('\', ')
            fd.write(str(province_code))
            fd.write(');\n')
            pbar.update(1)

    fd.write('\n\n')


def write_districts(fd, districts):
    """
    Write districts INSERT INTO statement.
    """
    fd.write(SECTION_HEADER.format(name='district'))

    with tqdm(
            total=len(districts), unit='e', leave=True,
            desc='INSERT INTO district') as pbar:

        for (province_code, canton_code, district_code), name \
                in districts.items():
            fd.write('INSERT INTO district VALUES (')
            fd.write(str(province_code))
            fd.write('{:02d}'.format(canton_code))
            fd.write('{:03d}'.format(district_code))
            fd.write(', \'')
            fd.write(name)
            fd.write('\', ')
            fd.write(str(province_code))
            fd.write('{:02d}'.format(canton_code))
            fd.write(');\n')
            pbar.update(1)

    fd.write('\n\n')


def write_voters(fd, voters):
    """
    Write voters INSERT INTO statement.
    """
    fd.write(SECTION_HEADER.format(name='voter'))

    with tqdm(
            total=voters.total_voters, unit='v', leave=True,
            unit_scale=True, desc='INSERT INTO voter') as pbar:

        for voter in voters:
            fd.write('INSERT INTO voter VALUES (')
            fd.write(str(voter['id'])),
            fd.write(', ')
            fd.write(str(voter['sex'])),
            fd.write(', \'')
            fd.write(voter['expiration'].strftime('%Y-%m-%d')),
            fd.write('\', ')
            fd.write(str(voter['site']))
            fd.write(', \'')
            fd.write(voter['name'])
            fd.write('\', \'')
            fd.write(voter['family_name_1'])
            fd.write('\', \'')
            fd.write(voter['family_name_2'])
            fd.write('\', ')
            fd.write(str(voter['district']))
            fd.write(');\n')
            pbar.update(1)

    fd.write('\n\n')


def write_mysql(fd, payload):
    """
    Write MySQL SQL output.

    :param fd: Output file descriptor.
    :param payload: Generation payload with provinces, cantons, districts and
     voters data.
    """
    fd.write(SCHEMA)
    write_provinces(fd, payload['provinces'])
    write_cantons(fd, payload['cantons'])
    write_districts(fd, payload['districts'])
    write_voters(fd, payload['voters'])


__all__ = ['write_mysql']
