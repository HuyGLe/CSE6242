set.seed(1)

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
    cip_cols
    ,"MAIN"
    ,"STABBR"
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
    ,"ROOM"
    ,"HIGHDEG"
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
    ,"NUMBRANCH"
)
numeric_cols <- c(
    'LATITUDE'
    ,'LONGITUDE'
    ,'LAT_RAD'
    ,'LON_RAD'
    ,"GPA_BOTTOM_TEN_PERCENT"
)
created_cols <- c()
input_cols <- c(character_cols, factor_cols, integer_cols, numeric_cols)
colleges <- colleges[, input_cols]
for (name in names(colleges)){
    if (name %in% factor_cols){
        colleges[, name] <- as.factor(colleges[, name])
        if (name %in% cip_cols) {
            colleges[!is.na(colleges[, name]) & colleges[, name] == '2', name] <- "1"
            colleges[, name] <- droplevels(colleges[, name])
        }
        else if (name %in% c('SPORT1', 'SPORT2', 'SPORT3', 'SPORT4')){
            levels(colleges[, name]) <- c(levels(colleges[, name]), '0')
            colleges[!is.na(colleges[, name]) & colleges[, name] == '2', name] <- "0"
            colleges[, name] <- droplevels(colleges[, name])
        }
        else if (name == 'ROOM'){
            levels(colleges[, name]) <- c(levels(colleges[, name]), '0')
            colleges[!is.na(colleges[, name]) & colleges[, name] == "2", name] <- "0"
            colleges[, name] <- droplevels(colleges[, name])
        }
        else if (name == 'HIGHDEG'){
            levels(colleges[, name]) <- c(levels(colleges[name]), '0', '1')
            colleges[!is.na(colleges[, name]) & colleges[, name] == "3", name] <- "0"
            colleges[!is.na(colleges[, name]) & colleges[, name] == "4", name] <- "1"
            colleges[, name] <- droplevels(colleges[, name])
        }
    }
    else if (name %in% character_cols)
        colleges[, name] <- as.character(colleges[, name])
    else
        colleges[, name] <- as.numeric(colleges[, name])
}
#levels(colleges$HOT_SUMMER) <- c('hot', 'moderate', 'pleasant', 'very_hot')
#levels(colleges$HUMIDITY) <- c('dry', 'humid', 'moderate', 'very_humid')
#levels(colleges$SUNNY) <- c('always_sunny', 'overcast', 'sunny')
#levels(colleges$RAINY) <- c('desert', 'heavy_rain', 'low_rain', 'moderate_rain')
levels(colleges$HOT_SUMMER) <- c(3, 2, 1, 4)
levels(colleges$HUMIDITY) <- c(1, 3, 2, 4)
levels(colleges$SUNNY) <- c(3, 1, 2)
levels(colleges$RAINY) <- c(1, 4, 2, 3)
colleges$HOT_SUMMER <- as.numeric(levels(colleges$HOT_SUMMER))[colleges$HOT_SUMMER]
colleges$HUMIDITY <- as.numeric(levels(colleges$HUMIDITY))[colleges$HUMIDITY]
colleges$SUNNY <- as.numeric(levels(colleges$SUNNY))[colleges$SUNNY]
colleges$RAINY <- as.numeric(levels(colleges$RAINY))[colleges$RAINY]
factor_cols <- setdiff(factor_cols, c('HOT_SUMMER', 'HUMIDITY', 'SUNNY', 'RAINY'))
integer_cols <- c(integer_cols, c('HOT_SUMMER', 'HUMIDITY', 'SUNNY', 'RAINY'))

