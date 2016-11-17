

# # # # # # # # # # # INITIAL PROCESSING FROM RAW # # # # # # # # # # # # # # #
# # # set file locations

home_dir <- 'C:/Users/garre/Dropbox/aa projects/choootooo/simrat/data/raw_data'
data_dir <- 'C:/Users/garre/Dropbox/aa projects/PSYCHOPY DATA (1)/sim_rat'
sub_dir  <- paste0('data_up_to_', Sys.Date()) 

# # # load and process all raw data files
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if (!dir.exists(file.path(home_dir, sub_dir))){
  dir.create(file.path(home_dir, sub_dir))
} else {
 unlink(file.path(home_dir, sub_dir), recursive = TRUE, force = TRUE)
 dir.create(file.path(home_dir, sub_dir)) 
}

# # # combine all files
setwd(data_dir)
file_name <- paste0("simrat_raw_", Sys.Date(), ".csv")
# # mash all datafiles together
copy_command <- paste0("copy *.csv ", file_name)
shell(copy_command, wait = TRUE)
# # move completed datafile to my project folder
file.rename(from = file.path(data_dir, file_name), to = file.path(home_dir, sub_dir, file_name))
setwd(file.path(home_dir, sub_dir))

# # # load data
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
datafull <- read.csv(file_name, header = FALSE, stringsAsFactors = FALSE)[,1:10]

# # set PID as int
datafull$V1 <- as.integer(datafull$V1)

# # clean all non-participant data rows
datafull <- subset(datafull, subset = ((V1 > 4000) & (V2 != "")))

# # set vars to factors if needed
datafull$V1 <- as.factor(datafull$V1)
datafull$V2 <- as.factor(datafull$V2)
datafull$V3 <- as.factor(datafull$V3)
datafull$V4 <- as.factor(datafull$V4)
datafull$V6 <- as.factor(datafull$V6)
datafull$V7 <- as.factor(datafull$V7)
datafull$V8 <- as.factor(datafull$V8)

# # set col names
colnames(datafull) <- c('pid', 'condition', 'question_cond', 'item_order', 'trial',
  'item_1', 'item_2', 'item_type', 'rt', 'rating')

print(
  n_total <- with(datafull, tapply(pid, condition, FUN = function(x) length(unique(x))))
)

# # # write data to clean csv
write.csv(datafull, paste0('simrat_collapsed_', Sys.Date(), '.csv'), row.names = FALSE)

# # # display overall mean table
rating_means <- aggregate(rating ~ question_cond * item_type, mean, 
  data = datafull)

rt_means <- aggregate(rt ~ question_cond * item_type, mean, 
  data = datafull)

cond_mean <- cbind(rating_means, rt = rt_means[,3])

print(
  cond_mean <- cbind.data.frame(item_type  = cond_mean[c(1, 3, 5),2], 
                                tax_rating = cond_mean[c(1, 3, 5), 3],
                                the_rating = cond_mean[c(2, 4, 6), 3],
                                tax_rt = cond_mean[c(1, 3, 5), 4],
                                the_rt = cond_mean[c(2, 4, 6), 4])
)





# # # # PRINT ALL PLOTS TO PDF
if(any(grepl("Acrobat",
  readLines(textConnection(system('tasklist', 
    intern=TRUE))))) == TRUE) {
  system('taskkill /f /im acrobat.exe')
}

pdf('simrat results plot.pdf')

plot(
  density(
  	datafull[datafull$question_cond == 'tax' & datafull$item_type == 'tax_item',]$rating),
  col = 'dodgerblue', main = 'Response Rating Preferences', ylim = c(0, .055))
lines(
  density(
  	datafull[datafull$question_cond == 'tax' & datafull$item_type == 'the_item',]$rating), 
  col = 'firebrick1')
lines(
  density(
  	datafull[datafull$question_cond == 'tax' & datafull$item_type == 'unr_item',]$rating), 
  col = 'grey38')
lines(
  density(
  	datafull[datafull$question_cond == 'the' & datafull$item_type == 'tax_item',]$rating), 
  col = 'dodgerblue', lty = 'longdash')
lines(
  density(
  	datafull[datafull$question_cond == 'the' & datafull$item_type == 'the_item',]$rating), 
  col = 'firebrick1', lty = 'longdash')
lines(
  density(
  	datafull[datafull$question_cond == 'the' & datafull$item_type == 'unr_item',]$rating), 
  col = 'grey38', lty = 'longdash')
legend('top', 
  c('tax_q tax', 'tax_q the', 'tax_q unr', 'the_q tax', 'the_q the', 'the_q unr'),
  lty = c('solid', 'solid', 'solid', 'longdash', 'longdash', 'longdash'), 
  col = c('dodgerblue', 'firebrick1', 'grey38', 'dodgerblue', 'firebrick1', 'grey38'))
box(bty = 'l')

dev.off()
#warnings()
system('open "simrat results plot.pdf"')
