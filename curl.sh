#!/bin/bash
if [ $# -ne 3 ]
then
echo "ERROR: Usage: curl.sh SYMBOL START_DATE END_DATE"
echo "E.g.: curl.sh PNB 01-01-2016 31-01-2016"
exit 1
fi
curl -H 'Host: www.nseindia.com' -H 'Cookie: JSESSIONID=F78DD49C58B01EC9A338FC9E23C6A9AB; NSE-TEST-1=1809850378.20480.0000' -H 'Accept: */*' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30' -H 'Referer: https://www.nseindia.com/products/content/equities/equities/eq_security.htm' -H 'Accept-Language: en-us' -H 'X-Requested-With: XMLHttpRequest' --compressed 'https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol='$1'&segmentLink=3&symbolCount=2&series=ALL&dateRange=+&fromDate='$2'&toDate='$3'&dataType=PRICEVOLUMEDELIVERABLE'
