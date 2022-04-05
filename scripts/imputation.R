colleges <- read.table(file = "..\\data\\temp4.csv",
                       header = T,
                       sep = ",",
                       quote = "\"",
                       dec = ".",
                       fill = T,
                       comment.char = "",
                       na.strings = c("NULL", "PrivacySuppressed", ""))




# Adjust the datatypes of the columns

factor_cols <- c("STABBR", "MAIN", "CONTROL", "ST_FIPS", "REGION",
                 "LOCALE", "CCBASIC", "CCUGPRO", "CCSIZESET", "HBCU", "PBI", "ANNHI",
                 "TRIBAL", "AANAPII", "HSI", "NANTI", "MENONLY", "WOMENONLY",
                 "RELAFFIL", "CIP01BACHL", "CIP03BACHL", "CIP04BACHL", "CIP05BACHL",
                 "CIP09BACHL", "CIP10BACHL", "CIP11BACHL", "CIP12BACHL", "CIP13BACHL",
                 "CIP14BACHL", "CIP15BACHL", "CIP16BACHL", "CIP19BACHL", "CIP22BACHL",
                 "CIP23BACHL", "CIP24BACHL", "CIP25BACHL", "CIP26BACHL", "CIP27BACHL",
                 "CIP29BACHL", "CIP30BACHL", "CIP31BACHL", "CIP38BACHL", "CIP39BACHL",
                 "CIP40BACHL", "CIP41BACHL", "CIP42BACHL", "CIP43BACHL", "CIP44BACHL",
                 "CIP45BACHL", "CIP46BACHL", "CIP47BACHL", "CIP48BACHL", "CIP49BACHL",
                 "CIP50BACHL", "CIP51BACHL", "CIP52BACHL", "CIP54BACHL", "DISTANCE",
                 "OPEFLAG", "ADMCON7", "DISTANCEONLY", "CLIMATE_ZONE")

integer_cols <- c("UNITID", "NUMBRANCH", "UGDS", "COUNT_NWNE_1YR",
                  "COUNT_WNE_1YR")

numeric_cols <- c("LATITUDE", "LONGITUDE", "ADM_RATE", "ADM_RATE_ALL", "SATVR25",
                  "SATVR75", "SATMT25", "SATMT75", "SATVRMID", "SATMTMID", "ACTCM25",
                  "ACTCM75", "ACTEN25", "ACTEN75", "ACTMT25", "ACTMT75", "ACTCMMID",
                  "ACTENMID", "ACTMTMID", "SAT_AVG", "SAT_ABG_ALL", "UGDS_WHITE",
                  "UGDS_BLACK", "UGDS_HISP", "UGDS_ASIAN", "UGDS_AIAN", "UGDS_NHPI",
                  "UGDS_2MOR", "UGDS_NRA", "UGDS_UNKN", "PPTUG_EF", "COSTT4_A",
                  "TUITIONFEE_IN", "TUITIONFEE_OUT", "TUITFTE",
                  "INEXPFTE", "AVGFACSAL", "PFTFAC", "UG25ABV", "COMP_ORIG_YR2_RT",
                  "COMP_ORIG_YR3_RT", "COMP_ORIG_YR4_RT", "COMP_ORIG_YR6_RT",
                  "COMP_ORIG_YR8_RT", "MDCOMP_ALL", "UGDS_MEN", "UGDS_WOMEN",
                  "MD_EARN_WNE_P6", "PCT25_EARN_WNE_P6", "PCT75_EARN_WNE_P6",
                  "BOOKSUPPLY", "ROOMBOARD_ON", "OTHEREXPENSE_ON", "ROOMBOARD_OFF",
                  "OTHEREXPENSE_OFF", "NPT4", "NPT41", "NPT42",
                  "NPT43", "NPT4", "NPT45", "C150_4", "GPA_BOTTOM_TEN_PERCENT")

character_cols <- c("INSTNM", "CITY", "INSTURL", "ZIP", "INSTURL")

for (name in names(colleges)){
    if (name %in% factor_cols)
        colleges[, name] <- as.factor(colleges[, name])
    else if (name %in% integer_cols)
        colleges[, name] <- as.integer(colleges[, name])
    else if (name %in% numeric_cols)
        colleges[, name] <- as.numeric(colleges[, name])
    else if (name %in% character_cols)
        colleges[, name] <- as.character(colleges[, name])
}




# Perform Imputation

