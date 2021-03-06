import requests 
from urllib.request import * 
import time 
from bs4 import BeautifulSoup
import json
import alpaca_trade_api as alpaca 
from dotenv import load_dotenv,find_dotenv
import os 
from os.path import join, dirname 
from pathlib import Path 
import datetime as datetime
import warnings


load_dotenv(verbose=True)

api_key_id = os.getenv('API_KEY_ID')
api_secret_key = os.getenv('API_SECRET_KEY')
endpoint_url = os.getenv('ENDPOINT_URL')
av_key = os.getenv('ALPHAVANTAGE_KEY')

api = alpaca.REST(api_key_id,api_secret_key,base_url=endpoint_url, api_version='v2')


def get_sp_tickers():
    url = 'https://www.slickcharts.com/sp500'
    response = requests.get(url,headers = {'User-Agent':'Mozilla/5.0'}) 
    soup = BeautifulSoup(response.text,'html.parser')
    rows = soup.findAll('tr')[1:]
    tickers = []
    for row in rows: 
        tickers.append(row.findAll('td')[2].text)
    return tickers 

rand = {'AAPL': {
        'buy': 100,
        'sell': 200,
        'shares': 20
    },'AMZN': {
    'buy': 150,
    'sell': 250,
    'shares': 1
}}


