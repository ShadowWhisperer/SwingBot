#!/bin/bash

#
# 1 - Go to   https://finviz.com/screener.ashx
# 2 - Set your options
# 3 - Copy url
# 4 - Paste after curl command - In " "
# 5 - Add   &r=$r  to the ennd - Like example
# 6 - Click last page on finviz's website
# 7 - Copy the number at the end of the URL  *After the =
# 8 - Replace the rc<= number below, with that number
#


# Loop through pages (starting at 1, incrementing by 20)
echo > /tmp/data
for ((r=1; r<=1321; r+=20)); do
    curl -s "https://finviz.com/screener.ashx?v=111&f=exch_nasd%2Cipodate_prev5yrs%2Csh_price_u30&o=price&r=$r" >> /tmp/data
   # Example https://finviz.com/screener.ashx?v=111&f=exch_nasd%2Cipodate_prev5yrs%2Csh_price_u30&o=price&r=$r
    sleep 1s
done


#Save Results
grep -v '[ /]' /tmp/data | grep '\.' | cut -f1 -d '|' | tr '[:upper:]' '[:lower:]' | sort -u > /tmp/keep
