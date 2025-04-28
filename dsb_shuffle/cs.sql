create table female
(
    web_serve               integer               not null,
    web_minimum               char(16)              not null,
    web_freedom        date                          ,
    web_product          date                          ,
    web_lay                  varchar(50)                   ,
    web_weird          integer                       ,
    web_suck         integer                       ,
    web_politics                 varchar(50)                   ,
    web_mark               varchar(40)                   ,
    web_row                integer                       ,
    web_help             varchar(50)                   ,
    web_go              varchar(100)                  ,
    web_permission        varchar(40)                   ,
    web_obligation            integer                       ,
    web_student          char(50)                      ,
    web_insurance         char(10)                      ,
    web_day           varchar(60)                   ,
    web_dark           char(15)                      ,
    web_oil          char(10)                      ,
    web_leading                  varchar(60)                   ,
    web_hunt                varchar(30)                   ,
    web_coach                 char(2)                       ,
    web_ask                   char(10)                      ,
    web_truck               varchar(20)                   ,
    web_lead            decimal(5,2)                  ,
    web_outside        decimal(5,2)                  ,
    primary key (web_serve)
);

create table red
(
    hd_debt                integer               not null,
    hd_rate         integer                       ,
    hd_bitter          char(15)                      ,
    hd_savings              integer                       ,
    hd_preference          integer                       ,
    primary key (hd_debt)
);

create table blank
(
    wp_train            integer               not null,
    wp_step            char(16)              not null,
    wp_freedom         date                          ,
    wp_product           date                          ,
    wp_brain       integer                       ,
    wp_maintenance         integer                       ,
    wp_basis           char(1)                       ,
    wp_branch            integer                       ,
    wp_improvement                    varchar(100)                  ,
    wp_thought                   char(50)                      ,
    wp_principle             integer                       ,
    wp_board             integer                       ,
    wp_calendar            integer                       ,
    wp_reach           integer                       ,
    primary key (wp_train)
);

create table push
(
    ib_rate         integer               not null,
    ib_designer            integer                       ,
    ib_page            integer                       ,
    primary key (ib_rate)
);

create table personal
(
    s_housing                integer               not null,
    s_split                char(16)              not null,
    s_freedom          date                          ,
    s_product            date                          ,
    s_ordinary          integer                       ,
    s_god              varchar(50)                   ,
    s_professor        integer                       ,
    s_quantity             integer                       ,
    s_emphasis                   char(20)                      ,
    s_mark                 varchar(40)                   ,
    s_show               integer                       ,
    s_one         varchar(100)                  ,
    s_hall             varchar(100)                  ,
    s_permission          varchar(40)                   ,
    s_sensitive             integer                       ,
    s_part           varchar(50)                   ,
    s_obligation              integer                       ,
    s_student            varchar(50)                   ,
    s_insurance           varchar(10)                   ,
    s_day             varchar(60)                   ,
    s_dark             char(15)                      ,
    s_oil            char(10)                      ,
    s_leading                    varchar(60)                   ,
    s_hunt                  varchar(30)                   ,
    s_coach                   char(2)                       ,
    s_ask                     char(10)                      ,
    s_truck                 varchar(20)                   ,
    s_lead              decimal(5,2)                  ,
    s_opening          decimal(5,2)                  ,
    primary key (s_housing)
);

create table beginning
(
    r_region               integer               not null,
    r_bowl               char(16)              not null,
    r_election             char(100)                     ,
    primary key (r_region)
);

create table pitch
(
    cd_debt                integer               not null,
    cd_sort                 char(1)                       ,
    cd_bathroom         char(1)                       ,
    cd_process       char(20)                      ,
    cd_consist      integer                       ,
    cd_driver          char(10)                      ,
    cd_savings              integer                       ,
    cd_tradition     integer                       ,
    cd_blow      integer                       ,
    primary key (cd_debt)
);

create table evening
(
    c_branch             integer               not null,
    c_currency             char(16)              not null,
    c_internal        integer                       ,
    c_union        integer                       ,
    c_tool         integer                       ,
    c_vast    integer                       ,
    c_lip     integer                       ,
    c_alarm              char(10)                      ,
    c_charity              char(20)                      ,
    c_person               char(30)                      ,
    c_spray     char(1)                       ,
    c_clothes               integer                       ,
    c_bone             integer                       ,
    c_profession              integer                       ,
    c_conclusion           varchar(20)                   ,
    c_credit                   char(13)                      ,
    c_chapter           char(50)                      ,
    c_cancer     integer                       ,
    primary key (c_branch)
);

