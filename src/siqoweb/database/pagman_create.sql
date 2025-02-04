/*------------------------------------------------------*/
/* Table PM_JOURNAL
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_JOURNAL;

CREATE TABLE IF NOT EXISTS PM_JOURNAL (
   JOURNAL_SID  INTEGER          NOT NULL                     /*  Identifikácia záznamu INTEGER PRIMARY KEY will autoincrement */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /*  Čas vzniku záznamu */
  ,USER_ID      VARCHAR(32)      NOT NULL                     /*  User ktorý bol prihlásený pri vzniku záznamu */
  ,PAGE_ID      VARCHAR(32)      NOT NULL                     /*  Identifikácia stránky na ktorej vznikol záznam */
  ,OBJ_ID       VARCHAR(32)      NOT NULL                     /*  Identifikácia objektu */
  ,SOURCE       VARCHAR(32)      NOT NULL                     /*  Metóda, v ktorej záznam vznikol */
  ,C_ACT        VARCHAR(32)      NOT NULL                     /*  Kód akcie */
  ,C_RES        CHAR(3)          NOT NULL                     /*  Výsledok akcie OK/WN/ER */
  ,N_ROWC       BIGINT(5)        NOT NULL                     /*  Počet dotknutých riadkov/objektov */
  ,N_LVL        SMALLINT         NOT NULL                     /*  Závažnosť chybového stavu */
  ,STAT         VARCHAR(4000)        NULL                     /*  Vyhodnocovaný výraz */
  ,ERR          VARCHAR(128)         NULL                     /*  Kód chyby */

  ,PRIMARY KEY (JOURNAL_SID)
)
/* Žurnál udalostí o objektoch, menežovaných PagMan-om */
;

/*------------------------------------------------------*/
/* Table PM_LANGUAGE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_LANGUAGE;

CREATE TABLE IF NOT EXISTS PM_LANGUAGE (
   LANG_ID      VARCHAR(32)      NOT NULL                     /* Language code */
  ,CODEPAGE     VARCHAR(32)      NOT NULL
  ,NAME         VARCHAR(128)     NOT NULL
  ,D_CREATED    TIMESTAMP        NOT NULL
  ,WHO          VARCHAR(32)      NOT NULL

  ,PRIMARY KEY (LANG_ID)
)
;

/*------------------------------------------------------*/
/* Table PM_PARAMETER */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_PARAMETER;