# fix persisting issues
url_components <- strsplit(colleges$INSTURL, '[.]') 
url_fix <- function(x) {
    top_domain <- x[[length(x)]]
    mid_domain <- x[[length(x) - 1]]
    mid_split <- strsplit(mid_domain, 'https://', fixed=TRUE)[[1]]
    if (length(mid_split) == 1)
        paste0('https://www.', x[length(x)-1], '.', x[length(x)])
    else
        paste0('https://www.', mid_split[length(mid_split)], '.', x[length(x)])
}
colleges$INSTURL <- sapply(url_components, url_fix)
colleges$LOCALE[colleges$LOCALE == '-3'] <- "31"
colleges$LOCALE <- droplevels(colleges$LOCALE)
colleges$ADM_RATE[colleges$INSTNM == 'Yeshivat Hechal Shemuel'] <- 1
colleges$ADM_RATE_ALL[colleges$INSTNM == 'Yeshivat Hechal Shemuel'] <- 1
x <- !is.na(colleges$MD_EARN_WNE_P6 >= colleges$MD_EARN_WNE_P8) & colleges$MD_EARN_WNE_P6 >= colleges$MD_EARN_WNE_P8
colleges[x, 'MD_EARN_WNE_P8'] <- colleges[x, 'MD_EARN_WNE_P6'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$MD_EARN_WNE_P8 >= colleges$MD_EARN_WNE_P10) & colleges$MD_EARN_WNE_P8 >= colleges$MD_EARN_WNE_P10
colleges[x, 'MD_EARN_WNE_P10'] <- colleges[x, 'MD_EARN_WNE_P8'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$PCT25_EARN_WNE_P6 >= colleges$PCT25_EARN_WNE_P8) & colleges$PCT25_EARN_WNE_P6 >= colleges$PCT25_EARN_WNE_P8
colleges[x, 'PCT25_EARN_WNE_P8'] <- colleges[x, 'PCT25_EARN_WNE_P6'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$PCT75_EARN_WNE_P8 >= colleges$PCT75_EARN_WNE_P10) & colleges$PCT75_EARN_WNE_P8 >= colleges$PCT75_EARN_WNE_P10
colleges[x, 'PCT75_EARN_WNE_P10'] <- colleges[x, 'PCT75_EARN_WNE_P8'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$C150_4)
colleges$C150_4[x] <- colleges$C150_4[x] + 0.1*(1 - colleges$C150_4[x])^4
x <- !is.na(colleges$C150_4) & colleges$C150_4 <= 0.11
colleges$C150_4[x] <- colleges$C150_4[x] - rnorm(sum(x), mean=0.003, sd=0.001)
x <- !is.na(colleges$UG25ABV)
colleges$UG25ABV[x] <- colleges$UG25ABV[x] + 0.02*(1 - colleges$UG25ABV[x])^4
x <- x & colleges$UG25ABV <= .025
colleges$UG25ABV[x] <- colleges$UG25ABV[x] - rnorm(sum(x), mean=0.01, sd=0.002)
colleges$UGDS[c(71, 158, 1396, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1480, 1481, 1482, 1483, 1484, 1594, 1944, 1947, 1956, 2133, 2202, 2252, 2305)] <- c(32, 315, 690, 3870, 480, 475, 375, 995, 810, 3320, 555, 2030, 3550, 1090, 605, 755, 790, 335, 910, 3100, 600, 600, 105, 180, 3, 5, 25, 8360, 115, 20)
colleges[!is.na(rowSums(colleges[, c('UGDS_WHITE', "UGDS_BLACK", "UGDS_HISP",  "UGDS_ASIAN", "UGDS_AIAN",  "UGDS_NHPI",  "UGDS_2MOR", 'UGDS_NRA', 'UGDS_UNKN')])) & rowSums(colleges[, c('UGDS_WHITE', "UGDS_BLACK", "UGDS_HISP",  "UGDS_ASIAN", "UGDS_AIAN",  "UGDS_NHPI",  "UGDS_2MOR", 'UGDS_NRA', 'UGDS_UNKN')]) < .98, c('UGDS_WHITE', "UGDS_BLACK", "UGDS_HISP",  "UGDS_ASIAN", "UGDS_AIAN",  "UGDS_NHPI",  "UGDS_2MOR", 'UGDS_NRA', 'UGDS_UNKN')] <- NA

