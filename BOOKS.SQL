
CREATE SEQUENCE public.cart_tno_seq
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        START 9
        CACHE 20
        NO CYCLE;


CREATE SEQUENCE public.member_mid_seq
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        START 5
        CACHE 20
        NO CYCLE;

CREATE SEQUENCE public.order_oid_seq
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        START 9
        CACHE 20
        NO CYCLE;

CREATE SEQUENCE public.po_oid_seq
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        START 9
        CACHE 20
        NO CYCLE;


CREATE SEQUENCE public.po_tno_seq
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        START 9
        CACHE 20
        NO CYCLE;



CREATE OR REPLACE FUNCTION public.set_member_mid()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.MID IS NULL THEN
        NEW.MID := NEXTVAL('MEMBER_MID_SEQ');
    END IF;
    RETURN NEW;
END;
$function$
;
CREATE OR REPLACE FUNCTION public.set_order_oid()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.OID IS NULL THEN
        NEW.OID := NEXTVAL('ORDER_OID_SEQ');
    END IF;
    RETURN NEW;
END;
$function$
;




CREATE TABLE public.cart (
        mid int8 NULL,
        carttime varchar(26) NULL,
        trans_no int8 NULL
);

CREATE TABLE public."member" (
        mid int8 NOT NULL,
        "name" varchar(128) NULL,
        account varchar(128) NULL,
        "password" varchar(128) NULL,
        "identity" varchar(128) NULL,
        tel varchar(128) NULL,
        addr varchar(128) NULL,
        birthday date NULL,
        CONSTRAINT member_pkey PRIMARY KEY (mid)
);


create trigger member_trg before
insert
    on
    public.member for each row execute function set_member_mid();



CREATE TABLE public.order_d (
        trans_no int8 NULL,
        prd_no varchar(26) NULL,
        amount int8 NULL,
        saleprice int8 NULL,
        total int8 NULL
);



CREATE TABLE public.order_m (
        "oid" int8 NULL,
        mid int8 NULL,
        order_date date NULL,
        price int8 NULL,
        trans_no int8 NULL
);


create trigger order_trg before
insert
    on
    public.order_m for each row execute function set_order_oid();



CREATE TABLE public.po_cart (
        mid int8 NULL,
        carttime varchar(26) NULL,
        po_num int8 NULL
);


CREATE TABLE public.po_mst (
        po_num int8 NULL,
        po_date date NULL,
        totalprice int4 NULL,
        mid int4 NULL
);
CREATE INDEX po_mst_po_num_idx ON public.po_mst USING btree (po_num);


CREATE TABLE public.poitem_mst (
        po_num int8 NULL,
        prd_no varchar NULL,
        qty int4 NULL,
        price int4 NULL,
        mid int4 NULL,
        total int8 NULL
);
CREATE INDEX poitem_mst_po_num_idx ON public.poitem_mst USING btree (po_num);

CREATE TABLE public.product (
        prd_no varchar(26) NOT NULL,
        prd_name varchar(128) NULL,
        prd_desc text NULL,
        prd_author varchar(40) NULL,
        prd_stock int8 NULL,
        prd_price int8 NULL,
        prd_publisher varchar(40) NULL,
        prd_cost int8 NULL
);



INSERT INTO public."member" (mid,"name",account,"password","identity",tel,addr,birthday) VALUES
         (1,'王大明','MINGWANG','TEST','user',NULL,NULL,NULL),
         (3,'林大偉','WEILIN','TEST','user',NULL,NULL,NULL),
         (4,'陳美環','MAYCHANG','TEST','user',NULL,NULL,NULL),
         (2,'孫小美','MAY','TEST','manager',NULL,NULL,NULL),
         (105,'a','abc@abc.com','1','user','tel','addr','2024-09-29');

INSERT INTO public.po_mst (po_num,po_date,totalprice,mid) VALUES
         (9,'2024-10-29',13921,2),
         (29,'2024-10-29',33,2),
         (30,'2024-10-29',39400,2),
         (49,'2024-10-29',506,2),
         (50,'2024-10-29',2428,2),
         (69,'2024-10-29',7000,2),
         (169,'2024-11-05',540,2),
         (170,'2024-11-05',5756,2),
         (189,'2024-11-05',788,2);