russell_3000 = ['A',
'AA',
'AAC',
'AAL',
'AAN',
'AAOI',
'AAON',
'AAP',
'AAPL',
'AAT',
'AAWW',
'AAXN',
'ABAX',
'ABBV',
'ABC',
'ABCB',
'ABCD',
'ABCO',
'ABEO',
'ABG',
'ABM',
'ABMD',
'ABT',
'ABTX',
'AC',
'ACAD',
'ACBI',
'ACC',
'ACCO',
'ACET',
'ACGL',
'ACHC',
'ACHN',
'ACIA',
'ACIW',
'ACLS',
'ACM',
'ACN',
'ACNB',
'ACOR',
'ACRE',
'ACRS',
'ACTA',
'ACTG',
'ACXM',
'ADBE',
'ADC',
'ADES',
'ADI',
'ADM',
'ADMS',
'ADNT',
'ADP',
'ADRO',
'ADS',
'ADSK',
'ADSW',
'ADTN',
'ADUS',
'ADXS',
'AE',
'AEE',
'AEGN',
'AEIS',
'AEL',
'AEO',
'AEP',
'AERI',
'AES',
'AET',
'AF',
'AFAM',
'AFG',
'AFH',
'AFI',
'AFL',
'AFSI',
'AGCO',
'AGEN',
'AGFS',
'AGII',
'AGIO',
'AGM',
'AGN',
'AGNC',
'AGO',
'AGR',
'AGX',
'AGYS',
'AHH',
'AHL',
'AHP',
'AHT',
'AI',
'AIG',
'AIMC',
'AIMT',
'AIN',
'AIR',
'AIT',
'AIV',
'AIZ',
'AJG',
'AJRD',
'AJX',
'AKAM',
'AKAO',
'AKBA',
'AKR',
'AKRX',
'AKS',
'AKTS',
'AL',
'ALB',
'ALCO',
'ALDR',
'ALE',
'ALEX',
'ALG',
'ALGN',
'ALGT',
'ALJ',
'ALK',
'ALKS',
'ALL',
'ALLE',
'ALLY',
'ALNY',
'ALOG',
'ALR',
'ALRM',
'ALSN',
'ALX',
'ALXN',
'AMAG',
'AMAT',
'AMBA',
'AMBC',
'AMBR',
'AMC',
'AMCX',
'AMD',
'AME',
'AMED',
'AMG',
'AMGN',
'AMH',
'AMKR',
'AMN',
'AMNB',
'AMOT',
'AMP',
'AMPH',
'AMRC',
'AMRI',
'AMSF',
'AMSWA',
'AMT',
'AMTD',
'AMWD',
'AMZN',
'AN',
'ANAB',
'ANAT',
'ANCX',
'ANDE',
'ANET',
'ANF',
'ANGI',
'ANGO',
'ANH',
'ANIK',
'ANIP',
'ANSS',
'ANTM',
'AOBC',
'AON',
'AOS',
'AOSL',
'AP',
'APA',
'APAM',
'APC',
'APD',
'APEI',
'APH',
'APLE',
'APOG',
'APPF',
'APTI',
'APTS',
'AQMS',
'AR',
'ARA',
'ARAY',
'ARC',
'ARCB',
'ARCH',
'ARD',
'ARDX',
'ARE',
'AREX',
'ARI',
'ARII',
'ARMK',
'ARNA',
'ARNC',
'AROC',
'AROW',
'ARR',
'ARRS',
'ARRY',
'ARTNA',
'ARW',
'ASB',
'ASBB',
'ASC',
'ASCMA',
'ASGN',
'ASH',
'ASIX',
'ASMB',
'ASNA',
'ASPS',
'AST',
'ASTE',
'AT',
'ATEN',
'ATGE',
'ATH',
'ATHN',
'ATHX',
'ATI',
'ATKR',
'ATLO',
'ATNI',
'ATO',
'ATR',
'ATRA',
'ATRC',
'ATRI',
'ATRO',
'ATRS',
'ATSG',
'ATU',
'ATVI',
'ATW',
'AVA',
'AVAV',
'AVB',
'AVD',
'AVGO',
'AVHI',
'AVID',
'AVT',
'AVX',
'AVXL',
'AVXS',
'AVY',
'AWH',
'AWI',
'AWK',
'AWR',
'AXAS',
'AXDX',
'AXE',
'AXGN',
'AXL',
'AXON',
'AXP',
'AXS',
'AXTA',
'AXTI',
'AYI',
'AYR',
'AYX',
'AZO',
'AZPN',
'AZZ',
'B',
'BA',
'BABY',
'BAC',
'BAH',
'BANC',
'BANF',
'BANR',
'BAS',
'BATRA',
'BATRK',
'BAX',
'BBBY',
'BBG',
'BBGI',
'BBSI',
'BBT',
'BBW',
'BBY',
'BC',
'BCBP',
'BCC',
'BCEI',
'BCO',
'BCOR',
'BCOV',
'BCPC',
'BCR',
'BCRH',
'BCRX',
'BDC',
'BDE',
'BDGE',
'BDN',
'BDX',
'BEAT',
'BECN',
'BEL',
'BELFB',
'BEN',
'BERY',
'BETR',
'BF.A',
'BF.B',
'BFAM',
'BFIN',
'BFS',
'BG',
'BGC',
'BGCP',
'BGFV',
'BGG',
'BGS',
'BGSF',
'BH',
'BHB',
'BHBK',
'BHE',
'BHI',
'BHLB',
'BHVN',
'BID',
'BIG',
'BIIB',
'BIO',
'BIOS',
'BIVV',
'BJRI',
'BK',
'BKD',
'BKE',
'BKFS',
'BKH',
'BKMU',
'BKS',
'BKU',
'BL',
'BLBD',
'BLCM',
'BLD',
'BLDR',
'BLK',
'BLKB',
'BLL',
'BLMN',
'BLMT',
'BLUE',
'BLX',
'BMCH',
'BMI',
'BMRC',
'BMRN',
'BMS',
'BMTC',
'BMY',
'BNCL',
'BNED',
'BNFT',
'BOBE',
'BOCH',
'BOFI',
'BOH',
'BOJA',
'BOKF',
'BOLD',
'BOOM',
'BOOT',
'BOX',
'BPFH',
'BPI',
'BPMC',
'BPOP',
'BR',
'BRC',
'BRCD',
'BREW',
'BRG',
'BRK.B',
'BRKL',
'BRKR',
'BRKS',
'BRO',
'BRS',
'BRSS',
'BRX',
'BSET',
'BSF',
'BSFT',
'BSRR',
'BSTC',
'BSX',
'BTU',
'BTX',
'BUFF',
'BURL',
'BUSE',
'BV',
'BW',
'BWA',
'BWFG',
'BWINB',
'BWLD',
'BWXT',
'BXP',
'BXS',
'BYD',
'BZH',
'C',
'CA',
'CAA',
'CAB',
'CABO',
'CAC',
'CACC',
'CACI',
'CACQ',
'CADE',
'CAG',
'CAH',
'CAI',
'CAKE',
'CAL',
'CALA',
'CALD',
'CALM',
'CALX',
'CAMP',
'CAR',
'CARA',
'CARB',
'CARO',
'CARS',
'CASC',
'CASH',
'CASS',
'CASY',
'CAT',
'CATM',
'CATO',
'CATY',
'CAVM',
'CB',
'CBB',
'CBF',
'CBG',
'CBI',
'CBL',
'CBM',
'CBOE',
'CBPX',
'CBRL',
'CBS',
'CBSH',
'CBT',
'CBU',
'CBZ',
'CC',
'CCBG',
'CCC',
'CCF',
'CCI',
'CCK',
'CCL',
'CCMP',
'CCN',
'CCNE',
'CCO',
'CCOI',
'CCP',
'CCRN',
'CCS',
'CCXI',
'CDE',
'CDEV',
'CDK',
'CDNS',
'CDR',
'CDW',
'CDXS',
'CDZI',
'CE',
'CECE',
'CECO',
'CELG',
'CEMP',
'CENT',
'CENTA',
'CENX',
'CERN',
'CERS',
'CETV',
'CEVA',
'CF',
'CFFI',
'CFFN',
'CFG',
'CFI',
'CFMS',
'CFNB',
'CFR',
'CFX',
'CGNX',
'CHCO',
'CHCT',
'CHD',
'CHDN',
'CHE',
'CHEF',
'CHFC',
'CHFN',
'CHGG',
'CHH',
'CHK',
'CHMG',
'CHMI',
'CHRS',
'CHRW',
'CHS',
'CHSP',
'CHTR',
'CHUBA',
'CHUBK',
'CHUY',
'CI',
'CIA',
'CIEN',
'CIM',
'CINF',
'CIO',
'CIR',
'CIT',
'CIVB',
'CIVI',
'CIX',
'CJ',
'CKH',
'CL',
'CLCT',
'CLD',
'CLDR',
'CLDT',
'CLDX',
'CLF',
'CLFD',
'CLGX',
'CLH',
'CLI',
'CLNE',
'CLNS',
'CLPR',
'CLR',
'CLSD',
'CLVS',
'CLW',
'CLX',
'CMA',
'CMC',
'CMCO',
'CMCSA',
'CMD',
'CME',
'CMG',
'CMI',
'CMO',
'CMP',
'CMPR',
'CMRE',
'CMRX',
'CMS',
'CMT',
'CMTL',
'CNA',
'CNAT',
'CNBKA',
'CNC',
'CNCE',
'CNDT',
'CNK',
'CNMD',
'CNO',
'CNOB',
'CNP',
'CNS',
'CNSL',
'CNTY',
'CNX',
'CNXN',
'COBZ',
'COF',
'COG',
'COGT',
'COH',
'COHR',
'COHU',
'COKE',
'COL',
'COLB',
'COLL',
'COLM',
'COMM',
'CONE',
'CONN',
'COO',
'COP',
'COR',
'CORE',
'CORI',
'CORR',
'CORT',
'COST',
'COTV',
'COTY',
'COUP',
'COWN',
'CPA',
'CPB',
'CPE',
'CPF',
'CPK',
'CPLA',
'CPN',
'CPRT',
'CPRX',
'CPS',
'CPSI',
'CPT',
'CR',
'CRAI',
'CRAY',
'CRBP',
'CRC',
'CRCM',
'CRD.B',
'CREE',
'CRI',
'CRIS',
'CRL',
'CRM',
'CRMT',
'CROX',
'CRR',
'CRS',
'CRUS',
'CRVL',
'CRVS',
'CRY',
'CRZO',
'CSBK',
'CSCO',
'CSFL',
'CSGP',
'CSGS',
'CSII',
'CSL',
'CSLT',
'CSOD',
'CSRA',
'CSS',
'CST',
'CSTE',
'CSTR',
'CSU',
'CSV',
'CSWI',
'CSX',
'CTAS',
'CTB',
'CTBI',
'CTL',
'CTLT',
'CTMX',
'CTO',
'CTRE',
'CTRL',
'CTRN',
'CTS',
'CTSH',
'CTT',
'CTWS',
'CTXS',
'CUB',
'CUBE',
'CUBI',
'CUBN',
'CUDA',
'CUNB',
'CUTR',
'CUZ',
'CVA',
'CVBF',
'CVCO',
'CVCY',
'CVG',
'CVGI',
'CVGW',
'CVI',
'CVLT',
'CVLY',
'CVNA',
'CVRS',
'CVS',
'CVTI',
'CVX',
'CW',
'CWCO',
'CWH',
'CWST',
'CWT',
'CXO',
'CXP',
'CXW',
'CY',
'CYBE',
'CYH',
'CYS',
'CYTK',
'CZNC',
'CZR',
'D',
'DAKT',
'DAL',
'DAN',
'DAR',
'DATA',
'DBD',
'DCI',
'DCO',
'DCOM',
'DCT',
'DD',
'DDD',
'DDR',
'DDS',
'DE',
'DEA',
'DECK',
'DEI',
'DEL',
'DENN',
'DEPO',
'DERM',
'DF',
'DFIN',
'DFRG',
'DFS',
'DFT',
'DG',
'DGAS',
'DGI',
'DGICA',
'DGII',
'DGX',
'DHI',
'DHIL',
'DHR',
'DHT',
'DHX',
'DIN',
'DIOD',
'DIS',
'DISCA',
'DISCK',
'DISH',
'DJCO',
'DK',
'DKS',
'DLA',
'DLB',
'DLPH',
'DLR',
'DLTH',
'DLTR',
'DLX',
'DMRC',
'DNB',
'DNBF',
'DNKN',
'DNOW',
'DNR',
'DO',
'DOC',
'DOOR',
'DORM',
'DOV',
'DOW',
'DOX',
'DPLO',
'DPS',
'DPZ',
'DRE',
'DRH',
'DRI',
'DRQ',
'DRRX',
'DS',
'DSKE',
'DSPG',
'DST',
'DSW',
'DTE',
'DUK',
'DVA',
'DVAX',
'DVMT',
'DVN',
'DX',
'DXC',
'DXCM',
'DXPE',
'DY',
'DYN',
'EA',
'EARN',
'EAT',
'EBAY',
'EBF',
'EBIX',
'EBS',
'EBSB',
'EBTC',
'ECHO',
'ECL',
'ECOL',
'ECOM',
'ECPG',
'ECR',
'ED',
'EDGE',
'EDIT',
'EDR',
'EE',
'EEFT',
'EEX',
'EFII',
'EFSC',
'EFX',
'EGBN',
'EGHT',
'EGL',
'EGLE',
'EGN',
'EGOV',
'EGP',
'EGRX',
'EHTH',
'EIG',
'EIGI',
'EIX',
'EL',
'ELF',
'ELGX',
'ELLI',
'ELS',
'ELVT',
'ELY',
'EMCI',
'EME',
'EMKR',
'EML',
'EMN',
'EMR',
'ENDP',
'ENFC',
'ENOC',
'ENR',
'ENS',
'ENSG',
'ENT',
'ENTA',
'ENTG',
'ENTL',
'ENV',
'ENVA',
'ENZ',
'EOG',
'EPAM',
'EPAY',
'EPC',
'EPE',
'EPM',
'EPR',
'EPZM',
'EQBK',
'EQC',
'EQIX',
'EQR',
'EQT',
'ERA',
'ERI',
'ERIE',
'ERII',
'EROS',
'ES',
'ESCA',
'ESE',
'ESGR',
'ESIO',
'ESL',
'ESND',
'ESNT',
'ESPR',
'ESRT',
'ESRX',
'ESS',
'ESSA',
'ESTE',
'ESV',
'ESXB',
'ETFC',
'ETH',
'ETM',
'ETN',
'ETR',
'ETSY',
'EV',
'EVBG',
'EVBN',
'EVC',
'EVH',
'EVHC',
'EVI',
'EVR',
'EVRI',
'EVTC',
'EW',
'EWBC',
'EXA',
'EXAC',
'EXAS',
'EXC',
'EXEL',
'EXLS',
'EXP',
'EXPD',
'EXPE',
'EXPO',
'EXPR',
'EXR',
'EXTN',
'EXTR',
'EXXI',
'EZPW',
'F',
'FAF',
'FANG',
'FARM',
'FARO',
'FAST',
'FATE',
'FB',
'FBC',
'FBHS',
'FBIO',
'FBIZ',
'FBK',
'FBM',
'FBMS',
'FBNC',
'FBNK',
'FBP',
'FC',
'FCB',
'FCBC',
'FCE.A',
'FCF',
'FCFP',
'FCFS',
'FCH',
'FCN',
'FCNCA',
'FCPT',
'FCX',
'FDC',
'FDEF',
'FDP',
'FDS',
'FDX',
'FE',
'FELE',
'FET',
'FEYE',
'FF',
'FFBC',
'FFG',
'FFIC',
'FFIN',
'FFIV',
'FFKT',
'FFNW',
'FFWM',
'FGBI',
'FGEN',
'FGL',
'FHB',
'FHN',
'FI',
'FIBK',
'FICO',
'FII',
'FINL',
'FIS',
'FISI',
'FISV',
'FIT',
'FITB',
'FIVE',
'FIVN',
'FIX',
'FIZZ',
'FL',
'FLDM',
'FLIC',
'FLIR',
'FLO',
'FLOW',
'FLR',
'FLS',
'FLT',
'FLWS',
'FLXN',
'FLXS',
'FMAO',
'FMBH',
'FMBI',
'FMC',
'FMI',
'FMNB',
'FMSA',
'FN',
'FNB',
'FNBG',
'FND',
'FNF',
'FNFV',
'FNGN',
'FNHC',
'FNLC',
'FNSR',
'FNWB',
'FOE',
'FOGO',
'FOLD',
'FONR',
'FOR',
'FORM',
'FORR',
'FOSL',
'FOX',
'FOXA',
'FOXF',
'FPI',
'FPO',
'FPRX',
'FR',
'FRAC',
'FRAN',
'FRBK',
'FRC',
'FRED',
'FRGI',
'FRME',
'FRO',
'FRP',
'FRPH',
'FRPT',
'FRT',
'FRTA',
'FSAM',
'FSB',
'FSLR',
'FSP',
'FSS',
'FSTR',
'FTD',
'FTK',
'FTNT',
'FTR',
'FTV',
'FUEL',
'FUL',
'FULT',
'FWONA',
'FWONK',
'FWRD',
'G',
'GABC',
'GAIA',
'GATX',
'GBCI',
'GBL',
'GBLI',
'GBNK',
'GBT',
'GBX',
'GCAP',
'GCBC',
'GCI',
'GCO',
'GCP',
'GD',
'GDDY',
'GDEN',
'GDI',
'GDOT',
'GE',
'GEF',
'GEF.B',
'GEN',
'GENC',
'GEO',
'GEOS',
'GERN',
'GES',
'GFF',
'GGG',
'GGP',
'GHC',
'GHDX',
'GHL',
'GHM',
'GIFI',
'GIII',
'GILD',
'GIMO',
'GIS',
'GKOS',
'GLBL',
'GLDD',
'GLNG',
'GLOG',
'GLPI',
'GLRE',
'GLT',
'GLUU',
'GLW',
'GM',
'GME',
'GMED',
'GMRE',
'GMS',
'GNBC',
'GNC',
'GNCA',
'GNCMA',
'GNE',
'GNK',
'GNL',
'GNMK',
'GNRC',
'GNRT',
'GNTX',
'GNTY',
'GNW',
'GOGO',
'GOLF',
'GOOD',
'GOOG',
'GOOGL',
'GORO',
'GOV',
'GPC',
'GPI',
'GPK',
'GPN',
'GPOR',
'GPRE',
'GPRO',
'GPS',
'GPT',
'GPX',
'GRA',
'GRBK',
'GRC',
'GRIF',
'GRMN',
'GRPN',
'GRUB',
'GS',
'GSAT',
'GSBC',
'GSIT',
'GSOL',
'GST',
'GT',
'GTLS',
'GTN',
'GTS',
'GTT',
'GTY',
'GUID',
'GVA',
'GWB',
'GWR',
'GWRE',
'GWRS',
'GWW',
'GXP',
'H',
'HA',
'HABT',
'HAE',
'HAFC',
'HAIN',
'HAL',
'HALL',
'HALO',
'HAS',
'HASI',
'HAWK',
'HAYN',
'HBAN',
'HBCP',
'HBHC',
'HBI',
'HBMD',
'HBNC',
'HBP',
'HCA',
'HCC',
'HCCI',
'HCHC',
'HCI',
'HCKT',
'HCN',
'HCOM',
'HCP',
'HCSG',
'HD',
'HDNG',
'HDP',
'HDS',
'HDSN',
'HE',
'HEES',
'HEI',
'HEI.A',
'HELE',
'HES',
'HF',
'HFC',
'HFWA',
'HGV',
'HHC',
'HI',
'HIBB',
'HIFR',
'HIFS',
'HIG',
'HII',
'HIIQ',
'HIL',
'HIVE',
'HIW',
'HK',
'HL',
'HLF',
'HLI',
'HLIT',
'HLNE',
'HLS',
'HLT',
'HLX',
'HMHC',
'HMN',
'HMST',
'HMSY',
'HMTV',
'HNH',
'HNI',
'HNRG',
'HOFT',
'HOG',
'HOLX',
'HOMB',
'HOME',
'HON',
'HONE',
'HOPE',
'HOV',
'HP',
'HPE',
'HPP',
'HPQ',
'HPT',
'HQY',
'HR',
'HRB',
'HRC',
'HRG',
'HRI',
'HRL',
'HRS',
'HRTG',
'HRTX',
'HSC',
'HSIC',
'HSII',
'HSKA',
'HSNI',
'HST',
'HSTM',
'HSY',
'HT',
'HTA',
'HTBI',
'HTBK',
'HTH',
'HTLD',
'HTLF',
'HTZ',
'HUBB',
'HUBG',
'HUBS',
'HUM',
'HUN',
'HURC',
'HURN',
'HVT',
'HWKN',
'HXL',
'HY',
'HYH',
'HZN',
'HZNP',
'HZO',
'I',
'IAC',
'IART',
'IBCP',
'IBKC',
'IBKR',
'IBM',
'IBOC',
'IBP',
'IBTX',
'ICBK',
'ICD',
'ICE',
'ICFI',
'ICHR',
'ICON',
'ICPT',
'ICUI',
'IDA',
'IDCC',
'IDRA',
'IDT',
'IDTI',
'IDXX',
'IESC',
'IEX',
'IFF',
'IGT',
'IHC',
'III',
'IIIN',
'IIVI',
'ILG',
'ILMN',
'IMAX',
'IMDZ',
'IMGN',
'IMH',
'IMKTA',
'IMMR',
'IMMU',
'IMPV',
'INAP',
'INBK',
'INCR',
'INCY',
'INDB',
'INFN',
'INFO',
'INGN',
'INGR',
'INN',
'INO',
'INOV',
'INSE',
'INSM',
'INST',
'INSW',
'INSY',
'INT',
'INTC',
'INTL',
'INTU',
'INVA',
'INVH',
'INWK',
'IONS',
'IOSP',
'IP',
'IPAR',
'IPCC',
'IPG',
'IPGP',
'IPHI',
'IPHS',
'IPI',
'IPXL',
'IR',
'IRBT',
'IRDM',
'IRET',
'IRM',
'IRT',
'IRTC',
'IRWD',
'ISBC',
'ISCA',
'ISRG',
'ISRL',
'ISTR',
'IT',
'ITCI',
'ITG',
'ITGR',
'ITI',
'ITIC',
'ITRI',
'ITT',
'ITW',
'IVAC',
'IVC',
'IVR',
'IVZ',
'IXYS',
'JACK',
'JAG',
'JAX',
'JBHT',
'JBL',
'JBLU',
'JBSS',
'JBT',
'JCAP',
'JCI',
'JCOM',
'JCP',
'JEC',
'JELD',
'JILL',
'JJSF',
'JKHY',
'JLL',
'JNCE',
'JNJ',
'JNPR',
'JOE',
'JONE',
'JOUT',
'JPM',
'JRVR',
'JUNO',
'JW.A',
'JWN',
'K',
'KAI',
'KALU',
'KAMN',
'KAR',
'KATE',
'KBAL',
'KBH',
'KBR',
'KCG',
'KE',
'KEG',
'KELYA',
'KEM',
'KERX',
'KEX',
'KEY',
'KEYS',
'KEYW',
'KFRC',
'KFY',
'KHC',
'KIM',
'KIN',
'KINS',
'KIRK',
'KITE',
'KLAC',
'KLDX',
'KLXI',
'KMB',
'KMG',
'KMI',
'KMPR',
'KMT',
'KMX',
'KN',
'KND',
'KNL',
'KNSL',
'KNX',
'KO',
'KODK',
'KOP',
'KOPN',
'KORS',
'KOS',
'KPTI',
'KR',
'KRA',
'KRC',
'KREF',
'KRG',
'KRNY',
'KRO',
'KS',
'KSS',
'KSU',
'KTOS',
'KTWO',
'KURA',
'KVHI',
'KW',
'KWR',
'L',
'LABL',
'LAD',
'LADR',
'LAMR',
'LANC',
'LAUR',
'LAWS',
'LAYN',
'LAZ',
'LB',
'LBAI',
'LBIO',
'LBRDA',
'LBRDK',
'LBY',
'LC',
'LCI',
'LCII',
'LCNB',
'LCUT',
'LDL',
'LDOS',
'LDR',
'LE',
'LEA',
'LECO',
'LEG',
'LEN',
'LEN.B',
'LEXEA',
'LFGR',
'LFUS',
'LGF.A',
'LGF.B',
'LGIH',
'LGND',
'LH',
'LHCG',
'LHO',
'LII',
'LIND',
'LION',
'LITE',
'LIVN',
'LJPC',
'LKFN',
'LKQ',
'LKSD',
'LL',
'LLEX',
'LLL',
'LLNW',
'LLY',
'LM',
'LMAT',
'LMIA',
'LMNR',
'LMNX',
'LMOS',
'LMT',
'LNC',
'LNCE',
'LNDC',
'LNG',
'LNN',
'LNT',
'LNTH',
'LOB',
'LOCO',
'LOGM',
'LOPE',
'LORL',
'LOW',
'LOXO',
'LPG',
'LPI',
'LPLA',
'LPNT',
'LPSN',
'LPT',
'LPX',
'LQ',
'LQDT',
'LRCX',
'LRN',
'LSCC',
'LSI',
'LSTR',
'LSXMA',
'LSXMK',
'LTC',
'LTRPA',
'LTS',
'LTXB',
'LUK',
'LULU',
'LUV',
'LVLT',
'LVNTA',
'LVS',
'LW',
'LWAY',
'LXP',
'LXRX',
'LXU',
'LYB',
'LYTS',
'LYV',
'LZB',
'M',
'MA',
'MAA',
'MAC',
'MACK',
'MAN',
'MANH',
'MANT',
'MAR',
'MAS',
'MASI',
'MAT',
'MATW',
'MATX',
'MB',
'MBCN',
'MBFI',
'MBI',
'MBTF',
'MBUU',
'MBWM',
'MC',
'MCBC',
'MCD',
'MCF',
'MCFT',
'MCHP',
'MCK',
'MCO',
'MCRB',
'MCRI',
'MCRN',
'MCS',
'MCY',
'MD',
'MDC',
'MDCA',
'MDCO',
'MDGL',
'MDLY',
'MDLZ',
'MDP',
'MDR',
'MDRX',
'MDSO',
'MDT',
'MDU',
'MDXG',
'MED',
'MEDP',
'MEET',
'MEI',
'MET',
'METC',
'MFA',
'MFSF',
'MG',
'MGEE',
'MGEN',
'MGI',
'MGLN',
'MGM',
'MGNX',
'MGPI',
'MGRC',
'MHK',
'MHLD',
'MHO',
'MIC',
'MIDD',
'MIK',
'MINI',
'MITK',
'MITT',
'MJCO',
'MKC',
'MKL',
'MKSI',
'MKTX',
'MLAB',
'MLHR',
'MLI',
'MLM',
'MLP',
'MLR',
'MLVF',
'MMC',
'MMI',
'MMM',
'MMS',
'MMSI',
'MNK',
'MNOV',
'MNR',
'MNRO',
'MNST',
'MNTA',
'MO',
'MOBL',
'MOD',
'MODN',
'MOFG',
'MOG.A',
'MOH',
'MON',
'MORE',
'MORN',
'MOS',
'MOV',
'MPAA',
'MPC',
'MPO',
'MPW',
'MPWR',
'MPX',
'MRC',
'MRCY',
'MRK',
'MRLN',
'MRO',
'MRT',
'MRTN',
'MRVL',
'MS',
'MSA',
'MSBI',
'MSCC',
'MSCI',
'MSEX',
'MSFG',
'MSFT',
'MSG',
'MSGN',
'MSI',
'MSL',
'MSM',
'MSTR',
'MTB',
'MTCH',
'MTD',
'MTDR',
'MTG',
'MTGE',
'MTH',
'MTN',
'MTNB',
'MTOR',
'MTRN',
'MTRX',
'MTSC',
'MTSI',
'MTW',
'MTX',
'MTZ',
'MU',
'MULE',
'MUR',
'MUSA',
'MVIS',
'MWA',
'MXIM',
'MXL',
'MXWL',
'MYCC',
'MYE',
'MYGN',
'MYL',
'MYOK',
'MYRG',
'NAME',
'NANO',
'NAT',
'NATH',
'NATI',
'NATR',
'NAV',
'NAVG',
'NAVI',
'NBHC',
'NBIX',
'NBL',
'NBN',
'NBR',
'NBTB',
'NC',
'NCBS',
'NCI',
'NCIT',
'NCLH',
'NCMI',
'NCOM',
'NCR',
'NCS',
'NCSM',
'NDAQ',
'NDLS',
'NDSN',
'NE',
'NEE',
'NEFF',
'NEM',
'NEO',
'NEOG',
'NEOS',
'NERV',
'NEU',
'NEWM',
'NEWR',
'NEWS',
'NFBK',
'NFG',
'NFLX',
'NFX',
'NGHC',
'NGS',
'NGVC',
'NGVT',
'NH',
'NHC',
'NHI',
'NHTC',
'NI',
'NJR',
'NK',
'NKE',
'NKSH',
'NKTR',
'NL',
'NLNK',
'NLS',
'NLSN',
'NLY',
'NM',
'NMIH',
'NNA',
'NNBR',
'NNI',
'NNN',
'NOC',
'NODK',
'NOV',
'NOVT',
'NOW',
'NP',
'NPK',
'NPO',
'NPTN',
'NR',
'NRCIA',
'NRE',
'NRG',
'NRIM',
'NRZ',
'NSA',
'NSC',
'NSIT',
'NSM',
'NSP',
'NSR',
'NSSC',
'NSTG',
'NTAP',
'NTB',
'NTCT',
'NTGR',
'NTLA',
'NTNX',
'NTRA',
'NTRI',
'NTRS',
'NUAN',
'NUE',
'NUS',
'NUTR',
'NUVA',
'NVAX',
'NVCR',
'NVDA',
'NVEC',
'NVEE',
'NVLN',
'NVR',
'NVRO',
'NVTA',
'NWBI',
'NWE',
'NWFL',
'NWHM',
'NWL',
'NWLI',
'NWN',
'NWPX',
'NWS',
'NWSA',
'NX',
'NXEO',
'NXPI',
'NXRT',
'NXST',
'NXTM',
'NYCB',
'NYLD',
'NYLD.A',
'NYMT',
'NYMX',
'NYNY',
'NYT',
'O',
'OA',
'OAS',
'OB',
'OBLN',
'OC',
'OCFC',
'OCLR',
'OCN',
'OCUL',
'OCX',
'ODC',
'ODFL',
'ODP',
'OFC',
'OFED',
'OFG',
'OFIX',
'OFLX',
'OGE',
'OGS',
'OHI',
'OI',
'OII',
'OIS',
'OKE',
'OKSB',
'OKTA',
'OLBK',
'OLED',
'OLLI',
'OLN',
'OLP',
'OMAM',
'OMC',
'OMCL',
'OME',
'OMER',
'OMF',
'OMI',
'OMN',
'OMNT',
'ON',
'ONB',
'ONCE',
'ONDK',
'ONVO',
'OOMA',
'OPB',
'OPK',
'OPOF',
'OPY',
'ORA',
'ORBC',
'ORC',
'ORCL',
'ORI',
'ORIT',
'ORLY',
'ORM',
'ORN',
'ORRF',
'OSBC',
'OSG',
'OSIS',
'OSK',
'OSTK',
'OSUR',
'OTIC',
'OTTR',
'OUT',
'OVBC',
'OVID',
'OXFD',
'OXM',
'OXY',
'OZRK',
'P',
'PACB',
'PACW',
'PAG',
'PAH',
'PAHC',
'PANW',
'PARR',
'PATK',
'PAY',
'PAYC',
'PAYX',
'PB',
'PBCT',
'PBF',
'PBH',
'PBI',
'PBIP',
'PBNC',
'PBPB',
'PBYI',
'PCAR',
'PCBK',
'PCG',
'PCH',
'PCLN',
'PCMI',
'PCO',
'PCRX',
'PCSB',
'PCTY',
'PCYG',
'PCYO',
'PDCE',
'PDCO',
'PDFS',
'PDLI',
'PDM',
'PDVW',
'PE',
'PEB',
'PEBK',
'PEBO',
'PEG',
'PEGA',
'PEGI',
'PEI',
'PEIX',
'PEN',
'PENN',
'PEP',
'PERY',
'PES',
'PETS',
'PETX',
'PF',
'PFBC',
'PFBI',
'PFE',
'PFG',
'PFGC',
'PFIS',
'PFPT',
'PFS',
'PFSI',
'PG',
'PGC',
'PGEM',
'PGNX',
'PGR',
'PGRE',
'PGTI',
'PH',
'PHH',
'PHIIK',
'PHM',
'PHX',
'PI',
'PICO',
'PII',
'PINC',
'PIR',
'PIRS',
'PJC',
'PJT',
'PK',
'PKBK',
'PKD',
'PKE',
'PKG',
'PKI',
'PKOH',
'PKY',
'PLAB',
'PLAY',
'PLCE',
'PLD',
'PLNT',
'PLOW',
'PLPC',
'PLPM',
'PLSE',
'PLT',
'PLUG',
'PLUS',
'PLXS',
'PM',
'PMBC',
'PMC',
'PMT',
'PMTS',
'PNC',
'PNFP',
'PNK',
'PNM',
'PNR',
'PNRA',
'PNW',
'PODD',
'POL',
'POOL',
'POR',
'POST',
'POWI',
'POWL',
'PPBI',
'PPC',
'PPG',
'PPL',
'PRA',
'PRAA',
'PRAH',
'PRFT',
'PRGO',
'PRGS',
'PRI',
'PRIM',
'PRK',
'PRLB',
'PRMW',
'PRO',
'PROV',
'PRSC',
'PRTA',
'PRTK',
'PRTY',
'PRU',
'PRXL',
'PSA',
'PSB',
'PSDO',
'PSMT',
'PSTB',
'PSTG',
'PSX',
'PTC',
'PTCT',
'PTEN',
'PTGX',
'PTHN',
'PTLA',
'PUB',
'PUMP',
'PVAC',
'PVBC',
'PVH',
'PWOD',
'PWR',
'PX',
'PXD',
'PXLW',
'PYPL',
'PZN',
'PZZA',
'Q',
'QADA',
'QCOM',
'QCP',
'QCRH',
'QDEL',
'QEP',
'QGEN',
'QLYS',
'QNST',
'QRVO',
'QSII',
'QTM',
'QTNA',
'QTNT',
'QTS',
'QTWO',
'QUAD',
'QUOT',
'QVCA',
'R',
'RAD',
'RAI',
'RAIL',
'RARE',
'RARX',
'RAS',
'RATE',
'RAVN',
'RBC',
'RBCAA',
'RCII',
'RCL',
'RCM',
'RDC',
'RDI',
'RDN',
'RDNT',
'RDUS',
'RE',
'RECN',
'REG',
'REGI',
'REGN',
'REI',
'REIS',
'REN',
'REPH',
'RES',
'RESI',
'RETA',
'REV',
'REVG',
'REX',
'REXR',
'RF',
'RGA',
'RGC',
'RGCO',
'RGEN',
'RGLD',
'RGNX',
'RGR',
'RGS',
'RH',
'RHI',
'RHP',
'RHT',
'RICE',
'RICK',
'RIG',
'RIGL',
'RILY',
'RJF',
'RL',
'RLGT',
'RLGY',
'RLH',
'RLI',
'RLJ',
'RM',
'RMAX',
'RMBS',
'RMD',
'RMR',
'RMTI',
'RNET',
'RNG',
'RNR',
'RNST',
'RNWK',
'ROCK',
'ROG',
'ROIC',
'ROK',
'ROL',
'ROLL',
'ROP',
'ROSE',
'ROST',
'ROX',
'RP',
'RPAI',
'RPD',
'RPM',
'RPT',
'RPXC',
'RRC',
'RRD',
'RRGB',
'RRR',
'RRTS',
'RS',
'RSG',
'RSO',
'RSPP',
'RST',
'RSYS',
'RT',
'RTEC',
'RTIX',
'RTN',
'RTRX',
'RUBI',
'RUN',
'RUSHA',
'RUSHB',
'RUTH',
'RVLT',
'RVNC',
'RVSB',
'RWT',
'RXDX',
'RXN',
'RYAM',
'RYI',
'RYN',
'S',
'SABR',
'SAFM',
'SAFT',
'SAGE',
'SAH',
'SAIA',
'SAIC',
'SALM',
'SALT',
'SAM',
'SAMG',
'SANM',
'SASR',
'SATS',
'SAVE',
'SB',
'SBAC',
'SBBP',
'SBCF',
'SBCP',
'SBGI',
'SBH',
'SBNY',
'SBOW',
'SBRA',
'SBSI',
'SBUX',
'SC',
'SCCO',
'SCG',
'SCHL',
'SCHN',
'SCHW',
'SCI',
'SCL',
'SCLN',
'SCMP',
'SCS',
'SCSC',
'SCSS',
'SCVL',
'SCWX',
'SD',
'SEAS',
'SEB',
'SEE',
'SEIC',
'SELB',
'SEM',
'SEMG',
'SENEA',
'SERV',
'SF',
'SFBS',
'SFE',
'SFL',
'SFLY',
'SFM',
'SFNC',
'SFR',
'SFS',
'SFST',
'SGA',
'SGBK',
'SGC',
'SGEN',
'SGMO',
'SGMS',
'SGRY',
'SGY',
'SGYP',
'SHAK',
'SHBI',
'SHEN',
'SHLD',
'SHLM',
'SHLO',
'SHO',
'SHOO',
'SHOR',
'SHW',
'SIEN',
'SIFI',
'SIG',
'SIGI',
'SIGM',
'SIR',
'SIRI',
'SITE',
'SIVB',
'SIX',
'SJI',
'SJM',
'SJW',
'SKT',
'SKX',
'SKYW',
'SLAB',
'SLB',
'SLCA',
'SLD',
'SLG',
'SLGN',
'SLM',
'SLP',
'SM',
'SMBC',
'SMBK',
'SMCI',
'SMG',
'SMHI',
'SMMF',
'SMP',
'SMTC',
'SN',
'SNA',
'SNBC',
'SNC',
'SNCR',
'SND',
'SNDR',
'SNDX',
'SNH',
'SNHY',
'SNI',
'SNOW',
'SNPS',
'SNR',
'SNV',
'SNX',
'SO',
'SOI',
'SON',
'SONA',
'SONC',
'SONS',
'SP',
'SPA',
'SPAR',
'SPB',
'SPG',
'SPGI',
'SPKE',
'SPLK',
'SPLS',
'SPN',
'SPNC',
'SPOK',
'SPPI',
'SPR',
'SPSC',
'SPTN',
'SPWH',
'SPWR',
'SPXC',
'SQ',
'SQBG',
'SR',
'SRC',
'SRCE',
'SRCI',
'SRCL',
'SRDX',
'SRE',
'SREV',
'SRG',
'SRI',
'SRPT',
'SRT',
'SSB',
'SSD',
'SSNC',
'SSNI',
'SSP',
'SSTK',
'SSYS',
'ST',
'STAA',
'STAG',
'STAR',
'STAY',
'STBA',
'STBZ',
'STC',
'STE',
'STFC',
'STI',
'STL',
'STLD',
'STML',
'STMP',
'STNG',
'STOR',
'STRA',
'STRL',
'STRP',
'STRS',
'STS',
'STT',
'STWD',
'STZ',
'SUI',
'SUM',
'SUP',
'SUPN',
'SVU',
'SWFT',
'SWK',
'SWKS',
'SWM',
'SWN',
'SWX',
'SXC',
'SXI',
'SXT',
'SYBT',
'SYF',
'SYK',
'SYKE',
'SYMC',
'SYNA',
'SYNT',
'SYRS',
'SYX',
'SYY',
'T',
'TACO',
'TAHO',
'TAP',
'TAST',
'TAX',
'TBBK',
'TBI',
'TBK',
'TBNK',
'TBPH',
'TCBI',
'TCBK',
'TCF',
'TCFC',
'TCI',
'TCMD',
'TCO',
'TCS',
'TCX',
'TDC',
'TDG',
'TDOC',
'TDS',
'TDY',
'TEAM',
'TECD',
'TECH',
'TELL',
'TEN',
'TER',
'TERP',
'TESO',
'TEX',
'TFSL',
'TFX',
'TG',
'TGH',
'TGI',
'TGNA',
'TGT',
'TGTX',
'THC',
'THFF',
'THG',
'THO',
'THR',
'THRM',
'THS',
'TIER',
'TIF',
'TILE',
'TIME',
'TIPT',
'TIS',
'TISI',
'TITN',
'TIVO',
'TJX',
'TK',
'TKR',
'TLGT',
'TLRD',
'TLYS',
'TMHC',
'TMK',
'TMO',
'TMP',
'TMST',
'TMUS',
'TNAV',
'TNC',
'TNET',
'TNK',
'TOCA',
'TOL',
'TOWN',
'TOWR',
'TPB',
'TPC',
'TPH',
'TPHS',
'TPIC',
'TPRE',
'TPX',
'TR',
'TRC',
'TRCB',
'TRCO',
'TREC',
'TREE',
'TREX',
'TRGP',
'TRHC',
'TRIP',
'TRK',
'TRMB',
'TRMK',
'TRN',
'TRNC',
'TRNO',
'TROW',
'TROX',
'TRS',
'TRST',
'TRTN',
'TRU',
'TRUE',
'TRUP',
'TRV',
'TRVN',
'TSBK',
'TSC',
'TSCO',
'TSE',
'TSLA',
'TSN',
'TSO',
'TSQ',
'TSRO',
'TSS',
'TTC',
'TTD',
'TTEC',
'TTEK',
'TTGT',
'TTI',
'TTMI',
'TTPH',
'TTS',
'TTWO',
'TUP',
'TUSK',
'TVPT',
'TVTY',
'TWI',
'TWIN',
'TWLO',
'TWNK',
'TWO',
'TWOU',
'TWTR',
'TWX',
'TXMD',
'TXN',
'TXRH',
'TXT',
'TYL',
'TYPE',
'UA',
'UAA',
'UAL',
'UBA',
'UBFO',
'UBNK',
'UBNT',
'UBSH',
'UBSI',
'UCBI',
'UCFC',
'UCP',
'UCTT',
'UDR',
'UE',
'UEC',
'UEIC',
'UFCS',
'UFI',
'UFPI',
'UFPT',
'UFS',
'UGI',
'UHAL',
'UHS',
'UHT',
'UIHC',
'UIS',
'ULH',
'ULTA',
'ULTI',
'UMBF',
'UMH',
'UMPQ',
'UNB',
'UNF',
'UNFI',
'UNH',
'UNIT',
'UNM',
'UNP',
'UNT',
'UNTY',
'UNVR',
'UPL',
'UPLD',
'UPS',
'URBN',
'URI',
'USAT',
'USB',
'USCR',
'USFD',
'USG',
'USLM',
'USM',
'USNA',
'USPH',
'UTHR',
'UTL',
'UTMD',
'UTX',
'UVE',
'UVSP',
'UVV',
'V',
'VAC',
'VALU',
'VAR',
'VBIV',
'VBTX',
'VC',
'VCRA',
'VCYT',
'VDSI',
'VEC',
'VECO',
'VEEV',
'VER',
'VERI',
'VFC',
'VG',
'VGR',
'VHC',
'VHI',
'VIA',
'VIAB',
'VIAV',
'VICR',
'VIRT',
'VIVE',
'VIVO',
'VLGEA',
'VLO',
'VLY',
'VMC',
'VMI',
'VMW',
'VNDA',
'VNO',
'VNTV',
'VOXX',
'VOYA',
'VPG',
'VR',
'VRA',
'VRAY',
'VREX',
'VRNS',
'VRNT',
'VRS',
'VRSK',
'VRSN',
'VRTS',
'VRTU',
'VRTV',
'VRTX',
'VSAR',
'VSAT',
'VSEC',
'VSH',
'VSI',
'VSLR',
'VSM',
'VST',
'VSTO',
'VTR',
'VTVT',
'VVC',
'VVI',
'VVV',
'VWR',
'VYGR',
'VZ',
'W',
'WAAS',
'WAB',
'WABC',
'WAFD',
'WAGE',
'WAIR',
'WAL',
'WASH',
'WAT',
'WATT',
'WBA',
'WBC',
'WBMD',
'WBS',
'WBT',
'WCC',
'WCG',
'WD',
'WDAY',
'WDC',
'WDFC',
'WDR',
'WEB',
'WEC',
'WEN',
'WERN',
'WETF',
'WEX',
'WEYS',
'WFBI',
'WFC',
'WFM',
'WFT',
'WG',
'WGL',
'WGO',
'WHG',
'WHR',
'WIFI',
'WIN',
'WINA',
'WING',
'WINS',
'WIRE',
'WK',
'WLB',
'WLDN',
'WLFC',
'WLH',
'WLK',
'WLL',
'WLTW',
'WM',
'WMAR',
'WMB',
'WMC',
'WMGI',
'WMIH',
'WMK',
'WMS',
'WMT',
'WNC',
'WNEB',
'WOOF',
'WOR',
'WPC',
'WPG',
'WPX',
'WR',
'WRB',
'WRD',
'WRE',
'WRI',
'WRK',
'WRLD',
'WSBC',
'WSBF',
'WSFS',
'WSM',
'WSO',
'WSR',
'WST',
'WSTC',
'WTBA',
'WTFC',
'WTI',
'WTM',
'WTR',
'WTS',
'WTTR',
'WTW',
'WU',
'WVE',
'WWD',
'WWE',
'WWW',
'WY',
'WYN',
'WYNN',
'X',
'XBIT',
'XBKS',
'XCRA',
'XEC',
'XEL',
'XENT',
'XHR',
'XL',
'XLNX',
'XLRN',
'XNCR',
'XOG',
'XOM',
'XON',
'XONE',
'XOXO',
'XPER',
'XPO',
'XRAY',
'XRX',
'XTLY',
'XYL',
'Y',
'YELP',
'YEXT',
'YORW',
'YRCW',
'YUM',
'YUMC',
'Z',
'ZAGG',
'ZAYO',
'ZBH',
'ZBRA',
'ZEN',
'ZEUS',
'ZG',
'ZGNX',
'ZION',
'ZIOP',
'ZIXI',
'ZNGA',
'ZOES',
'ZTS',
'ZUMZ',
'ZYNE']
