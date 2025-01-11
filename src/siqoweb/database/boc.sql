/* ===============================================================================================
/*                                                                (c) SIQO 11', '12', '13', '24 */
/* Inicializacia projektu Battle of Causality v systeme PagMan
/* ver 3v01
/*----------------------------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------------------------*/
/* Zmazanie existujucej verzie Battle of Causality */

/* Resources */
DELETE FROM PM_OBJ_RESOURCE WHERE OBJ_ID   = 'Stage_BOC';
--DELETE FROM PM_OBJ_RESOURCE WHERE CLASS_ID = '';

/* Homepage object */
DELETE FROM PM_OBJECT WHERE OBJ_ID   = 'Stage_BOC';
--DELETE FROM PM_OBJECT WHERE CLASS_ID = 'OHISTORY';

/*----------------------------------------------------------------------------------------------*/
/* Homepage object */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJECT       VALUES( 'PagManHomepage', 'Stage_BOC', '__STAG__', 'A', 'Internal PagMan page', DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* Resources */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '0_Stage', 'SK',   'A', 'Oral History',            DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '0_Stage', 'POS',  'A', '2',                       DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '1_Item',  'SK',   'A', 'Oral History',            DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '1_Item',  'TYPE', 'A', 'H2',                      DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '2_Item',  'SK',   'A', 'Veľká história sa zaoberá veľkými udalosťami, ktoré ovplyvnia mnoho ľudí a zvyčajne sa nezaobídu bez príslušného počtu mŕtvol alebo aspoň jedu, dýky a kráľa. Tieto príbehy sú také veľké, že sa nedokážu dostať k nášmu srdcu a dotýkajú sa nás asi ako boje medzi zelenokožími citrusmi v susednej galaxii.', DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '2_Item',  'TYPE', 'A', 'P',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '3_Item',  'SK',   'A', 'Príbehy ',                DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '3_Item',  'TYPE', 'A', 'P_START',                 DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '4_Item',  'SK',   'A', 'oral history ',           DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '4_Item',  'TYPE', 'A', 'A',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '4_Item',  'URL',  'A', 'pgOhistory',             DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '5_Item',  'SK',   'A', ' sú malé, omnoho menšie ako tie z učebníc dejepisu. Sú dostatočne drobné na to, aby sa dostali k nášmu vnútru a zanechali tam stopu. Tieto príbehy sa stali ľuďom, ktorí sa na nás veľmi podobali. Skoro by sa mohli stať aj nám, keby sme tam vtedy boli.', DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '5_Item',  'TYPE', 'A', 'P_STOP',                  DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '6_Item',  'SK',   'A', 'Ráčte ',                  DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '6_Item',  'TYPE', 'A', 'P_START',                 DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'SK',   'A', 'vstúpiť ',                DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'TYPE', 'A', 'A',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'URL',  'A', 'pgOhistory',             DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '8_Item',  'SK',   'A', '',                        DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '8_Item',  'TYPE', 'A', 'P_STOP',                  DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* OHISTORY Page Forum object */
/*----------------------------------------------------------------------------------------------*/
--INSERT INTO PM_OBJECT       VALUES( 'OHISTORY',  'HeadItems',   '__HEAD__', 'A', 'Oral history',               DATE('now'), DATE('now'), 'SIQO');
--INSERT INTO PM_OBJECT       VALUES( 'OHISTORY',  'NavLinks',    '__NAVB__', 'A', 'Oral history',               DATE('now'), DATE('now'), 'SIQO');
--INSERT INTO PM_OBJECT       VALUES( 'OHISTORY',  'OHIST_cont',  '__CONT__', 'A', 'Oral history',               DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* OHISTORY Page Forum Resources */
/*----------------------------------------------------------------------------------------------*/
/*
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '1_Title',    'SK',    'A', 'Oral History',            DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '1_Title',    'TYPE',  'A', 'HEADTITLE',               DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '2_Comment',  'SK',    'A', 'Development environment', DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '2_Comment',  'TYPE',  'A', 'HEADCOMMENT',             DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '3_SubTitle', 'SK',    'A', 'Fórum projektu SIQO',     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'HeadItems',   '3_SubTitle', 'TYPE',  'A', 'HEADSUBTIT',              DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','NAME',  'A', 'ForumWindow',             DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','TYPE',  'A', 'WINDOW',                  DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','target','A', 'pgOhistory',              DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','height','A', '94%',                     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','width', 'A', '99%',                     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','CLASS', 'A', 'FORUM',                   DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'OHISTORY',  'OHIST_cont',  'ForumObject','objId', 'A', 'OHISTORY',                DATE('now'), DATE('now'), 'SIQO');
*/


/*----------------------------------------------------------------------------------------------*/
/* Meta */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_JOURNAL      VALUES ( NULL, DATE('now'), 'INTERNAL', 'SIQO', 'PAGMAN', 'homepage.ini', 'Homepage initialisation', 'OK', 0, 1, 'PagMan Init', NULL);

/*====================================KONIEC SUBORU=============================================*/