impute_cols <- c("CONTROL"
                 ,"REGION"
                 ,"LOCALE"
                 ,"CCBASIC"
                 ,"CCUGPROF"
                 ,"CCSIZSET"
                 ,"HBCU"
                 ,"PBI"
                 ,"ANNHI"
                 ,"TRIBAL"
                 ,"AANAPII"
                 ,"HSI"
                 ,"NANTI"
                 ,"MENONLY"
                 ,"WOMENONLY"
                 ,"ADM_RATE"
                 ,"ADM_RATE_ALL"
                 ,"SATVR25"
                 ,"SATVR75"
                 ,"SATMT25"
                 ,"SATMT75"
                 ,"SATVRMID"
                 ,"SATMTMID"
                 ,"ACTCM25"
                 ,"ACTCM75"
                 ,"ACTEN25"
                 ,'ACTEN75'
                 ,"ACTMT25"
                 ,"ACTMT75"
                 ,"ACTCMMID"
                 ,"ACTENMID"
                 ,"ACTMTMID"
                 ,"SAT_AVG"
                 ,"SAT_AVG_ALL"
                 ,"CIP01BACHL"
                 ,"CIP03BACHL"
                 ,"CIP04BACHL"
                 ,"CIP05BACHL"
                 ,"CIP09BACHL"
                 ,"CIP10BACHL"
                 ,"CIP11BACHL"
                 ,"CIP12BACHL"
                 ,"CIP13BACHL"
                 ,"CIP14BACHL"
                 ,"CIP15BACHL"
                 ,"CIP16BACHL"
                 ,"CIP19BACHL"
                 ,"CIP22BACHL"
                 ,"CIP23BACHL"
                 ,"CIP24BACHL"
                 ,"CIP25BACHL"
                 ,"CIP26BACHL"
                 ,"CIP27BACHL"
                 ,"CIP29BACHL"
                 ,"CIP30BACHL"
                 ,"CIP31BACHL"
                 ,"CIP38BACHL"
                 ,"CIP39BACHL"
                 ,"CIP40BACHL"
                 ,"CIP41BACHL"
                 ,"CIP42BACHL"
                 ,"CIP43BACHL"
                 ,"CIP44BACHL"
                 ,"CIP45BACHL"
                 ,"CIP46BACHL"
                 ,"CIP47BACHL"
                 ,"CIP48BACHL"
                 ,"CIP49BACHL"
                 ,"CIP50BACHL"
                 ,"CIP51BACHL"
                 ,"CIP52BACHL"
                 ,"CIP54BACHL"
                 ,"DISTANCEONLY"
                 ,"UGDS"
                 ,"UGDS_WHITE"
                 ,"UGDS_BLACK"
                 ,"UGDS_HISP"
                 ,"UGDS_ASIAN"
                 ,"UGDS_AIAN"
                 ,"UGDS_NHPI"
                 ,"UGDS_2MOR"
                 ,"UGDS_NRA"
                 ,"UGDS_UNKN"
                 ,"COSTT4_A"
                 ,"TUITIONFEE_IN"
                 ,"TUITIONFEE_OUT"
                 ,"TUITFTE"
                 ,"INEXPFTE"
                 ,"AVGFACSAL"
                 ,"PFTFAC"
                 ,"UG25ABV"
                 ,"COMP_ORIG_YR2_RT"
                 ,"COMP_ORIG_YR3_RT"
                 ,"COMP_ORIG_YR4_RT"
                 ,"COMP_ORIG_YR6_RT"
                 ,"COMP_ORIG_YR8_RT"
                 ,"OPEFLAG"
                 ,"ADMCON7"
                 ,"UGDS_MEN"
                 ,"UGDS_WOMEN"
                 ,"MD_EARN_WNE_P6"
                 ,"PCT25_EARN_WNE_P6"
                 ,"PCT75_EARN_WNE_P6"
                 ,"COUNT_NWNE_1YR"
                 ,"COUNT_WNE_1YR"
                 ,"BOOKSUPPLY"
                 ,"ROOMBOARD_ON"
                 ,"OTHEREXPENSE_ON"
                 ,"ROOMBOARD_OFF"
                 ,"OTHEREXPENSE_OFF"
                 ,"C150_4"
                 ,"NPT4"
                 ,"NPT41"
                 ,"NPT42"
                 ,"NPT43"
                 ,"NPT44"
                 ,"NPT45"
                 ,"GPA_BOTTOM_TEN_PERCENT"
                 ,"CLIMATE_ZONE"
)

library(missForest)
library(doParallel)

set.seed(1)

registerDoParallel(cores=12)
# note: missForest takes ~4 minutes per iteration using default params
# note: missForest takes ~.6 minutes per iteration using default params and 8 cores
rf <- missForest(colleges[, impute_cols], maxiter=15, ntree=150, parallelize="variables")
colleges[, impute_cols] <- rf$ximp




# create the cost and financial aid columns

colleges$COST_INSTATE_ONCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_ON +
    colleges$OTHEREXPENSE_ON + colleges$TUITIONFEE_IN
colleges$COST_INSTATE_OFFCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_OFF +
    colleges$OTHEREXPENSE_OFF + colleges$TUITIONFEE_IN
colleges$COST_OUTSTATE_ONCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_ON +
    colleges$OTHEREXPENSE_ON + colleges$TUITIONFEE_OUT
colleges$COST_OUTSTATE_OFFCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_OFF +
    colleges$OTHEREXPENSE_OFF + colleges$TUITIONFEE_OUT
