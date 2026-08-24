#!/usr/bin/env python3
"""Extract a compact unit-year fiscal panel from one GFD type file (national, all years).
Keeps id/bridge/demography + core fiscal + full debt-flow block. Usage:
  python3 extract_compact.py <in.csv> <out.csv.gz> <gov_type_label>"""
import csv,gzip,sys
IN,OUT,LBL=sys.argv[1],sys.argv[2],sys.argv[3]
KEEP=["GOVSid","Year4","State_Code","Type_Code","County","Name",
 "FIPS_Code_State","FIPS_County","FIPS_Place","FIPS_Combined","YearPop","Population","Enrollment",
 "Total_Revenue","Gen_Rev_Own_Sources","Total_Taxes","Property_Tax",
 "Total_IG_Revenue","Total_Fed_IG_Revenue","Total_State_IG_Revenue",
 "Total_Expenditure","Total_Capital_Outlays",
 "Total_Debt_Outstanding","Total_Long_Term_Debt_Out","ST_Debt_End_of_Year","Total_Beg_LTD_Out",
 "Total_LTD_Issued","Total_LTD_Iss_FFC","Total_LTD_Iss_NG","Total_LTD_Iss_Unsp",
 "Total_LTD_Retired","Total_LTD_Out","Total_LTD_Out_FFC","Tot_LTD_Out_NG","Total_LTD_Out_Utility",
 "Total_Interest_on_Debt"]
with open(IN,newline="") as fi:
    rd=csv.DictReader(fi)
    cols=[c for c in KEEP if c in rd.fieldnames]
    missing=[c for c in KEEP if c not in rd.fieldnames]
    with gzip.open(OUT,"wt",newline="") as fo:
        w=csv.writer(fo); w.writerow(["gov_type"]+cols)
        n=0
        for r in rd:
            w.writerow([LBL]+[r[c] for c in cols]); n+=1
print(f"{LBL}: {n} rows -> {OUT}; kept {len(cols)} cols; missing from source: {missing}")
