import os

MAIN_URL_INFOS = [
    {
        "category_name": "銀行",
        "main_collection_name": "bank_main_url",
        "url_collection_name": "bank_url",
        "html_collection_name": "bank_html_data",
        "url_datas": [
            {
                "name": "台灣銀行",
                "domain_name": "bot.com.tw",
                "url": "https://www.bot.com.tw/Pages/default.aspx",
            },
            {
                "name": "土地銀行",
                "domain_name": "landbank.com.tw",
                "url": "https://www.landbank.com.tw/",
            },
            {
                "name": "合庫商銀",
                "domain_name": "tcb-bank.com.tw",
                "url": "https://www.tcb-bank.com.tw/Pages/index.aspx",
            },
            {
                "name": "第一銀行",
                "domain_name": "firstbank.com.tw",
                "url": "https://www.firstbank.com.tw/sites/fbweb/Home",
            },
            {
                "name": "華南銀行",
                "domain_name": "hncb.com.tw",
                "url": "https://www.hncb.com.tw/wps/portal/HNCB/",
            },
            {
                "name": "彰化銀行",
                "domain_name": "bankchb.com",
                "url": "https://www.bankchb.com/frontend/index.html",
            },
            {
                "name": "上海銀行",
                "domain_name": "scsb.com.tw",
                "url": "https://www.scsb.com.tw/",
            },
            {
                "name": "台北富邦",
                "domain_name": "taipeifubon.com.tw",
                "url": "https://ebank.taipeifubon.com.tw/B2C/common/Index.faces",
            },
            {
                "name": "國泰世華",
                "domain_name": "cathaybk.com.tw",
                "url": "https://www.cathaybk.com.tw/cathaybk/",
            },
            {
                "name": "高雄銀行",
                "domain_name": "bok.com.tw",
                "url": "https://www.bok.com.tw/welcome",
            },
            {
                "name": "兆豐商銀",
                "domain_name": "megabank.com.tw",
                "url": "https://www.megabank.com.tw/personal",
            },
            {
                "name": "花旗(台灣)銀行",
                "domain_name": "citibank.com.tw",
                "url": "https://www.citibank.com.tw/sim/index.htm",
            },
            {
                "name": "澳商澳盛銀行",
                "domain_name": "institutional.anz.com",
                "url": "https://institutional.anz.com/markets/taiwan/zh-hant",
            },
            {
                "name": "中華開發",
                "domain_name": "cdibh.com",
                "url": "https://www.cdibh.com/",
            },
            {
                "name": "臺灣企銀",
                "domain_name": "tbb.com.tw",
                "url": "https://www.tbb.com.tw/",
            },
            {
                "name": "渣打國際商銀",
                "domain_name": "sc.com",
                "url": "https://www.sc.com/tw/",
            },
            {
                "name": "台中商銀",
                "domain_name": "tcbbank.com.tw",
                "url": "https://www.tcbbank.com.tw/",
            },
            {
                "name": "京城商銀",
                "domain_name": "customer.ktb.com.tw",
                "url": "https://customer.ktb.com.tw/new/",
            },
            {
                "name": "永豐銀行",
                "domain_name": "bank.sinopac.com",
                "url": "https://bank.sinopac.com/sinopacBT/index.html",
            },
            {
                "name": "聯邦銀行",
                "domain_name": "ubot.com.tw",
                "url": "https://www.ubot.com.tw/",
            },
            {
                "name": "遠東銀行",
                "domain_name": "feib.com.tw",
                "url": "https://www.feib.com.tw/",
            },
            {
                "name": "元大銀行",
                "domain_name": "yuantabank.com.tw",
                "url": "https://www.yuantabank.com.tw/bank/",
            },
            {
                "name": "玉山銀行",
                "domain_name": "esunbank.com.tw",
                "url": "https://www.esunbank.com.tw/bank/personal",
            },
            {
                "name": "凱基銀行",
                "domain_name": "kgibank.com",
                "url": "https://www.kgibank.com/",
            },
            {
                "name": "星展銀行",
                "domain_name": "dbs.com.tw",
                "url": "https://www.dbs.com.tw/index-zh/default.page",
            },
            {
                "name": "台新銀行",
                "domain_name": "taishinbank.com.tw",
                "url": "https://www.taishinbank.com.tw/TSB/personal/",
            },
            {
                "name": "中國信託",
                "domain_name": "ctbcbank.com",
                "url": "https://www.ctbcbank.com/twrbo/zh_tw/index.html",
            },
            {
                "name": "中華郵政",
                "domain_name": "post.gov.tw",
                "url": "https://www.post.gov.tw/post/internet/index.jsp",
            },
        ],
    },
    {
        "category_name": "證券",
        "main_collection_name": "stock_main_url",
        "url_collection_name": "stock_url",
        "html_collection_name": "stock_html_data",
        "url_datas": [
            {
                "name": "元大證券",
                "domain_name": "yuanta.com.tw",
                "url": "https://www.yuanta.com.tw/eyuanta/",
            },
            {
                "name": "凱基證券",
                "domain_name": "kgieworld.com.tw",
                "url": "https://www.kgieworld.com.tw/index/",
            },
            {
                "name": "日盛證券",
                "domain_name": "jihsun.com.tw",
                "url": "https://www.jihsun.com.tw/",
            },
            {
                "name": "國泰證券",
                "domain_name": "cathaysec.com.tw",
                "url": "https://www.cathaysec.com.tw/",
            },
            {
                "name": "台銀證券",
                "domain_name": "twfhcsec.com.tw",
                "url": "https://www.twfhcsec.com.tw/",
            },
            {
                "name": "永豐金證券",
                "domain_name": "sinotrade.com.tw",
                "url": "https://www.sinotrade.com.tw/",
            },
            {
                "name": "新光證券",
                "domain_name": "skis.com.tw",
                "url": "https://www.skis.com.tw/n/",
            },
            {
                "name": "統一綜合證券",
                "domain_name": "pscnet.com.tw",
                "url": "https://www.pscnet.com.tw/pscnetStock/index.do",
            },
            {
                "name": "大昌證券",
                "domain_name": "dcn.com.tw",
                "url": "https://www.dcn.com.tw/",
            },
            {
                "name": "華南永昌證券",
                "domain_name": "entrust.com.tw",
                "url": "https://www.entrust.com.tw/entrust/place/list.do",
            },
            {
                "name": "中國信託證券",
                "domain_name": "win168.com.tw",
                "url": "https://www.win168.com.tw/",
            },
            {
                "name": "兆豐證券",
                "domain_name": "emega.com.tw",
                "url": "https://www.emega.com.tw/",
            },
            {
                "name": "台新證券",
                "domain_name": "tssco.com.tw",
                "url": "https://www.tssco.com.tw/",
            },
            {
                "name": "合庫證券",
                "domain_name": "tcfhc-sec.com.tw",
                "url": "https://www.tcfhc-sec.com.tw/Branch.aspx",
            },
            {
                "name": "康和證券",
                "domain_name": "concords.com.tw",
                "url": "https://stock.concords.com.tw/Default1.aspx",
            },
            {
                "name": "彰銀證券",
                "domain_name": "chb.com.tw",
                "url": "https://iwin.chb.com.tw/chbstk/WebLogin.html",
            },
            {
                "name": "渣打銀行證券",
                "domain_name": "sc.com",
                "url": "https://www.sc.com/tw/save/security-account.html",
            },
            {
                "name": "群益證券",
                "domain_name": "capital.com.tw",
                "url": "https://www.capital.com.tw/",
            },
        ],
    },
    {
        "category_name": "大眾運輸",
        "main_collection_name": "transport_main_url",
        "url_collection_name": "transport_url",
        "html_collection_name": "transport_html_data",
        "url_datas": [
            {
                "name": "台北捷運",
                "domain_name": "metro.taipei",
                "url": "https://www.metro.taipei/",
            },
            {
                "name": "高雄捷運",
                "domain_name": "krtc.com.tw",
                "url": "https://www.krtc.com.tw/",
            },
            {
                "name": "台鐵",
                "domain_name": "railway.gov.tw",
                "url": "https://www.railway.gov.tw/tra-tip-web/tip",
            },
            {
                "name": "台灣高鐵",
                "domain_name": "thsrc.com.tw",
                "url": "https://www.thsrc.com.tw/",
            },
            {
                "name": "桃園捷運",
                "domain_name": "tymetro.com.tw",
                "url": "https://www.tymetro.com.tw/tymetro-new/tw/index.php",
            },
            {
                "name": "首都客運",
                "domain_name": "capital-bus.com.tw",
                "url": "http://www.capital-bus.com.tw/",
            },
            {
                "name": "統聯客運",
                "domain_name": "ubus.com.tw",
                "url": "https://www.ubus.com.tw/Index",
            },
            {
                "name": "國光客運",
                "domain_name": "kingbus.com.tw",
                "url": "http://www.kingbus.com.tw/",
            },
            {
                "name": "和欣客運",
                "domain_name": "ebus.com.tw",
                "url": "http://www.ebus.com.tw/",
            },
            {
                "name": "阿囉哈客運",
                "domain_name": "aloha168.com.tw",
                "url": "https://www.aloha168.com.tw/",
            },
            {
                "name": "長榮航空",
                "domain_name": "evaair.com",
                "url": "https://www.evaair.com/zh-tw/index.html",
            },
            {
                "name": "中華航空",
                "domain_name": "china-airlines.com",
                "url": "https://www.china-airlines.com/tw/zh",
            },
            {
                "name": "台灣虎航",
                "domain_name": "tigerairtw.com",
                "url": "https://www.tigerairtw.com/zh-tw/",
            },
        ],
    },
    {
        "category_name": "電信",
        "main_collection_name": "telecom_main_url",
        "url_collection_name": "telecom_url",
        "html_collection_name": "telecom_html_data",
        "url_datas": [
            {
                "name": "中華電信",
                "domain_name": "cht.com.tw",
                "url": "https://www.cht.com.tw/home/consumer",
            },
            {
                "name": "遠傳電信",
                "domain_name": "fetnet.net",
                "url": "https://www.fetnet.net/content/cbu/tw/index.html",
            },
            {
                "name": "亞太電信",
                "domain_name": "aptg.com.tw",
                "url": "https://www.aptg.com.tw/my/",
            },
            {
                "name": "台灣之星",
                "domain_name": "tstartel.com",
                "url": "https://www.tstartel.com/CWS/",
            },
            {
                "name": "台灣大哥大",
                "domain_name": "taiwanmobile.com",
                "url": "https://www.taiwanmobile.com/index.html",
            },
        ],
    },
    {
        "category_name": "零售",
        "main_collection_name": "retail_main_url",
        "url_collection_name": "retail_url",
        "html_collection_name": "retail_html_data",
        "url_datas": [
            {
                "name": "7-11",
                "domain_name": "7-11.com.tw",
                "url": "https://www.7-11.com.tw/",
            },
            {
                "name": "全家",
                "domain_name": "family.com.tw",
                "url": "https://www.family.com.tw/Marketing/index.aspx",
            },
            {
                "name": "OK超商",
                "domain_name": "okmart.com.tw",
                "url": "https://www.okmart.com.tw/",
            },
            {
                "name": "萊爾富",
                "domain_name": "hilife.com.tw",
                "url": "https://www.hilife.com.tw/",
            },
            {
                "name": "屈臣氏",
                "domain_name": "watsons.com.tw",
                "url": "https://www.watsons.com.tw/",
            },
            {
                "name": "康是美",
                "domain_name": "cosmed.com.tw",
                "url": "https://www.cosmed.com.tw/",
            },
            {
                "name": "美廉社",
                "domain_name": "simplemart.com.tw",
                "url": "https://www.simplemart.com.tw/",
            },
        ],
    },
    {
        "category_name": "投信",
        "main_collection_name": "inv_trust_main_url",
        "url_collection_name": "inv_trust_url",
        "html_collection_name": "inv_trust_html_data",
        "url_datas": [
            {
                "name": "大華銀投信",
                "domain_name": "uobam.com.tw",
                "url": "https://www.uobam.com.tw/",
            },
            {
                "name": "中國信託投信",
                "domain_name": "ctbcinvestments.com.tw",
                "url": "https://www.ctbcinvestments.com.tw/",
            },
            {
                "name": "元大投信",
                "domain_name": "yuantafunds.com",
                "url": "https://www.yuantafunds.com/",
            },
            {
                "name": "日盛投信",
                "domain_name": "jsfunds.com.tw",
                "url": "https://www.jsfunds.com.tw/",
            },
            {
                "name": "台中銀投信",
                "domain_name": "tcbsitc.com.tw",
                "url": "https://www.tcbsitc.com.tw/",
            },
            {
                "name": "台新投信",
                "domain_name": "tsit.com.tw",
                "url": "https://www.tsit.com.tw/",
            },
            {
                "name": "永豐投信",
                "domain_name": "sitc.sinopac.com",
                "url": "http://sitc.sinopac.com/newweb/index.html",
            },
            {
                "name": "兆豐國際投信",
                "domain_name": "megafunds.com.tw",
                "url": "https://www.megafunds.com.tw/iitweb/messageform.aspx",
            },
            {
                "name": "合作金庫投信",
                "domain_name": "tcb-am.com.tw",
                "url": "http://www.tcb-am.com.tw/ID/Index.aspx",
            },
            {
                "name": "安本標準投信",
                "domain_name": "aberdeenstandard.com",
                "url": "https://www.aberdeenstandard.com/zh-tw/taiwan/who-we-are",
            },
            {
                "name": "安聯投信",
                "domain_name": "allianzgi.com",
                "url": "https://tw.allianzgi.com/",
            },
            {
                "name": "宏利投信",
                "domain_name": "manulifeam.com.tw",
                "url": "https://www.manulifeam.com.tw/",
            },
            {
                "name": "貝萊德投信",
                "domain_name": "blackrock.com",
                "url": "https://www.blackrock.com/tw",
            },
            {
                "name": "保德信投信",
                "domain_name": "pru.com.tw",
                "url": "https://www.pru.com.tw/",
            },
            {
                "name": "施羅德投信",
                "domain_name": "schroders.com",
                "url": "https://www.schroders.com/zh-tw/tw/asset-management/",
            },
            {
                "name": "柏瑞投信",
                "domain_name": "pinebridge.com.tw",
                "url": "https://www.pinebridge.com.tw/",
            },
            {
                "name": "國泰投信",
                "domain_name": "cathaysite.com.tw",
                "url": "https://www.cathaysite.com.tw/",
            },
            {
                "name": "第一金投信",
                "domain_name": "fsitc.com.tw",
                "url": "https://www.fsitc.com.tw/",
            },
            {
                "name": "統一投信",
                "domain_name": "ezmoney.com.tw",
                "url": "https://www.ezmoney.com.tw/",
            },
            {
                "name": "野村投信",
                "domain_name": "nomurafunds.com.tw",
                "url": "https://www.nomurafunds.com.tw/Web/Content/#/index",
            },
            {
                "name": "凱基投信",
                "domain_name": "kgifund.com.tw",
                "url": "https://www.kgifund.com.tw/",
            },
            {
                "name": "富邦投信",
                "domain_name": "fubon.com",
                "url": "https://www.fubon.com/asset-management/",
            },
            {
                "name": "富達投信",
                "domain_name": "fidelity.com.tw",
                "url": "https://www.fidelity.com.tw/index.html",
            },
            {
                "name": "富蘭克林華美投信",
                "domain_name": "ftft.com.tw",
                "url": "https://www.ftft.com.tw/",
            },
            {
                "name": "復華投信",
                "domain_name": "fhtrust.com.tw",
                "url": "https://www.fhtrust.com.tw/",
            },
            {
                "name": "景順投信",
                "domain_name": "invesco.com.tw",
                "url": "https://www.invesco.com.tw/retail/zh_TW",
            },
            {
                "name": "華南永昌投信",
                "domain_name": "hnitc.com.tw",
                "url": "http://www.hnitc.com.tw/www3/index.asp",
            },
            {
                "name": "街口投信",
                "domain_name": "paradigm-fund.com",
                "url": "http://www.paradigm-fund.com/",
            },
            {
                "name": "匯豐中華投信",
                "domain_name": "assetmanagement.hsbc.com.tw",
                "url": "https://www.assetmanagement.hsbc.com.tw/zh-tw",
            },
            {
                "name": "新光投信",
                "domain_name": "skit.com.tw",
                "url": "http://www.skit.com.tw/",
            },
            {
                "name": "瑞銀投信",
                "domain_name": "ubs.com",
                "url": "https://www.ubs.com/tw/tc/asset-management.html",
            },
            {
                "name": "群益投信",
                "domain_name": "capitalfund.com.tw",
                "url": "https://www.capitalfund.com.tw/web/tw/",
            },
            {
                "name": "德銀遠東投信",
                "domain_name": "funds.dws.com",
                "url": "https://funds.dws.com/tw/Home",
            },
            {
                "name": "摩根投信",
                "domain_name": "am.jpmorgan.com",
                "url": "https://am.jpmorgan.com/tw/zh/asset-management/per/",
            },
            {
                "name": "鋒裕匯理投信",
                "domain_name": "amundi.com.tw",
                "url": "https://www.amundi.com.tw/retail/node_11458/node_11459",
            },
            {
                "name": "聯邦投信",
                "domain_name": "usitc.com.tw",
                "url": "https://www.usitc.com.tw/",
            },
            {
                "name": "聯博投信",
                "domain_name": "abfunds.com.tw",
                "url": "https://www.abfunds.com.tw/",
            },
            {
                "name": "瀚亞投信",
                "domain_name": "eastspring.com.tw",
                "url": "https://www.eastspring.com.tw/",
            },
        ],
    },
    {
        "category_name": "旅行社",
        "main_collection_name": "travel_main_url",
        "url_collection_name": "travel_url",
        "html_collection_name": "travel_html_data",
        "url_datas": [
            {
                "name": "東南旅行社",
                "domain_name": "settour.com.tw",
                "url": "https://www.settour.com.tw/",
            },
            {
                "name": "雄獅旅遊",
                "domain_name": "liontravel.com",
                "url": "https://www.liontravel.com/category/zh-tw/index",
            },
            {
                "name": "燦星旅遊",
                "domain_name": "startravel.com.tw",
                "url": "https://www.startravel.com.tw/",
            },
            {
                "name": "易遊網",
                "domain_name": "eztravel.com.tw",
                "url": "https://www.eztravel.com.tw/",
            },
            {
                "name": "鳳凰旅行社",
                "domain_name": "travel.com.tw",
                "url": "https://www.travel.com.tw/",
            },
            {
                "name": "五福旅遊",
                "domain_name": "lifetour.com.tw",
                "url": "https://www.lifetour.com.tw/",
            },
            {
                "name": "山富旅遊",
                "domain_name": "travel4u.com.tw",
                "url": "https://www.travel4u.com.tw/",
            },
            {
                "name": "百威旅遊",
                "domain_name": "bwt.com.tw",
                "url": "https://www.bwt.com.tw/",
            },
            {
                "name": "可樂旅遊",
                "domain_name": "colatour.com.tw",
                "url": "https://www.colatour.com.tw/",
            },
            {
                "name": "喜鴻假期",
                "domain_name": "besttour.com.tw",
                "url": "https://www.besttour.com.tw/e_web/",
            },
            {
                "name": "世界旅行社",
                "domain_name": "worldwide.com.tw",
                "url": "https://www.worldwide.com.tw/",
            },
            {
                "name": "大興旅行社",
                "domain_name": "tahsintour.com.tw",
                "url": "https://www.tahsintour.com.tw/",
            },
            {
                "name": "旅天下",
                "domain_name": "uplantravel.com",
                "url": "https://www.uplantravel.com/category/zh-tw/index",
            },
            {
                "name": "良友旅行社",
                "domain_name": "ftstour.com.tw",
                "url": "https://www.ftstour.com.tw/",
            },
            {
                "name": "新進旅行社",
                "domain_name": "sunshinetour.com.tw",
                "url": "https://www.sunshinetour.com.tw/",
            },
        ],
    },
    {
        "category_name": "保險",
        "main_collection_name": "insurance_main_url",
        "url_collection_name": "insurance_url",
        "html_collection_name": "insurance_html_data",
        "url_datas": [
            {
                "name": "台銀人壽",
                "domain_name": "twfhclife.com.tw",
                "url": "https://www.twfhclife.com.tw/",
            },
            {
                "name": "台灣人壽",
                "domain_name": "taiwanlife.com",
                "url": "https://www.taiwanlife.com/",
            },
            {
                "name": "保誠人壽",
                "domain_name": "pcalife.com.tw",
                "url": "https://www.pcalife.com.tw/zh/",
            },
            {
                "name": "國泰人壽",
                "domain_name": "cathaylife.com.tw",
                "url": "https://www.cathaylife.com.tw/cathaylife/",
            },
            {
                "name": "中國人壽",
                "domain_name": "chinalife.com.tw",
                "url": "https://www.chinalife.com.tw/wps/portal/chinalife",
            },
            {
                "name": "南山人壽",
                "domain_name": "nanshanlife.com.tw",
                "url": "https://www.nanshanlife.com.tw/NanshanWeb",
            },
            {
                "name": "新光人壽",
                "domain_name": "skl.com.tw",
                "url": "https://www.skl.com.tw/",
            },
            {
                "name": "保德信人壽",
                "domain_name": "prulife.com.tw",
                "url": "http://www.prulife.com.tw/",
            },
            {
                "name": "遠雄人壽",
                "domain_name": "fglife.com.tw",
                "url": "https://www.fglife.com.tw/index.html",
            },
            {
                "name": "三商美邦人壽",
                "domain_name": "mli.com.tw",
                "url": "https://www.mli.com.tw/sites/mliportal/home",
            },
            {
                "name": "宏泰人壽",
                "domain_name": "hontai.com.tw",
                "url": "https://www.hontai.com.tw/18pages/index",
            },
            {
                "name": "安聯人壽",
                "domain_name": "allianz.com.tw",
                "url": "https://www.allianz.com.tw/",
            },
            {
                "name": "全球人壽",
                "domain_name": "transglobe.com.tw",
                "url": "https://www.transglobe.com.tw/",
            },
            {
                "name": "元大人壽",
                "domain_name": "yuantalife.com.tw",
                "url": "https://www.yuantalife.com.tw/",
            },
            {
                "name": "富邦人壽",
                "domain_name": "fubon.com",
                "url": "https://www.fubon.com/life/",
            },
            {
                "name": "第一金人壽",
                "domain_name": "firstlife.com.tw",
                "url": "https://www.firstlife.com.tw/FirstWeb/",
            },
            {
                "name": "合作金庫人壽",
                "domain_name": "my.tcb-life.com.tw",
                "url": "https://my.tcb-life.com.tw/",
            },
            {
                "name": "康健人壽",
                "domain_name": "cigna.com.tw",
                "url": "https://www.cigna.com.tw/",
            },
        ],
    },
]
HTML_CONTENT_TYPES = [
    "text/html;charset=utf-8",
    "text/html;charset=UTF-8",
    "text/html",
]

MONGO_URI = os.getenv("MONGO_URI", "mongodb://192.168.3.21:27019")
DB_NAME = os.getenv("DB_NAME", "industry_data")
MAIN_COLLECTION_NAME = os.getenv("MAIN_COLLECTION_NAME", "main_url")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