CREATE TABLE IF NOT EXISTS PM_PARAMETER (
   PARAM_ID     VARCHAR(32)      NOT NULL                     /* Jednoznačná identifikácia parametra */

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
/* Table PM_USER */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_USER;

CREATE TABLE IF NOT EXISTS PM_USER (
   USER_ID      VARCHAR(32)      NOT NULL                     /* Jednoznačná dentifikácia usera, Login */

  ,C_TYPE       CHAR(1)          DEFAULT 'P'                  /* User type: A application P person */
  ,C_FUNC       CHAR(1)          DEFAULT 'L'                  /* Users account status: W waiting for authentification A active L locked D deleted */
  ,LANG_ID      VARCHAR(32)      DEFAULT 'SK'                 /* Kod jazyka usera. Platí pre všetky aplikácie */
  ,FNAME        VARCHAR(64)          NULL                     /* First name */
  ,LNAME        VARCHAR(64)      NOT NULL                     /* Last name */
  ,EMAIL        VARCHAR(128)         NULL                     /* E-mail address for authentification */
  ,PASSWORD     VARCHAR(32)      DEFAULT 'heslo'              /* Password hash */
  ,AUTH_CODE    VARCHAR(128)         NULL                     /* Authentification code for email authentification*/
  ,N_FAILS      TINYINT          DEFAULT 0                    /* failed connections count */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* creations date */
  ,D_CHANGED    TIMESTAMP        NOT NULL                     /* Date of last connection */
  ,D_LOCKED     TIMESTAMP            NULL                     /* Meta last chage date */
  ,WHO          VARCHAR(32)      NOT NULL                     /* User ktorý vykonal ostatnú zmenu */

  ,PRIMARY KEY (USER_ID)
--  ,FOREIGN KEY (LANG_ID)         REFERENCES PM_LANGUAGE(LANG_ID)
)
/* Zoznam userov Page managera */
;

CREATE INDEX FKI_USR_LANG ON PM_USER(LANG_ID);

/*------------------------------------------------------*/
/* Table PM_OBJECT */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_OBJECT;

CREATE TABLE IF NOT EXISTS PM_OBJECT (
   CLASS_ID     VARCHAR(32)      NOT NULL                     /* Typ objektu/stránka - časť primárneho kľúča */
  ,OBJ_ID       VARCHAR(32)      NOT NULL                     /* Jednoznačná identifikácia objektu vrámci stránky - časť primárneho kľúča */

  ,OBJ_PAR      VARCHAR(32)      NOT NULL DEFAULT '__PAGE__'  /* Parent objekt, musí patriť CLASS_ID */
  ,C_FUNC       CHAR(1)          NOT NULL                     /* Object status A aktívny N neaktívny */
  ,NOTES        VARCHAR(4000)        NULL                     /* Poznámky k objektu */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* Dátum vytvorenia objektu */
  ,D_CHANGED    TIMESTAMP        NOT NULL                     /* Dátum ostatnej zmeny objektu */
  ,WHO          VARCHAR(32)      DEFAULT 'SIQO'               /* User ktorý vykonal ostatnú zmenu objektu */

  ,PRIMARY KEY (CLASS_ID, OBJ_ID)
)
/* Zoznam objektov, používaných v SPAGE a menežovaných PageMan-om. Objekty môžu byť rôzneho druhu, napr. stránka, objekt na stránke, proces, atď. Objekt je základnou jednotkou riadenia práv */
;

/*------------------------------------------------------*/
/* Table PM_OBJ_RESOURCE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_OBJ_RESOURCE ;

CREATE TABLE IF NOT EXISTS PM_OBJ_RESOURCE (
   CLASS_ID     VARCHAR(32)      NOT NULL                     /* Typ objektu/stránka ktorej objekt patrí - časť primárneho kľúča */
  ,OBJ_ID       VARCHAR(32)      NOT NULL                     /* Jednoznačná identifikácia objektu vrámci stránky - časť primárneho kľúča */
  ,ITEM_ID      VARCHAR(32)      NOT NULL                     /* Identifikácia itemu vrámci objektu - časť primárneho kľúča */
  ,S_KEY        VARCHAR(32)      NOT NULL                     /* Kľúč resource hodnoty (LANG/TYPE/CLASS/...)- časť primárneho kľúča */

  ,C_FUNC       CHAR(1)          NOT NULL                     /* Resource status A aktívny N neaktívny */
  ,S_VAL        VARCHAR(4000)    DEFAULT 'Test string'        /* Hodnota resource */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* Dátum vytvorenia resource */
  ,D_CHANGED    TIMESTAMP            NULL                     /* Dátum ostatnej zmeny resource */
  ,WHO          VARCHAR(32)      DEFAULT 'SIQO'               /* User ktorý vykonal ostatnú zmenu objektu */

  ,PRIMARY KEY (CLASS_ID, OBJ_ID, ITEM_ID, S_KEY)
--  ,FOREIGN KEY (CLASS_ID, OBJ_ID) REFERENCES PM_OBJECT (CLASS_ID, OBJ_ID)
)
/* Staticka cache literalov a vyhodnotitelnych vyrazov pre kombinaciu PAGE/LANGUAGE/OBJECT */
;

