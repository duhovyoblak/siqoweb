/*------------------------------------------------------*/
/* Table SJOURNAL
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SJOURNAL;

CREATE TABLE IF NOT EXISTS SJOURNAL (
   JOURNAL_SID  INTEGER          NOT NULL               /*  Identifikácia záznamu INTEGER PRIMARY KEY will autoincrement */
  ,D_CREATED    TIMESTAMP        NOT NULL               /*  Čas vzniku záznamu */
  ,USER_ID      VARCHAR(32)      NOT NULL               /*  User ktorý bol prihlásený pri vzniku záznamu */
  ,PAGE_ID      VARCHAR(32)      NOT NULL               /*  Identifikácia stránky na ktorej vznikol záznam */
  ,OBJ_ID       VARCHAR(32)      NOT NULL               /*  Identifikácia objektu */
  ,SOURCE       VARCHAR(32)      NOT NULL               /*  Metóda, v ktorej záznam vznikol */
  ,C_ACT        VARCHAR(32)      NOT NULL               /*  Kód akcie */
  ,C_RES        CHAR(3)          NOT NULL               /*  Výsledok akcie OK/WN/ER */
  ,N_ROWC       BIGINT(5)        NOT NULL               /*  Počet dotknutých riadkov/objektov */
  ,N_LVL        SMALLINT         NOT NULL               /*  Závažnosť chybového stavu */
  ,STAT         VARCHAR(4000)        NULL               /*  Vyhodnocovaný výraz */
  ,ERR          VARCHAR(128)         NULL               /*  Kód chyby */

  ,PRIMARY KEY (JOURNAL_SID)
)
/* Žurnál udalostí o objektoch, menežovaných PagMan-om */
;

/*------------------------------------------------------*/
/* Table SLANGUAGE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SLANGUAGE;

CREATE TABLE IF NOT EXISTS SLANGUAGE (
   LANG_ID      VARCHAR(32)      NOT NULL               /*  Language code */
  ,CODEPAGE     VARCHAR(32)      NOT NULL
  ,NAME         VARCHAR(128)     NOT NULL
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,WHO          VARCHAR(32)      NOT NULL

  ,PRIMARY KEY (LANG_ID)
)
;

/*------------------------------------------------------*/
/* Table SPARAMETER */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SPARAMETER;

CREATE TABLE IF NOT EXISTS SPARAMETER (
   PARAM_ID     VARCHAR(32)      NOT NULL
  ,S_VAL        VARCHAR(256)     NOT NULL
  ,NAME         VARCHAR(128)     NOT NULL
  ,C_FUNC       CHAR(1)          DEFAULT 'A'
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,D_CHANGED    TIMESTAMP        NOT NULL
  ,D_CLOSED     TIMESTAMP            NULL
  ,NOTES        VARCHAR(4000)        NULL
  ,WHO          VARCHAR(32)      DEFAULT 'SIQO'

  ,PRIMARY KEY (PARAM_ID)
)
;

/*------------------------------------------------------*/
/* Table SOBJECT */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SOBJECT;

CREATE TABLE IF NOT EXISTS SOBJECT (
   PAGE_ID      VARCHAR(32)      NOT NULL
  ,OBJ_ID       VARCHAR(32)      NOT NULL
  ,C_FUNC       CHAR(1)          NOT NULL
  ,NOTES        VARCHAR(4000)        NULL
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,D_CHANGED    TIMESTAMP        NOT NULL
  ,WHO          VARCHAR(32)      DEFAULT 'SIQO'

  ,PRIMARY KEY (PAGE_ID, OBJ_ID)
)
/* Zoznam objektov, používaných v SPAGE a menežovaných PageMan-om. Objekty môžu byť rôzneho druhu, napr. stránka, objekt na stránke, proces, atď. Objekt je základnou jednotkou riadenia práv */
;

