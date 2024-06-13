#!/bin/bash

# Setup
## Set colors
set -e
export cymipamconf="./unit_tests.ini"
greenTextColor='\033[0;32m'
redTextColor='\033[0;31m'
noTextColor='\033[0m'

## Remove database
rm -f ./unit_tests.db

InvokeTest() {
    if eval $1; then
        echo -e "${greenTextColor}$2 passed${noTextColor}"
    else
        echo -e "${redTextColor}$2 failed${noTextColor}"
        exit 1
    fi
}

Main() {
for i in {0..500}
do
    
    command="c$i"
    text="t$i"
    if ! ([[ -z "${!command}" ]] && [[ -z "${!text}" ]]); then
        InvokeTest "${!command}" "${!text}"
    fi
done

}


# Tests - Do NOT change the test in this section
t0="t0 add database"
c0="./new_ipamdb.py"
# Dependencies: all tests going forward

t1="t1 vlan list - no vlans"
c1="./vlan_list.py | grep exist"

t2="t2 vlan add"
c2="./vlan_add.py --vlanId 2 --vlanName main --vlanGateway 192.168.2.1 --vlanCidr 24 --vlanDesc 'main' --vlanNetwork 192.168.2.0"

t3="t3 addr list - no addresses"
c3="./addr_list.py | grep exist"

t4="t4 addr add"
c4="./addr_add.py --addrIp 192.168.2.4 --vlanId 2 --addrName four.cymcore.com --addrDesc 'four desktop'"
# Dependencies: some tests going forward

# Tests - Add your tests here

t5="t5 vlan add - already exists"
c5="./vlan_add.py --vlanId 2 --vlanName main --vlanGateway 192.168.2.1 --vlanCidr 24 --vlanDesc 'main' --vlanNetwork 192.168.2.0 | grep exist"

t6="t6 vlan update"
c6="./vlan_update.py --vlanId 2 --vlanName main --vlanGateway 192.168.2.1 --vlanCidr 24 --vlanDesc 'newmain' --vlanNetwork 192.168.2.0 ; ./vlan_list.py | grep newmain"

t7="t7 addr add - already exists"
c7="./addr_add.py --addrIp 192.168.2.7 --vlanId 2 --addrName seven.cymcore.com  ; ./addr_add.py --addrIp 192.168.2.7 --vlanId 2 --addrName seven.cymcore.com | grep exist"

t8="t8 addr add - no description"
c8="./addr_add.py --addrIp 192.168.2.8 --vlanId 2 --addrName eight.cymcore.com"

t9="t9 addr add - by vlanName instead of vlanId"
c9="./addr_add.py --addrIp 192.168.2.9 --vlanName main --addrName nine.cymcore.com"

t10="t10 addr add - vlan name doesn't exist"
c10="./addr_add.py --addrIp 192.168.10.100 --vlanName ten --addrName ten.cymcore.com | grep exist"

t11="t11 addr add - vlan id doesn't exist"
c11="./addr_add.py --addrIp 192.168.11.100 --vlanId 11 --addrName eleven.cymcore.com | grep exist"

t12="t12 vlan remove - vlan id doesn't exist"
c12="./vlan_remove.py --vlanId 12 | grep exist"

t13="t13 vlan remove - vlan name doesn't exist"
c13="./vlan_remove.py --vlanName thirteen | grep exist"

t14="t14 vlan remove - by vlan id"
c14="./vlan_add.py --vlanId 14 --vlanName fourteen --vlanGateway 192.168.14.1 --vlanCidr 24 --vlanNetwork 192.168.14.0 && ./vlan_remove.py --vlanId 14"

t15="t15 vlan remove - by vlan name"
c15="./vlan_add.py --vlanId 15 --vlanName fifteen --vlanGateway 192.168.15.1 --vlanCidr 24 --vlanNetwork 192.168.15.0 && ./vlan_remove.py --vlanName fifteen"

t16="t16 vlan update - vlan doesn't exist"
c16="./vlan_update.py --vlanId 16 --vlanName sixteen --vlanGateway 192.168.16.1 --vlanCidr 24 --vlanDesc 'sixteen' --vlanNetwork 192.168.16.0 | grep exist"