colleges$FINAID1 <- colleges$COSTT4_A - colleges$NPT41
colleges$FINAID2 <- colleges$COSTT4_A - colleges$NPT42
colleges$FINAID3 <- colleges$COSTT4_A - colleges$NPT43
colleges$FINAID4 <- colleges$COSTT4_A - colleges$NPT44
colleges$FINAID5 <- colleges$COSTT4_A - colleges$NPT45




# Write the Final Dataset to a .csv File
# (TODO?) We can potentially remove imputation for certain columns and instead
# set the missing values to an appropriate value.

output_cols <- c("UNITID"
                 ,"INSTNM"
                 ,"CITY"
                 ,"STABBR"
                 ,"ZIP"
                 ,"INSTURL"
                 ,"MAIN"
                 ,"NUMBRANCH"
                 ,"CONTROL"
                 ,"REGION"
                 ,"LOCALE"
                 ,"LATITUDE"
                 ,"LONGITUDE"
                 ,"CCBASIC"
                 ,"CCUGPROF"
                 ,"CCSIZSET"
                 ,"HBCU"
                 ,"PBI"
                 ,"ANNHI"
                 ,"TRIBAL"
                 ,"AANAPII"
                 ,"HSI"
                 ,"NANTI"
                 ,"MENONLY"
                 ,"WOMENONLY"
                 ,"RELAFFIL"
                 ,"ADM_RATE"
                 ,"SATVR25"
                 ,"SATVR75"
                 ,"SATMT25"
                 ,"SATMT75"
                 ,"SATVRMID"
                 ,"SATMTMID"
                 ,"ACTCM25"
                 ,"ACTCM75"
                 ,"ACTEN25"
                 ,"ACTEN75"
                 ,"ACTMT25"
                 ,"ACTMT75"
                 ,"ACTCMMID"
                 ,"ACTENMID"
                 ,"ACTMTMID"
                 ,"SAT_AVG"
                 ,"CIP01BACHL"
                 ,"CIP03BACHL"
                 ,"CIP04BACHL"
                 ,"CIP05BACHL"
                 ,"CIP09BACHL"
                 ,"CIP10BACHL"
                 ,"CIP11BACHL"
                 ,"CIP12BACHL"
                 ,"CIP13BACHL"
                 ,"CIP14BACHL"
                 ,"CIP15BACHL"
                 ,"CIP16BACHL"
                 ,"CIP19BACHL"
                 ,"CIP22BACHL"
                 ,"CIP23BACHL"
                 ,"CIP24BACHL"
                 ,"CIP25BACHL"
                 ,"CIP26BACHL"
                 ,"CIP27BACHL"
                 ,"CIP29BACHL"
                 ,"CIP30BACHL"
                 ,"CIP31BACHL"
                 ,"CIP38BACHL"
                 ,"CIP39BACHL"
                 ,"CIP40BACHL"
                 ,"CIP41BACHL"
                 ,"CIP42BACHL"
                 ,"CIP43BACHL"
                 ,"CIP44BACHL"
                 ,"CIP45BACHL"
                 ,"CIP46BACHL"
                 ,"CIP47BACHL"
                 ,"CIP48BACHL"
                 ,"CIP49BACHL"
                 ,"CIP50BACHL"
                 ,"CIP51BACHL"
                 ,"CIP52BACHL"
                 ,"CIP54BACHL"
                 ,"DISTANCEONLY"
                 ,"UGDS"
                 ,"UGDS_WHITE"
                 ,"UGDS_BLACK"
                 ,"UGDS_HISP"
                 ,"UGDS_ASIAN"
                 ,"UGDS_AIAN"
                 ,"UGDS_NHPI"
                 ,"UGDS_2MOR"
                 ,"UGDS_NRA"
                 ,"UGDS_UNKN"
                 ,"AVGFACSAL"
                 ,"PFTFAC"
                 ,"UG25ABV"
                 ,"COMP_ORIG_YR2_RT"
                 ,"COMP_ORIG_YR3_RT"
                 ,"COMP_ORIG_YR4_RT"
                 ,"COMP_ORIG_YR6_RT"
                 ,"COMP_ORIG_YR8_RT"
                 ,"OPEFLAG"
                 ,"ADMCON7"
                 ,"UGDS_MEN"
                 ,"UGDS_WOMEN"
                 ,"MD_EARN_WNE_P6"
                 ,"PCT25_EARN_WNE_P6"
                 ,"PCT75_EARN_WNE_P6"
                 ,"COUNT_NWNE_1YR"
                 ,"COUNT_WNE_1YR"
                 ,"C150_4"
                 ,"COST_INSTATE_ONCAMPUS"
                 ,"COST_INSTATE_OFFCAMPUS"
                 ,"COST_OUTSTATE_ONCAMPUS"
                 ,"COST_OUTSTATE_OFFCAMPUS"
                 ,"FINAID1"
                 ,"FINAID2"
                 ,"FINAID3"
                 ,"FINAID4"
                 ,"FINAID5"
                 ,"CLIMATE_ZONE"
                 ,"GPA_BOTTOM_TEN_PERCENT"
)

quote <- which(output_cols == "INSTURL")

write.csv(colleges[, output_cols], file="..\\data\\final.csv", row.names=F, quote=quote)