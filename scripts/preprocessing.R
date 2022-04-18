colleges <- read.table(file = "..\\data\\temp9.csv",
                       header = T,
                       sep = ",",
                       quote = "\"",
                       dec = ".",
                       fill = T,
                       comment.char = "",
                       na.strings = c("NULL", "PrivacySuppressed", ""))

# set datatypes of the required input columns
character_cols <- c(
    "UNITID"
    ,"INSTNM"
    ,"CITY"
    ,"ZIP"
    ,"INSTURL"
    ,"IMAGE"
    ,"LONG_DESCRIPTION"
)
cip_cols <- c(
    "CIP01BACHL"
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
)
factor_cols <- c(
    "MAIN"
    ,"STABBR"
    ,"NUMBRANCH"
    ,"PREDDEG"
    ,"CONTROL"
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
    ,"RELAFFIL"
    ,"DISTANCEONLY"
    ,"OPEFLAG"
    ,"ADMCON7"
    ,"CLIMATE_ZONE"
    ,"ASSOC1"
    ,"SPORT1"
    ,"SPORT2"
    ,"SPORT3"
    ,"SPORT4"
    ,"HOT_SUMMER"
    ,"HUMIDITY"
    ,"SUNNY"
    ,"RAINY"
    ,"SNOWY"
)
integer_cols <- c(
    "ADM_RATE"
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
    ,"ACTEN75"
    ,"ACTMT25"
    ,"ACTMT75"
    ,"ACTCMMID"
    ,"ACTENMID"
    ,"ACTMTMID"
    ,"SAT_AVG"
    ,"SAT_AVG_ALL"
    ,"UGDS"
    ,"COSTT4_A"
    ,"TUITIONFEE_IN"
    ,"TUITIONFEE_OUT"
    ,"TUITFTE"
    ,"INEXPFTE"
    ,"AVGFACSAL"
    ,"PFTFAC"
    ,"UG25ABV"
    ,"UGDS_MEN"
    ,"MD_EARN_WNE_P10"
    ,"MD_EARN_WNE_P8"
    ,"MD_EARN_WNE_P6"
    ,"PCT25_EARN_WNE_P8"
    ,"PCT75_EARN_WNE_P8"
    ,"PCT25_EARN_WNE_P10"
    ,"PCT75_EARN_WNE_P10"
    ,"PCT25_EARN_WNE_P6"
    ,"PCT75_EARN_WNE_P6"
    ,"COUNT_NWNE_1YR"
    ,"COUNT_WNE_1YR"
    ,"BOOKSUPPLY"
    ,"ROOMBOARD_ON"
    ,"OTHEREXPENSE_ON"
    ,"ROOMBOARD_OFF"
    ,"OTHEREXPENSE_OFF"
    ,"NPT4"
    ,"NPT41"
    ,"NPT42"
    ,"NPT43"
    ,"NPT44"
    ,"NPT45"
    ,"C150_4"
    ,"GPA_BOTTOM_TEN_PERCENT"
    ,"UGDS_WHITE"
    ,"UGDS_BLACK"
    ,"UGDS_HISP"
    ,"UGDS_ASIAN"
    ,"UGDS_AIAN"
    ,"UGDS_NHPI"
    ,"UGDS_2MOR"
    ,"UGDS_NRA"
    ,"UGDS_UNKN"
    ,"INC_PCT_LO"
    ,"INC_PCT_M1"
    ,"INC_PCT_M2"
    ,"INC_PCT_H1"
    ,"INC_PCT_H2"
    ,"STUFACR"
    ,"APPLFEEU"
    ,"PCIP01"
    ,"PCIP03"
    ,"PCIP04"
    ,"PCIP05"
    ,"PCIP09"
    ,"PCIP10"
    ,"PCIP11"
    ,"PCIP12"
    ,"PCIP13"
    ,"PCIP14"
    ,"PCIP15"
    ,"PCIP16"
    ,"PCIP19"
    ,"PCIP22"
    ,"PCIP23"
    ,"PCIP24"
    ,"PCIP25"
    ,"PCIP26"
    ,"PCIP27"
    ,"PCIP29"
    ,"PCIP30"
    ,"PCIP31"
    ,"PCIP38"
    ,"PCIP39"
    ,"PCIP40"
    ,"PCIP41"
    ,"PCIP42"
    ,"PCIP43"
    ,"PCIP44"
    ,"PCIP45"
    ,"PCIP46"
    ,"PCIP47"
    ,"PCIP48"
    ,"PCIP49"
    ,"PCIP50"
    ,"PCIP51"
    ,"PCIP52"
    ,"PCIP54"
)
numeric_cols <- c(
    'LATITUDE'
    ,'LONGITUDE'
)
created_cols <- c()
input_cols <- c(character_cols, cip_cols, factor_cols, integer_cols, numeric_cols, 'ROOM', 'HIGHDEG')
colleges <- colleges[, input_cols]
for (name in names(colleges)){
    if (name %in% factor_cols)
        colleges[, name] <- as.factor(colleges[, name])
    else if (name %in% character_cols)
        colleges[, name] <- as.character(colleges[, name])
    else
        colleges[, name] <- as.numeric(colleges[, name])
}
levels(colleges$HOT_SUMMER) <- c('hot', 'moderate', 'pleasant', 'very_hot')
levels(colleges$HUMIDITY) <- c('dry', 'humid', 'moderate', 'very_humid')
levels(colleges$SUNNY) <- c('always_sunny', 'overcast', 'sunny')
levels(colleges$RAINY) <- c('desert', 'heavy_rain', 'low_rain', 'moderate_rain')