create table boss
(
    ca_screw             integer               not null,
    ca_gate             char(16)              not null,
    ca_insurance          char(10)                      ,
    ca_day            varchar(60)                   ,
    ca_dark            char(15)                      ,
    ca_oil           char(10)                      ,
    ca_leading                   varchar(60)                   ,
    ca_hunt                 varchar(30)                   ,
    ca_coach                  char(2)                       ,
    ca_ask                    char(10)                      ,
    ca_truck                varchar(20)                   ,
    ca_lead             decimal(5,2)                  ,
    ca_routine          char(20)                      ,
    primary key (ca_screw)
);

create table negative
(
    t_economics                 integer               not null,
    t_face                 char(16)              not null,
    t_object                    integer                       ,
    t_carpet                    integer                       ,
    t_storage                  integer                       ,
    t_use                  integer                       ,
    t_volume                   char(2)                       ,
    t_blue                   char(20)                      ,
    t_king               char(20)                      ,
    t_salt               char(20)                      ,
    primary key (t_economics)
);

create table career
(
    ss_paper           integer                       ,
    ss_can           integer                       ,
    ss_recommendation                integer               not null,
    ss_branch            integer                       ,
    ss_mixture               integer                       ,
    ss_knowledge               integer                       ,
    ss_sport                integer                       ,
    ss_housing               integer                       ,
    ss_salad               integer                       ,
    ss_drag          integer               not null,
    ss_world               integer                       ,
    ss_health         decimal(7,2)                  ,
    ss_bother             decimal(7,2)                  ,
    ss_incident            decimal(7,2)                  ,
    ss_son       decimal(7,2)                  ,
    ss_stock        decimal(7,2)                  ,
    ss_angle     decimal(7,2)                  ,
    ss_door         decimal(7,2)                  ,
    ss_job                decimal(7,2)                  ,
    ss_hair             decimal(7,2)                  ,
    ss_activity               decimal(7,2)                  ,
    ss_debate       decimal(7,2)                  ,
    ss_queen             decimal(7,2)                  ,
    primary key (ss_recommendation, ss_drag)
);

create table analysis
(
    wr_investment       integer                       ,
    wr_calm       integer                       ,
    wr_recommendation                integer               not null,
    wr_formal   integer                       ,
    wr_while      integer                       ,
    wr_target      integer                       ,
    wr_let       integer                       ,
    wr_paint  integer                       ,
    wr_study     integer                       ,
    wr_drawer     integer                       ,
    wr_duty      integer                       ,
    wr_train            integer                       ,
    wr_region              integer                       ,
    wr_signature           integer               not null,
    wr_engineer        integer                       ,
    wr_stranger             decimal(7,2)                  ,
    wr_guide             decimal(7,2)                  ,
    wr_flight     decimal(7,2)                  ,
    wr_organization                    decimal(7,2)                  ,
    wr_factor       decimal(7,2)                  ,
    wr_friendship          decimal(7,2)                  ,
    wr_anxiety        decimal(7,2)                  ,
    wr_writer         decimal(7,2)                  ,
    wr_ease               decimal(7,2)                  ,
    primary key (wr_recommendation, wr_signature)
);

create table will
(
    dv_buy                varchar(16)                   ,
    dv_weakness            date                          ,
    dv_draft            time                          ,
    dv_spirit           varchar(200)                  
);

create table sleep
(
    d_shopping                 integer               not null,
    d_farmer                 char(16)              not null,
    d_raw                    date                          ,
    d_answer               integer                       ,
    d_assumption                integer                       ,
    d_injury             integer                       ,
    d_tune                    integer                       ,
    d_ruin                     integer                       ,
    d_particular                     integer                       ,
    d_ad                     integer                       ,
    d_ground                     integer                       ,
    d_focus                 integer                       ,
    d_writing          integer                       ,
    d_grocery             integer                       ,
    d_breath                char(9)                       ,
    d_earth            char(6)                       ,
    d_roll                 char(1)                       ,
    d_attitude                 char(1)                       ,
    d_piece       char(1)                       ,
    d_pattern               integer                       ,
    d_glad                integer                       ,
    d_track             integer                       ,
    d_oven             integer                       ,
    d_strain             char(1)                       ,
    d_data            char(1)                       ,
    d_criticism           char(1)                       ,
    d_situation         char(1)                       ,
    d_suggestion            char(1)                       ,
    primary key (d_shopping)
);

create table document
(
    w_cap            integer               not null,
    w_community            char(16)              not null,
    w_keep          varchar(20)                   ,
    w_web         integer                       ,
    w_insurance           char(10)                      ,
    w_day             varchar(60)                   ,
    w_dark             char(15)                      ,
    w_oil            char(10)                      ,
    w_leading                    varchar(60)                   ,
    w_hunt                  varchar(30)                   ,
    w_coach                   char(2)                       ,
    w_ask                     char(10)                      ,
    w_truck                 varchar(20)                   ,
    w_lead              decimal(5,2)                  ,
    primary key (w_cap)
);