INSERT INTO public.poitem_mst (po_num,prd_no,qty,price,mid,total) VALUES
         (170,'P00018',2,493,NULL,986),
         (170,'P00017',1,324,NULL,324),
         (170,'P00014',2,253,NULL,506),
         (170,'P00011',10,394,NULL,3940),
         (9,'P00020',1,332,NULL,332),
         (9,'s13526',1,1,NULL,1),
         (9,'p37103',2,3,NULL,6),
         (9,'P00004',12,94,NULL,1128),
         (189,'P00015',1,527,NULL,527),
         (189,'P00012',1,261,NULL,261);
INSERT INTO public.poitem_mst (po_num,prd_no,qty,price,mid,total) VALUES
         (9,'P00012',14,261,NULL,3654),
         (9,'P00009',11,800,NULL,8800),
         (29,'Z73909',1,33,NULL,33),
         (30,'P00011',100,394,NULL,39400),
         (49,'P00014',2,253,NULL,506),
         (50,'P00020',1,10,NULL,10),
         (50,'P00011',2,1000,NULL,2000),
         (50,'Z73909',22,19,NULL,418),
         (69,'P00014',2,2000,NULL,4000),
         (69,'P00015',3,1000,NULL,3000);
INSERT INTO public.poitem_mst (po_num,prd_no,qty,price,mid,total) VALUES
         (89,'P00016',1,270,NULL,270),
         (109,'P00016',1,270,NULL,270),
         (129,'P00016',1,270,NULL,270),
         (149,'P00016',1,270,NULL,270),
         (169,'P00016',2,270,NULL,540);


INSERT INTO public.order_m ("oid",mid,order_date,price,trans_no) VALUES
         (29,105,'2024-10-23',394,29),
         (30,105,'2024-10-23',630,30),
         (31,1,'2024-10-23',810,31),
         (32,1,'2024-10-23',308,32),
         (49,3,'2024-10-24',1575,49),
         (71,4,'2024-10-25',602,71),
         (69,4,'2024-09-25',1122,69),
         (70,4,'2024-08-25',282,70),
         (89,105,'2024-10-29',2088,89);


INSERT INTO public.order_d (trans_no,prd_no,amount,saleprice,total) VALUES
         (29,'P00011',1,394,394),
         (30,'P00006',2,315,630),
         (31,'P00016',3,270,810),
         (32,'P00002',1,308,308),
         (49,'P00006',5,315,1575),
         (69,'P00014',2,253,506),
         (69,'P00002',2,308,616),
         (70,'P00004',3,94,282),
         (71,'P00019',1,332,332),
         (71,'P00003',1,270,270);
INSERT INTO public.order_d (trans_no,prd_no,amount,saleprice,total) VALUES
         (89,'P00012',8,261,2088);