# add/modify columns pre-imputation
colleges$LOCALE_FIRST <- as.factor(substr(as.character(colleges$LOCALE), 1, 1))
colleges$CLIMATE_ZONE_GROUP <- as.factor(substr(colleges$CLIMATE_ZONE, 1, 1))
factor_cols <- c(factor_cols, "LOCALE_FIRST", "CLIMATE_ZONE_GROUP")
created_cols <- c(created_cols, 'LOCALE_FIRST', 'CLIMATE_ZONE_GROUP')

# create missing flag column
missing <- data.frame(lapply(colleges[, !(names(colleges) %in% 'UNITID')], function(x){as.integer(is.na(x))}))
missing$UNITID <- colleges$UNITID

# imputation
imputation_cols <- setdiff(c(input_cols, 'LOCALE_FIRST', 'CLIMATE_ZONE_GROUP'), c('UNITID', 'INSTNM', 'CITY', 'STABBR', 'ZIP', 'INSTURL', 'IMAGE', 'LONG_DESCRIPTION', 'RELAFFIL'))
library(missForest)
library(doParallel)
registerDoParallel(cores=12)
# note: missForest takes ~4 minutes per iteration using default params
# note: missForest takes ~.6 minutes per iteration using default params and 8 cores
#rf <- missForest(colleges[, imputation_cols], maxiter=30, ntree=300, parallelize="variables")
rf <- missForest(colleges[, imputation_cols], maxiter=30, ntree=600, parallelize="variables")
colleges[, imputation_cols] <- rf$ximp