create table virus
(
    sm_lock           integer               not null,
    sm_human           char(16)              not null,
    sm_thought                   char(30)                      ,
    sm_warning                   char(10)                      ,
    sm_foundation                char(20)                      ,
    sm_detail               char(20)                      ,
    primary key (sm_lock)
);

create table western
(
    cc_video         integer               not null,
    cc_owner         char(16)              not null,
    cc_freedom         date                          ,
    cc_product           date                          ,
    cc_ordinary         integer                       ,
    cc_weird           integer                       ,
    cc_lay                   varchar(50)                   ,
    cc_politics                  varchar(50)                   ,
    cc_being              integer                       ,
    cc_collar                  integer                       ,
    cc_emphasis                  char(20)                      ,
    cc_mark                varchar(40)                   ,
    cc_row                 integer                       ,
    cc_help              char(50)                      ,
    cc_go               varchar(100)                  ,
    cc_permission         varchar(40)                   ,
    cc_claim               integer                       ,
    cc_part          varchar(50)                   ,
    cc_parent                integer                       ,
    cc_student           char(50)                      ,
    cc_insurance          char(10)                      ,
    cc_day            varchar(60)                   ,
    cc_dark            char(15)                      ,
    cc_oil           char(10)                      ,
    cc_leading                   varchar(60)                   ,
    cc_hunt                 varchar(30)                   ,
    cc_coach                  char(2)                       ,
    cc_ask                    char(10)                      ,
    cc_truck                varchar(20)                   ,
    cc_lead             decimal(5,2)                  ,
    cc_outside         decimal(5,2)                  ,
    primary key (cc_video)
);

create table buddy
(
    sr_investment       integer                       ,
    sr_mate         integer                       ,
    sr_recommendation                integer               not null,
    sr_branch            integer                       ,
    sr_mixture               integer                       ,
    sr_knowledge               integer                       ,
    sr_sport                integer                       ,
    sr_housing               integer                       ,
    sr_region              integer                       ,
    sr_drag          integer               not null,
    sr_engineer        integer                       ,
    sr_stranger             decimal(7,2)                  ,
    sr_guide             decimal(7,2)                  ,
    sr_flight     decimal(7,2)                  ,
    sr_organization                    decimal(7,2)                  ,
    sr_factor       decimal(7,2)                  ,
    sr_friendship          decimal(7,2)                  ,
    sr_anxiety        decimal(7,2)                  ,
    sr_blame           decimal(7,2)                  ,
    sr_ease               decimal(7,2)                  ,
    primary key (sr_recommendation, sr_drag)
);

create table policy
(
    cs_paper           integer                       ,
    cs_can           integer                       ,
    cs_editor           integer                       ,
    cs_people       integer                       ,
    cs_result          integer                       ,
    cs_farm          integer                       ,
    cs_drive           integer                       ,
    cs_back       integer                       ,
    cs_put          integer                       ,
    cs_slide          integer                       ,
    cs_anything           integer                       ,
    cs_video         integer                       ,
    cs_plane        integer                       ,
    cs_lock           integer                       ,
    cs_cap           integer                       ,
    cs_recommendation                integer               not null,
    cs_salad               integer                       ,
    cs_signature           integer               not null,
    cs_world               integer                       ,
    cs_health         decimal(7,2)                  ,
    cs_bother             decimal(7,2)                  ,
    cs_incident            decimal(7,2)                  ,
    cs_son       decimal(7,2)                  ,
    cs_stock        decimal(7,2)                  ,
    cs_angle     decimal(7,2)                  ,
    cs_door         decimal(7,2)                  ,
    cs_job                decimal(7,2)                  ,
    cs_hair             decimal(7,2)                  ,
    cs_witness          decimal(7,2)                  ,
    cs_activity               decimal(7,2)                  ,
    cs_debate       decimal(7,2)                  ,
    cs_gas      decimal(7,2)                  ,
    cs_trick  decimal(7,2)                  ,
    cs_queen             decimal(7,2)                  ,
    primary key (cs_recommendation, cs_signature)
);