INSERT INTO public.product (prd_no,prd_name,prd_desc,prd_author,prd_stock,prd_price,prd_publisher,prd_cost) VALUES
         ('P00018','老人心理學導論','【內容簡介】','伊恩．史托特-漢米爾頓',12,493,'五南圖書出版有限公司',235),
         ('P00017','創客創業導師程天縱的管理力','【內容簡介】
程天縱先生曾任惠普、德州儀器、鴻海與富智康等跨國企業的高階主管，是電子科技產業無人不知的專業經理人。退休後，他積極投入創客圈，成立「Terry&Friends」創業社群，至今已輔導了超過五百個創業團隊。

因其兼具豐富的實務經驗與紮實的理論知識，對大型組織的經營與新創公司的第一線運作都非常熟悉，因此對職場中的問題總有一針見血的分析，並提出實際可行的建言。','程天縱',11,324,'商周出版',578),
         ('P00014','專案管理：玩一場從不確定到確定的遊戲','【内容簡介】淡馬錫集團前財務長、台積電前財務主管──郝旭烈（郝哥）
帶領高效團隊必懂的「專案管理」
一本老闆送主管、主管送部屬、部屬會團購的專案隨身讀！

 
專案大白話，帶你認識
3大核心觀念╳5項重要心法╳6個執行架構
14招開講，快速了解專案到底玩什麼
☻經營者☻新創團隊☻專案經理☻ 專案成員☻商務人士
通通都適用！','郝旭烈',6,253,'商業周刊',532),
         ('P00015','工商心理學導論','【內容簡介】本書譯自Schultz & Schultz(2009)的Psychology and Work Today第十版，該書可遠溯1973年，為美國各重要大學所經常採用，譯本亦在臺灣受到普遍的歡迎。後依2014年國際版再譯，惟該版不若原著完整流暢，故以增校為原則，並儘量保留了原譯。','李志鴻',14,527,'五南圖書出版有限公司',979),
         ('P00011','新制多益 TOEIC 單字大全','【內容簡介】本書特色
 
　　◆ 跟隨新制多益測驗的最新出題趨勢，更新常考字彙及出題重點
　　◆ 按照最常出現的內容分類成 30 個主題，只要 30 天就能征服新制多益常考單字','David Cho',113,394,'國際學村',352),
         ('P00020','逆思維','【內容簡介】','亞當．格蘭特',11,332,'平安文化',953),
         ('P00001','蛤蟆先生去看心理師','【內容簡介】這本老少咸宜、令人愉悅的作品，角色取材自英國經典童話《柳林中的風聲》，作者將心理治療過程運用在動物主角們身上：主角蛤蟆先生因為憂鬱症而離群索居，好友河鼠、鼴鼠和老獾擔憂他可能會做傻事，大力慫恿他去找心理諮商師蒼鷺。蒼鷺運用溝通分析（Transactional Analysis）協助蛤蟆先生面對內在小孩和成人，學會分析自己的感覺，發展情緒智商。到了書末，他恢復了以前的開朗，展開全新的旅程。','羅伯．狄保德',10,316,'三采',443),
         ('P00010','哈利波特与阿茲卡班都囚徒','【內容簡介】十二年來，在令人恐懼的阿茲卡班監獄，一直關押着一個臭名昭著的囚犯，名叫小天狼星布萊克。他的罪名是用一句咒語殺害了十三個人，據說他還是黑魔頭伏地魔的忠實追隨者。現在他逃出了監獄，而且阿茲卡班的守衛還聽到布萊克說的夢話:“他在霍格沃茨……他在霍格沃茨……”布萊克是不是想來殺掉哈利？即使在魔法學校里，身邊都是朋友，哈利·波特也並不安全。因為可怕的是，在他們當中也許隱藏着一個背叛者……','J.K.羅琳',10,520,'皇冠文化',489),
         ('P00013','破解黑心話術','【內容簡介】
　　▌揭開房市黑幕，避免你慘賠百萬的置產筆記
　　專家說Location、Location、Location，地段就是一切？
　　長輩說買房可以養老、抗通膨？
　　房仲說，房價只會越來越貴，早買早享受、現在不買以後會後悔？
　　眾說紛紜的建議，真的都是對的嗎？

　　本書不以「感覺」判斷，而是回歸理性分析、讓市場事實說話，看完本書，你將可以──
　　．精準預測房市走向，避免被當韭菜
　　．選擇進場的最佳時機，買屋、賣屋精準出手','李昌鵬',10,435,'采實文化 ',800),
         ('P00016','6年存到300張股票2022修訂版','【內容簡介】
零成本存股術，低薪族也能翻身致富！

「存股」不需要高超的操作技巧，
也不用整天提心吊膽地盯著大盤，
只要掌握幾個基本原則，
就能發揮驚人威力，為自己累積財富。

　　「一開始花3個月時間只能買1張股票，我還是拼命存錢，並學習『用錢賺錢』的知識，這樣持續了20幾年，現在終於可以每年領500多萬元股息，我靠理財改變了我的人生……」──陳重銘','陳重銘',12,270,'金尉',539);
INSERT INTO public.product (prd_no,prd_name,prd_desc,prd_author,prd_stock,prd_price,prd_publisher,prd_cost) VALUES
         ('P00006','暮光之城：新月','【內容簡介】

有三件事我很確定：
第一、愛德華是吸血鬼
第二、出於天性，他渴望喝我的血
第三、我無可救藥地愛上他了……

對貝拉來說，只有一件事比她的生命更重要：愛德華．庫倫。但愛上吸血鬼，比貝拉能想到的一切都還要危險。
愛德華從一個邪惡的吸血鬼手上，救了貝拉的小命，但現在，他們親密的關係，卻對周圍深愛的人造成威脅，他們知道，麻煩才剛要開始……','史蒂芬妮．梅爾',10,315,'尖端',650),
         ('P00019','富爸爸，窮爸爸【25週年紀念版】','【內容簡介】
　　如果你為錢工作，你就把力量給了雇主；
　　如果錢為你工作，你就能保有力量、掌控全局。

　　如果你想成為有錢人，就需要建立富人思維：
　　先明白為何富人不為錢工作。
　　了解為何存錢的人才是輸家。
　　懂得資產與負債的差異。
　　提高財務智商，學習會計、投資、瞭解市場及法律。
　　持續打造你的資產欄。','羅勃特．T．清崎',10,332,'高寶',69),
         ('P00008','那些年我們一起追的女孩','【內容簡介】一場名為青春的潮水淹沒了我們。浪退時，渾身溼透的我們一起坐在沙灘上，看著我們最喜愛的女孩子用力揮舞雙手，幸福踏向人生的另一端。下一次浪來，會帶走女孩留在沙灘上的美好足跡。但我們還在。刻在我們心中的女孩模樣，也還會在。豪情不減，嘻笑當年。','九把刀',10,205,'春天出版社',342),
         ('P00005','兒子使用說明書：在你放棄和兒子溝通之前，','【內容簡介】洞悉「男性腦」的腦科學專家教你有技巧地與兒子相處的方法，只看這一本就能秒懂男孩心事！

　　＊男孩子喜歡車子是為了促進小腦的發育？！
　　＊男孩子「發呆、磨蹭」是理科能力的證據？！
　　＊一直催小孩回家卻都叫不動，該怎麼辦？
　　＊兒子總是長不高，成績也跟不上，有什麼妙招呢？

　　身為女性的母親，要理解身為男性的兒子，真是相當困難啊，因為男性的大腦與女性的大腦，生來就擁有不同的特質，需要不同的栽培方式。','黑川伊保子',10,263,'時報出版社',136),
         ('P00007','制咒師','【內容簡介】
不論代價，保證人人平等。
不顧一切奪取的魔咒，將影響整個魔法世界……

一連串懸而未決的制咒師謀殺和盜竊案，已不再是艾兒希等人關切的重點。所有罪行的罪魁禍首已呼之欲出，然而，要成功舉發對方，就意味著艾兒希非法的破咒師身分必須曝光，而拒絕與對方合作的代價更高——她被關進了監獄，而幕後黑手也消失無蹤。

巴克斯突破禁制後，自身的法力快速成長，晉升成為法師。面對艾兒希的牢獄之災與日漸增生的情感，他只有兩條路可走：助她取得合法身分，或者眼睜睜看她踏上絞刑台。','夏莉．荷柏格',10,450,'奇幻基地',629),
         ('P00009','哈佛商業評論最有影響力的30篇文章','【內容簡介】《哈佛商業評論》於1922年由哈佛大學商學院創辦，100年來始終是國際最權威、最前瞻的商業管理雜誌，深入探討每個企業經理人關懷的核心問題，涵蓋：領導、策略、創新、變革、人才培育、大數據、物聯網、人工智慧、數位轉型、疫後新策略、永續經營等。','哈佛商業評論',10,800,'天下文化',999),
         ('P00002','做自己，為什麼還要說抱歉？','【內容簡介】經過20年，林依晨終於將漫長的沉澱與回望，化作書寫10組人生關鍵字的100則真實凝鍊。如絲如縷的細膩思辨，以及百無禁忌的自我揭露，是對過去所下的註腳，也是她踩下的一條堅實的專屬道路。看林依晨如何生活、如何思考，如何在眾人的想望與期待中矛盾掙扎，又如何在閃耀光芒的環繞下仍能時刻保有自我。有些叛逆，帶點俏皮，非常真實──她要在這本書裡，盡情做．自．己。','林依晨',10,308,'聯經出版公司',540),
         ('P00003','主題式ETF錢滾錢','【內容簡介】近來5G、電動車、ESG等主題式ETF火熱，想賺未來10年的趨勢財，在你的資產配置組合中，就不能缺少這些。

　　然而，業者發行的ETF種類越來越多，ESG、5G、電動車、半導體……以及鎖定美國、中國、越南等海外市場的ETF，

　　原本該是「無腦」的ETF投資術，也變得讓人很煩惱！

　　╲╲╲如果以下這些事你不知道，就不能錯過這本精彩好書！╱╱╱','陳重銘',10,270,'金尉',536),
         ('P00004','SPY×FAMILY 間諜家家酒 9','【內容簡介】約兒vs暗殺者集團的戰鬥進入尾聲…！另一方面，豪華郵輪上被人安裝了炸彈－－！察覺危機的洛伊德與安妮亞各自盡力解決難題，不過…？','遠藤達哉',10,94,'東立',946),
         ('P00012','原子習慣：細微改變帶來巨大成就的實證法則','【內容簡介】　　
　　每天都進步1%，一年後，你會進步37倍；
　　每天都退步1%，一年後，你會弱化到趨近於0！
　　你的一點小改變、一個好習慣，將會產生複利效應，
　　如滾雪球般，為你帶來豐碩的人生成果！','詹姆斯‧克利爾',11,261,'方智',547);