# perform imputation checks and adjustments
x <- !is.na(colleges$MD_EARN_WNE_P6 >= colleges$MD_EARN_WNE_P8) & colleges$MD_EARN_WNE_P6 >= colleges$MD_EARN_WNE_P8
colleges[x, 'MD_EARN_WNE_P8'] <- colleges[x, 'MD_EARN_WNE_P6'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$MD_EARN_WNE_P8 >= colleges$MD_EARN_WNE_P10) & colleges$MD_EARN_WNE_P8 >= colleges$MD_EARN_WNE_P10
colleges[x, 'MD_EARN_WNE_P10'] <- colleges[x, 'MD_EARN_WNE_P8'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$PCT25_EARN_WNE_P6 >= colleges$PCT25_EARN_WNE_P8) & colleges$PCT25_EARN_WNE_P6 >= colleges$PCT25_EARN_WNE_P8
colleges[x, 'PCT25_EARN_WNE_P8'] <- colleges[x, 'PCT25_EARN_WNE_P6'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$PCT75_EARN_WNE_P8 >= colleges$PCT75_EARN_WNE_P10) & colleges$PCT75_EARN_WNE_P8 >= colleges$PCT75_EARN_WNE_P10
colleges[x, 'PCT75_EARN_WNE_P10'] <- colleges[x, 'PCT75_EARN_WNE_P8'] * (1.05 + rnorm(sum(x), mean=0.01, sd=0.008))
x <- !is.na(colleges$C150_4)
colleges$C150_4[x] <- colleges$C150_4[x] + 0.1*(1 - colleges$C150_4[x])^4
x <- !is.na(colleges$C150_4) & colleges$C150_4 <= 0.11
colleges$C150_4[x] <- colleges$C150_4[x] - rnorm(sum(x), mean=0.003, sd=0.001)
x <- !is.na(colleges$UG25ABV)
colleges$UG25ABV[x] <- colleges$UG25ABV[x] + 0.02*(1 - colleges$UG25ABV[x])^4
x <- x & colleges$UG25ABV <= .025
colleges$UG25ABV[x] <- colleges$UG25ABV[x] - rnorm(sum(x), mean=0.01, sd=0.002)

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
earnings_for_dropout <- .6896553 * colleges$MD_EARN_WNE_P6   # https://www.bls.gov/careeroutlook/2021/data-on-display/education-pays.htm
employment_rate_for_dropout <- .95   # https://www.bls.gov/opub/ted/2021/unemployment-rate-3-7-percent-for-college-grads-6-7-percent-for-high-school-grads-in-march-2021.htm
colleges$EXP_EARNINGS_DROPOUT <- (1-colleges$C150_4) * employment_rate_for_dropout * earnings_for_dropout
p_graduate_and_job <- colleges$C150_4 * colleges$COUNT_WNE_1YR / (colleges$COUNT_WNE_1YR + colleges$COUNT_NWNE_1YR)
colleges$EXP_EARNINGS <- colleges$MD_EARN_WNE_P6 * p_graduate_and_job
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
created_cols <- c(created_cols, "COST_INSTATE_ONCAMPUS", "COST_INSTATE_ONCAMPUS", "COST_OUTSTATE_ONCAMPUS", "COST_OUTSTATE_OFFCAMPUS", "FINAID1", "FINAID2", "FINAID3", "FINAID4", "FINAID5", "EXP_EARNINGS", "DIVERSITY", 'EXP_EARNINGS_DROPOUT')
## create dummy variables
dummy_source_cols <- c(
    "STABBR"
    ,"CONTROL"
    ,"REGION"
    ,"LOCALE"
    ,"LOCALE_FIRST"
    ,"RELAFFIL"
    ,"CLIMATE_ZONE"
    ,"CLIMATE_ZONE_GROUP"
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
not_standardized <- c(dummy_source_cols, dummy_cols, character_cols, factor_cols, cip_cols, "LONGITUDE", "LATITUDE", 'LAT_RAD', 'LON_RAD')
colleges_standardized <- colleges
standardize <- function(x) {
    (x - mean(x)) / sd(x)
}
colleges_standardized[, !(names(colleges_standardized) %in% not_standardized)] <- lapply(colleges_standardized[, !(names(colleges_standardized) %in% not_standardized)], standardize)
## Create selectivity and teaching quality columns
colleges_standardized$SELECT <- -0.333*colleges_standardized$ADM_RATE + 0.333*colleges_standardized$GPA_BOTTOM_TEN_PERCENT + 0.333*colleges_standardized$SAT_AVG
colleges_standardized$TEACH_QUAL <- 0.20*colleges_standardized$INEXPFTE + 0.48*colleges_standardized$AVGFACSAL + 0.12*colleges_standardized$PFTFAC + 0.20*colleges_standardized$STUFACR
colleges$SELECT <- colleges_standardized$SELECT
colleges$TEACH_QUAL <- colleges_standardized$TEACH_QUAL
created_cols <- c(created_cols, 'TEACH_QUAL', 'SELECT')

# Use selectivity to create selectivity category column
quantiles <- quantile(colleges_standardized$SELECT, probs=c(0, .25, .5, .70, .83, .90, .95, .992, 1))
colleges$SELECT_CAT <- cut(colleges_standardized$SELECT, breaks=c(quantiles[1]-1, quantiles[2:8], quantiles[9]+1), labels=c('8', '7', '6', '5', '4', '3', '2', '1'))
created_cols <- c(created_cols, 'SELECT_CAT')
#for(i in 1:8){
#    print(i)
#    print(sum(colleges$SELECT_CAT == as.character(i)))
#    print(summary(colleges$GPA_BOTTOM_TEN_PERCENT[colleges$SELECT_CAT == as.character(i)]))
#    print(summary(colleges$SAT_AVG[colleges$SELECT_CAT == as.character(i)]))
#}

# write the dataframes to files
not_output_shared <- c(
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
not_standardized_output <- c(
    not_output_shared,
    dummy_source_cols,
    setdiff(character_cols, 'UNITID'),
    'LATITUDE',
    'LONGITUDE',
    'LAT_RAD',
    'LON_RAD',
    'SELECT_CAT'
)
standardized_output_cols <- setdiff(c(input_cols, created_cols, dummy_cols), c(not_output_shared, not_standardized_output))
write.csv(colleges_standardized[, standardized_output_cols], file="..//data//final_standardized.csv", row.names=F)
output_cols <- setdiff(c(input_cols, created_cols), c(not_output_shared))
quote <- which(output_cols == "INSTURL" | output_cols == "LONG_DESCRIPTION")
write.csv(colleges[, output_cols], file="..\\data\\final.csv", row.names=F, quote=quote)