create table extension
(
    i_recommendation                 integer               not null,
    i_tie                 char(16)              not null,
    i_freedom          date                          ,
    i_product            date                          ,
    i_mood               varchar(200)                  ,
    i_grass           decimal(7,2)                  ,
    i_health          decimal(7,2)                  ,
    i_guitar                integer                       ,
    i_mall                   char(50)                      ,
    i_normal                integer                       ,
    i_politics                   char(50)                      ,
    i_note             integer                       ,
    i_poem                char(50)                      ,
    i_loan             integer                       ,
    i_carry                char(50)                      ,
    i_weather                    char(20)                      ,
    i_leg             char(20)                      ,
    i_plastic                   char(20)                      ,
    i_long                   char(10)                      ,
    i_suit               char(10)                      ,
    i_sick              integer                       ,
    i_ambition            char(50)                      ,
    primary key (i_recommendation)
);

create table emergency
(
    ws_paper           integer                       ,
    ws_can           integer                       ,
    ws_editor           integer                       ,
    ws_recommendation                integer               not null,
    ws_people       integer                       ,
    ws_result          integer                       ,
    ws_farm          integer                       ,
    ws_drive           integer                       ,
    ws_back       integer                       ,
    ws_put          integer                       ,
    ws_slide          integer                       ,
    ws_anything           integer                       ,
    ws_train            integer                       ,
    ws_ball            integer                       ,
    ws_lock           integer                       ,
    ws_cap           integer                       ,
    ws_salad               integer                       ,
    ws_signature           integer               not null,
    ws_world               integer                       ,
    ws_health         decimal(7,2)                  ,
    ws_bother             decimal(7,2)                  ,
    ws_incident            decimal(7,2)                  ,
    ws_son       decimal(7,2)                  ,
    ws_stock        decimal(7,2)                  ,
    ws_angle     decimal(7,2)                  ,
    ws_door         decimal(7,2)                  ,
    ws_job                decimal(7,2)                  ,
    ws_hair             decimal(7,2)                  ,
    ws_witness          decimal(7,2)                  ,
    ws_activity               decimal(7,2)                  ,
    ws_debate       decimal(7,2)                  ,
    ws_gas      decimal(7,2)                  ,
    ws_trick  decimal(7,2)                  ,
    ws_queen             decimal(7,2)                  ,
    primary key (ws_recommendation, ws_signature)
);

create table court
(
    p_salad                integer               not null,
    p_store                char(16)              not null,
    p_somewhere           integer                       ,
    p_load             integer                       ,
    p_recommendation                 integer                       ,
    p_role                    decimal(15,2)                 ,
    p_regular         integer                       ,
    p_objective              char(50)                      ,
    p_specialist           char(1)                       ,
    p_trust           char(1)                       ,
    p_green         char(1)                       ,
    p_company              char(1)                       ,
    p_food           char(1)                       ,
    p_vehicle           char(1)                       ,
    p_shirt           char(1)                       ,
    p_childhood            char(1)                       ,
    p_dealer         varchar(100)                  ,
    p_peak                 char(15)                      ,
    p_task         char(1)                       ,
    primary key (p_salad)
);

create table classroom
(
    cp_plane        integer               not null,
    cp_usual        char(16)              not null,
    cp_somewhere          integer                       ,
    cp_load            integer                       ,
    cp_stand             varchar(50)                   ,
    cp_baby         integer                       ,
    cp_cup    integer                       ,
    cp_supermarket            varchar(100)                  ,
    cp_thought                   varchar(100)                  ,
    primary key (cp_plane)
);

create table appearance
(
    cr_investment       integer                       ,
    cr_calm       integer                       ,
    cr_recommendation                integer               not null,
    cr_formal   integer                       ,
    cr_while      integer                       ,
    cr_target      integer                       ,
    cr_let       integer                       ,
    cr_paint  integer                       ,
    cr_study     integer                       ,
    cr_drawer     integer                       ,
    cr_duty      integer                       ,
    cr_video         integer                       ,
    cr_plane        integer                       ,
    cr_lock           integer                       ,
    cr_cap           integer                       ,
    cr_region              integer                       ,
    cr_signature           integer               not null,
    cr_engineer        integer                       ,
    cr_atmosphere          decimal(7,2)                  ,
    cr_guide             decimal(7,2)                  ,
    cr_flight     decimal(7,2)                  ,
    cr_organization                    decimal(7,2)                  ,
    cr_factor       decimal(7,2)                  ,
    cr_friendship          decimal(7,2)                  ,
    cr_anxiety        decimal(7,2)                  ,
    cr_blame           decimal(7,2)                  ,
    cr_ease               decimal(7,2)                  ,
    primary key (cr_recommendation, cr_signature)
);

create table place
(
    inv_shopping               integer               not null,
    inv_recommendation               integer               not null,
    inv_cap          integer               not null,
    inv_fight      integer                       ,
    primary key (inv_shopping, inv_recommendation, inv_cap)
);