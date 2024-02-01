/* ===============================================================================================
/*                                                                      (c) SIQO 11', '12', '13', '24 */
/* Inicializacia systemu PagMan
/* ver 3v01
/*----------------------------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------------------------*/
/* Zmazanie systemovych objektov */

/* Fakty */
DELETE FROM SITEM;
DELETE FROM SSESSION;
DELETE FROM SOBJ_RESOURCE;
DELETE FROM SOBJ_CACHE;
DELETE FROM SOBJ_USER_ROLE;

/* Dimenzie */
DELETE FROM SDMS;
DELETE FROM SOBJECT;
DELETE FROM SUSER;
DELETE FROM SLANGUAGE;

/* Meta */
DELETE FROM SPARAMETER;
DELETE FROM SJOURNAL;

/*----------------------------------------------------------------------------------------------*/
/* Inicializacia systemovych objektov */

/* Meta */
INSERT INTO SJOURNAL     VALUES ( NULL, SYSDATE(), 'INTERNAL', 'SIQO', 'PAGMAN', 'Journal', 'pagman.ini', 'Init...', 'OK', '0', '1', 'PagMan Init štart', NULL);

/* Zakladne parametre */
INSERT INTO SPARAMETER   VALUES ( 'DEBUG LEVEL',       30, 'Maximálna úroveň zapisovania žurnálu',          'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO');
INSERT INTO SPARAMETER   VALUES ( 'SESSION IDLE',     600, 'Maximálna doba nečinnosti session v sekundách', 'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO');
INSERT INTO SPARAMETER   VALUES ( 'SESSION TIMEOUT', 7200, 'Maximálna doba platnosti session v sekundách',  'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO');
INSERT INTO SPARAMETER   VALUES ( 'MAX LOGIN FAILS',    3, 'Maximálny počet zlyhaní loginu',                'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO');
INSERT INTO SPARAMETER   VALUES ( 'DMS ROOT',          '/volume1/web/DMS/', 'Absolútna adresa DMS systému', 'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO)';
INSERT INTO SPARAMETER   VALUES ( 'BACKUP ROOT',       '/volume1/web/backup/', 'Absolútna adresa adresára pre backup databázy', 'A', sysdate(), sysdate(), 'NULL', 'pagman.ini', 'SIQO)';

/* Languages */
INSERT INTO SLANGUAGE    VALUES ( 'SK', 'UTF-8', 'Slovenčina', sysdate(), 'SIQO');
INSERT INTO SLANGUAGE    VALUES ( 'EN', 'UTF-8', 'English',    sysdate(), 'SIQO');

/* Users */
INSERT INTO SUSER        VALUES ( 'SIQO',      'A', 'SK', 'P', 'System',       'User',        NULL, 'SIQO',        NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ( 'Anonymous', 'A', 'SK', 'P', 'Guest',        'User',        NULL, 'guest',       NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');

INSERT INTO SUSER        VALUES ( 'palo4',     'A', 'SK', 'P', 'Pavol',        'Horanský',    NULL, 'strc',        NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('lubka',      'A', 'SK', 'P', 'Ľubomíra',     'Horanská',    NULL, 'poklop',      NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('marek',      'A', 'SK', 'P', 'Marek',        'Horanský',    NULL, 'zomripotter', NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('michal',     'A', 'SK', 'P', 'Michal',       'Horanský',    NULL, 'hora5nsky',   NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');

INSERT INTO SUSER        VALUES ('astronaut1', 'A', 'SK', 'P', 'Anonymný',     'Astronaut 1', NULL, 'au1',         NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('e.sandra',   'A', 'SK', 'P', 'Eva Alexandra','Kubaská',     NULL, 'sandra',      NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('eva',        'A', 'SK', 'P', 'Eva',          'Horanská',    NULL, 'milan',       NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('hanka',      'A', 'SK', 'P', 'Hanka',        'Laktičová',   NULL, 'heslo',       NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
INSERT INTO SUSER        VALUES ('helenka',    'A', 'SK', 'P', 'Babička',      'Helenka',     NULL, 'boldizar',    NULL, 0, sysdate(), sysdate(), NULL, 'SIQO');
  
/* Object */
INSERT INTO SOBJECT       VALUES( 'PagManAdmin',     '__PAGE__', 'A', 'Internal PagMan page', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJECT       VALUES( 'PagManResource',  '__PAGE__', 'A', 'Internal PagMan page', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJECT       VALUES( 'SiqoHomepage',    '__PAGE__', 'A', 'Internal PagMan page', sysdate(), sysdate(), 'SIQO');

/* Object Resources */
INSERT INTO SOBJ_RESOURCE VALUES( 'PagManAdmin',    '__PAGE__', 'SK', 'HeaderTitle',     'Page Manager Administration Page',     'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'PagManAdmin',    '__PAGE__', 'SK', 'HeaderSubTitle',  'Development enviroment',               'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'PagManAdmin',    '__PAGE__', 'SK', 'Header COMMENT',  'Administrácia Page managera',          'VAL', sysdate(), sysdate(), 'SIQO');

INSERT INTO SOBJ_RESOURCE VALUES( 'PagManResource', '__PAGE__', 'SK', 'HeaderTitle',     'Page Manager Resource Administration', 'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'PagManResource', '__PAGE__', 'SK', 'HeaderSubTitle',  'Development enviroment',               'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'PagManResource', '__PAGE__', 'SK', 'Header COMMENT',  'Menežment resources Page Manager-a',   'VAL', sysdate(), sysdate(), 'SIQO');

INSERT INTO SOBJ_RESOURCE VALUES( 'SiqoHomepage',   '__PAGE__', 'SK', 'HeaderTitle',     'SIQO Homepage',                        'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'SiqoHomepage',   '__PAGE__', 'SK', 'HeaderSubTitle',  'Development enviroment',               'VAL', sysdate(), sysdate(), 'SIQO');
INSERT INTO SOBJ_RESOURCE VALUES( 'SiqoHomepage',   '__PAGE__', 'SK', 'Header COMMENT',  'Hlavná stránka projektu SIQO',         'VAL', sysdate(), sysdate(), 'SIQO');

/* Object-User-Role */

/* SESSION */
INSERT INTO SSESSION     VALUES ( 'INTERNAL', 'E', 'localhost', 'NO_AGENT', 'NO_HOST', 'Anonymous', 'NO_PAGE', 'SK', sysdate(), sysdate(), sysdate(), 'pagman.ini');
                                          
/* DOCUMENT ITEMS */										  
INSERT INTO SITEM        VALUES ( NULL, 0, 'SIQO', 'SYSFORUM', 'A', '0', 'SYSFORUM Root item', 'Palo4', 'SYSFORUM je defaultné fórum sytému PagMan Item', sysdate(), sysdate(), 'SIQO');

/* Meta */
INSERT INTO SJOURNAL     VALUES ( NULL, sysdate(), 'INTERNAL', 'SIQO', 'PAGMAN', 'Journal', 'pagman.ini', 'Init done', 'OK', 0, 1, 'PagMan Init stop', NULL);

/*===================================KONIEC SUBORU=============================================*/