CREATE INDEX FKI_RES_OBJ  ON PM_OBJ_RESOURCE(CLASS_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table PM_OBJ_USER_ROLE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_OBJ_USER_ROLE;

CREATE TABLE IF NOT EXISTS PM_OBJ_USER_ROLE (
   CLASS_ID     VARCHAR(32)      DEFAULT 'PAGMAN'             /* Typ objektu/stránka ktorej objekt patrí - časť primárneho kľúča */
  ,OBJ_ID       VARCHAR(32)      DEFAULT 'PagManObject'       /* Jednoznačná identifikácia objektu vrámci stránky - časť primárneho kľúča */
  ,USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'          /*  Jednoznačná dentifikácia usera - časť primárneho kľúča */

  ,S_ROLE       VARCHAR(32)      DEFAULT 'Unknown'            /* Hodnota autorizácie usera k objektu */
  ,C_FUNC       CHAR(1)          DEFAULT 'A'                  /* Stav autorizacie pre rolu A aktivna N neaktivna */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* Dátum vytvorenia autorizácie */
  ,D_CHANGED    TIMESTAMP        NOT NULL                     /* Dátum ostatnej zmeny autorizácie */
  ,WHO          VARCHAR(32)      DEFAULT SIQO                 /* User ktorý vykonal ostatnú zmenu objektu */

  ,PRIMARY KEY (PAGE_ID, OBJ_ID, USER_ID)
--  ,FOREIGN KEY (USER_ID)         REFERENCES PM_USER   (USER_ID)
--  ,FOREIGN KEY (PAGE_ID, OBJ_ID) REFERENCES PM_OBJECT (PAGE_ID, OBJ_ID)
)
/*  Autorizacie ROLE pre kombinaciu USER/OBJECT */
;

CREATE INDEX FKI_ROL_OBJ ON PM_OBJ_USER_ROLE(PAGE_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table PM_OBJ_CACHE */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_OBJ_CACHE;

CREATE TABLE IF NOT EXISTS PM_OBJ_CACHE (
   PAGE_ID      VARCHAR(32)      NOT NULL                     /* Stránka ktorej objekt patrí - časť primárneho kľúča */
  ,OBJ_ID       VARCHAR(32)      NOT NULL                     /* Jednoznačná identifikácia objektu vrámci stránky - časť primárneho kľúča */
  ,USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'          /* Jednoznačná dentifikácia usera - časť primárneho kľúča */
  ,S_KEY        VARCHAR(32)      NOT NULL                     /* Kľúč hodnoty - časť primárneho kľúča */

  ,S_VAL        VARCHAR(4000)    NOT NULL                     /* Hodnota cache */
  ,D_CHANGED    TIMESTAMP        NOT NULL                     /* Dátum ostatnej zmeny cache */

  ,PRIMARY KEY (PAGE_ID, OBJ_ID, USER_ID, S_KEY)
--  ,FOREIGN KEY (USER_ID)         REFERENCES PM_USER (USER_ID)
--  ,FOREIGN KEY (PAGE_ID, OBJ_ID) REFERENCES PM_OBJECT (PAGE_ID, OBJ_ID)
)
/* Cache OBJECT/USER na perzistentné ukladanie hodnôt, vložených userom alebo získaných v priebehu práce s aplikáciou. Cache neexspiruje, ale prepisuje sa pri každom volaní */
;

CREATE INDEX FKI_CACH_USR ON PM_OBJ_CACHE(USER_ID);
CREATE INDEX FKI_CACH_OBJ ON PM_OBJ_CACHE(PAGE_ID, OBJ_ID);

/*------------------------------------------------------*/
/* Table PM_SESSION */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_SESSION;

CREATE TABLE IF NOT EXISTS PM_SESSION (
   SESSION_ID   VARCHAR(32)      NOT NULL                     /* Sssion ID */

  ,C_FUNC       CHAR(1)          DEFAULT 'E'                  /* Stav session A aktívna E exspirovaná R zrušená pre nesúlad NK */
  ,USER_ADDRESS VARCHAR(32)      DEFAULT 'localhost'          /* IP adresa klienta, ktorý volá stránku */
  ,USER_AGENT   VARCHAR(128)     DEFAULT 'NO_AGENT'           /* Identifikácia agenta (prehliadača), ktorý volá stránku */
  ,USER_HOST    VARCHAR(128)     DEFAULT 'NO_HOST'
  ,USER_ID      VARCHAR(32)      DEFAULT 'Anonymous'          /* User, priradený session */
  ,PAGE_ID      VARCHAR(32)      DEFAULT 'NO_PAGE'
  ,LANG_ID      VARCHAR(32)      DEFAULT 'SK'
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* Čas vzniku session */
  ,D_CHANGED    TIMESTAMP        NOT NULL                     /* Čas zmeny hodnôt (najmä refresh) session */
  ,D_CLOSED     TIMESTAMP            NULL                     /* Čas exspirácie a/lebo zrušenia session */
  ,MESSAGE      VARCHAR(1024)        NULL

  ,PRIMARY KEY (SESSION_ID)
--  ,FOREIGN KEY (USER_ID)    REFERENCES PM_USER (USER_ID)
)
;

CREATE INDEX FKI_SESS_USR ON PM_SESSION(USER_ID);

/*------------------------------------------------------*/
/* Table PM_DMS */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_DMS;

CREATE TABLE IF NOT EXISTS PM_DMS (
   DOC_ID       INTEGER          NOT NULL                     /* ID dokumentu INTEGER PRIMARY KEY will autoincrement */

  ,C_FUNC       CHAR(1)          DEFAULT 'E'                  /* Stav dokumentu E entered A aktívny D Neaktivny */
  ,USER_ID      VARCHAR(32)      NOT NULL                     /* Vlastnik dokumentu */
  ,D_CREATED    TIMESTAMP        NOT NULL                     /* Datum vlozenia do DMS */
  ,C_TYPE       VARCHAR(8)       NOT NULL                     /* Typ dokumentu - fileextension */
  ,FILENAME     VARCHAR(128)     NOT NULL                     /* Nazov suboru v DMS */
  ,ORIGNAME     VARCHAR(128)     NOT NULL                     /* Nazov originalneho suboru */
  ,THUMBNAME    VARCHAR(128)         NULL                     /* Nazov suboru nahladu dokumentu */
  ,N_SIZE       INT                  NULL                     /* Velkost dokumentu v Byte */
  ,C_PUB        CHAR(1)          DEFAULT 'N'                  /* Priznak PUBLIC (Y/N) */
  ,TITLE        VARCHAR(128)         NULL                     /* Nazov dokumentu */
  ,NOTES        VARCHAR(4000)        NULL                     /* Poznamky k dokumentu */
  ,D_VALID      INT                  NULL                     /* Datum zaciatku platnosti dokumentu */
  ,D_EXPIRY     INT                  NULL                     /* Datum konca platnosti dokumentu */
  ,MD5          VARCHAR(64)          NULL                     /* Hash of the file */

  ,PRIMARY KEY (DOC_ID)
--  ,FOREIGN KEY (USER_ID)         REFERENCES PM_USER (USER_ID)
)
/* Master tabulka Data Management Systemu */
;

CREATE INDEX FKI_DMS_USR ON PM_DMS(USER_ID);

/*------------------------------------------------------*/
/* Table PM_FORUM */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_FORUM;

CREATE TABLE IF NOT EXISTS PM_FORUM (
   ITEM_ID      INTEGER              NOT NULL                 /* Identifikácia Itemu. INTEGER PRIMARY KEY will autoincrement */
   
  ,PARENT_ID    INT                  DEFAULT 0                /* Identifikácia Itemu-rodiča */
  ,USER_ID      VARCHAR(32)          NOT NULL                 /* Majiteľ itemu */
  ,FORUM_ID     VARCHAR(32)          DEFAULT 'SYSTEM'         /* Identifikacia fora */
  ,C_FUNC       CHAR(1)              DEFAULT 'N'              /* Funkčnosť Itemu (New, Active, Deleted) */
  ,N_LVL        INT                  DEFAULT 0                /* Úroveň vnorenia do stromovej štruktúry */
  ,TITLE        VARCHAR(128)             NULL                 /* Názov Itemu */
  ,NARRATOR     VARCHAR(128)             NULL                 /* Rozprávač - kontext */
  ,ITEM         VARCHAR(16383)       NOT NULL                 /* Obsah Itemu */
  ,D_CREATED    TIMESTAMP            NOT NULL                 /* Dátum vytvorenia Itemu */
  ,D_CHANGED    TIMESTAMP            NOT NULL                 /* Dátum poslednej zmeny Itemu */
  ,WHO          VARCHAR(32)          NOT NULL                 /* User ID, ktorý vykonal poslednú zmenu */

  ,PRIMARY KEY (ITEM_ID)
--  ,FOREIGN KEY (USER_ID)    REFERENCES PM_USER (USER_ID)
)
/* Zoznam textov usporiadanych do vlaken */
;

CREATE INDEX FKI_ITM_USR ON PM_FORUM(USER_ID);

/*------------------------------------------------------*/
/* Table PM_BACKUP */
/*------------------------------------------------------*/
DROP TABLE IF EXISTS PM_BACKUP;

CREATE TABLE IF NOT EXISTS PM_BACKUP (
   BACKUP_ID    INTEGER              NOT NULL                 /* INTEGER PRIMARY KEY will autoincrement */
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