/*------------------------------------------------------*/
/* Table SOBJ_RESOURCE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SOBJ_RESOURCE ;

CREATE TABLE IF NOT EXISTS SOBJ_RESOURCE (
   PAGE_ID      VARCHAR(32)      NOT NULL
  ,OBJ_ID       VARCHAR(32)      NOT NULL
  ,LANG_ID      VARCHAR(32)      NOT NULL
  ,S_KEY        VARCHAR(32)      NOT NULL
  ,S_VAL        VARCHAR(4000)    DEFAULT 'Test string'
  ,C_TYPE       VARCHAR(8)       DEFAULT 'VAL'
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,D_CHANGED    TIMESTAMP            NULL                /*  Meta */
  ,WHO          VARCHAR(32)      DEFAULT 'SIQO'

  ,PRIMARY KEY (PAGE_ID, OBJ_ID, LANG_ID, S_KEY)
  ,FOREIGN KEY (LANG_ID)         REFERENCES SLANGUAGE(LANG_ID)
  ,FOREIGN KEY (PAGE_ID, OBJ_ID) REFERENCES SOBJECT  (PAGE_ID, OBJ_ID)
)
/* Staticka cache literalov a vyhodnotitelnych vyrazov pre kombinaciu PAGE/LANGUAGE/OBJECT */
;

CREATE INDEX FKI_RES_LANG ON SOBJ_RESOURCE(LANG_ID);
CREATE INDEX FKI_RES_OBJ  ON SOBJ_RESOURCE(PAGE_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table SUSER */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SUSER;

CREATE TABLE IF NOT EXISTS SUSER (
   USER_ID      VARCHAR(32)      NOT NULL                /*  Identifikácia usera, Login */
  ,C_FUNC       CHAR(1)          DEFAULT 'L'             /*  Users account status: W waiting for authentification A active L locked D deleted */
  ,LANG_ID      VARCHAR(32)      DEFAULT 'SK'            /*  Kod jazyka usera. Platí pre všetky aplikácie */
  ,C_TYPE       CHAR(1)          DEFAULT 'P'             /*  Users type:A application P person */
  ,FNAME        VARCHAR(64)          NULL                /*  First name */
  ,LNAME        VARCHAR(64)      NOT NULL                /*  Last name */
  ,EMAIL        VARCHAR(128)         NULL                /*  E-mail address for authentification */
  ,PASSWORD     VARCHAR(32)      DEFAULT 'heslo'         /*  Password by md5 */
  ,AUTHENT      VARCHAR(128)         NULL                /*  Authentification code */
  ,N_FAILS      TINYINT          DEFAULT 0               /*  failed connections count */
  ,D_CREATED    TIMESTAMP        NOT NULL                /*  creations date */
  ,D_CHANGED    TIMESTAMP        NOT NULL                /*  Date of last connection */
  ,D_LOCKED     TIMESTAMP            NULL                /*  Meta last chage date */
  ,WHO          VARCHAR(32)      NOT NULL                /*  Meta */
  
  ,PRIMARY KEY (USER_ID)
  ,FOREIGN KEY (LANG_ID)         REFERENCES SLANGUAGE(LANG_ID)
)
/* Zoznam userov Page managera */
;

CREATE INDEX FKI_USR_LANG ON SUSER(LANG_ID);

/*------------------------------------------------------*/
/* Table SSESSION */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SSESSION;

CREATE TABLE IF NOT EXISTS SSESSION (
   SESSION_ID   VARCHAR(32)      NOT NULL                /*  Sssion ID */
  ,C_FUNC       CHAR(1)          DEFAULT 'E'             /*  Stav session A aktívna E exspirovaná R zrušená pre nesúlad NK */
  ,USER_ADDRESS VARCHAR(32)      DEFAULT 'localhost'     /*  IP adresa klienta, ktorý volá stránku */
  ,USER_AGENT   VARCHAR(128)     DEFAULT 'NO_AGENT'      /*  Identifikácia agenta (prehliadača), ktorý volá stránku */
  ,USER_HOST    VARCHAR(128)     DEFAULT 'NO_HOST'
  ,USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'     /*  User, priradený session */
  ,PAGE_ID      VARCHAR(32)      DEFAULT 'NO_PAGE'
  ,LANG_ID      VARCHAR(32)      DEFAULT 'SK'
  ,D_CREATED    TIMESTAMP        NOT NULL                /*  Čas vzniku session */
  ,D_CHANGED    TIMESTAMP        NOT NULL                /*  Čas zmeny hodnôt (najmä refresh) session */
  ,D_CLOSED     TIMESTAMP            NULL                /*  Čas exspirácie a/lebo zrušenia session */
  ,MESSAGE      VARCHAR(1024)        NULL
  
  ,PRIMARY KEY (SESSION_ID)
  ,FOREIGN KEY (USER_ID)    REFERENCES SUSER (USER_ID)
)
;

CREATE INDEX FKI_SESS_USR ON SSESSION(USER_ID);

/*------------------------------------------------------*/
/* Table SOBJ_USER_ROLE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SOBJ_USER_ROLE;

CREATE TABLE IF NOT EXISTS SOBJ_USER_ROLE (
   USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'
  ,PAGE_ID      VARCHAR(32)      DEFAULT 'PAGMAN'
  ,OBJ_ID       VARCHAR(32)      DEFAULT 'PagManObject'
  ,S_ROLE       VARCHAR(32)      DEFAULT 'Unknown'
  ,C_FUNC       CHAR(1)          DEFAULT 'A'            /*  Stav autorizacie pre rolu A aktivna N neaktivna */
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,D_CHANGED    TIMESTAMP        NOT NULL               /*  Meta */
  ,WHO          VARCHAR(32)      DEFAULT SIQO           /*  Meta */
  
  ,PRIMARY KEY (USER_ID, PAGE_ID, OBJ_ID)
  ,FOREIGN KEY (USER_ID)         REFERENCES SUSER   (USER_ID)
  ,FOREIGN KEY (PAGE_ID, OBJ_ID) REFERENCES SOBJECT (PAGE_ID, OBJ_ID)
)
/*  Autorizacie ROLE pre kombinaciu USER/OBJECT */
;