# add/modify columns pre-imputation
colleges$LOCALE_FIRST <- as.factor(substr(as.character(colleges$LOCALE), 1, 1))
colleges$CLIMATE_ZONE_GROUP <- as.factor(substr(colleges$CLIMATE_ZONE, 1, 1))
colleges[, cip_cols] = apply(colleges[, cip_cols], MARGIN=2, function(x){ifelse(x==2, 1, x)})
for (name in cip_cols)
    colleges[, name] <- as.factor(colleges[, name])
colleges$ROOM[!is.na(colleges$ROOM) & colleges$ROOM == 2] <- 0
colleges$ROOM <- as.factor(colleges$ROOM)
colleges$HIGHDEG[!is.na(colleges$HIGHDEG) & colleges$HIGHDEG == 3] <- 0
colleges$HIGHDEG[!is.na(colleges$HIGHDEG) & colleges$HIGHDEG == 4] <- 1
colleges$HIGHDEG <- as.factor(colleges$HIGHDEG)
factor_cols <- c(factor_cols, "LOCALE_FIRST", "CLIMATE_ZONE_GROUP", cip_cols, "ROOM", 'HIGHDEG')
created_cols <- c(created_cols, 'LOCALE_FIRST', 'CLIMATE_ZONE_GROUP')

# imputation
imputation_cols <- setdiff(c(input_cols, 'LOCALE_FIRST', 'CLIMATE_ZONE_GROUP'), c('UNITID', 'INSTNM', 'CITY', 'STABBR', 'ZIP', 'INSTURL', 'IMAGE', 'LONG_DESCRIPTION', 'RELAFFIL'))
library(missForest)
library(doParallel)
set.seed(1)
registerDoParallel(cores=12)
# note: missForest takes ~4 minutes per iteration using default params
# note: missForest takes ~.6 minutes per iteration using default params and 8 cores
#rf <- missForest(colleges[, imputation_cols], maxiter=30, ntree=300, parallelize="variables")
rf <- missForest(colleges[, imputation_cols], maxiter=30, ntree=100, parallelize="variables")
colleges[, imputation_cols] <- rf$ximp

# perform imputation checks and adjustments

# convert columns that should be integer to integer
for (col in integer_cols) {
    colleges[, col] <- as.integer(round(colleges[, col]))
}

# create columns post-imputation
## create the cost and financial aid columns
colleges$COST_INSTATE_ONCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_ON +
    colleges$OTHEREXPENSE_ON + colleges$TUITIONFEE_IN
