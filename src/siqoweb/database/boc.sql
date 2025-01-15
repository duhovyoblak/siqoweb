/* ===============================================================================================
/*                                                                (c) SIQO 11', '12', '13', '24 */
/* Inicializacia projektu Battle of Causality v systeme PagMan
/* ver 3v01
/*----------------------------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------------------------*/
/* Zmazanie existujucej verzie Battle of Causality */

/* Resources */
DELETE FROM PM_OBJ_RESOURCE WHERE OBJ_ID   = 'Stage_BOC';
DELETE FROM PM_OBJ_RESOURCE WHERE CLASS_ID = 'PageBOC';

/* Homepage object */
DELETE FROM PM_OBJECT WHERE OBJ_ID   = 'Stage_BOC';
DELETE FROM PM_OBJECT WHERE CLASS_ID = 'PageBOC';

/*----------------------------------------------------------------------------------------------*/
/* Homepage object */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJECT       VALUES( 'PagManHomepage', 'Stage_BOC', '__STAG__', 'A', 'Internal PagMan page', DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* Resources */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '0_Stage', 'SK',   'A', 'Battle of causality',     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '0_Stage', 'POS',  'A', '5',                         DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '1_Item',  'SK',   'A', 'Battle of causality',     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '1_Item',  'TYPE', 'A', 'H2',                        DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '2_Item',  'SK',   'A', 'blah... blah... blah...',   DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '2_Item',  'TYPE', 'A', 'P',                         DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '6_Item',  'SK',   'A', 'Battle of causality is ', DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '6_Item',  'TYPE', 'A', 'P_START',                   DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'SK',   'A', 'waiting',                   DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'TYPE', 'A', 'A',                         DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '7_Item',  'URL',  'A', 'pgBoc',                     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '8_Item',  'SK',   'A', ' for You...',               DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PagManHomepage', 'Stage_BOC', '8_Item',  'TYPE', 'A', 'P_STOP',                    DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* BOC Page objects */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJECT       VALUES( 'PageBOC',        'HeadItems', '__HEAD__', 'A', 'Battle of causality',            DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJECT       VALUES( 'PageBOC',        'NavLinks',  '__NAVB__', 'A', 'Battle of causality',            DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJECT       VALUES( 'PageBOC',        'BOC_cont',  '__CONT__', 'A', 'Battle of causality',            DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* OHISTORY Page Forum Resources */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '1_Title',    'SK',    'A', 'Battle of causality',     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '1_Title',    'TYPE',  'A', 'HEADTITLE',                 DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '2_Comment',  'SK',    'A', 'Development environment',   DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '2_Comment',  'TYPE',  'A', 'HEADCOMMENT',               DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '3_SubTitle', 'SK',    'A', 'by Michal H',               DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'HeadItems',   '3_SubTitle', 'TYPE',  'A', 'HEADSUBTIT',                DATE('now'), DATE('now'), 'SIQO');

INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'NAME',  'A', 'BocWindow',                 DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'TYPE',  'A', 'WINDOW',                    DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'target','A', 'pgBoc',                     DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'height','A', '94%',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'width', 'A', '99%',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'CLASS', 'A', 'BOC',                       DATE('now'), DATE('now'), 'SIQO');
INSERT INTO PM_OBJ_RESOURCE VALUES( 'PageBOC',  'BOC_cont',    'BocObject',  'objId', 'A', 'BOC_A',                     DATE('now'), DATE('now'), 'SIQO');

/*----------------------------------------------------------------------------------------------*/
/* Meta */
/*----------------------------------------------------------------------------------------------*/
INSERT INTO PM_JOURNAL      VALUES ( NULL, DATE('now'), 'INTERNAL', 'SIQO', 'PAGMAN', 'boc.sql', 'PageBOC initialisation', 'OK', 0, 1, 'PageBOC', NULL);

/*====================================KONIEC SUBORU=============================================*/