CREATE INDEX FKI_ROL_OBJ ON SOBJ_USER_ROLE(PAGE_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table SOBJ_CACHE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SOBJ_CACHE;

CREATE TABLE IF NOT EXISTS SOBJ_CACHE (
   USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'
  ,PAGE_ID      VARCHAR(32)      NOT NULL
  ,OBJ_ID       VARCHAR(32)      NOT NULL
  ,S_KEY        VARCHAR(32)      NOT NULL               /*  Kluc hodnoty */
  ,S_VAL        VARCHAR(4000)    NOT NULL               /*  Hodnota kluca */
  ,D_CHANGED    TIMESTAMP        NOT NULL               /*  Meta */
  
  ,PRIMARY KEY (USER_ID, PAGE_ID, OBJ_ID, S_KEY)
  ,FOREIGN KEY (USER_ID)         REFERENCES SUSER (USER_ID)
  ,FOREIGN KEY (PAGE_ID, OBJ_ID) REFERENCES SOBJECT (PAGE_ID, OBJ_ID)
)
/* Cache OBJECT/USER na perzistentné ukladanie hodnôt, vložených userom alebo získaných v priebehu práce s aplikáciou. Cache neexspiruje, ale prepisuje sa pri každom volaní */
;

CREATE INDEX FKI_CACH_USR ON SOBJ_CACHE(USER_ID);
CREATE INDEX FKI_CACH_OBJ ON SOBJ_CACHE(PAGE_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table SDMS */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SDMS;

CREATE TABLE IF NOT EXISTS SDMS (
   DOC_ID       INTEGER          NOT NULL               /*  ID dokumentu INTEGER PRIMARY KEY will autoincrement */
  ,C_FUNC       CHAR(1)          DEFAULT 'E'            /*  Satv dokumentu */
  ,USER_ID      VARCHAR(32)      NOT NULL               /*  Vlastnik dokumentu */
  ,D_CREATED    TIMESTAMP        NOT NULL               /*  Datum vlozenia do DMS */
  ,C_TYPE       VARCHAR(8)       NOT NULL               /*  Typ dokumentu - fileextension */
  ,FILENAME     VARCHAR(128)     NOT NULL               /*  Nazov suboru v DMS */
  ,ORIGNAME     VARCHAR(128)     NOT NULL               /*  Nazov originalneho suboru */
  ,THUMBNAME    VARCHAR(128)         NULL               /*  Nazov suboru nahladu dokumentu */
  ,N_SIZE       INT                  NULL               /*  Velkost dokumentu v Byte */
  ,C_PUB        CHAR(1)          DEFAULT 'N'            /*  Priznak PUBLIC (Y/N) */
  ,TITLE        VARCHAR(128)         NULL               /*  Nazov dokumentu */
  ,NOTES        VARCHAR(4000)        NULL               /*  Poznamky k dokumentu */
  ,D_VALID      INT                  NULL               /*  Datum zaciatku platnosti dokumentu */
  ,D_EXPIRY     INT                  NULL               /*  Datum konca platnosti dokumentu */
  ,MD5          VARCHAR(64)          NULL               /*  Hash of the file */
  
  ,PRIMARY KEY (DOC_ID)
  ,FOREIGN KEY (USER_ID)         REFERENCES SUSER (USER_ID)
)
/* Master tabulka Data Management Systemu */
;

CREATE INDEX FKI_DMS_USR ON SDMS(USER_ID);

/*------------------------------------------------------*/
/* Table SITEM */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SITEM;

CREATE TABLE IF NOT EXISTS SITEM (
   ITEM_ID      INTEGER              NOT NULL           /*  Identifikácia Itemu. INTEGER PRIMARY KEY will autoincrement */
  ,PARENT_ID    INT                  DEFAULT 0          /*  Identifikácia Itemu-rodiča */
  ,USER_ID      VARCHAR(32)          NOT NULL           /*  Majiteľ itemu */
  ,FORUM_ID     VARCHAR(32)          DEFAULT 'SYSTEM'   /*  Identifikacia fora */
  ,C_FUNC       CHAR(1)              DEFAULT 'N'        /*  Funkčnosť Itemu (New, Active, Deleted) */
  ,N_LVL        INT                  DEFAULT 0          /*  Úroveň vnorenia do stromovej štruktúry */
  ,TITLE        VARCHAR(128)             NULL           /*  Názov Itemu */
  ,NARRATOR     VARCHAR(128)             NULL           /*  Rozprávač - kontext */
  ,ITEM         VARCHAR(16383)       NOT NULL           /*  Obsah Itemu */
  ,D_CREATED    TIMESTAMP            NOT NULL           /*  Dátum vytvorenia Itemu */
  ,D_CHANGED    TIMESTAMP            NOT NULL           /*  Dátum poslednej zmeny Itemu */
  ,WHO          VARCHAR(32)          NOT NULL           /*  User ID, ktorý vykonal poslednú zmenu */

  ,PRIMARY KEY (ITEM_ID)
  ,FOREIGN KEY (USER_ID)    REFERENCES SUSER (USER_ID)
)
/* Zoznam textov usporiadanych do vlaken */
;

CREATE INDEX FKI_ITM_USR ON SITEM(USER_ID);

/*------------------------------------------------------*/
/* Table SBACKUP */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS SBACKUP;

CREATE TABLE IF NOT EXISTS SBACKUP (
   BACKUP_ID    INTEGER              NOT NULL           /* INTEGER PRIMARY KEY will autoincrement */
  ,TITLE        VARCHAR(128)         NOT NULL
  ,D_CREATED    VARCHAR(45)          NOT NULL
  ,C_FUNC       CHAR(1)              NOT NULL
  ,USER_ID      VARCHAR(32)          NOT NULL
  ,NOTES        VARCHAR(128)             NULL

  ,PRIMARY KEY (BACKUP_ID)
)
/* Zoznam backupov databazy PagMan */
;

/*------------------------------------------------------*/
/*                 Koniec suboru                        */
/*------------------------------------------------------*/