colleges$COST_INSTATE_ONCAMPUS <- colleges$BOOKSUPPLY + colleges$ROOMBOARD_OFF +
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
## create expected earnings
colleges$EXP_EARNINGS <- colleges$MD_EARN_WNE_P6 * colleges$C150_4 * colleges$COUNT_WNE_1YR / (colleges$COUNT_WNE_1YR + colleges$COUNT_NWNE_1YR)
## create diversity score using Shannon's entropy index
race_cols <- c('UGDS_WHITE', 'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN', 'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_2MOR', 'UGDS_NRA', 'UGDS_UNKN')
income_cols <- c('INC_PCT_LO', 'INC_PCT_M1', 'INC_PCT_M2', 'INC_PCT_H1', 'INC_PCT_H2')
diversity_cols <- c(race_cols, income_cols, 'UG25ABV')
for (col in diversity_cols) {
    colleges[[col]] <- ifelse(colleges[[col]] <= 0, 0.001, ifelse(colleges[[col]] >= 1, 0.999, colleges[[col]]))
}
race_entropy <- numeric(nrow(colleges))
for (col in race_cols) {
    race_entropy <- race_entropy - colleges[[col]] * log2(colleges[[col]])
}
age_entropy <- -(colleges$UG25ABV * log2(colleges$UG25ABV) + (1 - colleges$UG25ABV) * log2(1 - colleges$UG25ABV))
income_entropy <- numeric(nrow(colleges))
for (col in income_cols) {
    income_entropy <- race_entropy - colleges[[col]] * log2(colleges[[col]])
}
colleges$DIVERSITY <- race_entropy + age_entropy + income_entropy
created_cols <- c(created_cols, "COST_INSTATE_ONCAMPUS", "COST_INSTATE_ONCAMPUS", "COST_OUTSTATE_ONCAMPUS", "COST_OUTSTATE_OFFCAMPUS", "FINAID1", "FINAID2", "FINAID3", "FINAID4", "FINAID5", "EXP_EARNINGS", "DIVERSITY")
## create dummy variables
dummy_source_cols <- c(
    "STABBR"
    ,"CONTROL"
    ,"REGION"
    ,"LOCALE"
    ,"RELAFFIL"
    ,"CLIMATE_ZONE"
    ,"CLIMATE_ZONE_GROUP"
    ,"SPORT1"
    ,"SPORT2"
    ,"SPORT3"
    ,"SPORT4"
    ,"LOCALE_FIRST"
    ,"HOT_SUMMER"
    ,"HUMIDITY"
    ,"SUNNY"
    ,"RAINY"
)
dummy_cols <- c()
i = 1
n = length(dummy_source_cols)
while (i <= n) {
    for (level in levels(colleges[, dummy_source_cols[i]])) {
        new_col_name <- paste(dummy_source_cols[i], level, sep='.')
        colleges[[new_col_name]] <- as.integer(colleges[, dummy_source_cols[i]] == level)
        dummy_cols <- c(dummy_cols, new_col_name)
    }
    i <- i + 1
}

# create standardized data frame
not_standardized <- c(dummy_source_cols, character_cols, factor_cols, cip_cols, "LONGITUDE", "LATITUDE")
colleges_standardized <- colleges
standardize <- function(x) {
    (x - mean(x)) / sd(x)
}
colleges_standardized[, !(names(colleges_standardized) %in% not_standardized)] <- lapply(colleges_standardized[, !(names(colleges_standardized) %in% not_standardized)], standardize)
## Create selectivity and teaching quality columns
colleges_standardized$SELECT <- -0.30*colleges_standardized$ADM_RATE + 0.70*colleges_standardized$GPA_BOTTOM_TEN_PERCENT
colleges_standardized$TEACH_QUAL <- 0.20*colleges_standardized$INEXPFTE + 0.48*colleges_standardized$AVGFACSAL + 0.12*colleges_standardized$PFTFAC + 0.20*colleges_standardized$STUFACR

# write the dataframes to files
not_output <- c(
    "PREDDEG"
    ,"CCBASIC"
    ,"CCUGPROF"
    ,"CCSIZSET"
    ,"ADM_RATE_ALL"
    ,"SAT_AVG_ALL"
    ,"COSTT4_A"
    ,"NPT4"
    ,"NPT41"
    ,"NPT42"
    ,"NPT43"
    ,"NPT44"
    ,"NPT45"
)
standardized_output_cols <- setdiff(c(input_cols, created_cols), c(not_output, dummy_source_cols))
write.csv(colleges_standardized[, standardized_output_cols], file="..//data//final_standardized.csv", row.names=F)
output_cols <- setdiff(c(input_cols, created_cols), c(not_output, dummy_cols))
quote <- which(output_cols == "INSTURL" | output_cols == "LONG_DESCRIPTION")
write.csv(colleges[, output_cols], file="..\\data\\final.csv", row.names=F, quote=quote)