t17="t17 vlan get - by vlan name"
c17="./vlan_add.py --vlanId 17 --vlanName seventeen --vlanGateway 192.168.17.1 --vlanCidr 24 --vlanNetwork 192.168.17.0 && ./vlan_get.py --vlanName seventeen | grep seventeen"

t18="t18 vlan get - by vlan id"
c18="./vlan_add.py --vlanId 18 --vlanName eighteen --vlanGateway 192.168.18.1 --vlanCidr 24 --vlanNetwork 192.168.18.0 && ./vlan_get.py --vlanId 18 | grep eighteen"

t19="t19 vlan get - vlan id not present"
c19="./vlan_get.py --vlanId 19 | grep exist"

t20="t20 vlan get - vlan name not present"
c20="./vlan_get.py --vlanName twenty | grep exist"

t21="t21 vlan list"
c21="./vlan_list.py | grep main"

t22="t22 addr remove"
c22="./addr_add.py --addrIp 192.168.2.22 --vlanId 2 --addrName twentytwo.cymcore.com --addrDesc 'twentytwo desktop' && ./addr_remove.py --addrIp 192.168.2.22"

t23="t23 addr remove - by addrName"
c23="./addr_add.py --addrIp 192.168.2.22 --vlanId 2 --addrName twentytwo.cymcore.com --addrDesc 'twentytwo desktop' && ./addr_remove.py --addrName twentytwo.cymcore.com"

t24="t24 addr remove - name does not exist"
c24="./addr_remove.py --addrName twentyfour.cymcore.com | grep exist"

t25="t25 addr remove - ip does not exist"
c25="./addr_remove.py --addrIp 192.168.2.25 | grep exist"

t28="t28 vlan add - no gateway or description"
c28="./vlan_add.py --vlanId 28 --vlanName twentyeight --vlanCidr 24 --vlanNetwork 192.168.28.0"

t29="t29 addr list"
c29="./addr_list.py | grep four.cymcore.com"

t30="t30 addr get"
c30="./addr_add.py --addrIp 192.168.2.30 --vlanId 2 --addrName thirty.cymcore.com ; ./addr_get.py --addrIp 192.168.2.30 | grep thirty"

t31="t31 addr get - ip not present"
c31="./addr_get.py --addrIp 192.168.2.31 | grep exist"

t32="t32 addr get - name not present"
c32="./addr_get.py --addrName thirtytwo.cymcore.com | grep exist"

t33="t33 addr get - by addr name"
c33="./addr_add.py --addrIp 192.168.2.33 --vlanId 2 --addrName thirtythree.cymcore.com ; ./addr_get.py --addrName thirtythree.cymcore.com | grep thirtythree"

t34="t34 vlan update - vlan name already exists"
c34="./vlan_update.py --vlanId 34 --vlanName main --vlanGateway 192.168.34.1 --vlanCidr 24 --vlanNetwork 192.168.34.0 | grep exist"

t35="t35 vlan add - vlan name already exists"
c35="./vlan_add.py --vlanId 35 --vlanName main --vlanGateway 192.168.35.1 --vlanCidr 24 --vlanNetwork 192.168.35.0 | grep exist"

t36="t36 addr add - name already exists"
c36="./addr_add.py --addrIp 192.168.2.36 --vlanId 2 --addrName thirtysix.cymcore.com  ; ./addr_add.py --addrIp 192.168.2.999 --vlanId 2 --addrName thirtysix.cymcore.com | grep exist"

t37="t37 addr register - vlan does not exist"
c37="./addr_register.py --vlanName thirtyseven --addrName thirtyseven.cymcore.com | grep exist"

t38="t38 addr register - addr does not exist"
c38="./addr_register.py --vlanName main --addrName thirtyeight.cymcore.com ; ./addr_list.py | grep  thirtyeight.cymcore.com"


# Run tests

Main
echo -e "${greenTextColor}all tests passed passed${noTextColor}"

